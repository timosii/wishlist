from urllib.parse import urlparse

def parse_message(message: str):
    '''
    Принимает сообщение (строка от пользователя) и парсит её на саму команду,
    title и url
    '''
    command = message[:4]
    title_url = message[4:]
    if 'http' in title_url:
        title_url_lst = title_url.split(' ')
        url = title_url_lst[-1].strip()
        title = ' '.join(title_url_lst[:-1]).strip()
    else:
        title = title_url.strip()
        url = None
    
    return command, title, url

