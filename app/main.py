from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.types import Message, ReplyKeyboardRemove, BotCommand, CallbackQuery
from utils import validate_url
from app.config import settings
from app.db_controller import delete_wish, delete_user, watch_wishlist, add_user, add_wish, check_user, check_item, update_wish
from app.view import HELP_TEXT,START_TEXT, DEL_INFO, DELETE_MESS, view_item_lst, NO_ITEMS
from app.markups import base_keyboard, cancel_keyboard, without_url, del_all_keyboard, without_description, update_keyboard, cancel_update_keyboard

BOT_TOKEN = settings.BOT_TOKEN

# storage = MemoryStorage() # при использовании MemoryStorage

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=storage)


class FSMAddItem(StatesGroup):
    title_add = State()
    url_add = State()
    description_add = State()


class FSMDelItem(StatesGroup):
    choose_number = State()


class FSMFriendsWish(StatesGroup):
    choose_friend = State()


class FSMUpdateWish(StatesGroup):
    choose_wish = State()
    choose_change = State()
    update = State()


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Начать'),
        BotCommand(command='/help',
                   description='Помощь'),
        BotCommand(command='/remove_all',
                   description='Удалить свой вишлист')
    ]
    await bot.set_my_commands(main_menu_commands)


@dp.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=START_TEXT,
                         reply_markup=base_keyboard)


@dp.message(F.text.lower() == 'отменить', ~StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(
        text='Возвращаемся в меню',
        reply_markup=base_keyboard
    )
    await state.clear()


@dp.message(F.text.lower() == 'добавить желание', StateFilter(default_state))
async def process_add_command(message: Message, state: FSMContext):
    await message.answer(text='Введите название подарка',
                         reply_markup=cancel_keyboard
                         )
    await state.set_state(FSMAddItem.title_add)


@dp.message(StateFilter(FSMAddItem.title_add), F.text.lower() != 'отменить')
async def process_title_add(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text='Спасибо! Теперь добавьте ссылку на ваш подарок!',
                         reply_markup=without_url
                         )
    await state.set_state(FSMAddItem.url_add)


@dp.message(StateFilter(FSMAddItem.url_add), F.text.lower() != 'отменить')
async def process_title_add(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await message.answer(text='Добавьте описание, если хотите!',
                         reply_markup=without_description
                         )
    await state.set_state(FSMAddItem.description_add)


@dp.message(StateFilter(FSMAddItem.description_add), F.text.lower() != 'отменить')
async def process_title_add(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    data = await state.get_data()
    print(data)
    title = data['title']
    url = data['url']
    description = data['description']

    if url.lower() == 'без ссылки':
        url = None
    if description.lower() == 'без описания':
        description = None

    user_id = str(message.from_user.id)
    username = message.from_user.username
    name = message.from_user.first_name

    add_user(user_id=user_id, 
             username=username, 
             name=name
             )
    
    add_wish(user_id=user_id,
             title=title,
             url=url,
             description=description
             )
    await state.clear()
    await message.answer(text='Подарок добавлен!',
                         reply_markup=base_keyboard,
                         )


@dp.message(F.text.lower() == 'удалить желание', StateFilter(default_state))
async def start_del_process(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    res = view_item_lst(watch_wishlist(user_id=user_id))
    link_preview_options = types.LinkPreviewOptions(
        is_disabled=True,
        disable_web_page_preview=True,
    )

    if not res:
        await state.clear()
        await message.answer(text= NO_ITEMS,
                             parse_mode='HTML',
                             reply_markup=base_keyboard)
    else:
        await message.answer(text=res,
                             link_preview_options=link_preview_options,
                             parse_mode='HTML')
        await state.set_state(FSMDelItem.choose_number)
        await message.answer(text='Введите номер или название подарка, который хотите удалить',
                             reply_markup=cancel_keyboard
                             )


@dp.message(StateFilter(FSMDelItem.choose_number), F.text.lower() != 'отменить')
async def process_wish_del(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    title = data['title']
    user_id = str(message.from_user.id)
    res = delete_wish(user_id=user_id,
                      title=title)
    await state.clear()
    await message.answer(text=res,
                         parse_mode='HTML',
                         reply_markup=base_keyboard)    

@dp.message(F.text.lower() == 'посмотреть свой вишлист')
async def process_my_wishlist(message: Message):
    user_id = str(message.from_user.id)
    res = view_item_lst(watch_wishlist(user_id=user_id))
    if res:
        link_preview_options = types.LinkPreviewOptions(
            is_disabled=True,
            disable_web_page_preview=True,
        )
        await message.answer(text=res,
                             link_preview_options=link_preview_options,
                             parse_mode='HTML')
    else:
        await message.answer(text=NO_ITEMS,
                             parse_mode='HTML',
                             reply_markup=base_keyboard)


@dp.message(F.text.lower() == 'посмотреть вишлисты друзей')
async def process_friends_wishlist(message: Message):
    await message.answer(text='Функция находится в разработке, следите за обновлениями!',
                         reply_markup=base_keyboard)


@dp.message(Command(commands="help"))
async def help_command(message: Message):
    await message.answer(text=HELP_TEXT,
                         reply_markup=base_keyboard,
                         parse_mode='HTML')


@dp.message(Command(commands='remove_all'))
async def process_del_user(message: Message):
    user_id = str(message.from_user.id)
    res = check_user(user_id=user_id)
    if not res:
        await message.answer(text='У вас нет вишлиста. Создайте скорее!')
    else:
        await message.answer(text=DELETE_MESS,
                             parse_mode='HTML',
                             reply_markup=del_all_keyboard)


@dp.message(F.text.lower() == 'удалить вишлист полностью')
async def process_del_user(message: Message):
    user_id = str(message.from_user.id)
    res = delete_user(user_id=user_id)
    await message.answer(text=res,
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode='HTML')


@dp.message(F.text.lower() == 'изменить подарок', StateFilter(default_state))
async def process_update_wish(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    res = view_item_lst(watch_wishlist(user_id=user_id))

    if not res:
        await state.clear()
        await message.answer(text= NO_ITEMS,
                             parse_mode='HTML',
                             reply_markup=base_keyboard)
    else:
        link_preview_options = types.LinkPreviewOptions(
                is_disabled=True,
                disable_web_page_preview=True,
            )
        await message.answer(text=res,
                             link_preview_options=link_preview_options,
                             parse_mode='HTML')
        await state.set_state(FSMUpdateWish.choose_wish)
        await message.answer(text='Введите номер или название подарка, который хотите изменить',
                             reply_markup=cancel_keyboard
                             )


@dp.message(StateFilter(FSMUpdateWish.choose_wish), F.text.lower() != 'отменить')
async def process_wish_update(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    user_id = str(message.from_user.id)
    data = await state.get_data()
    title = data['title']
    res = check_item(user_id=user_id,
                     title=title)
    if not res:    
        await state.clear()
        await message.answer(text='Подарок не найден',
                             reply_markup=base_keyboard)
    else:
        await state.set_state(FSMUpdateWish.choose_change)
        await message.answer(text='Выбери, что хотел бы изменить',
                            reply_markup=update_keyboard)


@dp.message(StateFilter(FSMUpdateWish.choose_change), F.text.lower() != 'отменить')
async def process_wish_update_cont(message: Message, state: FSMContext):
    rename_dict = {'URL': 'url',
                   'Название': 'title',
                   'Описание': 'description'
                   }
    await state.update_data(what_update=rename_dict[message.text])
    await state.set_state(FSMUpdateWish.update)
    await message.answer(text='Введите новые данные',
                         reply_markup=cancel_update_keyboard)


@dp.message(StateFilter(FSMUpdateWish.update), F.text.lower() != 'отменить')
async def process_update(message: Message, state: FSMContext):
    await state.update_data(new_data=message.text)
    user_id = str(message.from_user.id)
    data = await state.get_data()
    title = data['title']
    what_update = data['what_update']
    new_data = data['new_data']
    if new_data.lower() == 'удалить поле':
        new_data = None        

    res = update_wish(user_id=user_id,
                    title=title,
                    what_update=what_update,
                    new_data=new_data)

    await state.clear()
    await message.answer(text=res,
                        reply_markup=base_keyboard)



@dp.message()
async def process_day_command(message: Message):
     await message.answer(text="Для помощи введите /help")


# @dp.callback_query(F.data == 'pressed_inline_add')
# async def process_button_add(callback: CallbackQuery):
#     iser_id = callback.from_user.id # кто нажал на кнопку
#     await callback.message.answer(text='Напишите, что хотите добавить')
#     # await callback.answer(text='Желание добавлено!')


# @dp.callback_query(F.data == 'pressed_inline_all')
# async def process_button_all(callback: CallbackQuery):
#     await callback.message.answer(text='Напишите, что хотите удалить')
#     print('Работает?! Вроде да')
#     # await callback.answer(text='Желание добавлено!')
#     await callback.answer() # оставляем всегда, чтобы пользователь не видел часики


if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)