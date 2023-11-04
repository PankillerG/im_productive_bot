import logging
import time
import uuid

from lib.date_helpers import is_periods_equal
from lib.logging_helpers import get_function_logger


logger = logging.getLogger(__name__)
function_logger = get_function_logger(logger)

time_of_day_name_to_id = {
    'morning': 0,
    'afternoon': 1,
    'evening': 2,
}


class RepeatPeriods:
    day = 'day'
    week = 'week'
    month = 'month'


class HabitFields:
    id = 'id'
    name = 'name'
    time_of_day = 'time_of_day'
    repeat_period = 'repeat_period'
    repeat_count = 'repeat_count'
    done_count = 'done_count'
    reset_timestamp = 'reset_timestamp'


@function_logger
def generate_habit_id():
    return str(uuid.uuid4())


@function_logger
def get_habit_time_of_day_id(time_of_day: str):
    return time_of_day_name_to_id[time_of_day]


@function_logger
def get_habit_sort_key(habit: dict):
    habit_time_of_day_id = get_habit_time_of_day_id(habit[HabitFields.time_of_day])
    return f'{habit_time_of_day_id}__{habit[HabitFields.name]}'
    

@function_logger
def create_habit(name: str, time_of_day: str, repeat_period: str, repeat_count: int):
    return {
        HabitFields.id: generate_habit_id(),
        HabitFields.name: name,
        HabitFields.time_of_day: time_of_day,
        HabitFields.repeat_period: repeat_period,
        HabitFields.repeat_count: repeat_count,
        HabitFields.done_count: 0,
        HabitFields.reset_timestamp: time.time(),
    }


@function_logger
def need_reset_habit(habit: dict, timestamp: float=time.time()):
    if habit[HabitFields.done_count] == 0:
        return False
    habit_reset_timestamp = habit[HabitFields.reset_timestamp]
    habit_repeat_period = habit[HabitFields.repeat_period]
    return not is_periods_equal(habit_reset_timestamp, timestamp, habit_repeat_period)
