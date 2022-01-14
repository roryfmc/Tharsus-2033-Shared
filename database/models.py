"""This module stores all of the models used by the database.
These models are used when something is added to the database.
"""
from werkzeug.security import generate_password_hash
from app import db


class User(db.Model):
    """This model represents a users in the database.
    It should be called when you are handling users
    from the database.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar username: The username of the account
    :type username: str
    :cvar password: The password of the account
    :type password: str
    :cvar role: The role of the account, either users or admin
    :type role: str
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, role='users'):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role


class WhitelistedEmail(db.Model):
    """This model represents a whitelisted email address in the database.
    In the system, an admin has the ability to whitelist an email address,
    which then allows a users to register with that email address.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar email: The whitelisted email address
    :type email: str
    """
    __tablename__ = 'whitelisted_email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, email):
        self.email = email


class PartPrice(db.Model):
    """This model represents an entity which stores the price of
    a part at a given time. This is used when a part has been searched,
    and stores the lowest price of the part at that time, along with
    the date and time.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar part_id: The identifying name/ID of the part
    :type part_id: str
    :cvar price: The lowest price of the part at the given time
    :type price: float
    :cvar datetime: The datetime when the part is at this price. Defaults to current time
    :type datetime: datetime
    """
    __tablename__ = 'part_price'

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, part_id, price, datetime=datetime.now()):
        self.part_id = part_id
        self.price = price
        self.datetime = datetime


class DesiredPart(db.Model):
    """This model represents a part which a users has added to their wishlist.
    This means that they would like to be notified when the part has come into stock again.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar user_id: The ID of the users who wishes to add the part to their wishlist
    :type user_id: int
    :cvar part_id: The identifying name/ID of the part
    :type part_id: str
    :cvar quantity: The desired quantity of the part
    :type quantity: int
    """
    __tablename__ = 'desired_parts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    part_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, part_id, quantity):
        self.user_id = user_id
        self.part_id = part_id
        self.quantity = quantity


class FavouriteSupplier(db.Model):
    """This model represents a users's preferred supplier. When a supplier has
    been preferred by the users, it then appears higher a search result when it is
    included.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar user_id: The ID of the users who wishes to add the supplier to their preferred suppliers
    :type user_id: int
    :cvar supplier_name: The name of the supplier which the users prefers
    :type supplier_name: str
    """
    __tablename__ = 'favourite_suppliers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, supplier_name):
        self.user_id = user_id
        self.supplier_name = supplier_name


class BlacklistedSupplier(db.Model):
    """This model represents a users's blacklisted supplier. A supplier is blacklisted
    by a users when they would not like to see results from this supplier. This means
    the supplier won't show up in any of the users's search results.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar user_id: The ID of the users who wishes to add the supplier to their blacklisted suppliers
    :type user_id: int
    :cvar supplier_name: The name of the supplier which the users wants to blacklist
    :type supplier_name: str
    """
    __tablename__ = 'blacklisted_suppliers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, supplier_name):
        self.user_id = user_id
        self.supplier_name = supplier_name


class PartSearch(db.Model):
    """This model represents an individual part which the users has searched for.
    Since this model only represents an individual part, searches with multiple
    parts must be broken down into multiple PartSearch objects, which should be connected
    by containing the same datetime value.

    :cvar id: The incrementing ID number for each entity in the database
    :type id: int
    :cvar user_id: The ID of the users who has searched for the part
    :type user_id: int
    :cvar part_id: The identifying name/ID of the part
    :type part_id: str
    :cvar quantity: The desired quantity of the part
    :type quantity: int
    :cvar datetime: The datetime of the search. Must match the datetime of other parts
    in the same search
    :type datetime: datetime
    """
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    part_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id, part_id, quantity, datetime):
        self.user_id = user_id
        self.part_id = part_id
        self.quantity = quantity
        self.datetime = datetime


def init_db():
    """This function is used to reset the database
    and enter a test users entity.
    To use this function, type "from database.models import init_db", then "init_db()"
    in the python console.
    """
    db.drop_all()
    db.create_all()
    new_user = User(username='user1@test.com', password='password', role='users')
    db.session.add(new_user)
    db.session.commit()
