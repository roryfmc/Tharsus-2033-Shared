"""This module contains all the functions used by the flask application to GET or POST data
for the user functionality."""
from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from users.form import RegisterForm, LoginForm, ChangePassword
from database.models import WhitelistedEmail, User, FavouriteSupplier, BlacklistedSupplier
from database.add import add_user
from database.update import change_password_by_id
from database.remove import remove_favourite_supplier, remove_blacklisted_supplier
from search_function.views import search

users_blueprint = Blueprint('users', __name__, template_folder='templates')


def get_favourite_suppliers():
    """This function gets a list of all the user's favourite suppliers"""
    supplier_objects = FavouriteSupplier.query.filter_by(user_id=current_user.id).all()
    suppliers = []

    for supplier in supplier_objects:
        suppliers.append(supplier.supplier_name)

    return suppliers


def get_blacklisted_suppliers():
    """This function gets a list of all the user's blacklisted suppliers"""
    supplier_objects = BlacklistedSupplier.query.filter_by(user_id=current_user.id).all()
    suppliers = []

    for supplier in supplier_objects:
        suppliers.append(supplier.supplier_name)

    return suppliers


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
        change_password_by_id(current_user.id, form.password.data)
        flash("Password changed", "info")

    return render_template('accounts.html', form=form,
                           favourite_suppliers=get_favourite_suppliers(),
                           blacklisted_suppliers=get_blacklisted_suppliers())


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    """This function generates the register page for the flask webapp.
    """
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        whitelisted_email = WhitelistedEmail.query.filter_by(email=form.username.data).first()

        if not whitelisted_email:
            flash("This email address has not been whitelisted. "
                  "Please contact the system administrator", 'error')
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
    """This function logs the current user out"""
    logout_user()
    return redirect(url_for('users.index'))


@users_blueprint.route('/remove_favourite/<supplier>', methods=['GET'])
@login_required
def remove_f_supplier(supplier):
    """This function takes the supplier name and removes it from the user's favourites"""
    remove_favourite_supplier(current_user.id, supplier)
    return redirect(url_for('users.accounts'))


@users_blueprint.route('/remove_blacklist/<supplier>', methods=['GET'])
@login_required
def remove_b_supplier(supplier):
    """This function takes the supplier name and removes it from the user's blacklist"""
    remove_blacklisted_supplier(current_user.id, supplier)
    return redirect(url_for('users.accounts'))
