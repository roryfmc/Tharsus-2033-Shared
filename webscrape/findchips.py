from bs4 import BeautifulSoup
import requests
from scrape_objects import Scrape


def v1(part_name="AT0603FRE0747KL"):
    url = "https://www.findchips.com/search/" + part_name + "?currency=GBP"
    # Locates url, if it doesnt exist, error will be returned
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    scrape = Scrape(soup)

    for distributor in scrape.distributors:
        print(distributor.get_supplier_name())
        print()
        for tr in distributor.table.TRs:
            print(tr.get_stock())
            print(tr.get_price())
            print()
        print("-----------------")


v1()