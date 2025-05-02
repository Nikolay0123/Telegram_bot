from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, Cart, CartMeal, Category, Meal, Order, User


# user = relationship('User', back_populates='orders')
# User.orders = relationship('Order', back_populates='user')\
# meals = relationship('Meal', back_populates='category')
# category = relationship('Category', back_populates='meals')


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
        )]

    session.add_all(categories + meals)
    session.commit()


class DBController:
    def __init__(self, con_str):
        self.engine = create_engine(con_str)
        self.Session = sessionmaker(bind=self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

    def get_user_by_id(self, telegram_id):
        session = self.Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        session.close()
        return user

    def create_user(self, telegram_id, username, first_name, last_name):
        session = self.Session()
        user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name)
        session.add(user)
        session.commit()
        session.close()


db_controller = DBController('sqlite:///restaurant_bot.db')
