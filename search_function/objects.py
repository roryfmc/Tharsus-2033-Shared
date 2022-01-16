"""This module contains the classes Search, Part and Supplier.
These are used as data structures for the search functionality.

 The search class is used to represent a search made by the user on the application.
 This contains Part objects which represent each part the user is searching for,
 and contain all the data about the part. It also contains Supplier objects,
 which store the data on each supplier that has been searched for the part.
 """

import copy
import operator


class Search:  # pylint: disable=too-few-public-methods
    """
    The Search object represents a search which a user makes in the web app.
    It stores each part which is being searched as a separate Part object in a list

    :ivar parts: This is where all the parts, which the user is searching for, are stored.
    :type parts: list
    """

    def __init__(self):
        self.parts = []

    def sort_part_suppliers(self):
        """This function loops through all parts stored in self.parts
        and calls their sort.suppliers() functions.
        """
        for part in self.parts:
            part.sort_suppliers()


class Part:
    """The Part object represents a single part which the user is searching for.
    The Part object contains information regarding the part name(number),
    the desired quantity and the list of suppliers which have been searched.

    :param name: name is used to store the name of the part which the user has entered.
    :type name: str
    :param quantity: quantity is used to store the user's desired quantity of the part.
    :type quantity: int

    :ivar name: This is where the name of the part is stored.
    :type name: str
    :ivar quantity: This is where the desired quantity is stored.
    :type quantity: int
    :ivar suppliers: This is where the list of suppliers is stored.
    :type suppliers: list
    """

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = int(quantity)
        self.suppliers = []

    def sort_suppliers(self):
        """sort_suppliers() will sort the attribute suppliers by their quantity in stock,
        then the price of the part.

        If there are multiple suppliers which have more stock than the desired quantity,
        it will favour the cheaper supplier.

        If there are no suppliers with enough stock,
        it will sort by the best wait times, then price.

        If the user's favourite suppliers have enough stock,
        they are pushed to the front of the list.
        """
        if (len(self.suppliers)) == 0:
            return

        suppliers = [supplier for supplier in self.suppliers if (supplier.stock > self.quantity) and supplier.price]

        for supplier in suppliers:
            print(supplier.price_dict)
            for key in supplier.price_dict:
                print(supplier.price_dict[key])
                if self.quantity >= key:
                    supplier.price = supplier.price_dict[key]
                    break
            if supplier.price == -1:
                suppliers.remove(supplier)

        self.suppliers = sorted(suppliers, key=lambda supplier: supplier.price, reverse=True)

    def find_combination(self):
        """This method is called if there are no suppliers which have enough stock.
        It will then attempt to combine suppliers together to create the desired quantity.

        :returns: A list containing the combined suppliers if it is possible, None if it is not
        :rtype: list, None
        """


class Supplier:  # pylint: disable=too-few-public-methods
    """The Supplier object represents each supplier which has been searched for each Part.

    This object stores the information regarding the supplier,
    such as its name, link, as well as stock, price and wait times.

    :param name: name is used to store the name of the supplier.
    :type name: str

    :ivar name: This is where the supplier name is stored.
    :type name: str
    :ivar link: This is where the supplier's webpage link is stored.
    :type link: str
    :ivar stock: This is where the supplier's quantity of stock is stored.
    :type stock: int
    :ivar price: This is where the price of the part is stored.
    :type price: float
    :ivar wait_time: This is where the wait time until there is more stock is stored.
    :type wait_time: datetime
    """

    def __init__(self, name, stock, price=-1, price_dict={}):
        self.name = name
        self.link = ""
        self.stock = stock
        self.price = price
        self.price_dict = price_dict
        self.wait_time = None

    def __repr__(self):
        return self.name
