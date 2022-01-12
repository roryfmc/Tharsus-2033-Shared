from flask import Blueprint, render_template, request, flash

from form import RegisterForm

users_blueprint = Blueprint('users', __name__, template_folder='templates')


#check if the user is on the whitelist
##add user to the database


@users_blueprint.route('/login')
def login():
    return render_template('login.html')

@users_blueprint.route('/accounts')
def accounts():
    return render_template('accounts.html')


