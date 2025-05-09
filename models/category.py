from sqlalchemy import Column, String, Integer
from models.base import Base


class Category(Base):
    """Таблица категорий"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(200))
    # image_url = Column(String(255))

    # meals = relationship('Meal', back_populates='category')