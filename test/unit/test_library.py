# coding: utf-8
import datetime
import os
import unittest
from unittest import mock

import pandas as pd
import responses
import shutil

from library import get_list_of_days_in_month
from library import get_train_data_from_endpoint
from library import convert_list_to_normalized_df
from library import df_to_csv


class TestLibrary(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_url = "https://test.url"
        cls.test_url_without_https = "http://test.url"
        cls.date_now = datetime.datetime.now()
        cls.date = cls.date_now.strftime("%Y-%m-%d")
        cls.train_number = 4
        cls.url = f'{cls.test_url}/{cls.date}/{cls.train_number}'

        cls.train_correct_response = [{
            'column1': 'string1',
            'column2': 'string2',
            'record_column': [
                {
                    'column1': 'string11',
                    'column2': 'string21'
                },
                {
                    'column1': 'string12',
                    'column2': 'string22'
                },
                {
                    'column1': 'string13',
                    'column2': 'string23'
                }
            ]
        }
        ]

        cls.result_df = convert_list_to_normalized_df(data=cls.train_correct_response,
                                                      record_column='record_column',
                                                      meta_columns=['column1', 'column2'])
        cls.path = 'test_data'
        cls.csv_file_name = 'test_file'
        cls.file_path = os.path.join(cls.path, f"{cls.csv_file_name}.csv")

    def test_get_list_of_days_in_month__returns_29_days_for_february_in_leap_year(self):
        expected = 29
        result = len(get_list_of_days_in_month(year=2020, month=2))
        self.assertEqual(expected, result)

    def test_get_list_of_days_in_month__returns_31_days_for_long_months(self):
        long_months = [1, 3, 5, 7, 8, 10, 12]
        expected = 31
        result = [get_list_of_days_in_month(year=2020, month=month) for month in long_months]
        [self.assertEqual(expected, len(days_in_month)) for days_in_month in result]

    def test_get_list_of_days_in_month__returns_30_days_for_short_months(self):
        short_months = [4, 6, 9, 11]
        expected = 30
        result = [get_list_of_days_in_month(year=2020, month=month) for month in short_months]
        [self.assertEqual(expected, len(days_in_month)) for days_in_month in result]

    @responses.activate
    def test_get_train_data_from_endpoint__raises_exception_if_http_response_status_code_is_not_200(self):
        with mock.patch('library.train_data_endpoint', self.test_url):
            responses.add(responses.GET, url=self.url, status=404)
            with self.assertRaises(Exception):
                get_train_data_from_endpoint(date=self.date_now, train_number=self.train_number)

    @responses.activate
    def test_get_train_data_from_endpoint__raises_exception_if_url_does_not_start_with_https(self):
        with mock.patch('library.train_data_endpoint', self.test_url_without_https):
            with self.assertRaises(Exception):
                get_train_data_from_endpoint(date=self.date_now, train_number=self.train_number)

    @responses.activate
    def test_get_train_data_from_endpoint__returns_server_response(self):
        with mock.patch('library.train_data_endpoint', self.test_url):
            responses.add(responses.GET, url=self.url,
                          json=self.train_correct_response, status=200)
            resp = get_train_data_from_endpoint(date=self.date_now,
                                                train_number=self.train_number)
            self.assertEqual(self.train_correct_response, resp)

    def test_convert_list_to_normalized_df__returns_correct_number_of_record_rows(self):
        self.assertEqual(3, len(self.result_df.index))

    def test_convert_list_to_normalized_df__returns_correct_number_of_record_columns(self):
        self.assertEqual(4, len(self.result_df.columns))

    def test_convert_list_to_normalized_df__prefixed_meta_column_to_avoid_duplicates(self):
        self.assertTrue({'meta_column1',
                         'meta_column2'}.issubset(self.result_df.columns))

    def test_df_to_csv__file_exists_and_is_readable(self):
        df_to_csv(df=pd.DataFrame(),
                  path=self.path,
                  csv_file_name=self.csv_file_name)
        self.assertTrue(os.access(self.file_path, os.R_OK))

    def test_df_to_csv__overwrites_if_folder_exists(self):
        # running df_to_csv on test_file1 creates /Path/ folder
        # and running on test_file2 overwrites the existing folder
        list_of_csv = ['test_file1', 'test_file2']

        [df_to_csv(df=pd.DataFrame(),
                   path=self.path,
                   csv_file_name=csv) for csv in list_of_csv]

        self.assertTrue(os.path.isfile(self.file_path))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.path)
