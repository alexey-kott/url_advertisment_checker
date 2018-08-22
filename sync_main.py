import re
from time import sleep
from typing import List

from bs4 import BeautifulSoup
from pandas import DataFrame, read_excel
import requests as req
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


def get_driver() -> Chrome:
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")

    return Chrome("./webdriver/chromedriver", chrome_options=options)


def get_urls(file_name: str):
    with open(file_name, 'rb') as excel_file:
        return read_excel(excel_file, header=None)


def get_tic(url):
    response = req.get(f"https://webmaster.yandex.ru/tic/{url}")
    soup = BeautifulSoup(response.text, "lxml")
    tic_text = soup.find_all(class_="tic__text")[0].text

    return int(tic_text.split(' ')[-1])


def get_rank(driver, url):
    driver.get(f"https://a.pr-cy.ru/{url}")
    sleep(2)
    driver.find_element_by_tag_name("body").send_keys(Keys.ESCAPE)
    sleep(1)
    ya_rank = re.findall(r'\d+ из \d+', driver.page_source)
    print(ya_rank)


def get_theme(driver: Chrome, url: str):
    driver.get(f"https://ru.megaindex.com/a/tcategories?domain={url}")
    soup = BeautifulSoup(driver.page_source)
    themes = re.findall(r'Тематика', soup.text)
    print(themes)

def get_info(driver, url):
    url = re.sub(r'http(s)?://', '', url)
    tic = get_tic(url)
    # rank = get_rank(driver, url)
    theme = get_theme(driver, url)




def main(driver: Chrome, urls: DataFrame):
    for index, row in urls.iterrows():
        url = row[0]
        url_info = get_info(driver, url)
        sleep(2)



if __name__ == "__main__":
    chrome_driver = get_driver()
    urls = get_urls("./web.xlsx")
    main(chrome_driver, urls)

