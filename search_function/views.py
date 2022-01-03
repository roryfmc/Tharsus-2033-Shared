import json
from flask import Blueprint, render_template, session
from search_function.forms import SearchForm
from search_function.search import string_to_search_obj
from search_function.objects import Search, Part, Supplier


def setup():
    search_test = Search()
    part_test = Part("Bob", 24)
    search_test.parts.append(part_test)
    supplier_test = Supplier("Test Supplier")
    supplier_test.stock = 85
    supplier_test.price = 1.40
    part_test.suppliers.append(supplier_test)

    supplier_test2 = Supplier("Second Test Supplier")
    supplier_test2.stock = 42
    supplier_test2.price = 3.48
    part_test.suppliers.append(supplier_test2)

    part_test2 = Part("Bill", 98)
    search_test.parts.append(part_test2)
    supplier_test3 = Supplier("Test Supplier 2")
    supplier_test3.stock = 85
    supplier_test3.price = 1.40
    part_test2.suppliers.append(supplier_test)

    supplier_test4 = Supplier("Second Test Supplier 2")
    supplier_test4.stock = 42
    supplier_test4.price = 3.48
    part_test2.suppliers.append(supplier_test2)

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

    return render_template("search_result.html", search_results=string_to_search_obj(session['search']).parts)

