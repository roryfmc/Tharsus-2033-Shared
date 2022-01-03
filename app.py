import socket
import json
from flask import Flask, render_template, request, session
from search_function.forms import SearchForm
from search_function.objects import Search, Part, Supplier
from search_function.search import string_to_search_obj


# CONFIG
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lottery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'


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


# HOME PAGE VIEW
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        for field in form.parts:
            print(field.part_name.data)
            print(field.quantity.data)

    return render_template('index.html', form=form)


@app.route('/search')
def search():
    search_test = setup()

    session['search'] = json.dumps(search_test, default=lambda x: x.__dict__)

    return render_template("search.html", search_results=string_to_search_obj(session['search']).parts)

if __name__ == "__main__":
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    app.run(host=my_host, port=free_port, debug=True)



