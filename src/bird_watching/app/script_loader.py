from pathlib import Path

# --- LOAD SCHEMA ---
def load_sql(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
