"""This module contains all the forms which appear on the admin page"""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, ValidationError, Length
from users.form import character_check


class WhitelistForm(FlaskForm):
    """This class serves as a model for the add/remove whitelisted emails form
    on the admin webpage"""
    email = StringField(validators=[InputRequired(), Email()])
    add = SubmitField('Add')  # button to add email to whitelist
    remove = SubmitField('Remove')  # button to remove email from whitelist


class UserForm(FlaskForm):
    """This class serves as a model for the delete user form on the admin webpage"""
    u_username = StringField(validators=[InputRequired(), Email()])
    u_submit = SubmitField('Delete')


class ChangePasswordForm(FlaskForm):
    """This class serves as a model for the change password form on the webpage"""
    p_username = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(),
                    Length(min=8, message="Password must be at least 8 characters long"),
                    character_check])
    confirm_password = PasswordField(validators=[InputRequired(),
                    EqualTo('password', message='Both password fields must be equal!')])
    p_submit = SubmitField('Change Password')

    def validate_password(self, password):  # pylint: disable=unused-argument
        """This function checks that a password given into the register form is complex enough"""
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit and 1 uppercase letter.")
