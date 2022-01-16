from flask import Blueprint, render_template, request
from users.forms import AdminForm
whitelistArray = []

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/admin', methods=['GET', 'POST'])
def admin():
    form = AdminForm()

    if form.validate_on_submit():
        email = request.form.get('email')
        # whitelistArray.remove(email)
        whitelistArray.append(email)
        print(email, " has been added to the whitelist. ")  # print the input

        # print the whitelist
        for value in whitelistArray:
            print(value)

        # code for adding value the whitelist to the database goes here
        # return register() now?

    return render_template('admin.html', form=form)
