import urllib
from pathlib import Path

from decouple import Csv, config
from loguru import logger
from notifiers.logging import NotificationHandler
from notifiers.providers.telegram import Telegram

ROOT_DIR = Path(__file__).resolve().parent


BOT_TOKEN = config("BOT_TOKEN")

DATABASE_USERNAME = config("DATABASE_USERNAME")

DATABASE_PASSWORD = config("DATABASE_PASSWORD")

DATABASE_SUFFIX = config("DATABASE_SUFFIX")


DATABASE_NAME = config("DATABASE_NAME")

LOGGER_FILE_NAME = config("LOGGER_FILE_NAME", default="bot.log")

if config("DATABASE_USE_SRV", default="false").lower() == "true":
    DATABASE_URL_SCHEME = "mongodb+srv"
else:
    DATABASE_URL_SCHEME = "mongodb"

DATABASE_URL = f"{DATABASE_URL_SCHEME}://{urllib.parse.quote_plus(DATABASE_USERNAME)}:{urllib.parse.quote_plus(DATABASE_PASSWORD)}{DATABASE_SUFFIX}"
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
        "telegram",
        defaults={
            "chat_id": config("NOTIFICATION_RECIEPENT_ID"),
            "token": config("NOTIFIER_TOKEN"),
        },
    ),
    level="ERROR",
)


# Admins for the bot

ADMIN_USERS = set([int(s) for s in config("ADMIN_USERS", cast=Csv())])


# Super User of the Bot

SUPER_USER = set([int(s) for s in config("SUPER_USER", cast=Csv())])
