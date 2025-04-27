from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Float, create_engine
from datetime import datetime
from sqlalchemy import ForeignKey




class Base(DeclarativeBase):
    pass


class User(Base):
    """Таблица пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(50), nullable=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}>"


class Order(Base):
    """Таблица заказов"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = Column(String(500))
    status = Column(String(20), default='pending')

    user = relationship('User', back_populates='orders')


User.orders = relationship('Order', back_populates='user')\



class Category(Base):
    """Таблица категорий"""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    # photo_url = Column(String(255))

    meals = relationship('Meal', back_populates='category')


class Meal(Base):
    """Таблица блюд"""
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    weight = Column(String(20))
    description = Column(String(300))
    category_id = Column(Integer, ForeignKey('categories.id'))
    # photo_url = Column(String(255))

    category = relationship('Category', back_populates='meals')


class Cart(Base):
    """Таблица корзины"""
    __tablename__ = 'cart'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))


class CartMeal(Base):
    """Корзина с блюдами"""
    __tablename__ = 'cart_meal'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('cart.id'))
    meal_id = Column(Integer, ForeignKey('meals.id'))
    quantity = Column(Integer, default=1)


engine = create_engine('sqlite:///restaurant_bot.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def fill_initial_data():
    categories = [
        Category(
            name='Завтраки',
            description='Сытние и полезные завтраки'
            # photo_url = ''
        ),
        Category(
            name='Обеды',
            description='Горячие блюда на обед'
            # photo_url = ''
        ),
        Category(
            name='Напитки',
            description='Прохладительные и горячие напитки'
            # photo_url = ''
        )
    ]

    meals = [
        Meal(
            name='Омлет с ветчиной',
            price=200,
            description='Вкусный омлет с ветчиной',
            weight='250 г',
            category=categories[0]
            # photo_url = ''
        ),

        Meal(
            name='Суп том-ям',
            price=400,
            description='Острый суп том-ям с креветками',
            weight='350 мл',
            category=categories[1]
            # photo_url = ''
        ),

        Meal(
            name='Американо',
            price=200,
            description='Кофе американо',
            weight='300 мл',
            category=categories[2]
        # photo_url = ''
    ]

    session.add_all(categories + meals)
    session.commit()