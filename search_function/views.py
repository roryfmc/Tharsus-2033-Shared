"""This module contains the functions called when the user enters
the search and search_result webpages.
"""
import random
from flask import Blueprint, render_template, session, redirect, url_for
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj, search_form_to_obj, search_obj_to_json
from search_function.objects import Search, Part, Supplier
from webscrape.findchips import search_for_parts


def setup():  # pylint: disable=missing-function-docstring
    search_test = Search()
    for _ in range(100):
        part_test = Part(str(random.randint(3000000, 9999999)), 20)
        search_test.parts.append(part_test)

        for _ in range(random.randint(2,10)):

            supplier_test = Supplier("Test Supplier")
            supplier_test.stock = random.randint(5,250)
            supplier_test.price = random.randint(1,10)
            part_test.suppliers.append(supplier_test)

    return search_test


search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():  # pylint: disable=missing-function-docstring
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

            # Store the search object in session
            session['search'] = search_obj_to_json(search_object)

            return redirect(url_for('search.search_result'))

    return render_template('search.html', form=form, search=search_object)


@search_blueprint.route('/search_result')
def search_result():  # pylint: disable=missing-function-docstring
    if 'search' in session:
        search_object = string_to_search_obj(session['search'])
        search_object.sort_part_suppliers()
    else:
        search_object = Search()

    return render_template("search_result.html", search_results=search_object.parts)


@search_blueprint.route('/part/<part_count>')
def part(part_count):
    search_object = string_to_search_obj(session['search'])
    part_object = search_object.parts[int(part_count)]

    return render_template("part.html", part_object=part_object)
