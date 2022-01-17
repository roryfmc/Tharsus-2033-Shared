from models import *
from app import db


def remove_whitelisted_email(email):
    WhitelistedEmail.query.filter_by(email=email).delete()
    User.query.filter_by(username=email).delete()

    db.session.commit()


def remove_user(email):
    User.query.filter_by(username=email).delete()
    WhitelistedEmail.query.filter_by(email=email).delete()

    db.session.commit()


def remove_favourite_supplier(user_id, supplier_name):
    FavouriteSupplier.query.filter_by(user_id=user_id).filter_by(supplier_name=supplier_name).delete()

    db.session.commit()


def remove_blacklisted_supplier(user_id, supplier_name):
    BlacklistedSupplier.query.filter_by(user_id=user_id).filter_by(supplier_name=supplier_name).delete()

    db.session.commit()