start = """
Welcome to @im_productive_bot. It\'s easy to controll your habits. Use:
- /add_new_habit - to add new habit.
- /remove_habit - to remove habit. Then click on the habit to remove it.
- /show_habits - to show all your actual habits. The bot will always show actual habits, even if the habit period has been updated (for example, new day/week/month has come). Then click on the habit to mark it as completed.
- /show_all_habits - to show all habits.
Just try and get high!
"""

waiting_habit_name_to_add = """
Write the habit name:
"""

waiting_habit_time_of_day_to_add = """
Select time of day for doing habit {habit_name}:
"""

show_habits_not_empty = """
Your habits:
"""

show_habits_empty = """
You don't have any habits right now. Use /add_new_habit command to add them.
"""

remove_habits_not_empty = """
Select habit to remove:
"""

waiting_habit_repeat_period_to_add = """
Select repeat period for {habit_name}
"""

waiting_habit_repeat_count_to_add = """
Select repeat count for {habit_name} per {habit_repeat_period}
"""

habit_was_added = """
Habit was added:
Name: {habit_name}
Time of day: {habit_time_of_day}
Repeat period: {habit_repeat_period}
Repeat count: {habit_repeat_count}

Use:
- /add_new_habit to add more habits
- /show_habits to show added habits
"""

reseted_user_data = """
You just reseted all your data!
"""


def get_show_habits(habits):
    return show_habits_not_empty if len(habits) > 0 else show_habits_empty


def get_remove_habits(habits):
    return remove_habits_not_empty if len(habits) > 0 else show_habits_empty
