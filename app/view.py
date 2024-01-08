from typing import List
from app.model import Item


HELP_TEXT = "<b>/add</b> <em>название_подарка ссылка_на_подарок</em> — добавить подарок в вишлист\nСсылку оставлять не обязательно, но желательно\n<b>/my_wishlist</b> — посмотреть свой вишлист\n<b>/del</b> <em>название или номер подарка</em> — удалить подарок из вишлиста\n<b>/remove_all</b> — удалить свой вишлист полностью\n<b>/friends_wishlists</b> — посмотреть вишлисты друзей (пока недоступно)"
START_TEXT = "Помогу определиться с подарком для близкого человека\nДля получения помощи введи /help"
DEL_INFO = 'Для удаления введите:\n<b>/del</b> <em>номер_подарка</em>\nили\n<b>/del</b> <em>название_подарка</em>\nПосмотреть свой вишлист: <b>/my_wishlist</b>'


def view_item_lst(items: List[Item] | str) -> str:
    if isinstance(items, str):
        return items
    res = []
    for i, item in enumerate(items):
        url_view = f"<a href='{item.url}'>{item.title}</a>" if item.url else item.title
        res.append(f"<b>{i + 1}. {url_view}</b>")

    return '\n'.join(res)

