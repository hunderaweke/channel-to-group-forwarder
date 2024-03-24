import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher
from decouple import config
from fastapi import FastAPI
from pydantic import BaseModel

from core import config
from core.config import logger
from routers.admin.groups_router import groups_router
from routers.forward_router import forward_router
from routers.register_router import register_router

TOKEN = config.BOT_TOKEN

app = FastAPI()
dp = Dispatcher()
bot = Bot(TOKEN)


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


async def main():
    logger.info("Registering Handlers")
    dp.include_router(register_router)
    dp.include_router(forward_router)
    dp.include_router(groups_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logger.info("Started Polling")
        asyncio.run(main())
        logger.info("Stopped Polling")
    except Exception as e:
        logger.error(e)
