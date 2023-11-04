from collections import defaultdict
import json
import logging
import os
from typing import (
    Any,
    Union,
)

from lib.date_helpers import get_timestamp
from lib.logging_helpers import get_function_logger
from lib.state.habit import (
    create_habit,
    get_habit_sort_key,
    HabitFields,
    need_reset_habit,
)
from lib.state.utils import (
    ConvStatuses,
    StateFiels,
)


logger = logging.getLogger(__name__)
function_logger = get_function_logger(logger)


class StateClient:
    @function_logger
    def __init__(self, file_path: str=None, serialized_state: str=None):
        self.file_path = file_path
        self.state = self._get_state(file_path, serialized_state)
    
    @function_logger
    def _get_default_serialized_state(self):
        return '{}'
    
    @function_logger
    def _get_default_state(self):
        timestamp = get_timestamp()
        return defaultdict(lambda: {
            StateFiels.conv_status: ConvStatuses.default,
            StateFiels.conv_data: dict(),
            StateFiels.habits: defaultdict(list),
            StateFiels.habits_timestamp: timestamp,
            StateFiels.habits_reset_timestamp: timestamp,
            StateFiels.timestamp: timestamp,
        })
    
    @function_logger
    def state_parse_from_string(self, serialized_state: str):
        return json.loads(serialized_state)
    
    @function_logger
    def state_serialize_to_string(self, state: dict):
        return json.dumps(self.state)
    
    @function_logger
    def dump_state(self):
        with open(self.file_path, 'w') as state_file:
            state_file.write(self.state_serialize_to_string(self.state))
    
    @function_logger
    def _get_state(self, file_path: str, serialized_state: str):
        state = self._get_default_state()
        if os.path.exists(file_path):
            with open(file_path, 'r') as state_file:
                state.update(json.load(state_file))
        else:
            if serialized_state is None:
                serialized_state = self._get_default_serialized_state() 
            state.update(self.state_parse_from_string(serialized_state))
        return state
    
    @function_logger
    def get_timestamp(self, user_id: Union[int, str]):
        return self.state[str(user_id)][StateFiels.timestamp]
    
    @function_logger
    def set_timestamp(self, user_id: Union[int, str], timestamp: float=None):
        timestamp = get_timestamp(timestamp)
        self.state[str(user_id)][StateFiels.timestamp] = timestamp

    @function_logger
    def get_habits_timestamp(self, user_id: Union[int, str]):
        return self.state[str(user_id)][StateFiels.habits_timestamp]
    
    @function_logger
    def set_habits_timestamp(self, user_id: Union[int, str], timestamp: float=None):
        user_id = str(user_id)
        timestamp = get_timestamp(timestamp)
        self.state[user_id][StateFiels.habits_timestamp] = timestamp
        self.state[user_id][StateFiels.timestamp] = timestamp

    @function_logger
    def get_habit_reset_timestamp(self, user_id: Union[int, str], habit_id: str):
        return self.state[str(user_id)][StateFiels.habits][habit_id][HabitFields.reset_timestamp]

    @function_logger
    def set_habit_reset_timestamp(self, user_id: Union[int, str], habit_id: str, timestamp: float=None):
        timestamp = get_timestamp(timestamp)
        user_id = str(user_id)
        self.state[user_id][StateFiels.habits][habit_id][HabitFields.reset_timestamp] = timestamp
        self.state[user_id][StateFiels.habits_reset_timestamp] = timestamp

    @function_logger
    def get_habits_reset_timestamp(self, user_id: Union[int, str]):
        return self.state[str(user_id)][StateFiels.habits_reset_timestamp]
    
    @function_logger
    def set_habits_reset_timestamp(self, user_id: Union[int, str], timestamp: float=None):
        timestamp = get_timestamp(timestamp)
        self.state[str(user_id)][StateFiels.habits_reset_timestamp] = timestamp  

    @function_logger
    def get_conv_status(self, user_id: Union[int, str]):
        return self.state[str(user_id)][StateFiels.conv_status]
    
    @function_logger
    def set_conv_status(self, user_id: Union[int, str], status: str):
        user_id = str(user_id)
        self.state[user_id][StateFiels.conv_status] = status 
        self.set_timestamp(user_id)
    
    @function_logger
    def get_conv_data_value(self, user_id: Union[int, str], key: Any):
        return self.state[str(user_id)][StateFiels.conv_data][key]
    
    @function_logger
    def set_conv_data_value(self, user_id: Union[int, str], key: Any, value: Any):
        user_id = str(user_id)
        self.state[user_id][StateFiels.conv_data][key] = value
        self.set_timestamp(user_id)

    @function_logger
    def add_habit(
        self,
        user_id: Union[int, str],
        name: str,
        time_of_day : str,
        repeat_period: str,
        repeat_count: int,
    ):
        user_id = str(user_id)
        habit = create_habit(name, time_of_day, repeat_period, repeat_count)
        self.state[user_id][StateFiels.habits][habit[HabitFields.id]] = habit
        self.set_habits_timestamp(user_id)

    @function_logger
    def remove_habit(self, user_id: Union[int, str], habit_id: str):
        user_id = str(user_id)
        del self.state[user_id][StateFiels.habits][habit_id]
        self.set_habits_timestamp(user_id)
    
    @function_logger
    def get_habits(self, user_id: Union[int, str], actual: bool=True):
        habits = list(sorted(
            self.state[str(user_id)][StateFiels.habits].values(),
            key=lambda habit: get_habit_sort_key(habit),
        ))
        if actual:
            habits = list(filter(
                lambda habit: habit[HabitFields.done_count] < habit[HabitFields.repeat_count],
                habits,
            ))
        return habits

    @function_logger
    def reset_user_state(self, user_id: Union[int, str]):
        user_id = str(user_id)
        if user_id in self.state:
            del self.state[user_id]

    @function_logger
    def get_users_habits(self, actual: bool=True):
        users_habits = dict()
        for user_id in self.state:
            users_habits[user_id] = self.get_habits(user_id, actual)
        return users_habits

    @function_logger
    def increase_done_count(self, user_id: Union[int, str], habit_id: str):
        user_id = str(user_id)
        self.state[user_id][StateFiels.habits][habit_id][HabitFields.done_count] += 1
        self.set_habits_timestamp(user_id)

    @function_logger
    def _reset_habit(self, user_id: Union[int, str], habit_id: str, timestamp: float=None):
        user_id = str(user_id)
        timestamp = get_timestamp(timestamp)
        self.state[user_id][StateFiels.habits][habit_id][HabitFields.done_count] = 0
        self.set_habit_reset_timestamp(user_id, habit_id, timestamp)

    @function_logger
    def make_state_actual(self, timestamp: float=None):
        timestamp = get_timestamp(timestamp)
        for user_id, user_state in self.state.items():
            for habit_id, habit in user_state[StateFiels.habits].items():
                if need_reset_habit(habit, timestamp):
                    self._reset_habit(user_id, habit_id, timestamp)
