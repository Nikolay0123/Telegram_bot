import math

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')],
                                          [KeyboardButton(text='Корзина')],
                                          [KeyboardButton(text='Мои заказы')],
                                          [KeyboardButton(text='Связаться с нами')]], resize_keyboard=True,
                                input_field_placeholder="Выберите пункт меню")

menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Горячие блюда', callback_data='hot meals')],
                                             [InlineKeyboardButton(text='Гарниры', callback_data='garnishes')],
                                             [InlineKeyboardButton(text='Салаты и закуски', callback_data='salads')],
                                             [InlineKeyboardButton(text='Напитки', callback_data='drinks')],
                                             [InlineKeyboardButton(text='Десерты', callback_data='desserts')],
                                             [InlineKeyboardButton(text='Супы', callback_data='soups')],
                                             [InlineKeyboardButton(text='Японская кухня', callback_data='japanese')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]], resize_keyboard=True)


class MealArrowCallback(CallbackData, prefix='meal_arrow'):
    page: int
    action: str
    category_id: int


def create_menu_kb_by_category(db_controller, category_id, page, page_size=4):
    count = db_controller.get_meal_count_by_category(category_id)
    max_page = math.ceil(count / page_size)
    if page > max_page:
        page = 1
    if page < 1:
        page = max_page
    limit = page_size
    offset = (page - 1) * page_size + 1
    meals = db_controller.get_meals_slice(category_id, offset, limit)
    builder = InlineKeyboardBuilder()
    btns = list()
    for meal in meals:
        btns.append(InlineKeyboardButton(text=meal.name, callback_data=f'meal_{meal.id}'))
    builder.row(*btns, width=2)
    builder.adjust(2)

    # builder.row(InlineKeyboardButton(text=meal.name, callback_data=f'meal_{meal.id}'), width=2)

    builder.row(InlineKeyboardButton(
        text='<<', callback_data=MealArrowCallback(page=page, action='prev', category_id=category_id).pack()),
        InlineKeyboardButton(
            text='>>', callback_data=MealArrowCallback(page=page, action='next', category_id=category_id).pack()),
        width=2)
    # builder.button(
    #     text='>>', callback_data=MealArrowCallback(page=page, action='next', category_id=category_id)
    # )

    return builder.as_markup()


def meal_keyboard(meal):
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить в корзину', callback_data=f'CartMeal_{meal.id}')
    builder.button(text='Назад', callback_data=f'back_{meal.category_id}')
    return builder
