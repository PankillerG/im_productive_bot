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
    ConvDataFields,
)
from lib.telegram_bot.messages import (
    keyboards,
    texts,
)


logger = logging.getLogger(__name__)
function_logger = get_function_logger(logger)


@function_logger
async def text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    user_id = update.message.from_user.id
    conv_status = state_client.get_conv_status(user_id)

    if conv_status == ConvStatuses.waiting_habit_name_to_add:
        habit_name = update.message.text
        state_client.set_conv_data_value(
            user_id=user_id,
            key=ConvDataFields.habit_name,
            value=habit_name,
        )
        state_client.set_conv_status(
            user_id=user_id,
            status=ConvStatuses.waiting_habit_time_of_day_to_add,
        )
        await update.message.reply_text(
            text=texts.waiting_habit_time_of_day_to_add.format(habit_name=habit_name),
            reply_markup=InlineKeyboardMarkup(keyboards.waiting_habit_time_of_day_to_add),
        )
