import datetime
import calendar
from typing import List

import requests


train_data_endpoint = "https://rata.digitraffic.fi/api/v1/trains"


def get_day_in_month_list(year: int, month: int) -> List[str]:
    number_of_days_in_month = calendar.monthrange(year, month)[1]
    days_in_month = [datetime.date(year, month, day) for day in range(1, number_of_days_in_month+1)]
    date = [day.strftime("%Y-%m-%d") for day in days_in_month]

    return date


def get_train_data_from_endpoint(date: str, train_number: int) -> List:
    url_endpoint = f"{train_data_endpoint}/{date}/{train_number}"

    header = {"content-type": "application/json"}

    result = requests.get(url=url_endpoint, headers=header)
    if not result.status_code == 200:
        raise AssertionError(f"Expected HTTP code 200, but got {result.status_code}")

    subjects = result.json()

    return subjects
