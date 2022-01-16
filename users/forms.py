from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email


class AdminForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    whiteListEmail = SubmitField()  # button to add email to whitelist
    remove = SubmitField()  # button to remove email from whitelist
    deleteAccount = SubmitField()  # button to delete an account using the email
