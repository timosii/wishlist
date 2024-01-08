from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from utils import parse_message
from app.config import settings
from app.db_controller import delete_wish, delete_user, watch_wishlist, add_user, add_wish
from app.view import HELP_TEXT,START_TEXT, DEL_INFO, view_item_lst


BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=START_TEXT)


@dp.message(Command(commands="help"))
async def help_command(message: Message):
    await message.answer(text=HELP_TEXT, parse_mode='HTML')


@dp.message(F.text.startswith('/add'))
async def process_add_command(message: Message):
    user_id = str(message.from_user.id)
    username = message.from_user.username
    name = message.from_user.first_name
    _, title, url = parse_message(message.text)
    add_user(user_id=user_id,
                        username=username,
                        name=name,
                        )
    res = add_wish(user_id=user_id,
                        title=title,
                        url=url
                        )
    await message.answer(text=res)


@dp.message(F.text.startswith('/del'))
async def process_del_command(message: Message):
    user_id = str(message.from_user.id)
    name = message.from_user.first_name
    _, title, url = parse_message(message.text)
    if not title: # значит введена только команда
        res = DEL_INFO
    else:
        res = delete_wish(user_id=user_id,
                      title=title)
    await message.answer(text=res, parse_mode='HTML')


@dp.message(Command(commands='remove_all'))
async def process_del_user(message: Message):
    user_id = str(message.from_user.id)
    res = delete_user(user_id=user_id)
    await message.answer(text=res)


@dp.message(Command(commands="my_wishlist"))
async def process_watch_command(message: Message):
    user_id = str(message.from_user.id)
    res = view_item_lst(watch_wishlist(user_id=user_id))
    link_preview_options = types.LinkPreviewOptions(
        is_disabled=True,
        disable_web_page_preview=True,
    )
    await message.answer(text=res, link_preview_options=link_preview_options, parse_mode='HTML')


@dp.message()
async def process_day_command(message: Message):
     await message.answer(text="Для помощи введите /help")


if __name__ == '__main__':
    dp.run_polling(bot)