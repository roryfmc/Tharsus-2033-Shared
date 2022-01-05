from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, Form, FormField
from wtforms.validators import InputRequired, ValidationError

class PartForm(Form):
    part_name = StringField('Part Name', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])


class SearchForm(FlaskForm):
    parts = FieldList(FormField(PartForm))
    submit = SubmitField()