from aiogram import Bot, Router, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.callback_query import CallbackQuery


from core import config
from core.config import logger
from models.groups import Group


ADMIN_USERS = set(config.ADMIN_USERS)
logger.info(ADMIN_USERS)

forward_router = Router()


class Forward(CallbackData, prefix="forward"):
    status: str
    message_id: int


class ForwardMessage(StatesGroup):
    text = State()


@forward_router.message(Command("forward"))
@forward_router.message(F.text == "➡️ Forward Message")
async def get_message(message: Message, state: FSMContext):
    if message.chat.id < 0:
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
    buttons = InlineKeyboardBuilder()
    keyboard = [
        ("Yes", Forward(status="yes", message_id=message.message_id)),
        ("No", Forward(status="no", message_id=message.message_id)),
    ]
    for txt, var in keyboard:
        buttons.button(text=txt, callback_data=var)

    await message.reply(
        text="Do you want to forward the message?", reply_markup=buttons.as_markup()
    )


@forward_router.callback_query(Forward.filter(F.status == "yes"))
async def forward(query: CallbackQuery, callback_data: Forward, bot: Bot):
    logger.info("Forwading a message to the groups")
    groups = await Group.all()
    for group in groups:
        try:
            await bot.copy_message(
                chat_id=group.chat_id,
                from_chat_id=query.from_user.id,
                message_id=callback_data.message_id,
                disable_notification=False,
            )
        except:
            await group.delete()
    await query.message.delete()
    await bot.send_message(
        chat_id=query.from_user.id, text="Message Forwarded Successfully."
    )


@forward_router.callback_query(Forward.filter(F.status == "no"))
async def forward(query: CallbackQuery, callback_data: Forward, bot: Bot):
    logger.info("Canceled forwading a message")
    await query.message.delete()
    await bot.send_message(
        chat_id=query.from_user.id, text="Message Forwarding Canceled."
    )
