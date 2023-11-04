from telegram import InlineKeyboardButton


waiting_habit_time_of_day_to_add = [
    [
        InlineKeyboardButton('Morning', callback_data='morning'),
        InlineKeyboardButton('Afternoon', callback_data='afternoon'),
        InlineKeyboardButton('Evening', callback_data='evening'),
    ],
]

waiting_habit_repeat_period_to_add = [
    [
        InlineKeyboardButton('Day', callback_data='days'),
        InlineKeyboardButton('Week', callback_data='weeks'),
        InlineKeyboardButton('Month', callback_data='months'),
    ],
]

waiting_habit_repeat_count_to_add = [
    [
        InlineKeyboardButton('1', callback_data='1'),
        InlineKeyboardButton('2', callback_data='2'),
        InlineKeyboardButton('3', callback_data='3'),
    ],
    [
        InlineKeyboardButton('4', callback_data='4'),
        InlineKeyboardButton('5', callback_data='5'),
        InlineKeyboardButton('6', callback_data='6'),
    ],
]


def get_show_habits(habits):
    return [
        [
            InlineKeyboardButton(f'{habit["name"]} | {habit["done_count"]}/{habit["repeat_count"]} per {habit["repeat_period"]}', callback_data=habit['id'])
        ]
        for habit in habits
    ]
