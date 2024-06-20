# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CollectionRouteForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    area = StringField('Area', validators=[DataRequired()])
    schedule = StringField('Schedule', validators=[DataRequired()])
