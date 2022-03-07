# train_schedule
A python library to retrieve Finnish train traffic public data and output normalized csv.

### Virtual environment
- Create the virtualenv
```bash 
virtualenv -p python3.8 venv
```
- Activate the virtualenv
```bash
source venv/bin/activate
```

### How to Run It
- Install requirements as usual:
    ```bash
       pip install -r requirements/requirements.txt
       pip install -r requirements/test-requirements.txt
    ```

- Run unit tests with coverage:
  ```bash
  coverage run -m pytest
  ```
- Demo 1: Collect data for the whole month of July 2020 for train number 4 using train traffic API, normalize the data
and write the final output in a csv file.
  ```bash
    python3 main.py
  ```
- Demo 2: Calculate the average actual arrival time at the final destination of the train during the month July 2020. 
  ```bash
    jupyter notebook analysis.ipynb
  ```

### Improvement TODO:
- Add integration test for main.py
- Implement pauses and attempts-count in-between API call to avoid timeout similar to [this function](https://github.com/cuongish/unigloo/blob/69ec836dbc6865ef006e1b9269286fd6ed94b7a3/unigloo_lib.py#L29).
- Iterating through nested loop will retrieve entire history of data.
```python
    month_list = [1,...,12]
    year_list = [2016,...,2021]
    train_number = 4
    for year in year_list:
        for month in month_list:
            ...
 ```
    