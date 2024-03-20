from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient
from urllib import parse

DATABASE_USERNAME = config("DATABASE_USERNAME", cast=str, default=None)
DATABASE_PASSWORD = config("DATABASE_PASSWORD", cast=str, default=None)
DATABASE_SUFFIX = config("DATABASE_SUFFIX", cast=str, default=None)

# Quote the password
quoted_password = parse.quote(DATABASE_PASSWORD)

DATABASE_URL = f"mongodb+srv://{DATABASE_USERNAME}:{quoted_password}{DATABASE_SUFFIX}"


async def connect_to_mongo():
    client = await AsyncIOMotorClient(DATABASE_URL)
    return client


async def close_mongo_connection(client):
    client.close()


async def insert_id(client, group_id):
    db = client.message_forwarder
    await db.group_ids.insert_one({"group_id": group_id})
    return True


async def find_id(client, group_id):
    db = client.message_forwarder
    return await db.group_ids.distinct("group_id", {"group_id": group_id})


async def get_ids(client) -> list[dict]:
    db = client.message_forwarder
    return [document async for document in db.group_ids.find()]
