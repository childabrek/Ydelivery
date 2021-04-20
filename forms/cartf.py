from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class CartForm(FlaskForm):
    title = StringField('Позиции')
    sum = StringField("Итого")
    submit = SubmitField('Доставить')

