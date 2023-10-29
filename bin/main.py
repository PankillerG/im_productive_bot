import os

from lib.telegram_bot.bot import Bot

from lib import config
from lib import logging_helpers


logging_helpers.configure_logging(
    filename=config.LOGS_FILE,
)


def main():
    bot = Bot(
        token=os.environ.get('TG_BOT_TOKEN'),
        state_file=config.STATE_FILE,
    )
    bot.run()


if __name__ == '__main__':
    main()
