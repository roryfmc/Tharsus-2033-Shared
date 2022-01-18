"""This module contains the functions to add each item to the database."""
import datetime
from models import User, WhitelistedEmail, PartPrice, DesiredPart,\
    FavouriteSupplier, BlacklistedSupplier, PartSearch
from app import db


def add_user(username, password, role="user"):
    """Creates and adds a User object to the database.

    :param username: New user's username
    :param password: New user's password
    :param role: New user's role
    """
    user = User(username=username, password=password, role=role)

    db.session.add(user)
    db.session.commit()


def add_whitelisted_email(email):
    """Creates and adds a WhitelistedEmail object to the database

    :param email: The whitelisted email
    """
    whitelisted_email = WhitelistedEmail(email)

    db.session.add(email=whitelisted_email)
    db.session.commit()


def add_part_prices(search_object):
    """Splits a search object into its parts and
    stores the lowest price for each part in the database

    :param search_object: The Search object which stores all the parts and their prices
    """
    for part in search_object.parts:
        part_price = PartPrice(part_id=part.name, price=part.suppliers[0].price,
                               datetime=datetime.datetime.now())

        db.session.add(part_price)
    db.session.commit()


def add_desired_part(user_id, part_id, quantity):
    """Creates and adds a DesiredPart object to the database

    :param user_id: The user who wants to add the part to their wishlist
    :param part_id: The name of the part
    :param quantity: The quantity of the part
    """
    desired_part = DesiredPart(user_id=user_id, part_id=part_id, quantity=quantity)

    db.session.add(desired_part)
    db.session.commit()


def add_favourite_supplier(user_id, supplier_name):
    """Creates a FavouriteSupplier object and adds it to the database

    :param user_id: The user who is favouriting the supplier
    :param supplier_name: The supplier being favourited
    """
    favourite_supplier = FavouriteSupplier(user_id=user_id, supplier_name=supplier_name)

    db.session.add(favourite_supplier)
    db.session.commit()


def add_blacklisted_supplier(user_id, supplier_name):
    """Creates a BlacklistedSupplier object and adds it to the database

    :param user_id: The user who is blacklisting the supplier
    :param supplier_name: The supplier being blacklisted
    """
    blacklisted_supplier = BlacklistedSupplier(user_id=user_id, supplier_name=supplier_name)

    db.session.add(blacklisted_supplier)
    db.session.commit()


def add_part_search(user_id, search_object):
    """Separates a Search object into its parts and
    stores each part as a PartSearch object in the database

    :param user_id: The user who is searching for the part
    :param search_object: The Search object containing all of the parts being searched
    """
    for part in search_object.parts:
        part_search = PartSearch(user_id=user_id, part_id=part.name,
                                 quantity=part.quantity, datetime=datetime.now())

        db.session.add(part_search)

    db.session.commit()
