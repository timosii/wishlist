from urllib.parse import urlparse
from typing import List
from app.model import Item


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



