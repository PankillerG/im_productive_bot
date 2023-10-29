import logging

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from lib.logging_helpers import get_function_logger
from lib.state.client import StateClient
from lib.telegram_bot import jobs
from lib.telegram_bot.handlers import (
    button_handlers,
    command_handlers,
    text_handlers,
)
from lib.telegram_bot.fields import BotDataFields
from lib import config


logger = logging.getLogger(__name__)
function_logger = get_function_logger(logger)


class Bot:
    @function_logger
    def __init__(self, token, state_file):
        self.token = token
        self.state_client = StateClient(file_path=state_file)
    
    @function_logger
    def initialize_data(self):
        self.application.bot_data = {
            BotDataFields.state_client: self.state_client,
            BotDataFields.jobs_data: dict(),
        }

    @function_logger
    def add_handlers(self):
        self.application.add_handler(CommandHandler('start', command_handlers.start))
        self.application.add_handler(CommandHandler('help', command_handlers.help))
        self.application.add_handler(CommandHandler('add_new_habit', command_handlers.add_new_habit))
        self.application.add_handler(CommandHandler('remove_habit', command_handlers.remove_habit))
        self.application.add_handler(CommandHandler('show_habits', command_handlers.show_habits))
        self.application.add_handler(CommandHandler('show_all_habits', command_handlers.show_all_habits))
        self.application.add_handler(CommandHandler('reset_all', command_handlers.reset_all))
        self.application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handlers.text))
        self.application.add_handler(CallbackQueryHandler(button_handlers.button))

    @function_logger
    def add_jobs(self):
        self.application.job_queue.run_repeating(
            jobs.dump_state,
            interval=config.Jobs.DumpState.interval,
            first=config.Jobs.DumpState.first,
        )
        self.application.job_queue.run_repeating(
            jobs.make_state_actual,
            interval=config.Jobs.MakeStateActual.interval,
            first=config.Jobs.MakeStateActual.first,
        )
        self.application.job_queue.run_repeating(
            jobs.show_actual_habits,
            interval=config.Jobs.ShowActualHabits.interval,
            first=config.Jobs.ShowActualHabits.first,
        )

    @function_logger
    def run(self):
        self.application = Application.builder().token(self.token).build()
        self.initialize_data()
        self.add_handlers()
        self.add_jobs()
        self.application.run_polling()
