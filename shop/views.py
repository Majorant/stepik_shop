from datetime import date
from flask import session, redirect, request, render_template
from sqlalchemy.sql.expression import func
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from shop import app, db
from shop.models import User, Meal, Category, Order
from shop.forms import CartForm, LoginForm, RegistrationForm


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Meal, db.session))
admin.add_view(ModelView(Order, db.session))

# – / для главной страницы
@app.route('/')
def index():
    ordered_meals = []
    categories = db.session.query(Category).order_by(Category.id).all()
    cart = session.get('cart', [])
    for id in cart:
        ordered_meals.append(db.session.query(Meal).filter(Meal.id == id).scalar())
    return render_template('main.html', categories=categories, ordered_meals=ordered_meals)


# – /cart/ для корзины
@app.route('/cart/', methods=['GET', 'POST'])
def cart():
    ordered_meals = []
    form = CartForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            session['name'] = request.form.get('name')
            session['address'] = request.form.get('address')
            session['username'] = request.form.get('email')
            session['phone'] = request.form.get('phone')
            session['order_summ'] = request.form.get('order_summ')
            session['ordered'] = True
            if session.get('is_auth'):
                return redirect('/account/')
            # сохраняем заказ для неавторизованного пользователя, чтобы добавить его после авторизации
            return redirect('/ordered/')
    cart = session.get('cart', [])
    # вернутся только уникальные строки
    # ordered_meals = db.session.query(Meal).filter(Meal.id.in_(cart)).all()
    for id in cart:
        ordered_meals.append(db.session.query(Meal).filter(Meal.id == id).scalar())
    return render_template('cart.html', ordered_meals=ordered_meals, form=form)


# – /account/ для личного кабинета
@app.route('/account/')
def account():
    user = db.session.query(User).filter(User.mail == session['username']).scalar()
    if session.pop('ordered', None):
        order = Order(
                    date = date.today().strftime('%d.%m.%Y'),
                    sum = session['order_summ'],
                    status = 1,
                    mail = session['username'],
                    phone = session['phone'],
                    address = session['address'],
                    user_id = user.id,
                    )
        # в cart записаны id блюд
        for id in session.get('cart', []):
            meal = db.session.query(Meal).filter(Meal.id == id).scalar()
            order.meals.append(meal)
        db.session.add(order)
        db.session.commit()


    orders = db.session.query(Order).filter(Order.user_id == user.id).order_by(Order.date.desc()).all()

    print(user)
    print(user.orders)
    return render_template('account.html', orders=orders)


# – /auth/ для аутентификации
@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            user = User.query.filter(User.mail == email).scalar()
            if user and user.password_valid(request.form.get('password')):
                session['is_auth'] = True
                session['id'] = db.session.query(User.id).filter(User.mail == email).scalar()
                session['username'] = email
                return redirect('/account/')
            else:
                form.email.errors.append("Не верная электропочта или пароль")

    return render_template('auth.html', form=form)




# – /register/ для регистрации
@app.route('/register/', methods=['GET', 'POST'])
def register():
    if session.get('is_auth'):
        redirect('/')

    form = RegistrationForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('register.html', form=form)

        user = User()
        email = request.form.get('email')
        user.mail = email
        user.password = request.form.get('password')
        db.session.add(user)
        db.session.commit()
        # print(db.session.query(User).filter(User.mail == email).scalar().id)
        # сразу авторизуем пользователя
        session['is_auth'] = True
        session['id'] = db.session.query(User.id).filter(User.mail == email).scalar()
        session['username'] = email
        return redirect('/account/')

    return render_template('register.html', form=form)


# – /logout/ для аутентификации
@app.route('/logout/')
def logout():
    session.clear()
    return redirect('/')


# – /ordered/ для подтверждения отправки
@app.route('/ordered/')
def ordered():
    return render_template('ordered.html')


@app.route('/addtocart/<id>')
def addtocart(id):
    cart = session.get('cart', [])
    cart.append(id)
    session['cart'] = cart
    return redirect('/cart/')


@app.route('/submit/', methods=['POST'])
def submit():
    form = CartForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)
