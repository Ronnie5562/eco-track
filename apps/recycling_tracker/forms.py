from flask_wtf import FlaskForm
from wtforms import SelectField, DateField, FloatField
from wtforms.validators import DataRequired


class RecyclingTrackerForm(FlaskForm):
    user_id = SelectField('User', coerce=int, validators=[DataRequired()])
    waste_type_id = SelectField(
        'Waste Type', coerce=int, validators=[DataRequired()])
    date_collected = DateField(
        'Date', validators=[DataRequired()], render_kw={"type": "date"}
    )
    weight = FloatField('Weight', validators=[DataRequired()])
