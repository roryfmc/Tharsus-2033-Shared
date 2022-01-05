import json
import random
from flask import Blueprint, render_template, session
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj
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
        for field in form.parts:
            print(field.part_name.data)
            print(field.quantity.data)


    return render_template('search.html', form=form)


@search_blueprint.route('/search_result')
def search_result():
    search_test = setup()

    session['search'] = json.dumps(search_test, default=lambda x: x.__dict__)

    search_object = string_to_search_obj(session['search'])
    search_object.sort_part_suppliers()

    return render_template("search_result.html", search_results=search_object.parts)

