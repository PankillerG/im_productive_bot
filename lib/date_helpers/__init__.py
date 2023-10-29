from datetime import datetime
import time


def get_timestamp(timestamp=None):
    return time.time() if timestamp is None else timestamp


def is_days_equal(first_timestamp, second_timestamp):
    datetime.fromtimestamp(first_timestamp).date == \
        datetime.fromtimestamp(second_timestamp).date


def is_weeks_equal(first_timestamp, second_timestamp):
    datetime.fromtimestamp(first_timestamp).isocalendar().week == \
        datetime.fromtimestamp(second_timestamp).isocalendar().week


def is_months_equal(first_timestamp, second_timestamp):
    datetime.fromtimestamp(first_timestamp).month == \
        datetime.fromtimestamp(second_timestamp).month


def is_periods_equal(first_timestamp, second_timestamp, period):
    if period == 'days':
        return is_days_equal(first_timestamp, second_timestamp)
    elif period == 'weeks':
        return is_weeks_equal(first_timestamp, second_timestamp)
    elif period == 'months':
        return is_months_equal(first_timestamp, second_timestamp)
