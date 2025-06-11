from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import MealArrowCallback, create_menu_kb_by_category, meal_keyboard
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
    await callback.message.answer(text='Еда', reply_markup=create_menu_kb_by_category(db, cat_id, page=1).
                                  as_markup(resize_keyboard=True))
    # await callback.message.edit_text(
    #     text=message_text,
    #     reply_markup=builder.as_markup(),
    #     parse_mode='HTML'
    # )

@router.callback_query(MealArrowCallback.filter())
async def callback_for_meal_arrows(callback: CallbackQuery, callback_data: MealArrowCallback):
    page = callback_data.page
    action = callback_data.action
    category_id = callback_data.category_id

    if action == 'next':
        page += 1
    else:
        page -= 1

    await callback.message.edit_reply_markup(reply_markup=create_menu_kb_by_category(db, category_id, page).
                                             as_markup(resize_keyboard=True))


def get_meal_card_text(meal):
    return f"<b>{meal.name}</b>\n<b>{meal.description}</b>\n<b>{meal.weight}</b>{meal.price}"


async def edit_meal_card(callback, meal_id, reply_kb):
    meal = db.get_meal(meal_id)
    text = get_meal_card_text(meal)
    await callback.message.edit_text(text, reply_markup=reply_kb(meal).as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('meal_'))
async def show_meal_card(callback: CallbackQuery):
    meal_id = int(callback.data.split('_')[1])
    await edit_meal_card(callback, meal_id, meal_keyboard)
    # meal = db.meal_card(meal_id)
    # await callback.message.edit_text(
    #     text=f"<b>{meal.name}</b>\n<b>{meal.description}</b>\n<b>{meal.weight}</b>{meal.price}",
    #     parse_mode='HTML',
    #     reply_markup=meal_keyboard(meal).as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('back_'))
async def back_to_meals_by_category(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])
    await callback.message.answer(text='Еда', reply_markup=create_menu_kb_by_category(db, cat_id, page=1).
                                  as_markup(resize_keyboard=True))


@router.callback_query(F.data.startswith('cart_meal_'))
async def add_meal_to_card(callback: CallbackQuery):
    meal_id = int(callback.data.split('_')[1])
    meal = db.get_meal(meal_id)
    db.add_to_cart(callback.from_user.id, meal_id)
    await callback.answer(text=f'{meal.name} добавлено в корзину!')



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