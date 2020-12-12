import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email


def password_check(form, field):
    msg = "Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры"
    patern1 = re.compile('[a-z]+')
    patern2 = re.compile('[A-Z]+')
    patern3 = re.compile('\\d+')
    # Проверяем данные поля
    if (not patern1.search(field.data) or
        not patern2.search(field.data) or
        not patern3.search(field.data)):
        # Хоть одно правило не сработает, то вызываем исключение
        raise ValidationError(msg)


class CartForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired(message='Поле не может быть пустым')])
    address = StringField('Ваше Адрес', validators=[DataRequired(message='Поле не может быть пустым')])
    email = EmailField('Электропочта', validators=[DataRequired(message='Поле не может быть пустым'),
                                                Email(message='введите корректный email')],
                                                render_kw={'autofocus': True})
    phone = StringField('Телефон', validators=[DataRequired()])



# Форма аутентификации
class LoginForm(FlaskForm):
    email = EmailField('Электропочта', validators=[DataRequired(message='Поле не может быть пустым'),
                                                Email(message='введите корректный email')],
                                                render_kw={'autofocus': True})
    password = PasswordField('Пароль', validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        "Пароль:",
        validators=[
            DataRequired(),
            # Пароль не менее 8 символов
            Length(min=8, message="Пароль должен быть не менее 8 символов"),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            password_check
        ]
    )
    confirm_password = PasswordField("Пароль ещё раз:")


# Форма регистрации
class RegistrationForm(FlaskForm):
    email = EmailField('Электропочта', validators=[DataRequired(message='Поле не может быть пустым'),
                                                Email(message='введите корректный email')],
                                                render_kw={'autofocus': True})
    password = PasswordField(
        'Пароль',
        validators=[
            DataRequired(),
            # Пароль не менее 5 символов
            Length(min=5, message='Пароль должен быть не менее 5 символов'),
            EqualTo('confirm_password', message="Пароли не одинаковые"),
            # отключил, чтобы не мучаться при проверках
            # password_check,
            ]
    )
    confirm_password = PasswordField('Веедите пароль повторно', validators=[DataRequired(),])
