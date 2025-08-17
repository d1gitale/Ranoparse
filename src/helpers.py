import logging

import aiohttp
from aiohttp.web import HTTPException
from ebooklib.epub import EpubBook

from src.parse import *


async def make_tome(link: str, session: aiohttp.ClientSession) -> EpubBook:
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
            offset += 1
            cur_chapter_link = link + str(offset)
            resp = await ping(cur_chapter_link, session)
    except HTTPException as e:
        logging.error(e)

    tome_title = await parse_tome_title(link + str(offset-1), session)

    return EpubBook()


async def make_chapter(link: str, session: aiohttp.ClientSession):
    # TODO: make chapter in epub
    chapter_text = await parse_chapter(link, session)
    chapter_title = await parse_chapter_title(link, session)


async def ping(link: str, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
    async with session.get(link) as resp:
        return resp