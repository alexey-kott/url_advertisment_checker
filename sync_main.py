import re
from time import sleep
from typing import List

from bs4 import BeautifulSoup
from pandas import DataFrame, read_excel
import requests as req


def get_urls(file_name: str):
    with open(file_name, 'rb') as excel_file:
        return read_excel(excel_file, header=None)


def get_tic(url):
    response = req.get(f"https://webmaster.yandex.ru/tic/{url}")
    soup = BeautifulSoup(response.text, "lxml")
    try:
        tic_text = soup.find_all(class_="tic__text")[0].text
    except IndexError:
        print(f"ТИЦ error: {url}")
        return 0

    return int(tic_text.split(' ')[-1])


def get_theme(url: str):
    megaindex_url = f'https://ru.megaindex.com/a/tcategories?domain={url}'

    response = req.get(f'https://api.proxycrawl.com/?token=jbzJeTVyoiUlgSKZsyO3eQ&url={megaindex_url}')
    soup = BeautifulSoup(response.text, "lxml")

    with open("response.html", "w") as file:
        file.write(response.text)

    lines = soup.findAll(class_="line")
    words = set()
    for line in lines:
        try:
            themes = line.findAll("a", class_='')[0]
            words = words.union(set(themes.text.split('/')))
        except IndexError:
            pass

    return "/".join(words)


def get_info(url):

    print(url)
    tic = get_tic(url)
    themes = get_theme(url)

    with open("data.csv", "a") as file:
        file.write(f"{url}; {tic}; {themes}\n")

    return tic, themes


def get_parsed_urls():
    with open("data.csv") as file:
        return {line.split(';')[0] for line in file.readlines()}


def main(urls: DataFrame):

    for index, row in urls.iterrows():
        url = re.sub(r'http(s)?://', '', row[0])

        if url in urls:
            continue

        tic, themes = get_info(url)

        sleep(2)


if __name__ == "__main__":
    parsed_urls = get_parsed_urls()

    urls = get_urls("./web.xlsx")
    main(urls)

