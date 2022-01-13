import scrapy
from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def v1():
    # Input for testing
    part_name = input('PART NAME: ')
    url = "https://www.findchips.com/search/" + part_name
    # Locates url, if it doesnt exist, error will be returned
    page = requests.get(url)

    soup = BeautifulSoup(page.text, 'lxml')
    # loop to scrape each table on the website
    for x in range(8):
        # selects the table with the xth index
        table_body = soup.select('table')[x]
        row_data = []
        # tr = table row element
        for row in table_body.find_all('tr'):
            # td = table data cell
            col = row.find_all('td')
            # stripping the data of blank spaces and excess
            col = [ele.text.strip() for ele in col]
            row_data.append(col)
        # adding the list to a dataframe, data becomes easier to manipulate
        df = pd.DataFrame(row_data)
        # mode 'a' doesnt overwrite previous searches
        df.to_csv('test.csv', mode='a')

# useful tester for counting tables 
def table_count():
    # useful when trying to figure out how many times to loop the scraper
    executable = r"C:\Users\roryf\Desktop\chromedriver.exe"
    options = Options()
    # headless = no open browser
    options.headless = True
    driver = webdriver.Chrome(executable, options=options)
    driver.get('https://octopart.com/search?q=AT0603FRE0747KL')
    # finds table by using its tag
    t = driver.find_elements_by_tag_name("table")
    print(len(t))
