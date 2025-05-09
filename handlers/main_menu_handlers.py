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
    category_id = int(callback.data.split('_')[1])
    page = 0

    meals, total_meals, total_pages = db.show_meals_page(category_id=category_id,
                                                         page_size=3,
                                                         page=page)

    message_text = '\n\n'.join(
        f"<b>{meal.name}</b>\n"
        f"{meal.weight} | {meal.price} руб. \n"
        f"{meal.description}"
        for meal in meals
    )

    builder = InlineKeyboardBuilder()

    if page > 0:
        builder.button(text="назад", callback_data=f"category_{category_id}_{page-1}")

    if page < total_pages - 1:
        builder.button(text='вперед', callback_data=f"category_{category_id}_{page+1}")

    for meal in meals:
        builder.button(text=f"{meal.name}",
                       callback_data=f'add_{meal.id}')

    builder.adjust(2,2)

    await callback.answer()

    # await callback.message.edit_text(
    #     text=message_text,
    #     reply_markup=builder.as_markup(),
    #     parse_mode='HTML'
    # )

@router.callback_query(MealArrowCallback.filter())
def callback_for_meal_arrows(callback: CallbackQuery, callback_data: dict):
    page = callback_data['page']
    action = callback_data['action']
    category_id = callback_data['category_id']

    if action == 'next':
        page += 1
    else:
        page -= 1

    reply_markup = create_menu_kb_by_category(db, category_id, page)

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