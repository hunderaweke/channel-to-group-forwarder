from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from models.groups import Group

groups_router = Router()


@groups_router.message(Command("groups"))
async def groups_list(message: Message):
    no_of_groups = await Group.count()
    await message.reply(f"No of Groups registered is: {no_of_groups}")
