from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired


class CodeForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    info = TextAreaField('О программе', validators=[DataRequired()])
    script = TextAreaField('Код программы', validators=[DataRequired()])
    top = StringField('Основная тема', validators=[DataRequired()])
    submit = SubmitField('Добавить')