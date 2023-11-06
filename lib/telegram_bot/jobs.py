import logging

from telegram import InlineKeyboardMarkup
from telegram.ext import ContextTypes

from lib.date_helpers import get_timestamp
from lib.logging_helpers import get_function_logger
from lib.state.utils import ConvStatuses
from lib.telegram_bot.fields import (
    BotDataFields,
    ConvDataFields,
    JobsDataFields,
)
from lib.telegram_bot.messages import (
    keyboards,
    texts,
)


logger = logging.getLogger(__name__)
function_logger = get_function_logger(logger)


@function_logger
async def dump_state(context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    state_client.dump_state()


@function_logger
async def show_actual_habits(context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    state_client.make_state_actual()

    prev_timestamp = context.bot_data[BotDataFields.jobs_data].get(
        JobsDataFields.show_actual_habits_timetamp,
        None,
    )
    context.bot_data[BotDataFields.jobs_data][JobsDataFields.show_actual_habits_timetamp] = get_timestamp()

    for user_id, habits in state_client.get_users_habits().items():
        if len(habits) == 0:
            continue
        if state_client.get_conv_status(user_id) != ConvStatuses.show_habits:
            continue
        habits_timestamp = state_client.get_habits_timestamp(user_id)
        habits_reset_timestamp = state_client.get_habits_reset_timestamp(user_id)
        if habits_timestamp >= habits_reset_timestamp:
            continue
        if prev_timestamp is not None and prev_timestamp >= habits_reset_timestamp:
            continue
        
        message_id = state_client.get_conv_data_value(
            user_id=user_id,
            key=ConvDataFields.show_habits_message_id,
        )
        await context.bot.edit_message_text(
            text=texts.get_show_habits(habits),
            chat_id=user_id,
            message_id=message_id,
            reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits))
        )
