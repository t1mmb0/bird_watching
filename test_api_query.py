import pytest
from requests import HTTPError
from api_query import get_wikitext, _API

@pytest.mark.parametrize("mock_json, expected",[
    ({"parse": {"wikitext": "txt"}}, "txt"),
    ({"parse": {"wikitext": ""}}, ""),
    ({"parse": {"wikitext": "txt", "title": "txt"}}, "txt"),
    ({"parse": {"wikitext": "{{test_structure}}, [[test_link]]"}}, "{{test_structure}}, [[test_link]]"),
])
def test_get_wikitext(requests_mock, mock_json, expected):
    requests_mock.get(_API, json=mock_json)
    assert get_wikitext("placeholder") == expected


@pytest.mark.parametrize("mock_json, exc_type, match_text",[
    ({"error": {"info": "Die Seite existiert nicht."}},RuntimeError, "Die Seite existiert nicht."),
    ({}, KeyError,None)
])
def test_get_wikitext_error(requests_mock, mock_json, exc_type, match_text):
    requests_mock.get(_API, json=mock_json)
    with pytest.raises(exc_type, match=match_text):
        get_wikitext("placeholder")


@pytest.mark.parametrize("status_code",[400,401,404,429,500,503])
def test_get_wikitext_http_error(requests_mock, status_code):
    requests_mock.get(_API, status_code=status_code)
    with pytest.raises(HTTPError, match= str(status_code)):
        get_wikitext("placeholder")