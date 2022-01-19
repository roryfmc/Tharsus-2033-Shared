"""This module contains all the functions to remove an item from the database"""
from database.models import WhitelistedEmail, User, FavouriteSupplier, BlacklistedSupplier
from app import db


def remove_whitelisted_email(email):
    """This function removes a chosen whitelisted email from the database.
    If there is a user under that email, it deletes the user too.
    """
    WhitelistedEmail.query.filter_by(email=email).delete()
    User.query.filter_by(username=email).delete()

    db.session.commit()


def remove_user(email):
    """This function removes a chosen user and its email from the user
    and whitelisted email tables in the database.
    """
    User.query.filter_by(username=email).delete()
    WhitelistedEmail.query.filter_by(email=email).delete()

    db.session.commit()


def remove_favourite_supplier(user_id, supplier_name):
    """This function removes a user's favourite supplier."""
    FavouriteSupplier.query.filter_by(user_id=user_id).\
        filter_by(supplier_name=supplier_name).delete()

    db.session.commit()


def remove_blacklisted_supplier(user_id, supplier_name):
    """This function removes a user's blacklisted supplier."""
    BlacklistedSupplier.query.filter_by(user_id=user_id).\
        filter_by(supplier_name=supplier_name).delete()

    db.session.commit()
