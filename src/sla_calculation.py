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

def calculate_business_hours(start_datetime: datetime,
                             end_datetime: datetime,
                             holidays: set) -> float:
    """
    Calculate business hours between two datetimes.
    Excludes weekends and national holidays.
    """

    if end_datetime <= start_datetime:
        return 0.0

    current = start_datetime
    total_hours = 0.0

    while current < end_datetime:
        next_hour = current + timedelta(hours=1)

        is_weekend = current.weekday() >= 5  # 5 = Saturday, 6 = Sunday
        is_holiday = current.date().isoformat() in holidays

        if not is_weekend and not is_holiday:
            total_hours += 1

        current = next_hour

    return total_hours

