import datetime
from models import *
from app import db


def add_user(username, password, role="user"):
    user = User(username=username, password=password, role=role)

    db.session.add(user)
    db.session.commit()


def add_whitelisted_email(email):
    whitelisted_email = WhitelistedEmail(email)

    db.session.add(email=whitelisted_email)
    db.session.commit()


def add_part_prices(search_object):
    for part in search_object.parts:
        part_price = PartPrice(part_id=part.name, price=part.suppliers[0].price, datetime=datetime.datetime.now())

        db.session.add(part_price)
    db.session.commit()


def add_desired_part(user_id, part_id, quantity):
    desired_part = DesiredPart(user_id=user_id, part_id=part_id, quantity=quantity)

    db.session.add(desired_part)
    db.session.commit()


def add_favourite_supplier(user_id, supplier_name):
    favourite_supplier = FavouriteSupplier(user_id=user_id, supplier_name=supplier_name)

    db.session.add(favourite_supplier)
    db.session.commit()


def add_blacklisted_supplier(user_id, supplier_name):
    blacklisted_supplier = BlacklistedSupplier(user_id=user_id, supplier_name=supplier_name)

    db.session.add(blacklisted_supplier)
    db.session.commit()


def add_part_search(user_id, search_object):
    for part in search_object.parts:
        part_search = PartSearch(user_id=user_id, part_id=part.name, quantity=part.quantity, datetime=datetime.now())

        db.session.add(part_search)

    db.session.commit()
