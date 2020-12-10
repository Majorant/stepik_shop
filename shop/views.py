from flask import session, redirect, request, render_template
from sqlalchemy.sql.expression import func

from shop import app, db
from shop.models import User, Meal, Category, Order
from shop.forms import CartForm, LoginForm


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
            return redirect('/cart/')
    cart = session.get('cart', [])
    # вернуться только уникальные строки
    # ordered_meals = db.session.query(Meal).filter(Meal.id.in_(cart)).all()
    for id in cart:
        ordered_meals.append(db.session.query(Meal).filter(Meal.id == id).scalar())
    return render_template('cart.html', ordered_meals=ordered_meals, form=form)


# – /account/ для личного кабинета
@app.route('/account/')
def account():
    return render_template('account.html')


# – /auth/ для аутентификации
@app.route('/auth/', methods=['GET', 'POST'])
def auth():
    form = LoginForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('auth.html', form=form)

        user = User.query.filter(User.username == form.email.data).scalar()
        email = request.form.get('email')
        password = request.form.get('password')
        session['is_auth'] = True
        session['username'] = email
        print(email, password)
        return redirect('/')
    return render_template('auth.html', form=form)




# – /register/ для регистрации
@app.route('/register/')
def register():
    return render_template('register.html')


# – /logout/ для аутентификации
@app.route('/logout/')
def logout():
    return redirect('/')


# – /ordered/ для подтверждения отправки
@app.route('/ordered/', methods=['GET', 'POST'])
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
