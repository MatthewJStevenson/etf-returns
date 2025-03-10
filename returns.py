"""
Calculates price return for an ETF over a period of time
Splits and ticker changes are considered
Takes ETF ticker and timeframe as inputs
"""
import sys
import csv
from datetime import date, timedelta, datetime

# TODO: Extend this to dynamically calculate days from any input string, 
# then any timeframe can be given as an input
timeframes = {
    "1 day": 1,
    "5 days": 5,
    "6 months": 182,
    "1 year": 365
}

price_data = None
splits_data = None


def calc_price_return(end_price, start_price):
    return ((end_price / start_price - 1) * 100)


def action_split_calculation(ticker, start_date, end_date, start_price):
    splits = splits_data[ticker]
    for split_date_str, split_ratio in splits.items():
        split_date = datetime.strptime(split_date_str, "%d/%m/%Y").date()
        
        # Only action splits that occurred within timeframe
        if start_date < split_date < end_date:
            numerator, denominator = split_ratio
            start_price *= float(numerator) / float(denominator)
    return start_price


def get_prices_for_period(ticker, timeframe):
    end_date = date(2024, 12, 31)
    start_date = end_date - timedelta(days=timeframes[timeframe])

    # When date is a weekend or holiday, go back to last close price
    while start_date.strftime("%Y-%m-%d") not in price_data[ticker]:
        start_date -= timedelta(days=1)

    end_date_str = end_date.strftime("%Y-%m-%d")
    start_date_str = start_date.strftime("%Y-%m-%d")

    end_price = float(price_data[ticker][end_date_str])
    start_price = float(price_data[ticker][start_date_str])

    # Check if stock split has occured during period
    if ticker in splits_data:
        start_price = action_split_calculation(ticker, start_date, end_date, start_price)

    print(f"Period {start_date_str} to {end_date_str}")
    return end_price, start_price


def read_splits_input():
    data = {}
    with open("splits.csv") as splits_file:
        reader = csv.DictReader(splits_file)
        for row in reader:
            if row["ticker"] not in data:
                data[row["ticker"]] = {row["effective_date"]: [row["from_quantity"], row["to_quantity"]]}
            else:
                data[row["ticker"]][row["effective_date"]] = [row["from_quantity"], row["to_quantity"]]
        return data


def read_price_input():
    data = {}
    with open("prices.csv") as price_file:
        reader = csv.DictReader(price_file)
        for row in reader:
            if row["ticker"] not in data:
                data[row["ticker"]] = {row["date"]: row["close_price"]}
            else:
                data[row["ticker"]][row["date"]] = row["close_price"]
        return data


def valid_arguments():
    return len(sys.argv) == 3 and sys.argv[2] in timeframes


if __name__ == "__main__":
    if not valid_arguments():
        print("Usage: returns.py <ticker> <'timeframe'>")
        print("Example: returns.py NDQ '6 months'")
        sys.exit(1)

    arg_ticker = sys.argv[1]
    arg_timeframe = sys.argv[2]
    print(f"Price return for {arg_ticker} for {arg_timeframe}")

    price_data = read_price_input()
    splits_data = read_splits_input()
    end_price, start_price = get_prices_for_period(arg_ticker, arg_timeframe)
    result = calc_price_return(end_price, start_price)

    print(f"{result:.2f}%")
