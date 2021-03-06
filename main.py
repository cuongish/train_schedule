import os

from library import get_train_data_from_endpoint
from library import get_list_of_days_in_month
from library import convert_list_to_normalized_df
from library import df_to_csv

folder = "data"
year = 2020
month = 7
train_number = 4
path = os.path.join(folder, str(year))
meta_columns = ['trainNumber', 'departureDate', 'operatorUICCode', 'operatorShortCode',
                'trainType', 'trainCategory', 'commuterLineID', 'runningCurrently',
                'cancelled', 'version', 'timetableType', 'timetableAcceptanceDate']
record_column = "timeTableRows"


def main():
    # Get datetime.date for days in the month
    days_list = get_list_of_days_in_month(year=year, month=month)
    csv_file_name = f"{days_list[0].strftime('%Y-%m')}-train{train_number}"

    # Iterate API calls to retrieve train traffic data for every day in the month
    data = [get_train_data_from_endpoint(train_number=train_number, date=day)
            for day in days_list]

    # Normalize and output one concat df for the entire month
    result = convert_list_to_normalized_df(data=data,
                                           record_column=record_column,
                                           meta_columns=meta_columns)

    # Output CSV into data folder in data/year/ partition structure
    df_to_csv(df=result,
              path=path,
              csv_file_name=csv_file_name)


if __name__ == "__main__":
    main()
