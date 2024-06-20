from flask_wtf import FlaskForm
from wtforms import IntegerField, DateTimeField, FloatField
from wtforms.validators import DataRequired


class RecyclingTrackerForm(FlaskForm):
    user_id = IntegerField('User ID', validators=[DataRequired()])
    waste_type_id = IntegerField('Waste Type ID', validators=[DataRequired()])
    date_collected = DateTimeField(
        'Date Collected', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
