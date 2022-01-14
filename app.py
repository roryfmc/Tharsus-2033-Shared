import socket
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# CONFIG
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock_checker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

db = SQLAlchemy(app)


# HOME PAGE VIEW
@app.route('/', methods=['GET', 'POST'])
def index(): # pylint: disable=missing-function-docstring
    return render_template('index.html')


if __name__ == "__main__":
    MY_HOST = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((MY_HOST, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    from users.views import users_blueprint

    app.register_blueprint(users_blueprint)

    app.run(host=MY_HOST, port=free_port, debug=True)
