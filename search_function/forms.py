from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import InputRequired, ValidationError


class SearchForm(FlaskForm):
    part_name = StringField(validators=[InputRequired()])
    quantity = IntegerField(validators=[InputRequired()])
    submit = SubmitField()