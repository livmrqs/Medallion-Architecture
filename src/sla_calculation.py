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