import sqlite3

_SCHEMA = {
    "bird_id": "INTEGER PRIMARY KEY",
    "german_name": "TEXT",
    "english_name": "TEXT",
    "taxon_rank": "TEXT",
    "taxon_order": "TEXT",
    "taxon_family": "TEXT",
    "family_common_name": "TEXT",
    "scientific_name": "TEXT",
    "status": "TEXT",
    "rl_status": "TEXT",
}

def create_connection(db_name: str = ":memory:") -> sqlite3.Connection:
    connection = sqlite3.connect(db_name)
    return connection

def close_connection(connection):
    connection.close()

def create_table(database_schema: dict, db_name: str = ":memory:", table_name: str = "birds")-> str:
    try:
        connection = create_connection(db_name)
        cursor = connection.cursor()
        command_base = f"CREATE TABLE {table_name} ("
        command =  command_base + ", ".join([f"{column} {data_type}" for column, data_type in database_schema.items()]) + ");"
        cursor.execute(command)
        table_column_info(connection, table_name)
        close_connection(connection)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Error occurred while creating table."
    return "Table created successfully."

def table_column_info(connection: sqlite3.Connection, table_name: str = "birds")-> list:

    cursor = connection.cursor()
    command = f"PRAGMA table_info({table_name})"
    cursor.execute(command)
    column_info = []
    for row in cursor:
        print(f"Column: {row[1]}, Type: {row[2]}, Not Null: {row[3]}, Default Value: {row[4]}, Primary Key: {row[5]}")
        column_info.append(row)

    return column_info

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
    create_table(_SCHEMA)



