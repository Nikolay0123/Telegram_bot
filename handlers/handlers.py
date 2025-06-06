from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram import html
from datetime import datetime
from aiogram import types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import keyboards as kb

router = Router()

class Register(StatesGroup):
    name = State()
    number = State()

greeted_users = set()

@router.message(F.text)
async def handle_first_message(message: Message):
    user_id = message.from_user.id
    if user_id not in greeted_users:
        greeted_users.add(user_id)
        welcome_text = """
            Привет, я бот для заказа еды!

            Вот список доступных команд:
            /start - Перезапустить бота
            /menu - Показать меню
            /cart - Показать корзину
            /help - Помощь

            Выберите действие или нажмите на кнопку ниже:
            """
        await message.answer(
            welcome_text, reply_markup=kb.main_menu
        )
    else:
        await message.answer('Используйте кнопки ниже!')



@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = """
    Привет, я бот для заказа еды!
    
    Вот список доступных команд:
    /start - Перезапустить бота
    /menu - Показать меню
    /cart - Показать корзину
    /help - Помощь
    
    Выберите действие или нажмите на кнопку ниже:
    """
    await message.answer(
        welcome_text, reply_markup=kb.main_menu
    )


@router.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer('Введите ваше имя:')

@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.number)
    await message.answer('Введите ваш номер телефона:', reply_markup=kb.get_number)

@router.message(Register.number, F.number)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    await message.answer(f'Вы зарегистрированы:\nИмя: {data["name"]}\nНомер: {data["number"]}')
    await state.clear()


@router.message(F.text == 'Меню')
async def cmd_menu(message: Message):
    await message.answer(
        f"Меню", reply_markup=kb.menu
    )


@router.callback_query(F.data == 'hot meals')
async def cmd_hot_meals(callback: CallbackQuery):
    await callback.answer('Горячие блюда')


@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(
        f"Меню", reply_markup=kb.menu
    )
# @router.message(Command("hello"))
# async def cmd_hello(message: Message):
#     await message.answer(
#         f"Hello, {html.bold(html.quote(message.from_user.full_name))}", reply_markup=kb.main_menu
#     )
#
# @router.message(F.text)
# async def echo_with_time(message: Message):
#     # Получаем текущее время в часовом поясе ПК
#     time_now = datetime.now().strftime('%H:%M')
#     # Создаём подчёркнутый текст
#     added_text = html.underline(f"Создано в {time_now}")
#     # Отправляем новое сообщение с добавленным текстом
#     await message.answer(f"{message.html_text}\n\n{added_text}", parse_mode="HTML")


# @router.message(Command("add_to_list"))
# async def cmd_add_to_list(message: types.Message, mylist: list[int]):
#     mylist.append(7)
#     await message.answer("Добавлено число 7")


# @router.message(Command("show_list"))
# async def cmd_show_list(message: types.Message, mylist: list[int]):
#     await message.answer(f"Ваш список: {mylist}")


# @router.message(Command("info"))
# async def cmd_info(message: types.Message, started_at: str):
#     await message.answer(f"Бот запущен {started_at}")


# # Хэндлер на команду /start
# @router.message(Command("start"))
# async def cmd_start(message: types.Message):
#     await message.answer("Hello!")








