import json
from search_function.objects import Search, Part, Supplier


def string_to_search_obj(string_value):
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
            supplier = Supplier(supplier_value['name'], supplier_value['stock'], supplier_value['price'])
            # Store Supplier object in the Part object
            part.suppliers.append(supplier)

        # Store Part object in the Search object
        search_result.parts.append(part)

    return search_result


def search_form_to_obj(search_form):
    search_result = Search()

    for field in search_form.parts:
        part = Part(field.part_name.data, field.quantity.data)
        search_result.parts.append(part)

    return search_result

