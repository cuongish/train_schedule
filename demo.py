from library import get_train_data_from_endpoint
from library import get_day_in_month_list

days_str = get_day_in_month_list(year=2020, month=7)
print(days_str)

train_number = 4

data = get_train_data_from_endpoint(train_number=4, date=days_str[0])
timetable_rows = data[0]['timeTableRows']
print(data)
