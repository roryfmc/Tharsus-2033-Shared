from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo


class WhitelistForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    add = SubmitField('Add')  # button to add email to whitelist
    remove = SubmitField('Remove')  # button to remove email from whitelist


class UserForm(FlaskForm):
    u_username = StringField(validators=[InputRequired(), Email()])
    u_submit = SubmitField('Delete')


class ChangePasswordForm(FlaskForm):
    p_username = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
    confirm_password = PasswordField(validators=[InputRequired(),
                                                 EqualTo('password', message='Both password fields must be equal!')])
    p_submit = SubmitField('Change Password')