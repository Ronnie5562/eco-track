# forms.py
from flask_wtf import FlaskForm
from wtforms import SelectField, DateField
from wtforms.validators import DataRequired


class CollectionScheduleForm(FlaskForm):
    route_id = SelectField('Route ID', validators=[DataRequired()], coerce=int)
    date = DateField(
        'Date', validators=[DataRequired()], render_kw={"type": "date"}
    )
