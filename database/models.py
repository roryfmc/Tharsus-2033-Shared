from app import db
from werkzeug.security import generate_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password, role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role


class WhitelistedEmail(db.Model):
    __tablename__ = 'whitelisted_email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)

    def __init__(self, email):
        self.email = email


class PartPrice(db.Model):
    __tablename__ = 'part_price'

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)

    def __init__(self, part_id, price, datetime):
        self.part_id = part_id
        self.price = price
        self.datetime = datetime


class DesiredPart(db.Model):
    __tablename__ = 'desired_parts'

    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, part_id, quantity):
        self.part_id = part_id
        self.quantity = quantity


class FavouriteSupplier(db.Model):
    __tablename__ = 'favourite_suppliers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, supplier_name):
        self.user_id = user_id
        self.supplier_name = supplier_name


class BlacklistedSupplier(db.Model):
    __tablename__ = 'blacklisted_suppliers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    supplier_name = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, supplier_name):
        self.user_id = user_id
        self.supplier_name = supplier_name


class PartSearch(db.Model):
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
    db.drop_all()
    db.create_all()
    new_user = User(username='user1@test.com', password='password', role='user')
    db.session.add(new_user)
    db.session.commit()
