import logging

import aiohttp
import pypub
from aiohttp.web import HTTPException
from tqdm.asyncio import tqdm_asyncio

from src.parse import *


async def make_tome(link: str, session: aiohttp.ClientSession) -> pypub.Epub:
    try:
        (await ping(link + "0", session)).raise_for_status()
        offset = 0
    except:
        offset = 1

    cur_chapter_link = link + str(offset)
    resp = await ping(cur_chapter_link, session)
    tasks = []

    tome_title = await parse_tome_title(link + str(offset), session)
    tome_epub = pypub.Epub(
        title=tome_title,
        language="ru",
        )

    try:
        while resp.status != 404:
            resp.raise_for_status()
            cur_chapter = make_chapter(cur_chapter_link, session)
            tasks.append(cur_chapter)
            offset += 1
            cur_chapter_link = link + str(offset)
            resp = await ping(cur_chapter_link, session)
    except HTTPException as e:
        logging.error(e)
    
    tome_num = int(link.split("/")[-2])

    chapters: list[pypub.Chapter] = await tqdm_asyncio.gather(
        *tasks, 
        desc=f"Том №{tome_num}📖",
        leave=False,
        position=tome_num,
        ascii=" ░▒▓█",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
    ) # type: ignore
    
    for chapter in chapters:
        tome_epub.add_chapter(chapter)

    return tome_epub


async def make_chapter(link: str, session: aiohttp.ClientSession) -> pypub.Chapter:
    chapter_text = await parse_chapter(link, session)
    chapter_title = await parse_chapter_title(link, session)

    chapter_epub = pypub.create_chapter_from_html(
        html=chapter_text.encode(),
        title=chapter_title,
        url="http://localhost:1488/"
    )

    return chapter_epub


async def ping(link: str, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
    async with session.get(link) as resp:
        return resp
