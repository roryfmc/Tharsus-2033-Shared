"""This module contains the functions which update data within the database."""
from werkzeug.security import generate_password_hash
from app import db
from database.models import User


def change_password_by_username(username, password):
    """This function changes a user's password by finding them by username"""
    User.query.filter_by(username=username).update({'password': generate_password_hash(password)})
    db.session.commit()


def change_password_by_id(user_id, password):
    """This function changes a user's password by finding them by user id"""
    User.query.filter_by(id=user_id).update({'password': generate_password_hash(password)})
    db.session.commit()
