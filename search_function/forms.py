"""This module stores the Flask forms used by the search function.
The form SearchForm utilises the form PartForm within itself, using
a FieldList to allow a dynamic number of part_names and quantities
to be supplied in the form.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList, Form, FormField
from wtforms.validators import InputRequired


class PartForm(Form):
    """This form stores the data for each individual part entered
    into the form. This form is used multiple times in the main form,
    to accommodate for as many parts entered as the user desires.
    """
    part_name = StringField('Part Name', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])


class SearchForm(FlaskForm):
    """This is the main form used by the search function.
    It utilises the PartForm a dynamic number of times to
    create a form which allows the user to enter as many
    parts, along with quantities, as they desire.
    """
    parts = FieldList(FormField(PartForm))
    submit = SubmitField()
