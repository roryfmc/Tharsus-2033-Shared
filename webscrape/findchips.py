"""This module is used to scrape findchips.com for the desired parts"""
import requests
from bs4 import BeautifulSoup
from search_function.objects import Supplier
from webscrape.scrape_objects import Scrape


def search_for_parts(search_object):
    """This function is called when the user wishes to search for parts.
    It creates the relevant webpage for each part and creates a BeautifulSoup.
    This soup is then passed to the Scrape object which parses the page to find the relevant data.

    :param search_object: The Search object which contains all the parts to be searched for
    :return: The Search object containing all the data regarding the suppliers.
    """

    # Loop through the parts in the Search object
    for part in search_object.parts:
        # Create the page URL
        url = "https://www.findchips.com/search/" + part.name + "?currency=GBP"
        # Return the page
        page = requests.get(url)

        # Create the soup
        soup = BeautifulSoup(page.text, 'lxml')
        # Create the Scrape object
        scrape = Scrape(soup)

        # For each distributor on the page
        for distributor in scrape.distributors:
            # Get their name
            supplier_name = distributor.get_supplier_name()

            # For each part supplied by the distributor
            for tr in distributor.table.TRs: # pylint: disable=invalid-name
                # Create a supplier object
                supplier = Supplier(name=supplier_name, stock=tr.get_stock(),
                                    price_dict=tr.get_price(), link=tr.get_link())
                # Add it to the part's list of suppliers
                part.suppliers.append(supplier)

    return search_object
