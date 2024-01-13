from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, CallbackQuery
from utils import parse_message, validate_url
from app.config import settings
from app.db_controller import delete_wish, delete_user, watch_wishlist, add_user, add_wish, check_user
from app.view import HELP_TEXT,START_TEXT, DEL_INFO, DELETE_MESS, view_item_lst
from app.markups import base_keyboard, button_friends, button_add, button_all, button_del


BOT_TOKEN = settings.BOT_TOKEN

# storage = MemoryStorage() # при использовании MemoryStorage

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)

class FSMAddItem(StatesGroup):
    title_add = State()
    url_add = State()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать'),
        BotCommand(command='/help',
                   description='Помощь'),
        BotCommand(command='/add',
                   description='Добавить желание'),
        BotCommand(command='/my_wishlist',
                   description='Посмотреть свой вишлист'),
        BotCommand(command='/del',
                   description='Удалить желание'),
        BotCommand(command='/friends_wishlist',
                   description='Посмотреть вишлисты друзей')
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    await message.answer(text=START_TEXT,
                         reply_markup=base_keyboard)


@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(
        text='Вы перестали добавлять желание! Выберите, что хотите сделать',
        reply_markup=base_keyboard
    )
    await state.clear()


@dp.message(F.text == 'Добавить желание', StateFilter(default_state))
async def process_add_command(message: Message, state: FSMContext):
    await message.answer(text='Введите название подарка')
    await state.set_state(FSMAddItem.title_add)


@dp.message(StateFilter(FSMAddItem.title_add))
async def process_title_add(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text='Спасибо! Теперь добавьте ссылку на ваш подарок!')
    await state.set_state(FSMAddItem.url_add)


@dp.message(StateFilter(FSMAddItem.url_add))
async def process_url_add(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(text='Спасибо! Ссылка добавлена!')
    data = await state.get_data()
    print(data)
    title = data['title']
    # while not validate_url(data['url']):
    url = data['url']
    user_id = str(message.from_user.id)
    username = message.from_user.username
    name = message.from_user.first_name

    add_user(user_id=user_id, 
             username=username, 
             name=name
             )
    
    add_wish(user_id=user_id,
             title=title,
             url=url
             )

    # Завершаем машину состояний
    await state.clear()
    await message.answer(text='Подарок полностью добавлен!')




    # user_id = str(message.from_user.id)
    # username = message.from_user.username
    # name = message.from_user.first_name
    # _, title, url = parse_message(message.text)
    # add_user(user_id=user_id,
    #                     username=username,
    #                     name=name,
    #                     )
    # res = add_wish(user_id=user_id,
    #                     title=title,
    #                     url=url
    #                     )
    # await message.answer(text=res)


@dp.message(F.text == 'Удалить желание')

@dp.message(F.text == 'Посмотреть свой вишлист')

@dp.message(F.text == 'Посмотреть вишлисты друзей')

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
    res = check_user(user_id=user_id)
    if not res:
        await message.answer(text='У вас нет вишлиста. Создайте скорее!')
    else:
        await message.answer(text=DELETE_MESS,
                             parse_mode='HTML')


@dp.message(F.text.lower() == 'удалить вишлист')
async def process_del_user(message: Message):
    user_id = str(message.from_user.id)
    res = delete_user(user_id=user_id)
    await message.answer(text=res,
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')


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


@dp.callback_query(F.data == 'pressed_inline_add')
async def process_button_add(callback: CallbackQuery):
    iser_id = callback.from_user.id # кто нажал на кнопку
    await callback.message.answer(text='Напишите, что хотите добавить')
    # await callback.answer(text='Желание добавлено!')


@dp.callback_query(F.data == 'pressed_inline_all')
async def process_button_all(callback: CallbackQuery):
    await callback.message.answer(text='Напишите, что хотите удалить')
    print('Работает?! Вроде да')
    # await callback.answer(text='Желание добавлено!')
    await callback.answer() # оставляем всегда, чтобы пользователь не видел часики


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)