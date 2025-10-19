from datetime import datetime
from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'

class Status(Enum):
    ACTIVE = 'active'
    NEW = 'new'
    DONE = 'done'

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    role: Mapped[Role] = mapped_column(default=Role.USER)
    phone_number: Mapped[str] = mapped_column(unique=True)
    tokens = relationship('UserToken', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    description: Mapped[str] = mapped_column()
    status: Mapped[Status] = mapped_column(default=Status.NEW)
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class UserToken(Base):
    __tablename__ = 'user_tokens'
    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id:Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

    user = relationship('User', back_populates='tokens')
