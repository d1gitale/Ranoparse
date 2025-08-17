import sys
import asyncio
import logging

import aiohttp
from aiohttp.web import HTTPException
from ebooklib.epub import EpubBook

from src.parse import parse


BASE_URL = "https://ranobehub.org/ranobe/"


async def make_tome(link: str, session: aiohttp.ClientSession) -> EpubBook:
    # TODO: make chapters' epub pages
    # TODO: glue epub pages
    # TODO: divide into chapters

    try:
        (await ping(link + "0", session)).raise_for_status()
        offset = 0
    except:
        offset = 1

    cur_chapter_link = link + str(offset)
    resp = await ping(cur_chapter_link, session)
    chapters = []
    try:
        while resp.status != 404:
            resp.raise_for_status()
            cur_chapter = await make_chapter(cur_chapter_link, session)
            chapters.append(cur_chapter)
            print(cur_chapter_link)
            offset += 1
            cur_chapter_link = link + str(offset)
            resp = await ping(cur_chapter_link, session)
    except HTTPException as e:
        logging.error(e)

    return EpubBook()



async def make_chapter(link: str, session: aiohttp.ClientSession):
    # TODO: parse illustrations
    pass


async def ping(link, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
    async with session.get(link) as resp:
        return resp


async def main(ranobe_id: str):
    ranobe_link = BASE_URL + ranobe_id + "/"
    async with aiohttp.ClientSession() as session:
        tasks = []
        count = 1
        resp = await ping(ranobe_link + str(count) + "/1", session)

        try:
            while resp.status != 404:
                resp.raise_for_status()
                tome_link = ranobe_link + str(count) + "/" 
                count += 1
                tasks.append(make_tome(tome_link, session))
                resp = await ping(ranobe_link + str(count) + "/1", session)
        except HTTPException as e:
            logging.error(str(e))
            exit(2)
        
        tomes = await asyncio.gather(*tasks)
        for tome in tomes:
            ...


if __name__ == "__main__":
    if len(sys.argv) != 2:
        logging.error("Использование: uv run app.py {ссылка на главную страницу ранобэ}")
        exit(1)

    ranobe_url = sys.argv[1]
    ranobe_id = ""
    for char in ranobe_url[8:].split("/")[2]:
        if not char.isdigit():
            break
        ranobe_id += char
    
    asyncio.run(main(ranobe_id))
