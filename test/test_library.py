# coding: utf-8
import datetime
import unittest
from unittest import mock

import responses

import pandas
from unittest.mock import patch

from library import get_list_of_days_in_month
from library import get_train_data_from_endpoint
from library import convert_list_to_normalized_df
from library import df_to_csv

from library import train_data_endpoint


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_url = "https://test.url"
        cls.test_url_without_https = "http://test.url"
        cls.date_now = datetime.datetime.now()
        cls.date = cls.date_now.strftime("%Y-%m-%d")
        cls.train_number = 4
        cls.url = f'{cls.test_url}/{cls.date}/{cls.train_number}'

        cls.train_correct_response = [
            {
                'trainNumber': cls.train_number,
                'departureDate': cls.date,
                'operatorUICCode': 1,
                'operatorShortCode': 'ab',
                'trainType': 'AB',
                'trainCategory': 'train_category',
                'commuterLineID': '',
                'runningCurrently': False,
                'cancelled': False,
                'version': 12344567890,
                'timetableType': 'TIMETABLE_TYPE',
                'timetableAcceptanceDate': cls.date,
                'timeTableRows': [
                    {'stationShortCode': 'ABC',
                     'stationUICCode': 123,
                     'countryCode': 'FI',
                     'type': 'DEPARTURE',
                     'trainStopping': True,
                     'commercialStop': True,
                     'commercialTrack': '1',
                     'cancelled': False,
                     'scheduledTime': '2020-01-01T03:10:00.000Z',
                     'actualTime': '2020-01-01T03:10:54.000Z',
                     'differenceInMinutes': 1,
                     'causes': [],
                     'trainReady': {'source': 'ABCDEF',
                                    'accepted': True,
                                    'timestamp': '2020-01-01T03:01:36.000Z'}
                     }
                ]
            }
        ]

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