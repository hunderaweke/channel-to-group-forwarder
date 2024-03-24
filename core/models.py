import json
from datetime import datetime
from typing import Self

from core.config import logger
from core.db import Database


class BaseModel:
    class Meta:
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls.meta = cls.Meta()
        cls.meta.model = cls
        cls.meta.model_name = cls.__name__

    def __init__(self, **kwargs) -> None:
        self.kwargs = kwargs

        if self.meta.pk_field not in self.meta.fields:
            self.meta.fields.append(self.meta.pk_field)

        for field in self.meta.fields:
            value = self.kwargs.get(field)
            if value is None:
                default = getattr(self, field, None)
                if callable(default):
                    value = default()
                else:
                    value = default
            setattr(self, field, value)

    def __repr__(self) -> str:
        return f"<{self.meta.model_name} {getattr(self,self.pk_field)}"

    def __str__(self) -> str:
        return f"<{self.meta.model_name.upper()} {getattr(self,self.pk_field)}"

    def to_dict(self):
        return {field: getattr(self, field) for field in self.meta.fields}

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_json(cls, data):
        return cls.from_dict(json.loads(data))


class DatabaseModel(BaseModel):
    db = Database()

    def __new__(cls, *args, **kwargs) -> Self:
        if not hasattr(cls, "collection"):
            cls.collection = cls.db.get_collection(cls.meta.collection_name)
        return super().__new__(cls)

    async def save(self):
        data = {
            key: value for key, value in self.to_dict().items() if key in self.kwargs
        }
        pk = data.pop(self.pk_field, None)
        defaults = {
            key: value
            for key, value in self.to_dict().items()
            if key not in self.kwargs and key != "_id"
        }
        await self.collection.create_index(self.pk_field, unique=True)
        if pk:
            await self.collection.update_one(
                {self.pk_field: pk},
                {
                    "$set": data,
                    "$currentDate": {
                        "lastModified": True,
                    },
                    "$setOnInsert": {
                        **defaults,
                        "created": datetime.utcnow(),
                    },
                },
                upsert=True,
            )
        else:
            result = await self.collection.insert_one(
                {
                    **data,
                    **defaults,
                    "created": datetime.utcnow(),
                }
            )
            setattr(self, self.pk_field, result.inserted_id)
        return await self.get()

    async def delete(self):
        return self.collection.delete_one({self.pk_field: self.pk})

    async def get(self):
        data = await self.collection.find_one({self.pk_field: self.pk})
        if data:
            return self.from_dict(data)

    @classmethod
    async def all(cls):
        if not hasattr(cls, "collection"):
            cls.collection = cls.db.get_collection(cls.meta.collection_name)
        data = cls.collection.find({})
        return [cls.from_dict(d) async for d in data]

    @classmethod
    async def count(cls):
        if not hasattr(cls, "collection"):
            cls.collection = cls.db.get_collection(cls.meta.collection_name)
        return await cls.collection.count_documents({})

    @classmethod
    async def filter(cls, **kwargs):
        """
        Get all models from the database that match the filter.
        """
        if not hasattr(cls, "collection"):
            cls.collection = cls.db.get_collection(cls.meta.collection_name)

        data = cls.collection.find(kwargs)

        return [cls.from_dict(d) async for d in data]

    async def get_or_create(self, **kwargs):
        """
        Get the model from the database or create a new one.
        """

        document = await self.get()
        if document:
            return document
        else:
            return await self.save()

    @property
    def pk(self):
        """
        Get the primary key of the model.
        """
        return getattr(self, self.pk_field, None)

    @property
    def pk_field(self):
        """
        Get the primary key field of the model.
        """
        return self.meta.pk_field

    class Meta(BaseModel.Meta):
        pk_field = "_id"
        collection_name = None
        fields = []
