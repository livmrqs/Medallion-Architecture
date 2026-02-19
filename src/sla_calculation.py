from datetime import datetime, timedelta
import requests

def get_sla_expected_hours(priority: str) -> int:
    """
    Return expected SLA in hours based on issue priority.
    """

    if priority == "High":
        return 24
    elif priority == "Medium":
        return 72
    elif priority == "Low":
        return 120
    else:
        return None

def get_national_holidays(year: int) -> set:
    """
    Fetch Brazilian national holidays from public API.
    Returns a set of dates (YYYY-MM-DD).
    """

    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/BR"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch holidays from API")

    holidays = response.json()

    return {holiday["date"] for holiday in holidays}

