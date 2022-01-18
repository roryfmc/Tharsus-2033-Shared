"""This module contains the functions used by the flask application to GET or POST data
for the admin functionality."""
from flask import Blueprint, render_template, flash
from flask_login import login_required
from admin.forms import WhitelistForm, UserForm, ChangePasswordForm
from database.models import WhitelistedEmail, User
from database.add import add_whitelisted_email
from database.remove import remove_whitelisted_email, remove_user
from database.update import change_password
from app import requires_roles

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def admin():
    """This function generates the admin page for the flask webapp.
    """
    whitelist_form = WhitelistForm()
    user_form = UserForm()
    change_password_form = ChangePasswordForm()

    # If the whitelist form was submitted
    if (whitelist_form.add.data or whitelist_form.remove.data)\
            and whitelist_form.validate_on_submit():
        # Get email
        email = whitelist_form.email.data
        whitelisted = WhitelistedEmail.query.filter_by(email=email).first()

        # If the add button was clicked
        if whitelist_form.add.data:
            if whitelisted:
                flash("Can't add email. Email has already been added.", 'error')
            else:
                add_whitelisted_email(email)
                flash(f"{email} added.", 'info')

        # If the remove button was clicked
        elif whitelist_form.remove.data:
            if whitelisted:
                remove_whitelisted_email(email)
                flash(f"{email} removed.", 'info')
            else:
                flash("Can't remove email. Email is not on the system.", 'error')

    # If the user form was submitted
    elif user_form.u_submit.data and user_form.validate_on_submit():
        # Get email
        email = user_form.u_username.data
        user = User.query.filter_by(username=email).first()

        if not user:
            flash(f"Can't delete user {email}. User does not exist", 'error')
        else:
            remove_user(email)
            flash(f"User {email} removed", 'info')

    # If the change password form was submitted
    elif change_password_form.p_submit.data and change_password_form.validate_on_submit():
        email = change_password_form.p_username.data
        password = change_password_form.password.data
        user = User.query.filter_by(username=email).first()

        if not user:
            flash("Can't change password. User does not exist", 'error')
        else:
            change_password(email, password)
            flash("Password changed", 'info')

    whitelist = []
    whitelist_models = WhitelistedEmail.query.order_by('id').all()
    for whitelist_model in whitelist_models:
        whitelist.append(whitelist_model.email)

    userlist = []
    userlist_models = User.query.order_by('id').all()
    for userlist_model in userlist_models:
        userlist.append(userlist_model.username)

    return render_template('admin.html', whitelist_form=whitelist_form,
                           user_form=user_form,
                           change_password_form=change_password_form,
                           whitelist=whitelist, userlist=userlist)
