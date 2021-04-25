from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class BlankForm(FlaskForm):
    name = StringField('Ваше имя (указанное при регистрации)', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    street = StringField('улица', validators=[DataRequired()])
    house = StringField('дом', validators=[DataRequired()])
    flat = StringField('квартира', validators=[DataRequired()])
    # title = StringField('Позиции')
    # sum = StringField("Итого")
    submit = SubmitField('Доставить')

