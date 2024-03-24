from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from core import config


class SingleTon:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls, *args, **kwargs)
        return cls.instance


class Database(SingleTon):
    def __init__(self):
        logger.info("Initializing Database")
        self.db = self.get_database()

    def get_client(self):
        logger.info("Getting client for the database")
        _client = AsyncIOMotorClient(config.DATABASE_URL)
        return _client

    def get_database(self):
        logger.info("Getting Database")
        return self.get_client().get_database(config.DATABASE_NAME)

    def get_collection(self, collection_name: str):
        logger.info(f"Getting collection from the Database{collection_name}")
        return self.db.get_collection(collection_name)
