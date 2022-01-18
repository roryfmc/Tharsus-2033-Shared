"""This module contains all the functions used by the flask application to GET or POST data
for the user functionality."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from users.form import RegisterForm, LoginForm, ChangePassword
from database.models import WhitelistedEmail, User
from database.add import add_user
from search_function.views import search

users_blueprint = Blueprint('users', __name__, template_folder='templates')


# HOME PAGE VIEW
@users_blueprint.route('/', methods=['GET', 'POST'])
@login_required
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
        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            flash("Please check your login details and try again", 'error')

            return render_template('login.html', form=form)
        login_user(user)
        return redirect(url_for('search.search'))

    return render_template('login.html', form=form)


@users_blueprint.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    """This function generates the accounts page for the flask webapp.
    """
    form = ChangePassword()

    if form.validate_on_submit():
        print(request.form.get('old_password'))
        print(request.form.get('password'))

    return render_template('accounts.html', form=form,
                           favourite_suppliers=[], blacklisted_suppliers=["hello"])


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """This function generates the register page for the flask webapp.
    """
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        whitelisted_email = WhitelistedEmail.query.filter_by(email=form.username.data).first()

        if not whitelisted_email:
            flash("This email address has not been whitelisted. Please contact the system administrator", 'error')
        else:
            if user:
                flash('An account with this email address already exists', 'error')
            else:
                add_user(form.username.data, form.password.data)
                return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('users.index'))
