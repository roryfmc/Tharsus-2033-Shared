from werkzeug.security import generate_password_hash
from app import db
from database.models import User


def change_password(username, password):
    User.query.filter_by(username=username).update({'password': generate_password_hash(password)})
    db.session.commit()
