import sqlite3

from pathlib import Path

_BASE_DIR = Path(__file__).parent
_SCHEMA_DIR = _BASE_DIR / "schemas"

# --- LOAD SCHEMA ---
def load_sql_schema(file_name: str):
    with open(_SCHEMA_DIR / file_name, "r", encoding="utf-8") as file:
        return file.read()

SCHEMA_SIGHTINGS = load_sql_schema("sightings.sql")
SCHEMA_BIRDS = load_sql_schema("birds.sql")


def create_connection(db_name: str = "birds.db") -> sqlite3.Connection:
    connection = sqlite3.connect(db_name)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection

def close_connection(connection):
    connection.close()

def create_table(connection: sqlite3.Connection, schema: str)-> None:
    
    cursor = connection.cursor()
    cursor.executescript(schema)


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


def table_add_row(connection: sqlite3.Connection, data: dict, table_name: str = "birds"):
    if connection is None:
        raise ValueError("A valid database connection must be provided.")   
    try:
        cursor = connection.cursor()
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        command = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(command, tuple(data.values()))
        connection.commit()
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while adding row."


if __name__ == "__main__":
    connection = create_connection()
    create_table(connection, SCHEMA_BIRDS)
    create_table(connection, SCHEMA_SIGHTINGS)



