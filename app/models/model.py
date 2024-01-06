from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List

from app.models.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    surname: Mapped[str] = mapped_column(String(30))
    items: Mapped[List["Item"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, name={self.name!r}, surname={self.surname!r})"


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    price: Mapped[Optional[int]]
    description: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, title={self.title!r}, description={self.fullname!r})"