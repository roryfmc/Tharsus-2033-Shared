from flask import Blueprint, render_template, request, flash
from users.form import RegisterForm, LoginForm, ChangePassword

users_blueprint = Blueprint('users', __name__, template_folder='templates')

favourite_suppliers = ["1", "2", "3", "4", "5", "6", "7", "8"]

# HOME PAGE VIEW
@users_blueprint.route('/', methods=['GET', 'POST'])
def index(): # pylint: disable=missing-function-docstring
    return render_template('index.html')


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return accounts()

    return render_template('login.html', form=form)


@users_blueprint.route('/accounts', methods=['GET', 'POST'])
def accounts():
    form = ChangePassword()

    if form.validate_on_submit():
        print(request.form.get('old_password'))
        print(request.form.get('password'))

    return render_template('accounts.html', form=form, favourite_suppliers=favourite_suppliers, blacklisted_suppliers=["hello"])


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print(request.form.get('username'))
        print(request.form.get('password'))
        return accounts()

    return render_template('register.html', form=form)


