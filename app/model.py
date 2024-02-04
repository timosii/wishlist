from sqlalchemy import Column, ForeignKey, Numeric, String, Table, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List

from app.database import Base, session, engine


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    name: Mapped[Optional[str]]
    items: Mapped[List["Item"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, username={self.username!r}, name={self.name!r}, surname={self.surname!r})"


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, title={self.title!r}, url={self.url!r})"


Base.metadata.create_all(engine)
