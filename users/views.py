"""This module contains all the functions used by the flask application to GET or POST data
for the user functionality."""
from flask import Blueprint, render_template, request
from users.form import RegisterForm, LoginForm, ChangePassword
from search_function.views import search

users_blueprint = Blueprint('users', __name__, template_folder='templates')

favourite_suppliers = ["1", "2", "3", "4", "5", "6", "7", "8"]


# HOME PAGE VIEW
@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    """This function generates the index page for the flask webapp,
    which redirects to the search page.
    """
    return search()


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """This function generates the login page for the flask webapp.
    """
    form = LoginForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return accounts()

    return render_template('login.html', form=form)


@users_blueprint.route('/accounts', methods=['GET', 'POST'])
def accounts():
    """This function generates the accounts page for the flask webapp.
    """
    form = ChangePassword()

    if form.validate_on_submit():
        print(request.form.get('old_password'))
        print(request.form.get('password'))

    return render_template('accounts.html', form=form,
                           favourite_suppliers=favourite_suppliers, blacklisted_suppliers=["hello"])


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """This function generates the register page for the flask webapp.
    """
    form = RegisterForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return accounts()

    return render_template('register.html', form=form)
