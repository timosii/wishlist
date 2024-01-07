from sqlalchemy import Column, ForeignKey, Numeric, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List

from app.models.database import Base, session, engine


class User(Base):
    __tablename__ = 'users'

    # id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    name: Mapped[Optional[str]]
    surname: Mapped[Optional[str]]
    items: Mapped[List["Item"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, name={self.name!r}, surname={self.surname!r})"


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    username: Mapped[int] = mapped_column(ForeignKey("users.username"))
    price: Mapped[Optional[int]]
    description: Mapped[Optional[str]]
    url: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, title={self.title!r}, description={self.description!r})"


Base.metadata.create_all(engine)

# user = User(username='Testing_man', name="John", surname="Doe")
# session.add(user)
# session.commit()

# item = Item(title='Tickets', user_id=user.id, price=500, description='My present')

# session.add(item)
# session.commit()

# user = session.query(User).filter(User.name == "John").first()
# print(user.id)
# print(item.user)



