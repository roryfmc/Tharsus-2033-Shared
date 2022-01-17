from flask import Blueprint, render_template, request
from admin.forms import WhitelistForm, UserForm, ChangePasswordForm
whitelistArray = []
userlist = ["BOB", "John", "James"]
admin_blueprint = Blueprint('admin', __name__, template_folder='templates')


@admin_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    whitelist_form = WhitelistForm()
    user_form = UserForm()
    change_password_form = ChangePasswordForm()

    # If the whitelist form was submitted
    if (whitelist_form.add.data or whitelist_form.remove.data) and whitelist_form.validate_on_submit():
        # Get email
        email = request.form.get('email')

        # If the add button was clicked
        if whitelist_form.add.data:
            whitelistArray.append(email)

        # If the remove button was clicked
        elif whitelist_form.remove.data:
            if email in whitelistArray:
                whitelistArray.remove(email)

    # If the user form was submitted
    elif user_form.u_submit.data and user_form.validate_on_submit():
        email = request.form.get('u_username')

    elif change_password_form.p_submit.data and change_password_form.validate_on_submit():
        print(request.form.get('password'))

    return render_template('admin.html', whitelist_form=whitelist_form, user_form=user_form,
                           change_password_form=change_password_form, whitelist=whitelistArray, userlist=userlist)