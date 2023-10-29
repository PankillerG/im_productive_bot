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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(texts.start)


@function_logger
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(texts.start)


@function_logger
async def add_new_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    state_client.set_conv_status(
        user_id=update.message.from_user.id,
        status=ConvStatuses.waiting_habit_name_to_add,
    )
    await update.message.reply_text(texts.waiting_habit_name_to_add)


@function_logger
async def remove_habit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    user_id = update.message.from_user.id
    habits = state_client.get_habits(user_id, actual=False)
    state_client.set_conv_status(
        user_id=user_id,
        status=ConvStatuses.waiting_habit_id_to_remove,
    )
    await update.message.reply_text(
        text=texts.get_remove_habits(habits),
        reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits))
    )


@function_logger
async def show_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    user_id = update.message.from_user.id
    habits = state_client.get_habits(user_id)
    state_client.set_conv_status(
        user_id=user_id,
        status=ConvStatuses.show_habits,
    )
    replied_message = await update.message.reply_text(
        text=texts.get_show_habits(habits),
        reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits))
    )
    state_client.set_conv_data_value(
        user_id=user_id,
        key=ConvDataFields.show_habits_message_id,
        value=replied_message.message_id,
    )


@function_logger
async def show_all_habits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    user_id = update.message.from_user.id
    habits = state_client.get_habits(user_id, actual=False)
    state_client.set_conv_status(
        user_id=user_id,
        status=ConvStatuses.default,
    )
    await update.message.reply_text(
        text=texts.get_show_habits(habits),
        reply_markup=InlineKeyboardMarkup(keyboards.get_show_habits(habits)),
    )


@function_logger
async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state_client = context.bot_data[BotDataFields.state_client]
    state_client.reset_user_state(update.message.from_user.id)
    state_client.set_conv_status(ConvStatuses.default)
    await update.message.reply_text(texts.reseted_user_data)
