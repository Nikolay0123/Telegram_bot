from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import db_controller as db


router = Router()


@router.message(CommandStart())
async def register_user(message: Message):
    """Регистрация при команде /start"""
    user = db.get_user_by_id(message.from_user.id)

    if user:
        await message.reply(f"С возвращением, {user.first_name}!")
    else:
        db.create_user(telegram_id=message.from_user.id,
                       first_name=message.from_user.first_name,
                       last_name=message.from_user.last_name,
                       phone=message.contact.phone_number)
        await message.reply('Вы зарегистрированы!')