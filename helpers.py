import urllib
from pymongo import MongoClient
from decouple import config


DATABASE_USERNAME = config("DATABASE_USERNAME", cast=str, default=None)
DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=str, default=None)
DATABASE_SUFFIX = config("DATABASE_SUFFIX", cast=str, default=None)

DATABASE_URL = f"mongodb+srv://{DATABASE_USERNAME}:{urllib.parse.quote(DATABASE_PASSWORD)}{DATABASE_SUFFIX}"

client = MongoClient(DATABASE_URL)

db = client.message_forwarder


def insert_id(group_id):
    db.group_ids.insert_one({"group_id": group_id})
    return True


def find_id(group_id):
    return db.group_ids.distinct("group_id", {"group_id": group_id})


def get_ids() -> list[dict]:
    return db.group_ids.find()
