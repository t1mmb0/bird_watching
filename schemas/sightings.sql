CREATE TABLE IF NOT EXISTS sightings(
    sighting_id INTEGER PRIMARY KEY,
    scientific_name TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    location_name TEXT,
    latitude REAL,
    longitude REAL,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (scientific_name)
        REFERENCES birds(scientific_name)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_sightings_name
    ON sightings(scientific_name);
    


