from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class MarkForm(FlaskForm):
    ma = StringField('Ваша оценка', validators=[DataRequired()])
    submit = SubmitField('Поставить')