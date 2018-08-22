import asyncio
import re
from pathlib import Path
from typing import Union
from time import sleep

import pandas as pd
from aiohttp import ClientSession
from bs4 import BeautifulSoup


def get_urls(file_name: Union[Path, str]):
    with open(file_name, 'rb') as excel_file:
        return pd.read_excel(excel_file, header=None)


async def get_tic(session: ClientSession, url: str):
    url = re.sub(r'http(s)?://', '', url)
    async with session.get(f"https://webmaster.yandex.ru/tic/{url}") as response:
        page_source = await response.text()
        soup = BeautifulSoup(page_source, "lxml")
        tic_text = soup.find_all(class_="tic__text")[0].text
        return int(tic_text.split(' ')[-1])


async def get_rank(session: ClientSession, url: str):
    url = re.sub(r'http(s)?://', '', url)
    async with session.get(f"https://a.pr-cy.ru/{url}") as response:
        page_source = await response.text()
        soup = BeautifulSoup(page_source, "lxml")
        print(url)
        ya_rank = re.findall(r'\d+ из \d+', soup.text)
        print(ya_rank)
        # print(soup.text.find("Яндекс Rank"), end='\n\n')


async def get_info(session: ClientSession, url: str):
    tic = await get_tic(session, url)
    await get_rank(session, url)


async def main(excel_file_name):
    async with ClientSession() as session:
        url_list = get_urls(excel_file_name)

        for index, row in url_list.iterrows():
            url = row[0]
            url_info = await get_info(session, url)
            sleep(2)


if __name__ == "__main__":
    asyncio.run(main("./web.xlsx"))

