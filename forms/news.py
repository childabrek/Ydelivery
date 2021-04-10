from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Job title', validators=[DataRequired()])
    content = StringField("Team Leader Id")
    work_size = StringField("Work Size")
    collaborators = StringField("Collaborators")
    is_private = BooleanField("is job finished")
    submit = SubmitField('Применить')

