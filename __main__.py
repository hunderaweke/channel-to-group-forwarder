import asyncio

from loguru import logger
from decouple import config
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI

from aiogram import Dispatcher, Bot
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


from helpers import *
from core import config
from routers.register_router import register_router

TOKEN = config.BOT_TOKEN
ADMIN_USERS = config.SUPER_USERS

app = FastAPI()
dp = Dispatcher()
bot = Bot(TOKEN)


class ForwardMessage(StatesGroup):
    text = State()


class TelegramWebhook(BaseModel):
    update_id: int
    message: Optional[dict] = None
    edited_message: Optional[dict] = None
    channel_post: Optional[dict] = None
    edited_channel_post: Optional[dict] = None
    inline_query: Optional[dict] = None
    chosen_inline_result: Optional[dict] = None
    callback_query: Optional[dict] = None
    shipping_query: Optional[dict] = None
    pre_checkout_query: Optional[dict] = None
    poll: Optional[dict] = None
    poll_answer: Optional[dict] = None


async def get_message(message: Message, state: FSMContext):
    if message.chat.id in ADMIN_USERS:
        await state.set_state(ForwardMessage.text)
        await message.reply("Send the message to forward please")
    else:
        await message.reply("Command Allowed for Admin User Only")


@dp.message(ForwardMessage.text)
async def forward_message(message: Message, state: FSMContext):
    client = await connect_to_mongo()
    await state.clear()
    id_object = await get_ids(client)
    for object in id_object:
        await bot.copy_message(
            chat_id=object["group_id"],
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            disable_notification=True,
        )
    await close_mongo_connection(client=client)


async def main():
    logger.info("Registering Handlers")
    dp.message.register(get_message, Command("forward"))
    dp.include_router(register_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.info("Started Polling")
    asyncio.run(main())
