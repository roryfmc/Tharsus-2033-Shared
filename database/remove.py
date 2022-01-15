from models import User, FavouriteSupplier, WhitelistedEmail, BlacklistedSupplier
from app import db

class remove_whitelist_email():
    #sql_DeleteUser = "DELETE FROM whitelisted_email WHERE username = username"
    db.execute(sql_DeleteUser)
    db.commit()

class remove_user():
    #sql_DeleteUser = "DELETE FROM users WHERE username = username"
    db.execute(sql_DeleteUser)
    db.commit()

class search_history():
    #track what the user has previously searched

class remove_favorite_supplier():
    # sql_DeleteUser = "DELETE FROM whitelisted_email WHERE username = username"
    db.execute(sql_DeleteUser)
    db.commit()

class remove_blacklist_supplier():
    # sql_DeleteUser = "DELETE FROM whitelisted_email WHERE username = username"
    db.execute(sql_DeleteUser)
    db.commit()