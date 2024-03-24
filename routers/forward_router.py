from aiogram import Bot, Router
from aiogram.enums.chat_type import ChatType
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from core import config
from core.config import logger
from models.groups import Group

ADMIN_USERS = set(config.ADMIN_USERS)

forward_router = Router()


class ForwardMessage(StatesGroup):
    text = State()


@forward_router.message(Command("forward"))
async def get_message(message: Message, state: FSMContext):
    if message.chat.type == ChatType.GROUP:
        await message.reply("This Method is not allowed in Groups")
    elif message.chat.id in ADMIN_USERS:
        await state.set_state(ForwardMessage.text)
        await message.reply("Send the message to forward please")
    else:
        await message.reply("Command Allowed for Admin User Only")


@forward_router.message(ForwardMessage.text)
async def forward_message(message: Message, state: FSMContext, bot: Bot):
    logger.info("Getting the message from user")
    await state.clear()
    groups = await Group.all()
    for group in groups:
        try:
            await bot.copy_message(
                chat_id=group.chat_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
                disable_notification=True,
            )
        except:
            await group.delete()
