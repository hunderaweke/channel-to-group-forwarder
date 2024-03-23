from pathlib import Path

from decouple import Csv, config
from loguru import logger
from notifiers.logging import NotificationHandler
from notifiers.providers.telegram import Telegram

ROOT_DIR = Path(__file__).resolve().parent


BOT_TOKEN = config("BOT_TOKEN")

DATABASE_URL = config("DATABASE_URL")

DATABASE_NAME = config("DATABASE_NAME")

LOGGER_FILE_NAME = config("LOGGER_FILE_NAME", default="bot.log")

# Debugger log file

logger.add(
    ROOT_DIR.parent / "logs" / LOGGER_FILE_NAME,
    rotation=config("LOG_ROTATION_SIZE", default="50 MB"),
    backtrace=True,
    diagnose=True,
    level="DEBUG",
)

# Error Notifier

logger.add(
    NotificationHandler(
        provider=Telegram(
            chat_id=config("NOTIFICATION_RECIEPENT_ID"),
            token=config("NOTIFIER_TOKEN"),
        ),
    ),
    level="ERROR",
)

# Admins for the bot

SUPER_USERS = config("SUPER_USERS", cast=Csv())
