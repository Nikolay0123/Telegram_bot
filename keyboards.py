from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')],
                                          [KeyboardButton(text='Корзина')],
                                           [KeyboardButton(text='Контакты'),
                                KeyboardButton(text='О нас')]], resize_keyboard=True,
                                input_field_placeholder="Выберите пункт меню")

menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Горячие блюда', callback_data='hot meals')],
                                             [InlineKeyboardButton(text='Гарниры', callback_data='garnishes')],
                                             [InlineKeyboardButton(text='Салаты и закуски', callback_data='salads')],
                                             [InlineKeyboardButton(text='Напитки', callback_data='drinks')],
                                             [InlineKeyboardButton(text='Десерты', callback_data='desserts')],
                                             [InlineKeyboardButton(text='Супы', callback_data='soups')],
                                             [InlineKeyboardButton(text='Японская кухня', callback_data='japanese')]])

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер', request_contact=True)]], resize_keyboard=True)