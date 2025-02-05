from aiogram import Router
from aiogram.filters import Command,CommandStart
from aiogram.types import Message

from src.models.db import DB
from src.models.user import User

router = Router()

@router.message(CommandStart())
async def on_start(message: Message):
    user = DB.get_user(message.from_user.id)
    await user.enable_first_state()

@router.message()
async def on_message(message: Message):
    user = DB.get_user(message.from_user.id)
    await user.process_message(message)    