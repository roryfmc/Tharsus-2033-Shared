"""This is the main file of the project, which should be ran.
"""
import datetime
import socket
from os import environ
from sshtunnel import SSHTunnelForwarder
import flask_excel as excel
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_session import Session

# CONFIG
app = Flask(__name__, static_folder='templates/assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_checker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SESSION_TYPE'] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=24)
Session(app)
db = SQLAlchemy(app)


def create_app():
    """This function creates the Flask application and registers the blueprints
    """
    from users.views import users_blueprint  # pylint: disable=import-outside-toplevel
    from search_function.views import search_blueprint # pylint: disable=import-outside-toplevel
    from admin.views import admin_blueprint # pylint: disable=import-outside-toplevel

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(search_blueprint)
    excel.init_excel(app)

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

    app.run(host=MY_HOST, port=free_port, debug=True)
