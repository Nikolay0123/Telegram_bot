from sqlalchemy import Column, String, Integer
from sqlalchemy import ForeignKey
from models.base import Base


class Order(Base):
    """Таблица заказов"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = Column(String(500))
    status = Column(String(20), default='pending')

#     user = relationship('User', back_populates='orders')
# #
# #
# # User.orders = relationship('Order', back_populates='user')