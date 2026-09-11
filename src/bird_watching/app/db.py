import sqlite3
from pathlib import Path
import pandas as pd
from bird_watching.app.script_loader import load_sql
from bird_watching.app.paths import DIR_SCRIPTS

# --- BUILDING TABLES / CONNECTION ---

def create_connection(db_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def close_connection(connection):
    connection.close()

def create_table(connection: sqlite3.Connection, schema: str)-> None:
    
    cursor = connection.cursor()
    cursor.executescript(schema)

# --- INTROSPECTION ---


def describe_table(connection: sqlite3.Connection, t: str = "birds")-> dict:
    cursor = connection.cursor()

    ddl = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (t,)).fetchone()
    columns = [dict(r) for r in cursor.execute(f"PRAGMA table_info({t})")]
    fks = [dict(r) for r in cursor.execute(f"PRAGMA foreign_key_list({t})")]

    indexes = []
    rows = cursor.execute(f"PRAGMA index_list({t})").fetchall()
    for r in rows:
        idx = dict(r)
        idx["columns"] = [c["name"] for c in cursor.execute(f"PRAGMA index_info({idx['name']})")]
        indexes.append(idx)

    return {
    "name": t,
    "ddl": ddl["sql"] if ddl else None,
    "columns": columns,
    "foreign_keys": fks,
    "indexes": indexes,
}

# --- TABLE INSERTION ---


def bulk_insert(connection: sqlite3.Connection, data: pd.DataFrame, script_name="insert_bird.sql")-> int:
    if connection is None:
        raise ValueError("A valid database connection must be provided.")
    records = data.to_dict(orient="records")
    sql_script = load_sql(DIR_SCRIPTS / script_name)
    with connection: 
        cur = connection.executemany(sql_script, records)

    return cur.rowcount





