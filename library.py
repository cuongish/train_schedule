import calendar
from datetime import date as Date
from typing import Dict
from typing import List
import os
import requests
import pandas as pd

train_data_endpoint = "https://rata.digitraffic.fi/api/v1/trains"


def get_list_of_days_in_month(year: int, month: int) -> List[Date]:
    number_of_days_in_month = calendar.monthrange(year, month)[1]

    days_in_month = [Date(year, month, day) for day in range(1, number_of_days_in_month+1)]

    return days_in_month


def get_train_data_from_endpoint(date: Date, train_number: int) -> List[Dict]:
    day = date.strftime("%Y-%m-%d")

    url_endpoint = f"{train_data_endpoint}/{day}/{train_number}"
    if not url_endpoint.startswith("https://"):
        raise ValueError('url does not starts with https://')

    header = {"content-type": "application/json"}

    result = requests.get(url=url_endpoint, headers=header)
    if not result.status_code == 200:
        raise AssertionError(f"Expected HTTP code 200, but got {result.status_code}")

    subjects = result.json()

    return subjects


def convert_list_to_normalized_df(data: List[Dict], record_column: str,
                                  meta_columns: List[str]) -> pd.DataFrame:
    result = pd.concat([pd.json_normalize(data=data[i], record_path=record_column,
                                          meta=meta_columns, meta_prefix='meta_')
                        for i in range(len(data))])
    return result


def df_to_csv(df: pd.DataFrame, path: str, csv_file_name: str) -> str:
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, f"{csv_file_name}.csv")

    df.to_csv(file_path)

    print(f'{csv_file_name}.csv is created in {file_path}')
