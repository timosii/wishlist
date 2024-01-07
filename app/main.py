from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.config import settings

BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text="Помогу определиться с подарком для близкого человека. Выбери команду:")

# команды: /watch - посмотреть свой вишлист /add добавить предмет в свой вишлист


@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(text="/new - добавить товар в вишлист /watch_my - посмотреть мой вишлист /watch_other - посмотреть чужие вишлисты")


@dp.message(Command(commands="add"))
async def process_add_command(message: Message):
    await message.answer(text="Что хотите добавить?")

# @dp.message(Command(commands=["today", "tomorrow"]))
# async def process_time_command(message: Message):
#     period = message.text.split("/")[-1]
#     for sign in signs:
#         response = form_response(sign=sign, period=period)
#         await message.answer(text=response, parse_mode="MarkdownV2")


# @dp.message(Command(commands=["week_sagittarius", "week_lion", "week_pisces"]))
# async def process_week_command(message: Message):
#     _, period, sign = message.text.replace("/", "_").split("_")
#     response = form_response(sign=sign, period=period)
#     await message.answer(text=response, parse_mode="MarkdownV2")


@dp.message()
async def process_day_command(message: Message):
     await message.answer(text="Пока ничего не умею")


if __name__ == '__main__':
    dp.run_polling(bot)