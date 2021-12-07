from bs4 import BeautifulSoup
import requests
import pandas as pd


def stock():
    stock = []
    url = 'https://www.findchips.com/detail/MPTC-02-80-02-6.30-01-L-V-LC/2373-Samtec%20Inc?quantity=1'
    r = requests.get(url)
    url = r.content
    soup = BeautifulSoup(url, 'html.parser')
    for name in soup.find_all("td", {"class": "td-col-2"}):
        stock.append(name)
    print(stock)

def prices():
    prices = []
    url = 'https://www.findchips.com/detail/MPTC-02-80-02-6.30-01-L-V-LC/2373-Samtec%20Inc?quantity=1'
    r = requests.get(url)
    url = r.content
    soup = BeautifulSoup(url, 'html.parser')
    for price in soup.find_all("td", {"class": "td-col-5"}):
        prices.append(price)


def package_type():
    type = []
    url = 'https://www.findchips.com/detail/MPTC-02-80-02-6.30-01-L-V-LC/2373-Samtec%20Inc?quantity=1'
    r = requests.get(url)
    url = r.content
    soup = BeautifulSoup(url, 'html.parser')
    for package in soup.find_all("td", {"class": "td-col-4"}):
        type.append(package)
    print(type)


if __name__ == '__main__':
    stock()

