from core.config import logger

from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart, Command


from models.groups import Group

register_router = Router()


@register_router.message(CommandStart())
async def handle_start(message: Message):
    logger.info(f"Handling /start Command in {message.chat.id}")
    if message.chat.id < 0:
        new_group = Group.from_dict(
            {
                "is_active": True,
                "chat_id": message.chat.id,
            }
        )
        found = await new_group.get()
        if found:
            await message.reply("This Group is Already Registered.")
            return
        await new_group.save()
        await message.reply("Successfully Registered")
    else:
        await message.reply("This Bot doesn't support User Accounts.")


@register_router.message(Command("stop"))
async def remove_group(message: Message):
    logger.info(f"Handling /stop command in {message.chat.id}")
    if message.chat.id < 0:
        group = Group.from_dict(
            {
                "is_active": True,
                "chat_id": message.chat.id,
            }
        )
        found = await group.get()
        if found:
            await group.delete()
            await message.reply(
                "Service Stoped Succesfully. Use /start for restarting the service"
            )
        else:
            await message.reply(
                "This group is not registered Please register with /start first"
            )
    else:
        await message.reply("This Bot doesn't support User Accounts.")
