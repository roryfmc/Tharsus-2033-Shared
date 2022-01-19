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
                                price=supplier_value['price'],
                                price_dict=supplier_value['price_dict'],
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


def sort_search_history(part_search_list):
    """This function returns all of the searches the user has made,
    separating out the individual part searches into the grouped searches
    which the user made.

    :param part_search_list: The list of individual part searches
    :return: A list of grouped searches the user has made
    """
    history = []
    entry = ''
    # Set the date time to be equal to the first part search
    date_time = part_search_list[0].datetime

    # For each individual part search made
    for count, part_search in enumerate(part_search_list):
        # If the date time is the same, it must be part of the same search
        if part_search.datetime == date_time:
            # Add it to the string with correct formatting
            if count == 0:
                entry = entry + part_search.part_id
            else:
                entry = entry + ", " + part_search.part_id
        # If it is not part of the same search (different date time)
        else:
            # Add the previous search to the list of searches
            history.append(entry)
            # Restart the string with the new part search
            entry = part_search.part_id
            # Set the date time to equal the new part search
            date_time = part_search.datetime

    # Add the last search to the list
    history.append(entry)
    return history


def get_specific_search_history(part_search_list, list_count):
    """This function gets the specific search from history
    which the user wants to reuse.

    :param part_search_list: The list of individual part searches
    :param list_count: How many searches ago was the search the user would like to reuse
    :return: A 2D list storing the part names and quantities from the search
    """
    history = []
    entry = []
    date_time = part_search_list[0].datetime
    # How many grouped searches have passed, starting the counter at 1
    dt_count = 1

    for part_search in part_search_list:
        # If the searches date time is different (it's part of a different search)
        if date_time != part_search.datetime:
            # A new grouped search has passed
            dt_count = dt_count + 1
            # Set the new date time
            date_time = part_search.datetime

        # If this is the correct grouped search
        if int(dt_count) == int(list_count):
            # Store the data
            entry.append(part_search.part_id)
            entry.append(part_search.quantity)
            history.append(entry)
            entry = []

    return history
