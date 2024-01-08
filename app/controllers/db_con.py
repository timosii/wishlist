import asyncio
from typing import List
from app.models.model import Item, User
from app.models.database import engine
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound


def check_user(username: str):
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        try:
            res = session.scalars(stmt).one()
            print('Найден юзер')
            return res
        except NoResultFound:
            print('Не найден юзер')
            return False


def check_item(username: str,
                     title: str):
    with Session(engine) as session:
        stmt = select(Item).where(Item.title == title).where(Item.username == username)
        try:
            res = session.scalars(stmt).one()
            print('Найден итем')
            return res
        except NoResultFound:
            print('Не найден итем')
            return False


def add_user(username: str, 
                   name: str= None
                   ):
    with Session(engine) as session:
        if not check_user(username=username):
            user = User(
                username=username,
                name=name
            )
            session.add(user)
            session.commit()


def add_wish(username: str, 
                   title: str, 
                   price: int = None,  
                   url: str = None,
                   engine=engine
                   ):
    with Session(engine) as session:
        if not check_item(username=username,
                          title=title):
            item = Item(
                username=username, 
                title=title, 
                url=url)
            
            session.add(item)
            session.commit()


def delete_wish(username: str,
                title: str # удаление по title, реализовать позже через id
                ) -> None:
    
    with Session(engine) as session:
        stmt = select(Item).where(Item.username == username).where(Item.title == title)
        wish_for_delete = session.scalars(stmt).one()
        session.delete(wish_for_delete) # удаляется итем
        session.commit()


def watch_wishlist(username: str,
                    ) -> List[Item]:
    with Session(engine) as session:
        if check_user(username=username):
            stmt = select(User).where(User.username == username)
            res = session.scalars(stmt)
            result = [item for user in res for item in user.items]
            if result:
                print(result)
            else:
                return 'Ничего нет'
            # return [item for user in res for item in user.items]
        else:
            return 'У вас нет вишлиста <3. Скорее заведите его!'


def delete_user(username: str):
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        user_for_delete = session.scalars(stmt).one()
        session.delete(user_for_delete) # удаляется пользователь и связанные сущности - все итемы
        session.commit()

