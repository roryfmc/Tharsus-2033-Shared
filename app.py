"""This is the main file of the project, which should be ran.
"""
import datetime
import socket
from os import environ
from functools import wraps
from sshtunnel import SSHTunnelForwarder
import flask_excel as excel
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_session import Session
from database.database import db


def requires_roles(*roles):
    """This function handles the wrapper which determines whether a user
    has the required role to view the webpage.
    """
    def wrapper(f):  # pylint: disable=invalid-name
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                return render_template('403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def create_app():
    """This function creates the Flask application and registers the blueprints
    """
    # CONFIG
    flask_app = Flask(__name__, static_folder='templates/assets')
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    flask_app.config['SECRET_KEY'] = 'kjhfskadulfhusdLFLDJYUSGYFuiasduihuh'
    flask_app.config['SESSION_TYPE'] = "filesystem"
    flask_app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=1)
    Session(flask_app)
    db.init_app(flask_app)

    from users.views import users_blueprint  # pylint: disable=import-outside-toplevel
    from search_function.views import search_blueprint # pylint: disable=import-outside-toplevel
    from admin.views import admin_blueprint # pylint: disable=import-outside-toplevel

    flask_app.register_blueprint(admin_blueprint)
    flask_app.register_blueprint(users_blueprint)
    flask_app.register_blueprint(search_blueprint)
    excel.init_excel(flask_app)

    return app


def get_db_uri():
    """This function creates the connection to the database through the university SSH

    :return: The database URI
    """
    server = SSHTunnelForwarder(('linux.cs.ncl.ac.uk', 22),
                                ssh_username=environ['CSC_USER'], ssh_password=environ['CSC_PASS'],
                                remote_bind_address=('cs-db.ncl.ac.uk', 3306))
    server.start()
    return f'mysql+pymysql://csc2033_team45:{environ["DB_PASS"]}' \
           f'@localhost:{server.local_bind_port}/csc2033_team45'


if __name__ == "__main__":
    MY_HOST = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((MY_HOST, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app = create_app()

    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from database.models import User  # pylint: disable=import-outside-toplevel

    @login_manager.user_loader
    def load_user(id):  # pylint: disable=invalid-name,redefined-builtin
        """This function sets the current user to be the user who has just logged in."""
        return User.query.get(int(id))

    app.run(host=MY_HOST, port=free_port, debug=True)


    @app.errorhandler(403)
    def page_forbidden(error):  # pylint: disable=unused-argument
        """This function handles the 403 page for the flask webapp."""
        return render_template('403.html'), 403


    @app.errorhandler(404)
    def page_not_found(error):  # pylint: disable=unused-argument
        """This function handles the 404 page for the flask webapp"""
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_error(error):  # pylint: disable=unused-argument
        """This function handles the 500 page for the flask webapp"""
        return render_template('500.html'), 500
