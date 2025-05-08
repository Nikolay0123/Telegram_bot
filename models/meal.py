from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey
from models.base import Base


class Meal(Base):
    """Таблица блюд"""
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    weight = Column(String(20))
    description = Column(String(300))
    category_id = Column(Integer, ForeignKey('categories.id'))
    image_url = Column(String(255))

    # category = relationship('Category', back_populates='meals')