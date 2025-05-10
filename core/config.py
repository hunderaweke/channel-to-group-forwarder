import urllib
from pathlib import Path

from decouple import Csv, RepositoryEnv, Config
from loguru import logger
from notifiers.logging import NotificationHandler
from notifiers.providers.telegram import Telegram

ROOT_DIR = Path(__file__).resolve().parent.parent

config = Config(RepositoryEnv(ROOT_DIR / ".env"))

ADMIN_USERS = set([int(s) for s in config.get("ADMIN_USERS", cast=Csv())])

SUPER_USER = set([int(s) for s in config.get("SUPER_USER", cast=Csv())])

BOT_TOKEN = config.get("BOT_TOKEN")

DATABASE_USERNAME = config.get("DATABASE_USERNAME")

DATABASE_PASSWORD = config.get("DATABASE_PASSWORD")

DATABASE_SUFFIX = config.get("DATABASE_SUFFIX")

DATABASE_NAME = config.get("DATABASE_NAME")

LOGGER_FILE_NAME = config.get("LOGGER_FILE_NAME", default="bot.log")

if config.get("DATABASE_USE_SRV", default="false").lower() == "true":
    DATABASE_URL_SCHEME = "mongodb+srv"
else:
    DATABASE_URL_SCHEME = "mongodb"

DATABASE_URL = f"{DATABASE_URL_SCHEME}://{urllib.parse.quote_plus(DATABASE_USERNAME)}:{urllib.parse.quote_plus(DATABASE_PASSWORD)}@{DATABASE_SUFFIX}"
# Debugger log file

logger.add(
    ROOT_DIR / "logs" / LOGGER_FILE_NAME,
    rotation=config.get("LOG_ROTATION_SIZE", default="50 MB"),
    backtrace=True,
    diagnose=True,
    level="DEBUG",
)

# Error Notifier

logger.add(
    NotificationHandler(
        "telegram",
        defaults={
            "chat_id": config.get("NOTIFICATION_RECIEPENT_ID"),
            "token": config.get("NOTIFIER_TOKEN"),
        },
    ),
    level="ERROR",
)


# Admins for the bot


# Super User of the Bot
