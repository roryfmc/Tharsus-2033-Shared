import json
import random
from flask import Blueprint, render_template, session, redirect, url_for
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj, search_form_to_obj, search_obj_to_json
from search_function.objects import Search, Part, Supplier


def setup():
    search_test = Search()
    for i in range(100):
        part_test = Part(str(random.randint(3000000, 9999999)), 20)
        search_test.parts.append(part_test)

        for p in range(random.randint(2,10)):

            supplier_test = Supplier("Test Supplier")
            supplier_test.stock = random.randint(5,250)
            supplier_test.price = random.randint(1,10)
            part_test.suppliers.append(supplier_test)

    return search_test


search_blueprint = Blueprint('search', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        search_object = search_form_to_obj(form)

        session['search'] = search_obj_to_json(search_object)

        return redirect(url_for('search.search_result'))

    return render_template('search.html', form=form)


@search_blueprint.route('/search_result')
def search_result():
    if 'search' in session:
        search_object = string_to_search_obj(session['search'])
        search_object.sort_part_suppliers()
    else:
        search_object = Search()

    return render_template("search_result.html", search_results=search_object.parts)

