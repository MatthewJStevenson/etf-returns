"""
Example tests for ETF returns functions
Usage: python -m unittest tests.py
"""

import unittest

from returns import get_prices_for_period, calc_price_return, sort_dates, unittest_setup

class TestReturns(unittest.TestCase):

    def test_five_day_return(self):
        unittest_setup()
        ticker = "ETHI"
        timeframe = "5 days"
        expected_start_price = 16.18
        expected_end_price = 16.10

        actual_end_price, actual_start_price = get_prices_for_period(ticker, timeframe)
        # Test the correct close_prices
        self.assertListEqual([actual_start_price, actual_end_price], [expected_start_price, expected_end_price])

        expected_price_return = ((float(expected_end_price) / float(expected_start_price)) - 1) * 100
        actual_price_return = calc_price_return(actual_end_price, actual_start_price)
        self.assertEqual(actual_price_return, expected_price_return) # Test return calculation is accurate


    def test_get_prices(self):
        unittest_setup()
        ticker = "NDQ"
        timeframe = "6 months"
        expected_start_price = 44.24
        expected_end_price = 50.75

        actual_end_price, actual_start_price = get_prices_for_period(ticker, timeframe)
        # Test the correct close_prices
        self.assertListEqual([actual_start_price, actual_end_price], [expected_start_price, expected_end_price])

        expected_price_return = ((float(expected_end_price) / float(expected_start_price)) - 1) * 100
        actual_price_return = calc_price_return(actual_end_price, actual_start_price)
        self.assertEqual(actual_price_return, expected_price_return) # Test return calculation is accurate


    def test_ticker_change(self):
        unittest_setup()
        ticker = "CYBR"
        timeframe = "1 year"
        expected_start_price = 10.83
        expected_end_price = 14.02

        actual_end_price, actual_start_price = get_prices_for_period(ticker, timeframe)
        # Test the correct close_prices
        self.assertListEqual([actual_start_price, actual_end_price], [expected_start_price, expected_end_price])

        expected_price_return = ((float(expected_end_price) / float(expected_start_price)) - 1) * 100
        actual_price_return = calc_price_return(actual_end_price, actual_start_price)
        self.assertEqual(actual_price_return, expected_price_return) # Test return calculation is accurate


    def test_split(self):
        unittest_setup()
        ticker = "A123"
        timeframe = "1 year"
        expected_start_price_after_split = 126.93 / 5
        expected_end_price = 27.42

        actual_end_price, actual_start_price = get_prices_for_period(ticker, timeframe)
        # Test the correct close_prices
        self.assertListEqual([actual_start_price, actual_end_price], [expected_start_price_after_split, expected_end_price])

        expected_price_return = ((float(expected_end_price) / float(expected_start_price_after_split)) - 1) * 100
        actual_price_return = calc_price_return(actual_end_price, actual_start_price)
        self.assertEqual(actual_price_return, expected_price_return) # Test return calculation is accurate


    def test_sort(self):
        test_list = ["2024-06-07", "2024-05-30", "2024-08-15", "2024-08-20", "2023-12-27", "2023-12-13", "2024-06-28"]
        expected = ["2023-12-13", "2023-12-27", "2024-05-30", "2024-06-07", "2024-06-28", "2024-08-15", "2024-08-20"]
        actual = sort_dates(test_list)
        self.assertEqual(actual, expected) # Test sort works with odd number of elements, this passes :)

        expected = ["2023-12-13", "2023-12-27", "2024-05-30", "2024-06-07", "2024-06-28", "2024-08-15", "2024-08-20", "2025-02-03"]
        test_list = ["2024-06-07", "2024-05-30", "2024-08-15", "2024-08-20", "2025-02-03", "2023-12-27", "2023-12-13", "2024-06-28"]
        actual = sort_dates(test_list)
        self.assertEqual(actual, expected) # Test sort works with even number of elements, this passes :)

        expected = ["2023-12-13", "2023-12-27", "2024-05-30", "2024-06-07", "2024-06-28", "2024-08-15", "2024-08-20"]
        test_list = ["2024/06/07", "2024-05-30", "2024-08-15", "2024/08/20", "2023-12-27", "2023-12-13", "2024-06-28"]
        actual = sort_dates(test_list)
        self.assertEqual(actual, expected) # Test different date formats, this fails :(

        test_list = ["2024-06-07"]
        expected = ["2024-06-07"]
        actual = sort_dates(test_list)
        self.assertEqual(actual, expected) # Test single element list, this passes :)

        test_list = []
        expected = []
        actual = sort_dates(test_list)
        self.assertEqual(actual, expected) # Test empty list, this passes :)


if __name__ == "__main__":
    unittest.main()
