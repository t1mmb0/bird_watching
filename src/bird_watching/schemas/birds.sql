CREATE TABLE IF NOT EXISTS birds(
    bird_id INTEGER PRIMARY KEY,
    german_name TEXT NOT NULL,
    english_name TEXT NOT NULL,
    taxon_order TEXT NOT NULL,
    taxon_family TEXT NOT NULL,
    family_common_name TEXT NOT NULL,
    scientific_name TEXT NOT NULL UNIQUE,
    status TEXT,
    rl_status TEXT,
    rl_status_description TEXT
);
