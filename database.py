from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,  func, inspect
from models import Base, Cart, CartMeal, Category, Meal, Order, User

# user = relationship('User', back_populates='orders')
# User.orders = relationship('Order', back_populates='user')\
# meals = relationship('Meal', back_populates='category')
# category = relationship('Category', back_populates='meals')


class DBController:
    def __init__(self, con_str):
        self.engine = create_engine(con_str)
        self.Session = sessionmaker(bind=self.engine)

    # def init_db(self):
    #     inspector = inspect(self.engine)
    #     existing_tables = inspector.get_table_names()
    #
    #     if 'categories' not in existing_tables or 'meals' not in existing_tables:
    #         db_controller.create_all_tables()
    #         db_controller.fill_categories()
    #         db_controller.fill_meals()
    #     else:
    #         print('Таблицы уже существуют!')
    #
    # def get_session(self):
    #     return self.Session()

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

    def get_meal(self, meal_id):
        session = self.Session()
        meal = session.query(Meal).filter_by(id=meal_id).scalar()
        return meal

    def add_to_cart(self, user_id, meal_id, quantity=1):
        session = self.Session()
        cart = session.query(Cart).filter_by(user_id=user_id).scalar()
        curr_meal = session.query(CartMeal).filter_by(cart_id=cart.id, meal_id=meal_id).first()
        if curr_meal:
            curr_meal.quantity += 1
            session.commit()
        else:
            add_meal = CartMeal(cart_id=cart.id,
                                meal_id=meal_id,
                                quantity=quantity)
            session.add(add_meal)
            session.commit()
        # if not cart:
        #     cart = Cart(user_id=user_id)
        #     session.add(cart)

    def get_users_cart(self, user_id):
        session = self.Session()
        cart = session.query(Cart).filter_by(user_id=user_id).first()
        print(cart)
        cart_meal = session.query(CartMeal).filter_by(cart_id=cart.id).all()
        return cart_meal

    def fill_categories(self):
        session = self.Session()
        if not session.query(Category).all():
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

            session.add_all(categories)
            session.commit()

    def fill_meals(self):
        session = self.Session()
        if not session.query(Meal).all():
            categories = db_controller.get_all_categories()
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
                    name='Творожные блинчики',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Кабачковые маффины',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Сырники',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Овсяные оладьи',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Пшенная каша',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Банановые панкейки',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Творожная запеканка',
                    price=200,
                    description='Вкусный омлет с ветчиной',
                    weight='250 г',
                    category_id=categories[0].id
                    # photo_url = ''
                ),
                Meal(
                    name='Вареники',
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

            session.add_all(meals)
            session.commit()


db_controller = DBController('sqlite:///restaurant_bot.db')


