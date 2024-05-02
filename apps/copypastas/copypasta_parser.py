from bs4 import BeautifulSoup

import aiohttp
import random


async def random_copypasta() -> str:
    """
    Возвращает рандомную копипасту с сайта copypastas.ru
    """
    async with aiohttp.ClientSession() as session:
        x = True
        while x == True:
            async with session.get(f'https://copypastas.ru/copypasta/{random.randint(1, 10000)}/') as response:
                if response.status != 200:
                    continue

                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                x = False
                return soup.find("div", {"class": "dGiOO"}).text
