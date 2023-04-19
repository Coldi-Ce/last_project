from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class MarkForm(FlaskForm):
    one = BooleanField('Единица')
    two = BooleanField('Двойка')
    three = BooleanField('Тройка')
    four = BooleanField('Четверка')
    five = BooleanField('Пятерка')
    submit = SubmitField('Поставить')