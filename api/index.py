import json
import logging

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

logging.basicConfig(level=logging.INFO)

TOKEN = config("BOT_TOKEN")
ADMIN_USER = config("ADMIN", cast=int)
CHANNEL_ID = config("CHANNEL_ID", cast=int)

app = FastAPI()
dp = Dispatcher()
router = Router()
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
    if message.chat.id < 0:
        chat_id = str(message.chat.id)
        with open("groups.json", "r+") as file:
            try:
                data = json.load(file)
            except:
                data = {"chat_ids": []}
            if chat_id not in data["chat_ids"]:
                data["chat_ids"].append(chat_id)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()


async def get_message(message: Message, state: FSMContext):
    if message.chat.id == ADMIN_USER:
        await state.set_state(ForwardMessage.text)
        await message.reply("Send the message to forward please")


@dp.message(ForwardMessage.text)
async def forward_message(message: Message, state: FSMContext):
    await state.clear()
    with open("groups.json", "r") as file:
        data = json.load(file)
        chat_ids = data["chat_ids"]
        for line in chat_ids:
            await bot.forward_message(
                chat_id=int(line),
                message_id=message.message_id,
                from_chat_id=message.chat.id,
            )


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


logging.info(dp.sub_routers)


@app.post("/webhook")
async def webhook(webhook_data: TelegramWebhook):
    try:
        dp.message.register(get_message, Command("forward"))
        await dp._process_update(bot=bot, update=Update(**webhook_data.dict()))
        return {"message": "ok"}
    except HTTPException as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def index():
    return {"message": "Hello world"}


# async def main():
#     dp.include_router(router)
#     await dp.start_polling(bot)


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())
