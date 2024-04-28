from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from models.groups import Group

groups_router = Router()


@groups_router.message(Command("groups"))
@groups_router.message(F.text == "👥 Groups")
async def groups_list(message: Message):
    no_of_groups = await Group.count()
    await message.reply(f"Number of Groups registered is: {no_of_groups}")
