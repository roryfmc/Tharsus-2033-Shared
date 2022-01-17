import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length


def character_check(form,field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


class WhitelistForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    add = SubmitField('Add')  # button to add email to whitelist
    remove = SubmitField('Remove')  # button to remove email from whitelist


class UserForm(FlaskForm):
    u_username = StringField(validators=[InputRequired(), Email()])
    u_submit = SubmitField('Delete')


class ChangePasswordForm(FlaskForm):
    p_username = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(),
                                         Length(min=8, message="Password must be at least 8 characters long"),
                                         character_check])
    confirm_password = PasswordField(validators=[InputRequired(),
                                                 EqualTo('password', message='Both password fields must be equal!')])
    p_submit = SubmitField('Change Password')

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*["*?!^+%&/()=}{$#@<>"])')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 lowercase letter, 1 uppercase letter and 1 special character.")