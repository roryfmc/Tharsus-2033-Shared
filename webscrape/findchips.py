import requests
from bs4 import BeautifulSoup
from search_function.objects import Supplier
from webscrape.scrape_objects import Scrape


def search_for_parts(search_object):

    for part in search_object.parts:
        url = "https://www.findchips.com/search/" + part.name + "?currency=GBP"
        page = requests.get(url)

        soup = BeautifulSoup(page.text, 'lxml')
        scrape = Scrape(soup)

        for distributor in scrape.distributors:
            supplier_name = distributor.get_supplier_name()

            for tr in distributor.table.TRs:
                supplier = Supplier(supplier_name, tr.get_stock(), tr.get_price())
                part.suppliers.append(supplier)

    return search_object
