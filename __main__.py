import json
import logging
import asyncio

from decouple import config
from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI, HTTPException

from aiogram import Dispatcher, Bot, Router
from aiogram.types import Message, Update
from aiogram.filters.command import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums.parse_mode import ParseMode
from helpers import *

logging.basicConfig(level=logging.INFO)

TOKEN = config("BOT_TOKEN")
ADMIN_USERS = set([int(s) for s in (config("ADMINS", cast=str)).split(",")])
CHANNEL_ID = config("CHANNEL_ID", cast=int)

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


@dp.message(CommandStart())
async def handle_start(message: Message):
    client = await connect_to_mongo()
    if message.chat.id < 0:
        group_id = message.chat.id
        if not await find_id(client, group_id):
            await insert_id(client, group_id)
            await message.reply("Successfully registered for the service")
    await close_mongo_connection(client=client)


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


@dp.channel_post()
async def handle_channel_post(message: Message):
    with open("groups.json", "r") as file:
        data = json.load(file)
        chat_ids = data["chat_ids"]
        for line in chat_ids:
            await bot.forward_message(
                chat_id=int(line),
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )


async def main():
    dp.message.register(get_message, Command("forward"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
