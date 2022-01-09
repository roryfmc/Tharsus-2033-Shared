from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


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
