"""This module contains the classes Search, Part and Supplier.
These are used as data structures for the search functionality.

 The search class is used to represent a search made by the user on the application.
 This contains Part objects which represent each part the user is searching for,
 and contain all the data about the part. It also contains Supplier objects,
 which store the data on each supplier that has been searched for the part.
 """


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
        """sort_suppliers() will sort the attribute suppliers so that only suppliers
        with enough stock are kept. THey are then sorted by price.

        The user's blacklisted suppliers are also removed.
        """
        # Return if the part has no suppliers
        if (len(self.suppliers)) == 0:
            return

        from users.views import get_blacklisted_suppliers
        blacklisted_suppliers = get_blacklisted_suppliers()

        # Sorts supplier list so that it only contains suppliers with enough stock and a price
        suppliers = [supplier for supplier in self.suppliers
                     if (supplier.stock > self.quantity)
                     and supplier.price
                     and supplier.name not in blacklisted_suppliers]

        suppliers_with_price = []

        for supplier in suppliers:
            # For each stock starting with the biggest
            for stock in supplier.price_dict:
                # If the desired quantity is bigger than the chosen stock
                if self.quantity >= stock:
                    # This would be the price of the stock therefore set the price
                    supplier.price = supplier.price_dict[stock]
                    break
            # If the price is -1 (default value)
            if supplier.price != -1:
                suppliers_with_price.append(supplier)

        # Sort the suppliers by price (lowest first)
        self.suppliers = sorted(suppliers_with_price,
                                key=lambda supplier: supplier.price)


class Supplier:  # pylint: disable=too-few-public-methods
    """The Supplier object represents each supplier which has been searched for each Part.

    This object stores the information regarding the supplier,
    such as its name, link, as well as stock, price and wait times.

    :param name: name is used to store the name of the supplier.
    :type name: str

    :ivar name: This is where the supplier name is stored.
    :type name: str
    :ivar stock: This is where the supplier's quantity of stock is stored.
    :type stock: int
    :ivar price: This is where the price of the part is stored.
    :type price: float
    :ivar price_dict: This is where the initial dictionary of prices is stored.
    :type price_dict: dict
    :ivar link: This is where the supplier's webpage link is stored.
    :type link: str
    """

    def __init__(self, name, stock, price=-1, price_dict=None, link=""): # pylint: disable=too-many-arguments
        self.name = name
        self.link = link
        self.stock = stock
        self.price = price
        self.price_dict = price_dict

    def __repr__(self):
        return self.name
