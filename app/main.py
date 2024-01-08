from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from utils import parse_message
from app.config import settings
from app.controllers import db_con

BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text="Помогу определиться с подарком для близкого человека. Выбери команду:")


@dp.message(Command(commands="help"))
async def help_command(message: Message):
    await message.answer(text="/add - добавить товар в вишлист\
                                /watch_my - посмотреть мой вишлист \
                                /watch_username - посмотреть чужой вишлист")


@dp.message(F.text.startswith('/add'))
async def process_add_command(message: Message):
    username = message.from_user.username
    name = message.from_user.first_name
    _, title, url = parse_message(message.text)
    db_con.add_user(username=username, 
                    name=name)
    db_con.add_wish(username=username,
                    title=title,
                    url=url
                    )
    await message.answer(text="Подарок добавлен <3")


@dp.message(F.text.startswith('/del'))
async def process_del_command(message: Message):
    username = message.from_user.username
    name = message.from_user.first_name
    _, title, url = parse_message(message.text)
    db_con.delete_wish(username=username, 
                    title=title)
    await message.answer(text="Подарок удален <3")


@dp.message(Command(commands="add"))
async def add_define_command(message: Message):
    await message.answer(text="Введите /add и название подарка, который хотите добавить.\
                         Например: /add Кофеварка\
                         После названия через пробел вы можете добавить ссылку на товар, если хотите")
    

@dp.message(Command(commands="del"))
async def add_define_command(message: Message):
    await message.answer(text="Введите /del и название подарка, который хотите удалить.\
                         Например: /del Кофеварка\
                         Если вы хотите удалить свой вишлист полностью, введите: /delete_all")


@dp.message(Command(commands='remove_all'))
async def process_del_user(message: Message):
    username = message.from_user.username
    db_con.delete_user(username=username)
    await message.answer(text="Вишлист удален <3")


@dp.message(Command(commands="watch_my"))
async def process_watch_command(message: Message):
    username = message.from_user.username
    res = db_con.watch_wishlist(username=username)
    await message.answer(text=res)


@dp.message()
async def process_day_command(message: Message):
     await message.answer(text="Введите команду")


if __name__ == '__main__':
    dp.run_polling(bot)