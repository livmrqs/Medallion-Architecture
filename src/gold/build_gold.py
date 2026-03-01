import os
from pathlib import Path
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sla_calculation import (
    get_sla_expected_hours,
    get_national_holidays,
    calculate_business_hours,
    check_sla_compliance
)

def get_project_paths():
    """
    Resolve Silver and Gold directories.
    """
    base_dir = Path(__file__).resolve().parents[2]

    silver_dir = base_dir / "data" / "silver"
    gold_dir = base_dir / "data" / "gold"
    gold_dir.mkdir(parents=True, exist_ok=True)

    return silver_dir, gold_dir

def read_silver_data(silver_dir: Path) -> pd.DataFrame:
    """
    Read transformed dataset from Silver layer.
    """
    file_path = silver_dir / "silver_issues.parquet"
    return pd.read_parquet(file_path)

def filter_resolved_issues(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only Done and Resolved issues.
    """
    return df[df["status"].isin(["Done", "Resolved"])].copy()

def calculate_sla_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply SLA calculations row by row.
    """

    # Ensure datetime format
    df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
    df["resolved_at"] = pd.to_datetime(df["resolved_at"], utc=True)

    # Collect unique years to minimize API calls
    years = df["created_at"].dt.year.unique()

    holidays = set()
    for year in years:
        holidays.update(get_national_holidays(int(year)))

    resolution_hours_list = []
    sla_expected_list = []
    sla_met_list = []

    for _, row in df.iterrows():

        resolution_hours = calculate_business_hours(
            row["created_at"],
            row["resolved_at"],
            holidays
        )

        sla_expected = get_sla_expected_hours(row["priority"])

        sla_met = check_sla_compliance(
            resolution_hours,
            sla_expected
        )

        resolution_hours_list.append(resolution_hours)
        sla_expected_list.append(sla_expected)
        sla_met_list.append(sla_met)

    df["resolution_hours"] = resolution_hours_list
    df["sla_expected_hours"] = sla_expected_list
    df["is_sla_met"] = sla_met_list

    return df

def generate_reports(df: pd.DataFrame, gold_dir: Path):
    """
    Generate required aggregated reports.
    """

    # SLA by Analyst
    sla_by_analyst = (
        df.groupby("assignee_name")
        .agg(
            issue_count=("issue_id", "count"),
            avg_sla_hours=("resolution_hours", "mean")
        )
        .reset_index()
    )

    # SLA by Issue Type
    sla_by_issue_type = (
        df.groupby("issue_type")
        .agg(
            issue_count=("issue_id", "count"),
            avg_sla_hours=("resolution_hours", "mean")
        )
        .reset_index()
    )

    sla_by_analyst.to_csv(
        gold_dir / "gold_sla_by_analyst.csv",
        index=False
    )

    sla_by_issue_type.to_csv(
        gold_dir / "gold_sla_by_issue_type.csv",
        index=False
    )

def save_gold_table(df: pd.DataFrame, gold_dir: Path):
    """
    Save final SLA table.
    """

    output_path = gold_dir / "gold_sla_issues.csv"
    df.to_csv(output_path, index=False)

    print(f"Gold table saved at: {output_path}")

def main():
    """
    Main execution flow for Gold layer.
    """

    silver_dir, gold_dir = get_project_paths()

    # Step 1: Read Silver
    df = read_silver_data(silver_dir)

    # Step 2: Filter resolved issues
    df = filter_resolved_issues(df)

    # Step 3: Apply SLA calculations
    df = calculate_sla_metrics(df)

    # Step 4: Save final SLA table
    save_gold_table(df, gold_dir)

    # Step 5: Generate reports
    generate_reports(df, gold_dir)

if __name__ == "__main__":
    main()