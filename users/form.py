"""This module contains the Forms used by the Login, Register and Accounts pages."""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError


def character_check(form,field):  # pylint: disable=unused-argument
    """This function checks that the field does not contain any characters which are prohibited"""
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed")


class RegisterForm(FlaskForm):
    """This class serves as a model for the register form on the webpage"""
    username = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(),
                Length(min=8, message="Password must be at least 8 characters long"),
                character_check])
    confirm_password = PasswordField(validators=[InputRequired(),
                EqualTo('password',
                message='Both password fields must be equal!')])
    submit = SubmitField()

    def validate_password(self, password):  # pylint: disable=unused-argument
        """This function checks that a password given into the register form is complex enough"""
        regex = re.compile(r'(?=.*\d)(?=.*[A-Z])')
        if not regex.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit and 1 uppercase letter.")


class LoginForm(FlaskForm):
    """This class serves as a model for the login form on the webpage"""
    username = StringField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired()])
    submit = SubmitField()


class ChangePassword(FlaskForm):
    """This class serves as a model for the change password form on the webpage"""
    old_password = PasswordField(validators=[InputRequired()])
    password = PasswordField(validators=[InputRequired(),  Length(min=8, message="Password must be at least 8 characters long"),
                character_check])
    confirm_password = PasswordField(validators=[InputRequired(),
                EqualTo('password', message='Both password fields must be equal!')])

    def validate_password(self, password):  # pylint: disable=unused-argument
        """This function checks that a password given into the register form is complex enough"""
        regex = re.compile(r'(?=.*\d)(?=.*[A-Z])')
        if not regex.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit and 1 uppercase letter.")
    submit = SubmitField()
