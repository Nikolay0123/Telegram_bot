import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from datetime import datetime
from config_reader import config
from aiogram.client.default import DefaultBotProperties
from handlers import router


# Запуск процесса поллинга новых апдейтов
async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token=config.bot_token.get_secret_value(), default=DefaultBotProperties(parse_mode='HTML'))
    # Диспетчер
    dp = Dispatcher()
    dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    dp.include_router(router)
    await dp.start_polling(bot, mylist=[1, 2, 3])
    # await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())




