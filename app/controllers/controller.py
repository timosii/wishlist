import asyncio
from typing import List
from app.models.model import Item, User
from app.models.database import engine
from sqlalchemy import select, delete
from sqlalchemy.orm import Session


async def add_user(username: str, 
                   name: str= None,
                   surname: str = None
                   ):
    with Session(engine) as session:
        user = User(
            username=username,
            name=name, 
            surname=surname)
        session.add(user)
        session.commit()


async def add_wish(username: str, 
                   title: str, 
                   price: int = None, 
                   description: str = None, 
                   url: str = None,
                   engine=engine
                   ):
    with Session(engine) as session:  
        item = Item(
            username=username, 
            title=title, 
            price=price, 
            description=description, 
            url=url)
        
        session.add(item)
        session.commit()


async def delete_wish(username: str,
                      id: int
                      ) -> None:
    
    with Session(engine) as session:
        stmt = select(Item).where(Item.username == username).where(Item.id == id)
        wish_for_delete = session.scalars(stmt).one()
        session.delete(wish_for_delete) # удалим пользователя и связанные сущности - все итемы
        session.commit()


async def watch_wishlist(username: str,
                         engine=engine) -> List[Item]:
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        res = session.scalars(stmt)
        print([item for user in res for item in user.items])   


async def delete_user(username: str):
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        user_for_delete = session.scalars(stmt).one()
        session.delete(user_for_delete) # удалим пользователя и связанные сущности - все итемы
        session.commit()


# asyncio.run(
#     add_user(
#         username='HELLO'
#     )
# )

# asyncio.run(
#     add_wish(
#         username= 'HELLO', 
#         title='test_2'
#     )
# )

# asyncio.run(
#     delete_wish(
#         username='HELLO',
#         id='1'
#     )
# )
        
# asyncio.run(
#     delete_user(
#         username='HELLO'
#     )
# )
        
asyncio.run(
    watch_wishlist(
        username='HELLO'
    )
)