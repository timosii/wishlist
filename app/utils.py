from urllib.parse import urlparse
from typing import List
from app.model import Item


import re

def validate_url(url):
    """
    Проверяет, является ли указанный URL-адрес допустимым.

    Аргументы:
        url: URL-адрес для проверки

    Возвращает:
        True, если URL-адрес действителен, False в противном случае.
    """
    if len(url) > 2048:
        return False
    if not re.match("^[a-z]+://", url):
        return False
    for char in url:
        if not re.match("[a-z0-9.@:%+_\\-~#?&//=]", char):
            return False
    return True


def parse_message(message: str):
    '''
    Принимает сообщение (строка от пользователя) и парсит её на команду,
    title и url
    '''
    command = message[:4] # пользователь может ввести title с пробелом или без
    title_url = message[4:]

    if 'http' in title_url:
        title_url_lst = title_url.split(' ')
        url = title_url_lst[-1].strip()
        title = ' '.join(title_url_lst[:-1]).strip()
    else:
        title = title_url.strip()
        url = None
    
    return command, title, url



