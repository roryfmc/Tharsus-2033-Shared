"""This module contains functions used by the search process.
These functions include string_to_search_obj, which turns the json format
stored in the session cookie as a string, into a Search object which can be used.
This module also contains search_form_to_obj, which turns the flask form containing
the user inputted data into a Search object.
"""

import json
from search_function.objects import Search, Part, Supplier


def string_to_search_obj(string_value):
    """This function turns a string into a Search object.
    This is used when the search data is retrieved from the session,
    as it is in json format, stored as a string.

    :param string_value: the json formatted search data stored in a string
    :return: the Search object storing the search data.
    """
    # Turn string json into a dict
    dictionary_value = json.loads(string_value)

    # Create empty Search object
    search_result = Search()

    # Create list of parts stored in the dict
    parts = dictionary_value['parts']

    # For each part in the list
    for part_value in parts:
        # Create a new Part object
        part = Part(part_value['name'], part_value['quantity'])

        # For every supplier stored in the part
        for supplier_value in part_value['suppliers']:
            # Create a new Supplier object
            supplier = Supplier(name=supplier_value['name'], stock=supplier_value['stock'],
                                price=supplier_value['price'], price_dict=supplier_value['price_dict'],
                                link=supplier_value['link'])
            # Store Supplier object in the Part object
            part.suppliers.append(supplier)

        # Store Part object in the Search object
        search_result.parts.append(part)

    return search_result


def search_form_to_obj(search_form):
    """This function takes the flask SearchForm
    and returns a Search object with the relevant data stored.

    :param search_form: Flask SearchForm
    :return: Search object storing the data from the SearchForm
    """
    # Create new Search object
    search_result = Search()

    # For each part inputted into the form
    for field in search_form.parts:
        # Create new part object
        part = Part(field.part_name.data, field.quantity.data)
        # Add the part object to the list in the Search object
        search_result.parts.append(part)

    return search_result


def search_obj_to_json(search_object):
    """This function turns a Search object into a json format,
    stored within a string. This is required when storing the
    Search object within the Flask session.

    :param search_object: Search object to be reformatted
    :return: json format stored as a string containing all part and supplier details
    """
    return json.dumps(search_object, default=lambda x: x.__dict__)
