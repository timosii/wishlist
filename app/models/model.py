from sqlalchemy import Column, ForeignKey, Numeric, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List

from app.models.database import Base, session, engine


class User(Base):
    __tablename__ = 'users'

    # id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), primary_key=True)
    name: Mapped[Optional[str]]
    items: Mapped[List["Item"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(username={self.username!r}, name={self.name!r}, surname={self.surname!r})"


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    username: Mapped[int] = mapped_column(ForeignKey("users.username"))
    url: Mapped[Optional[str]]

    user: Mapped["User"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return f"Item(id={self.id!r}, title={self.title!r}, url={self.url!r})"


Base.metadata.create_all(engine)



