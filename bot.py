import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from datetime import datetime
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from handlers.user_handlers import router as user_router
from handlers.main_menu_handlers import router as main_menu_router

from database import db_controller as db


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
    # Диспетчер
    dp = Dispatcher()
    # dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp.include_router(user_router)
    dp.include_router(main_menu_router)
    # db.fill_categories()
    # db.fill_meals()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




