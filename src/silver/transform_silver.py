from pathlib import Path
import json
import pandas as pd

def get_project_paths():
    """
    Resolve project directories for Bronze and Silver layers
    """
    base_dir = Path(__file__).resolve().parents[2]
    bronze_dir = base_dir / "data" / "bronze"
    silver_dir = base_dir / "data" / "silver"
    silver_dir.mkdir(parents=True, exist_ok=True)

    return bronze_dir, silver_dir

def read_bronze_data(bronze_dir: Path) -> dict:
    """
    Read raw JSON file from Bronze layer
    """
    file_path = bronze_dir / "bronze_issues.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def normalize_issues(json_data: dict) -> pd.DataFrame:
    """
    Normalize nested JSON structure into a flat DataFrame
    """

    # Flatten main issues structure
    df = pd.json_normalize(
        json_data["issues"],
        sep="_"
    )

    # Explode nested lists (if applicable)
    if "assignee" in df.columns:
        df = df.explode("assignee")

    if "timestamps" in df.columns:
        df = df.explode("timestamps")

    # Normalize nested assignee object
    if "assignee" in df.columns:
        assignee_df = pd.json_normalize(df["assignee"]).add_prefix("assignee_")
        df = df.drop(columns=["assignee"]).reset_index(drop=True).join(assignee_df)

    # Normalize nested timestamps object
    if "timestamps" in df.columns:
        timestamps_df = pd.json_normalize(df["timestamps"])
        df = df.drop(columns=["timestamps"]).reset_index(drop=True).join(timestamps_df)

    return df

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to snake_case
    """

    df.columns = (
        df.columns
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )

    # Rename specific fields
    rename_map = {
        "id": "issue_id",
        "fields_priority_name": "priority",
        "fields_issuetype_name": "issue_type",
        "fields_status_name": "status",
        "fields_created": "created_at",
        "fields_resolutiondate": "resolved_at",
        "fields_assignee_displayname": "assignee_name"
    }

    df = df.rename(columns=rename_map)

    return df