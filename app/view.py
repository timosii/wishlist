from typing import List
from app.model import Item

HELP_TEXT = "Вы находитесь в главном меню. Нажимайте на кнопки и следуйте инструкциям! :)"
START_TEXT = "Помогу определиться с подарком для близкого человека\nДля получения помощи введи /help"
DEL_INFO = 'Для удаления введите:\n<b>/del</b> <em>номер_подарка</em>\nили\n<b>/del</b> <em>название_подарка</em>\nПосмотреть свой вишлист: <b>/my_wishlist</b>'
DELETE_MESS = 'Ваш вишлист будет <b>полностью удалён</b>.\nЕсли вы уверены, нажмите на кнопку'
NO_ITEMS = 'В виш-листе ничего нет! Добавьте что-нибудь'


def view_item_lst(items: List[Item] | None) -> str:
    if not items:
        return 
    res = []
    for i, item in enumerate(items):
        url_view = f"<a href='{item.url}'>{item.title}</a>" if item.url != 'Без ссылки' else item.title
        description = f". {item.description}" if item.description != 'Без описания' else ''
        res.append(f"<b>{i + 1}. {url_view}</b>{description}")

    return '\n'.join(res)

