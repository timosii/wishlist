from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup


# button_delete = KeyboardButton(text='Удалить вишлист')
# keyboard_del = ReplyKeyboardMarkup(keyboard=[[button_delete]],
#                                    resize_keyboard=True
#                                    )

# button_inline_del = InlineKeyboardButton(
#     text='Удалить желание',
#     callback_data='pressed_inline_del'
#     )

# button_inline_add = InlineKeyboardButton(
#     text='Добавить желание',
#     callback_data='pressed_inline_add'
#     )

# button_inline_all = InlineKeyboardButton(
#     text='Посмотреть свой вишлист',
#     callback_data='pressed_inline_all'
#     )

# button_inline_friends = InlineKeyboardButton(
#     text='Посмотреть вишлист друга',
#     callback_data='pressed_friends'
#     )

# keyboard_inline = InlineKeyboardMarkup(
#     row_width=2,
#     inline_keyboard=[[button_inline_add,
#                       button_inline_all,
#                       button_inline_del,
#                       button_inline_friends]]
# )


button_del = KeyboardButton(text='Удалить желание')
button_add = KeyboardButton(text='Добавить желание')
button_all = KeyboardButton(text='Посмотреть свой вишлист')
button_friends = KeyboardButton(text='Посмотреть вишлисты друзей')
button_del_all = KeyboardButton(text='Удалить вишлист полностью')

base_keyboard = ReplyKeyboardMarkup(keyboard=[[button_add,
                                               button_del],
                                               [button_all,
                                               button_friends
                                               ]],
                                               resize_keyboard=True
                                               )

del_all_keyboard = ReplyKeyboardMarkup(keyboard=[[button_del_all]],
                                                  resize_keyboard=True)

button_cancel = KeyboardButton(text='Отменить')
cancel_keyboard = ReplyKeyboardMarkup(
    keyboard=[[
        button_cancel
    ]], resize_keyboard=True
)

btn_url = KeyboardButton(text='Без ссылки')
btn_description = KeyboardButton(text='Без описания')
without_url = ReplyKeyboardMarkup(
    keyboard=[[
        btn_url,
        button_cancel
    ]], resize_keyboard=True
)

without_description = ReplyKeyboardMarkup(
    keyboard=[[
        btn_description,
        button_cancel
    ]], resize_keyboard=True
)


