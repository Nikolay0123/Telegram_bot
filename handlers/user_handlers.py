from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import db_controller

router = Router()

@router.message(CommandStart())
async def register_user(message: Message):
    """Регистрация при команде /start"""
    # user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    user = db_controller.get_user_by_id(telegram_id=)
    if user:
        await message.answer('С возвращением!')
        return

    new_user = db_controller.create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    session.add(new_user)
    session.commit()
    await message.answer('Вы успешно зарегистрированы!')