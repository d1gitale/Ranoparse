import aiohttp
from bs4 import BeautifulSoup

async def parse_chapter(link: str, session: aiohttp.ClientSession):
    # TODO: parse chapter text
    # TODO: parse illustrations
    pass


async def parse_chapter_title(link: str, session: aiohttp.ClientSession):
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        title = soup.find("h1", class_="header")
        if title is None:
            return "None"
        return title.text


async def parse_tome_title(link: str, session: aiohttp.ClientSession):
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        title = soup.find_all("span", attrs={"itemprop": "name"})[-1]
        return title.text