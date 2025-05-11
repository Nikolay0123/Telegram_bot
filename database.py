from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,  func
from models import Base, Cart, CartMeal, Category, Meal, Order, User

# user = relationship('User', back_populates='orders')
# User.orders = relationship('Order', back_populates='user')\
# meals = relationship('Meal', back_populates='category')
# category = relationship('Category', back_populates='meals')


class DBController:
    def __init__(self, con_str):
        self.engine = create_engine(con_str)
        self.Session = sessionmaker(bind=self.engine)

    def create_all_tables(self):
        Base.metadata.create_all(self.engine)

    def get_user_by_id(self, telegram_id):
        session = self.Session()
        user = session.query(User).filter_by(telegram_id=telegram_id).first()
        return user

    def create_user_with_cart(self, telegram_id, username, first_name, last_name, phone):
        session = self.Session()
        user = User(telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone)
        session.add(user)
        session.commit()
        cart = Cart(user_id=user.id)
        session.add(cart)
        session.commit()

    def get_all_categories(self):
        session = self.Session()
        categories = session.query(Category).all()
        return categories

    def get_meals_by_category_id(self, category_id):
        session = self.Session()
        meals = session.query(Meal).filter_by(category_id=category_id).all()
        return meals

    def get_meals_slice(self, category_id, offset, limit):
        session = self.Session()
        meals_slice = session.query(Meal).filter_by(category_id=category_id).offset(offset).limit(limit).all()
        return meals_slice

    def get_meal_count_by_category(self, category_id):
        session = self.Session()
        meal_count = session.query(func.count(Meal.id)).filter_by(category_id=category_id).scalar()
        return meal_count

    def fill_initial_data(self):
        session = self.Session()
        categories = [
            Category(
                name='Завтраки',
                description='Сытные и полезные завтраки'
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
                category_id=categories[0].id
                # photo_url = ''
            ),

            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),
            Meal(
                name='Омлет с ветчиной',
                price=200,
                description='Вкусный омлет с ветчиной',
                weight='250 г',
                category_id=categories[0].id
                # photo_url = ''
            ),

            Meal(
                name='Суп том-ям',
                price=400,
                description='Острый суп том-ям с креветками',
                weight='350 мл',
                category_id=categories[1].id
                # photo_url = ''
            ),

            Meal(
                name='Американо',
                price=200,
                description='Кофе американо',
                weight='300 мл',
                category_id=categories[2].id
                # photo_url = ''
            )]

        session.add_all(categories + meals)
        session.commit()


db_controller = DBController('sqlite:///restaurant_bot.db')
db_controller.create_all_tables()
