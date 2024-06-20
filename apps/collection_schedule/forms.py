from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeField, StringField
from wtforms.validators import DataRequired


class CollectionScheduleForm(FlaskForm):
    route_id = IntegerField('Route ID', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
