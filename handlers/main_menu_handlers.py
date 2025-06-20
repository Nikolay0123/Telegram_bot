from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from keyboards import MealArrowCallback, create_menu_kb_by_category, meal_keyboard, delete_from_cart
from aiogram.filters import Command
from database import db_controller as db

router = Router()


@router.message(F.text == 'Меню')
async def show_categories(message: Message):
    categories = db.get_all_categories()

    for category in categories:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=category.name,
                                         callback_data=f'category_{category.id}'), width=6)
        # builder.button(text=category.name, callback_data=f'category_{category.id}')

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


@router.message(Command('menu'))
async def command_menu(message: Message):
    categories = db.get_all_categories()

    for category in categories:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text=category.name,
                                         callback_data=f'category_{category.id}'), width=6)

        await message.answer(
            text=f"<b>{category.name}</b>\n{category.description}",
            parse_mode='HTML',
            reply_markup=builder.as_markup(resize_keyboard=True)
        )


@router.callback_query(F.data.startswith('category_'))
async def show_meals(callback: CallbackQuery):
    cat_id = int(callback.data.split('_')[1])
    await callback.message.answer(text='Еда', reply_markup=create_menu_kb_by_category(db, cat_id, page=1),
                                  resize_keyboard=True)
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

    await callback.message.edit_reply_markup(reply_markup=create_menu_kb_by_category(db, category_id, page),
                                             resize_keyboard=True)


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
    await callback.message.edit_text(text='Еда', reply_markup=create_menu_kb_by_category(db, cat_id, page=1),
                                     resize_keyboard=True)


@router.callback_query(F.data.startswith('CartMeal_'))
async def add_meal_to_cart(callback: CallbackQuery):
    meal_id = int(callback.data.split('_')[1])
    meal = db.get_meal(meal_id)
    user = db.get_user_by_id(callback.from_user.id)
    db.add_to_cart(user.id, meal_id)
    await callback.answer(text=f'{meal.name} добавлено в корзину!')


@router.callback_query(F.data.startswith('cart'))
async def open_cart(callback: CallbackQuery):
    user = db.get_user_by_id(callback.from_user.id)
    cart_meals = db.get_users_cart(user.id)
    if not cart_meals:
        await callback.message.answer(text='Ваша корзина пуста!')
        await callback.message.delete()
    else:
        for cart_meal in cart_meals:
            meal = cart_meal.meal
            builder = InlineKeyboardBuilder()
            builder.row(InlineKeyboardButton(text='Удалить из корзины', callback_data=f'delete_{meal.id}'),
                        InlineKeyboardButton(text='Сделать заказ', callback_data='make_order'))
            await callback.message.answer(text=f'В Вашей корзине {meal.name} - {cart_meal.quantity} штук',
                                          reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('make_order'))
async def make_order(callback: CallbackQuery):
    user = db.get_user_by_id(callback.from_user.id)
    cart_meals = db.get_users_cart(user.id)

    # else:
    #     for cart_meal in cart_meals:


@router.message(F.text == 'Корзина')
async def show_cart(message: Message):
    user = db.get_user_by_id(message.from_user.id)
    cart_meals = db.get_users_cart(user.id)
    if not cart_meals:
        await message.answer(text='Ваша корзина пуста!')
        await message.delete()
    else:
        for cart_meal in cart_meals:
            meal = cart_meal.meal
            builder = InlineKeyboardBuilder()
            builder.row(InlineKeyboardButton(text='Удалить из корзины', callback_data=f'delete_{meal.id}'),
                        InlineKeyboardButton(text='Сделать заказ', callback_data='make_order'))
            await message.answer(text=f'В Вашей корзине {meal.name} - {cart_meal.quantity} штук',
                                          reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith('delete'))
async def delete_from_cart(callback: CallbackQuery):
    user = db.get_user_by_id(callback.from_user.id)
    meal_id = int(callback.data.split('_')[1])
    meal = db.get_meal(meal_id)
    db.delete_meal_from_cart(user.id, meal_id)
    await callback.answer(text=f'{meal.name} удалено из корзины!')
    await callback.message.delete()

# @router.message(F.text == 'Мои заказы'):
# async def show_orders(message: Message):
#
#
# @router.message(F.text == 'Связаться с нами'):
# async def call_us(message: Message):