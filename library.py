import calendar
import io
from datetime import date as Date
from typing import Dict
from typing import List

import requests
import pandas as pd

train_data_endpoint = "https://rata.digitraffic.fi/api/v1/trains"


def get_day_in_month_list(year: int, month: int) -> List[Date]:
    number_of_days_in_month = calendar.monthrange(year, month)[1]

    days_in_month = [Date(year, month, day) for day in range(1, number_of_days_in_month+1)]

    return days_in_month


def get_train_data_from_endpoint(date: Date, train_number: int) -> List[Dict]:
    day = date.strftime("%Y-%m-%d")

    url_endpoint = f"{train_data_endpoint}/{day}/{train_number}"

    header = {"content-type": "application/json"}

    result = requests.get(url=url_endpoint, headers=header)
    if not result.status_code == 200:
        raise AssertionError(f"Expected HTTP code 200, but got {result.status_code}")

    subjects = result.json()

    return subjects


def convert_list_to_normalize_df(list_of_data: List[Dict]) -> pd.DataFrame:
    result = pd.DataFrame(list_of_data)
    return result


def df_to_csv(df: pd.DataFrame) -> io.BytesIO:
    result = df.to_csv()
    return result
