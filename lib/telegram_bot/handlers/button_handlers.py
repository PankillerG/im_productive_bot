import logging

from telegram import (
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes

from lib.logging_helpers import get_function_logger
from lib.state.utils import ConvStatuses
from lib.telegram_bot.fields import (
    BotDataFields,
    ConvDataFields
)
from lib.telegram_bot.messages import (
    keyboards,
    texts,
)


logger = logging.getLogger(__name__)
funciton_logger = get_function_logger(logger)


@funciton_logger
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    state_client = context.bot_data[BotDataFields.state_client]
    user_id = query.from_user.id
    conv_status = state_client.get_conv_status(user_id)

    if conv_status == ConvStatuses.waiting_habit_time_of_day_to_add:
        habit_name = state_client.get_conv_data_value(user_id, ConvDataFields.habit_name)
        habit_time_of_day = query.data
        state_client.set_conv_data_value(
            user_id=user_id,
            key=ConvDataFields.habit_time_of_day,
            value=habit_time_of_day,
        )
        state_client.set_conv_status(
            user_id=user_id,
            status=ConvStatuses.waiting_habit_repeat_period_to_add,
        )
        await query.edit_message_text(
            text=texts.waiting_habit_repeat_period_to_add.format(habit_name=habit_name),
            reply_markup=InlineKeyboardMarkup(keyboards.waiting_habit_repeat_period_to_add),
        )

    if conv_status == ConvStatuses.waiting_habit_repeat_period_to_add:
        habit_name = state_client.get_conv_data_value(user_id, ConvDataFields.habit_name)
        habit_repeat_period = query.data
        state_client.set_conv_data_value(
            user_id=user_id,
            key=ConvDataFields.habit_repeat_period,
            value=habit_repeat_period,
        )
        state_client.set_conv_status(
            user_id=user_id,
            status=ConvStatuses.waiting_habit_repeat_count_to_add,
        )
        await query.edit_message_text(
            text=texts.waiting_habit_repeat_count_to_add.format(
                habit_name=habit_name,
                habit_repeat_period=habit_repeat_period,
            ),
            reply_markup=InlineKeyboardMarkup(keyboards.waiting_habit_repeat_count_to_add),
        )

    elif conv_status == ConvStatuses.waiting_habit_repeat_count_to_add:
        habit_name = state_client.get_conv_data_value(user_id, ConvDataFields.habit_name)
        habit_time_of_day = state_client.get_conv_data_value(user_id, ConvDataFields.habit_time_of_day)
        habit_repeat_period = state_client.get_conv_data_value(user_id, ConvDataFields.habit_repeat_period)
        habit_repeat_count = int(query.data)
        state_client.add_habit(
            user_id=user_id,
            name=habit_name,
            time_of_day=habit_time_of_day,
            repeat_period=habit_repeat_period,
            repeat_count=habit_repeat_count,
        )
        state_client.set_conv_status(
            user_id=user_id,
            status=ConvStatuses.default,
        )
        await query.edit_message_text(texts.habit_was_added.format(
            habit_name=habit_name,
            habit_time_of_day=habit_time_of_day,
            habit_repeat_period=habit_repeat_period,
            habit_repeat_count=habit_repeat_count,
        ))
    
    elif conv_status == ConvStatuses.waiting_habit_id_to_remove:
        habit_id = query.data
        state_client.remove_habit(user_id, habit_id)
        habits = state_client.get_habits(user_id, actual=False)
        await query.edit_message_text(
            text=texts.get_remove_habits(habits),
            reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits))
        )

    elif conv_status == ConvStatuses.show_habits:
        habit_id = query.data
        state_client.increase_done_count(user_id, habit_id)
        habits = state_client.get_habits(user_id)
        await query.edit_message_text(
            text=texts.get_show_habits(habits),
            reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits))
        )
