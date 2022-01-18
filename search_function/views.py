"""This module contains the functions called when the user enters
the search and search_result webpages.
"""
import flask_excel as excel
from flask import Blueprint, render_template, session, redirect, url_for
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj, search_form_to_obj, search_obj_to_json
from search_function.objects import Search
from webscrape.findchips import search_for_parts

search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET', 'POST'])
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

            # Store the search object in session
            session['search'] = search_obj_to_json(search_object)

            search_object = search_for_parts(search_object)
            search_object.sort_part_suppliers()

            # Store the search object in session
            session['search'] = search_obj_to_json(search_object)

            return redirect(url_for('search.search_result'))

    return render_template('search.html', form=form, search=search_object, history=[1,2,3,4,5,6,7])


@search_blueprint.route('/search_result')
def search_result():
    """This function generates the search result page for the flask webapp.
    """
    if 'search' in session:
        search_object = string_to_search_obj(session['search'])
    else:
        search_object = Search()

    return render_template("search_result.html", search_results=search_object.parts)


@search_blueprint.route('/part/<part_count>', methods=['GET'])
def part(part_count):
    """This function generates the part page for the flask webapp.
    """
    search_object = string_to_search_obj(session['search'])
    part_object = search_object.parts[int(part_count)-1]

    return render_template("part.html", part_object=part_object)


@search_blueprint.route('/export', methods=['GET'])
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
def search_history(history_count):  # pylint: disable=unused-argument
    """This function passes the chosen search history into the search form
    on the search page.
    """
    form = SearchForm()
    search_object = Search()

    # Get history and put it into search object

    return render_template('search.html', form=form, search=search_object,
                           history=[1, 2, 3, 4, 5, 6, 7])
