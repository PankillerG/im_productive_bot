class StateFiels:
    conv_status = 'conv_status'
    conv_data = 'conv_data'
    habits = 'habits'
    habits_timestamp = 'habits_timestamp'
    habits_reset_timestamp = 'habits_reset_timestamp'
    timestamp = 'timestamp'


class ConvStatuses:
    default = None
    waiting_habit_name_to_add = 'waiting_habit_name_to_add'
    waiting_habit_repeat_period_to_add = 'waiting_habit_repeat_period_to_add'
    waiting_habit_repeat_count_to_add = 'waiting_habit_repeat_count_to_add'
    show_habits = 'show_habits'
    waiting_habit_id_to_remove = 'waiting_habit_id_to_remove'
