from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from models.base import Base


class CartMeal(Base):
    """Корзина с блюдами"""
    __tablename__ = 'cart_meal'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    quantity = Column(Integer, default=1)