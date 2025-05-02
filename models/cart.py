from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from models.base import Base


class Cart(Base):
    """Таблица корзины"""
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
