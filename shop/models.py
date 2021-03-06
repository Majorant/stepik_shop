from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

# table for ManyToMamy relationship between orders and meals
# orders_meals_association = db.Table(
#     'orders_meals',
#
#     db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
#     db.Column('meal_id', db.Integer, db.ForeignKey('meals.id')),
#     db.Column('meal_num', db.Integer, default=1, nullable=False),
# )

# for ManyToMany relationship with additional Column
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#association-object
class Association_orders_meals(db.Model):
    __tablename__ = 'association_orders_meals'

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    meal_id = db.Column('meal_id', db.Integer, db.ForeignKey('meals.id'), primary_key=True)
    meal_num = db.Column(db.Integer, default=1, nullable=False) # колическтво заказанных блюд одного типа
    meal = db.relationship('Meal', back_populates='orders')
    order = db.relationship('Order', back_populates='meals')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = db.relationship('Order')


    @property
    def password(self):
    	# Запретим прямое обращение к паролю
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
    	# Устанавливаем пароль через этот метод
    	self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
    	# Проверяем пароль через этот метод
    	# Функция check_password_hash превращает password в хеш и сравнивает с хранимым
    	return check_password_hash(self.password_hash, password)



class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=False)
    # –– категория (category, отношение)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='meals')
    # category = db.relationship('Category', backref=backref('meals', uselist=False))

    # orders = db.relationship('Order', secondary=orders_meals_association, back_populates='meals')
    orders = db.relationship('Association_orders_meals', back_populates='meal')



class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    # –– блюда (meals, отношение) судя по таблице OneToOne
    meals = db.relationship('Meal', back_populates='category')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False) # при замене поля на DateTime alembic не видит изменений в схеме
    sum = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    mail = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # –– список блюд в заказе (можно через запятую, можно many2many)
    # meals = db.relationship('Meal', secondary=orders_meals_association, back_populates='orders')
    meals = db.relationship('Association_orders_meals', back_populates='order')
