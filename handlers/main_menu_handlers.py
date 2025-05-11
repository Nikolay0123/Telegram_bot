from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import MealArrowCallback, create_menu_kb_by_category
from database import db_controller as db

router = Router()


@router.message(F.text == 'Меню')
async def show_categories(message: Message):
    categories = db.get_all_categories()

    for category in categories:
        builder = InlineKeyboardBuilder()
        builder.button(text=category.name, callback_data=f'category_{category.id}')

        # if category.image_url:
        #     await message.answer_photo(
        #         photo=category.image_url,
        #         text=f"<b>{category.name}</b>\n{category.description}",
        #         parse_mode='HTML',
        #         reply_markup=builder.as_markup(resize_keyboard=True)
        #     )
        # else:
        await message.answer(
                text=f"<b>{category.name}</b>\n{category.description}",
                parse_mode='HTML',
                reply_markup=builder.as_markup(resize_keyboard=True)
            )

    builder.adjust(2)

# def gen_keyboard():


@router.callback_query(F.data.startswith('category_'))
async def show_meals(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])

    await callback.message.answer(text='Еда', reply_markup=create_menu_kb_by_category(db, cat_id, page=1))

    # await callback.message.edit_text(
    #     text=message_text,
    #     reply_markup=builder.as_markup(),
    #     parse_mode='HTML'
    # )

@router.callback_query(MealArrowCallback.filter())
async def callback_for_meal_arrows(callback: CallbackQuery, callback_data: dict):
    page = callback_data['page']
    action = callback_data['action']
    category_id = callback_data['category_id']

    if action == 'next':
        page += 1
    else:
        page -= 1

    await callback.message.edit_reply_markup(reply_markup=create_menu_kb_by_category(db, category_id, page))

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