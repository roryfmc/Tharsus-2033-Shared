"""This module contains the functions called when the user enters
the search and search_result webpages.
"""
import flask_excel as excel
from flask import Blueprint, render_template, session, redirect, url_for
from flask_login import login_required, current_user
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj, search_form_to_obj, search_obj_to_json, sort_search_history,\
    get_specific_search_history
from search_function.objects import Search
from webscrape.findchips import search_for_parts
from search_function.objects import Part
from database.add import add_part_search, add_favourite_supplier, add_blacklisted_supplier
from database.models import PartSearch, FavouriteSupplier, BlacklistedSupplier

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    """This function generates the search page for the flask webapp.
    """
    form = SearchForm()
    search_object = Search()

    # If a search has already been made by the user
    if 'search' in session:
        # Store search object to fill in form
        search_object = string_to_search_obj(session['search'])

    if form.validate_on_submit():
        # If any rows have been filled in
        if len(form.parts) > 0:
            # Turn the form into a Search object
            search_object = search_form_to_obj(form)

            # Store search in database
            add_part_search(current_user.id, search_object)

            # Store the search object in session
            session['search'] = search_obj_to_json(search_object)

            search_object = search_for_parts(search_object)
            search_object.sort_part_suppliers()

            # Store the search object in session
            session['search'] = search_obj_to_json(search_object)

            return redirect(url_for('search.search_result'))

    search_history = PartSearch.query.filter_by(user_id=current_user.id).order_by(PartSearch.datetime.desc()).all()
    if search_history:
        history = sort_search_history(search_history)
    else:
        history = []

    return render_template('search.html', form=form, search=search_object, history=history)


@search_blueprint.route('/search_result')
@login_required
def search_result():
    """This function generates the search result page for the flask webapp.
    """
    if 'search' in session:
        search_object = string_to_search_obj(session['search'])
    else:
        search_object = Search()

    return render_template("search_result.html", search_results=search_object.parts)


@search_blueprint.route('/part/<part_count>', methods=['GET'])
@login_required
def part(part_count):
    """This function generates the part page for the flask webapp.
    """
    search_object = string_to_search_obj(session['search'])
    part_object = search_object.parts[int(part_count)-1]

    return render_template("part.html", part_object=part_object)


@search_blueprint.route('/export', methods=['GET'])
@login_required
def export():
    """This function creates an excel file containing all of the part data
    and exports it to the user.
    """
    search_object = string_to_search_obj(session['search'])
    sheets = {}

    for i in enumerate(search_object.parts):
        column_titles = ["Name", "Stock", "Price"]
        sheet = [column_titles]

        for supplier in search_object.parts[i].suppliers:
            new_supplier = [supplier.name, supplier.stock, supplier.price]
            sheet.append(new_supplier)

        sheets[search_object.parts[i].name] = sheet

    return excel.make_response_from_book_dict(sheets, 'xls', file_name="export_search")


@search_blueprint.route('/search_history/<history_count>', methods=['GET'])
@login_required
def search_history(history_count):
    """This function passes the chosen search history into the search form
    on the search page.
    """
    form = SearchForm()
    search_object = Search()

    search_history = PartSearch.query.filter_by(user_id=current_user.id).order_by(PartSearch.datetime.desc()).all()

    if search_history:
        history = sort_search_history(search_history)
        form_history = get_specific_search_history(search_history, history_count)

        for part_history in form_history:
            new_part = Part(part_history[0], part_history[1])
            search_object.parts.append(new_part)
    else:
        history = []

    return render_template('search.html', form=form, search=search_object,
                           history=history)


@search_blueprint.route('/favourite/<supplier>', methods=['GET'])
@login_required
def favourite_supplier(supplier):
    f_supplier = FavouriteSupplier.query.filter_by(user_id=current_user.id).filter_by(supplier_name=supplier).first()

    if not f_supplier:
        add_favourite_supplier(current_user.id, supplier)

    return search_result()


@search_blueprint.route('/blacklist/<supplier>', methods=['GET'])
@login_required
def blacklist_supplier(supplier):
    b_supplier = BlacklistedSupplier.query.filter_by(user_id=current_user.id).filter_by(supplier_name=supplier).first()

    if not b_supplier:
        add_blacklisted_supplier(current_user.id, supplier)

    return search_result()