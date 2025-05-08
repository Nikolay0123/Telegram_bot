from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import db_controller as db


router = Router()

@router.message(F.text == 'Меню')
async def show_categories(message: Message):
    categories = db.get_categories()

    builder = InlineKeyboardBuilder()
    for category in categories:
        builder.button(text=category.name, callback_data=f'category_{category.id}')

        if category.image_url:
            await message.answer_photo(
                photo=category.image_url,
                text=f"<b>{category.name}</b>\n{category.description}",
                parse_mode='HTML',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )
        else:
            await message.answer(
                text=f"<b>{category.name}</b>\n{category.description}",
                parse_mode='HTML',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )

    builder.adjust(1)

def gen_keyboard():


@router.callback_query(F.data.startswith('category_'))
async def show_meals(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[1])
    meals = db.get_meals_by_category(category_id)

    builder = InlineKeyboardBuilder()
    for meal in meals:
        builder.button(text=meal.name, callback_data=f'meal_{meal.id}')

        if meal.image_url:


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