from pathlib import Path
import json
import pandas as pd

def get_project_paths():
    """
    Resolve project directories for Bronze and Silver layers.
    """
    base_dir = Path(__file__).resolve().parents[2]
    bronze_dir = base_dir / "data" / "bronze"
    silver_dir = base_dir / "data" / "silver"
    silver_dir.mkdir(parents=True, exist_ok=True)

    return bronze_dir, silver_dir

def read_bronze_data(bronze_dir: Path) -> dict:
    """
    Read raw JSON file from Bronze layer.
    """
    file_path = bronze_dir / "bronze_issues.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)