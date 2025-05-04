from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import keyboards as kb

from database import db_controller as db


router = Router()


class Registration(StatesGroup):
    waiting_phone = State()


@router.message(CommandStart())
async def register_user(message: Message, state: FSMContext):
    """Регистрация при команде /start"""
    user = db.get_user_by_id(message.from_user.id)

    if user:
        await message.reply(f"С возвращением, {user.first_name}!")
    else:
        await message.answer('Для оформления заказов нам нужен Ваш номер телефона:',
                             reply_markup=kb.get_number)
        await state.set_state(Registration.waiting_phone)


@router.message(F.contact, Registration.waiting_phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    db.create_user_with_cart(telegram_id=message.from_user.id,
                   first_name=message.from_user.first_name,
                   last_name=message.from_user.last_name,
                   username=message.from_user.username,
                   phone=phone)

    await message.answer('Регистрация успешно завершена!', reply_markup=ReplyKeyboardRemove())
    await state.clear()
