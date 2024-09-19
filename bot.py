import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F

# Получаем токен из переменной окружения
API_TOKEN = os.getenv('API_TOKEN')

if not API_TOKEN:
    raise ValueError("Отсутствует переменная окружения API_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Обработка команды /start
@router.message(F.text == "/start")
async def send_welcome(message: Message):
    await message.answer("Привет! Я бот для приема заказов. Как я могу помочь?")

# Обработка текстовых сообщений
@router.message()
async def echo(message: Message):
    await message.answer(f"Вы сказали: {message.text}")

# Функция для запуска бота
async def main():
    # Регистрируем роутеры
    dp.include_router(router)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
