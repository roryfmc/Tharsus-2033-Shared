import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError

def character_check(form,field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


class RegisterForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required(), Length(min=8, max=15, message="Password must be between 8 and 15 characters in length."), character_check])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*["*?!^+%&/()=}{$#@<>"])')
        if not p.match(self.password.data):
            raise ValidationError(
                "Password must contain at least 1 digit, 1 lowercase letter, 1 uppercase letter and 1 special character.")

class LoginForm(FlaskForm):
    email = StringField(validators=[Required()])
    password = PasswordField(validators=[Required()])
    submit = SubmitField()

class ChangePassword(FlaskForm):
    old_password = PasswordField(validators=[Required(), EqualTo('password', message='Must be equal to the old password!')])
    password = PasswordField(validators=[Required()])
    corfirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField()