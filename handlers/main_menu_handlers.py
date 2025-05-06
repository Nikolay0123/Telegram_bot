from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import keyboards as kb

from database import db_controller as db


router = Router()

@router.message(F.text == 'Меню')
async def show_categories(message: Message):
    categories = db.get_categories()

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category.name, callback_data=f'category_{category.id}')

    builder.adjust(1)

    await message.answer('Выберите категорию:', reply_markup=builder.as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('category_'))
async def show_meals(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    meals = db.get_meals_by_category(category_id)

    builder = InlineKeyboardBuilder()
    for meal in meals:
        # builder.button(text=meal.name, callback_data=f'meal_{meal.id}')

#
#
# @router.message(F.text == 'Корзина'):
# async def show_cart(message: Message):
#
#
# @router.message(F.text == 'Мои заказы'):
# async def show_orders(message: Message):
#
#
# @router.message(F.text == 'Связаться с нами'):
# async def call_us(message: Message):