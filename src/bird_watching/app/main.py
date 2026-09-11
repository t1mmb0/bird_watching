import pandas as pd

from bird_watching.app.db import create_connection, create_table, bulk_insert
from bird_watching.app.script_loader import load_sql
from bird_watching.app.paths import DIR_SCHEMAS, DIR_SCRIPTS, _BASE_DIR


#--- SETUP CONNECTION ---

connection = create_connection(_BASE_DIR / "birds.db")

#--- LOAD DATA ---

data = pd.read_csv(_BASE_DIR / "data/birds.csv")

#--- LOAD SCHEMAS ---

SCHEMA_BIRDS = load_sql(DIR_SCHEMAS / "birds.sql")
SCHEMA_SIGHTINGS = load_sql(DIR_SCHEMAS / "sightings.sql")

#--- TABLE CREATION ---

create_table(connection, SCHEMA_BIRDS)
create_table(connection, SCHEMA_SIGHTINGS)

#--- INSERT BIRDS ---

print(bulk_insert(connection, data, "insert_bird.sql"))
