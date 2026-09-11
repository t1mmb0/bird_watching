INSERT OR IGNORE INTO birds (
    german_name, english_name, taxon_order,
    taxon_family, family_common_name, scientific_name, status, rl_status, rl_status_description
) VALUES (
    :german_name, :english_name, :taxon_order,
    :taxon_family, :family_common_name, :scientific_name, :status, :rl_status, :rl_status_description
);