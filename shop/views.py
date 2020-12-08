from flask import session, redirect, request, render_template
from sqlalchemy.sql.expression import func

from shop import app, db
from shop.models import User, Meal, Category, Order

# – / для главной страницы
@app.route('/')
def index():
    categories = db.session.query(Category).order_by(Category.id).all()
    cart = session.get('cart', [])
    if cart:
        ordered_meals = db.session.query(Meal).filter(Meal.id.in_(cart)).all()
    else:
        ordered_meals = []
    return render_template('main.html', categories=categories, ordered_meals=ordered_meals)


# – /cart/ для корзины
@app.route('/cart/')
def cart():
    cart = session.get('cart', [])
    if cart:
        ordered_meals = db.session.query(Meal).filter(Meal.id.in_(cart)).all()
    else:
        ordered_meals = []
    return render_template('cart.html', ordered_meals=ordered_meals)


# – /account/ для личного кабинета
@app.route('/account/')
def account():
    return render_template('account.html')


# – /auth/ для аутентификации
@app.route('/auth/')
def auth():
    pass


# – /register/ для регистрации
@app.route('/register/')
def register():
    return render_template('register.html')


# – /logout/ для аутентификации
@app.route('/logout/')
def logout():
    pass


# – /ordered/ для подтверждения отправки
@app.route('/ordered/')
def ordered():
    pass


@app.route('/addtocart/<id>')
def addtocart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    return redirect('/cart/')
