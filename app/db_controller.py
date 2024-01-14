import asyncio
from typing import List
from app.model import Item, User
from app.database import engine
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


def check_user(user_id: str):
    with Session(engine) as session:
        stmt = select(User).where(User.user_id == user_id)
        try:
            res = session.scalars(stmt).one()
            return res
        except NoResultFound:
            return False


def check_item(user_id: str, 
               title: str):
    with Session(engine) as session:
        stmt = select(Item).where(Item.title == title).where(Item.user_id == user_id)
        try:
            res = session.scalars(stmt).one()
            return res
        except NoResultFound:
            return False


def add_user(user_id: str, 
             username: str, 
             name: str
             ):
    with Session(engine) as session:
        if not check_user(user_id=user_id):
            user = User(
                user_id=user_id,
                username=username,
                name=name
            )
            session.add(user)
            session.commit()


def add_wish(user_id: str, 
             title: str, 
             url: str = None
             ):
    with Session(engine) as session:
        if not title:
            return 'Вы не указали, что нужно добавить.\nВведите /add и подарок, например "/add Кофеварка"'
        
        elif check_item(user_id=user_id,
                        title=title):
            return 'Подарок уже есть, придумайте что-нибудь ещё!'
        
        else:
            item = Item(
                user_id=user_id, 
                title=title, 
                url=url)
            session.add(item)
            session.commit()
            return 'Подарок добавлен!'


def delete_wish(user_id: str,
                title: str # удаление по title
                ) -> None:
    
    if not title:
        return 'Подарок не найден'

    if title.isdigit():
        title = find_item_by_number(user_id=user_id, number=title)

    with Session(engine) as session:
        if not check_item(user_id=user_id, title=title):
            return 'Подарок не найден'
        else:
            stmt = select(Item).where(Item.user_id == user_id).where(Item.title == title)
            wish_for_delete = session.scalars(stmt).one()
            session.delete(wish_for_delete) # удаляется итем
            session.commit()
            return 'Подарок удалён!'


def watch_wishlist(user_id: str) -> List[Item]:
    with Session(engine) as session:
        if not check_user(user_id=user_id):
            return 'У вас нет вишлиста! Добавьте что-нибудь'
        else:
            stmt = select(User).where(User.user_id == user_id)
            res = session.scalars(stmt)
            result = [item for user in res for item in user.items]
            if not result:
                return 'В виш-листе ничего нет! Добавьте что-нибудь'
            else:
                return result


def find_item_by_number(user_id: str, number: str):
    items = watch_wishlist(user_id=user_id)
    if isinstance(items, str):
        return 'Не найдено подарка'
    
    res = {}
    for i, item in enumerate(items):
        res[str(i + 1)] = item.title

    return res.get(number) if res.get(number) else 'Не найдено подарка'


def empty_del(user_id: str):
    return 


def delete_user(user_id: str):
    with Session(engine) as session:
        if not check_user(user_id=user_id):
            return 'У вас нет вишлиста. Создайте скорее!'
        else:
            stmt = select(User).where(User.user_id == user_id)
            user_for_delete = session.scalars(stmt).one()
            session.delete(user_for_delete) # удаляется пользователь и связанные сущности - все итемы
            session.commit()
            return 'Мы всё удалили ...'
