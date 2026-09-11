import requests

_API = "https://de.wikipedia.org/w/api.php"
session = requests.Session()
session.headers.update({
    "User-Agent": "BirdApp/0.1 (timmnicklpl@gmail.com)"
})

def get_wikitext(title: str)-> str:
    """Gets raw wikitext from site."""
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
        "formatversion": "2",
    }
    r = session.get(_API, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if "error" in data:
        raise RuntimeError(data["error"].get("info", "Unbekannter API_Fehler"))
    return data["parse"]["wikitext"]