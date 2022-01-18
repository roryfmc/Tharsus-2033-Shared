"""This module stores the classes which are used to parse the information
obtained by the BeautifulSoup scrape. It then retrieves the relevant data."""


class Scrape:
    """This class stores all of the distributors on the webpage.
    This is the class which is called when webscraping, in order to parse
    all of the relevant information.
    """
    def __init__(self, soup):
        self.soup = soup
        self.distributors = []

        # Find all distributors on the page
        distributor_list = self.soup.find_all(class_="distributor-results")

        for distributor_element in distributor_list:
            # Create a Distributor object for each distributor
            distributor = Distributor(distributor_element)
            self.distributors.append(distributor)


class Distributor:
    """This class represents each distributor on the webpage.
    It stores the table element, which each distributor has, as a Table object.
    It also has the function to return the supplier's name.
    """
    def __init__(self, element):
        self.element = element

        # Find table within distributor
        tables_element = self.element.find("table")
        self.table = Table(tables_element)

    def get_supplier_name(self):
        """This function returns the name of the supplier"""
        return self.element["data-distributor_name"]


class Table:
    """This class represents each table on the webpage.
    It stores all of the table row elements as Tr objects.
    """
    def __init__(self, element):
        self.element = element
        self.TRs = []  # pylint: disable=invalid-name

        # Find all tr tags within the table
        tr_list = self.element.find("tbody").findAll("tr")

        for tr_element in tr_list:
            tr_tag = Tr(tr_element)
            self.TRs.append(tr_tag)


class Tr:
    """This class represents each table row element on the webpage.
    It has the functions to get the stock of the part for each supplier,
    as well as the price and also the link to the part's webpage.
    """
    def __init__(self, element):
        self.element = element
        self.TDs = self.element.findAll("td")  # pylint: disable=invalid-name

    def get_stock(self):
        """This function gets the stock of the part for this specific supplier.

        :return: The supplier's stock of the part
        """
        # The characters to be removed from the text
        disallowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n -"

        # Grab the td tag storing the stock value
        element = self.element.find(class_="td-stock")
        # Strip the text of disallowed characters
        text = element.text.strip(disallowed_characters)

        # Try to return the text as an integer
        try:
            return int(text)
        # If it fails it means that there is no stock within the text and therefore the stock is 0
        except ValueError:
            return 0

    def get_price(self):
        """This function gets the price of the stock for this specific supplier.

        :return: The price of the stock for the supplier.
        """
        # Find the td tag storing the price value
        element = self.element.find(class_="td-price")
        text = element.text

        dictionary = {}
        # For each line in the price text
        # Each line of the price is formatted as "{STOCK} {PRICE}\n"
        for line in text.split('\n'):
            # Try to split it by the space in the middle
            try:
                (count, price) = line.split(' ')
                # First half of the line is the stock and second half is the price
                dictionary[int(count)] = float(price[1:])
            # If that doesn't work then you have either reached the end or the prices are not listed
            except ValueError:
                continue

        return dictionary

    def get_link(self):
        """This function gets the supplier's link for the part.

        :return: The link for the part
        """
        return self.element.find("a")['href']
