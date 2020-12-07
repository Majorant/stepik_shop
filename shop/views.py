from flask import session, redirect, request, render_template

from shop import app, db
from shop.models import User, Meal, Category, Order

# – / для главной страницы
@app.route('/')
def index():
    return render_template('main.html')


# – /cart/ для корзины
@app.route('/cart/')
def cart():
    pass


# – /account/ для личного кабинета
@app.route('/account/')
def account():
    pass


# – /auth/ для аутентификации
@app.route('/auth/')
def auth():
    pass


# – /register/ для регистрации
@app.route('/register/')
def register():
    pass


# – /logout/ для аутентификации
@app.route('/logout/')
def logout():
    pass


# – /ordered/ для подтверждения отправки
@app.route('/ordered/')
def ordered():
    pass
