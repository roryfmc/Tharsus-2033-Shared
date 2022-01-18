from werkzeug.security import generate_password_hash
from app import db
from database.models import User


def change_password_by_username(username, password):
    User.query.filter_by(username=username).update({'password': generate_password_hash(password)})
    db.session.commit()


def change_password_by_id(user_id, password):
    User.query.filter_by(user_id=user_id).update({'password': generate_password_hash(password)})
    db.session.commit()
