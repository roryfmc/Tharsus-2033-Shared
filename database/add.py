from app import db
from search_function.objects import Search, Part, Supplier
from models import PartPrice, User, FavouriteSupplier, WhitelistedEmail, BlacklistedSupplier
from flask import flash, render_template, redirect, url_for
from webscrape.findchips import search_for_parts

class Whitelist_Email(WhitelistedEmail):
    #allow the admin to whitelist an email from the user

class register(Whitelist_Email):
    def register(WhitelistedEmail):
        # create signup form object
        form = User()

        # if request method is POST or form is valid
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            # if this returns a user, then the email already exists in database

            # if email already exists redirect user back to signup page with error message so user can try again
            if user:
                flash('Email address already exists')
                return render_template('register.html', form=form)

            for i in range(len(whitelisted_email)):
                if user == whitelist_email[i]:
                    # create a new user with the form data
                    new_user = User(email=form.email.data,
                                    password=form.password.data,
                                    role='user')

                    # add the new user to the database
                    db.execute('''INSERT INTO users VALUES(?,?,?)''', (User))
                    db.session.commit()
                else:
                    flash('Email address isnt approved by the admin')
                    return render_template('register.html', form=form)

            # sends user to login page
            return redirect(url_for('users.login'))
        # if request method is GET or form not valid re-render signup page
        return render_template('register.html', form=form)

class Add_Database(db,Part, Supplier, PartPrice):
    form = PartPrice()
    for i in search_for_parts():
        db.execute('''INSERT INTO part_price VALUES(?,?,?)''', (Supplier))
        db.session.commit()

class Add_Favorite_Supplier(FavouriteSupplier):
    #adds a supplier to the favorite suppliers list
    db.execute(''''INSERT INTO favourite_suppliers VALUE(?,?,?)''', (id, user_id, supplier_name))
    db.session.commit()

class Block_Supplier(BlacklistedSupplier):
    #if user blocks supplier name
    db.execute(''''INSERT INTO blacklisted_suppliers VALUE(?,?,?)''', (id, user_id, supplier_name))
    db.session.commit()

class Alert_User():
    #alerts user when their part has lowered their price





