import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError


def character_check(form,field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=8, message="Password must be at least 8 characters long"), character_check])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*["*?!^+%&/()=}{$#@<>"])')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 lowercase letter, 1 uppercase letter and 1 special character.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField()


class ChangePassword(FlaskForm):
    old_password = PasswordField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()