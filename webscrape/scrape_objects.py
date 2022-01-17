class Scrape:

    def __init__(self, soup):
        self.soup = soup
        self.distributors = []

        distributor_list = self.soup.find_all(class_="distributor-results")
        for distributor_element in distributor_list:
            distributor = Distributor(distributor_element)
            self.distributors.append(distributor)


class Distributor:
    def __init__(self, element):
        self.element = element

        tables_element = self.element.find("table")
        self.table = Table(tables_element)

    def get_supplier_name(self):
        return self.element["data-distributor_name"]


class Table:
    def __init__(self, element):
        self.element = element
        self.TRs = []

        tr_list = self.element.find("tbody").findAll("tr")
        for tr_element in tr_list:
            tr = Tr(tr_element)
            self.TRs.append(tr)


class Tr:
    def __init__(self, element):
        self.element = element
        self.TDs = self.element.findAll("td")

    def get_stock(self):
        disallowed_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n -"
        element = self.element.find(class_="td-stock")
        text = element.text.strip(disallowed_characters)
        try:
            return int(text)
        except ValueError:
            return 0

    def get_price(self):
        element = self.element.find(class_="td-price")
        text = element.text

        dict = {}
        for line in text.split('\n'):
            try:
                (count, price) = line.split(' ')
                dict[int(count)] = float(price[1:])
            except ValueError:
                continue

        return dict

    def get_link(self):
        return self.element.find("a")['href']
