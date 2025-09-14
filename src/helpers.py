import logging
import aiofiles

import aiohttp
from aiohttp.web import HTTPException
from ebooklib.epub import EpubBook, EpubHtml, EpubImage, EpubNcx
from tqdm.asyncio import tqdm_asyncio

from src.parse import *


async def make_tome(link: str, session: aiohttp.ClientSession) -> EpubBook:
    try:
        (await ping(link + "0", session)).raise_for_status()
        offset = 0
    except:
        offset = 1

    cur_chapter_link = link + str(offset)
    resp = await ping(cur_chapter_link, session)
    tasks = []
    tome_epub = EpubBook()
    tome_epub.spine = ["ncx"]

    try:
        while resp.status != 404:
            resp.raise_for_status()
            cur_chapter = make_chapter(tome_epub, cur_chapter_link, session)
            tasks.append(cur_chapter)
            offset += 1
            cur_chapter_link = link + str(offset)
            resp = await ping(cur_chapter_link, session)
    except HTTPException as e:
        logging.error(e)
    
    tome_num = int(link.split("/")[-2])
    tome_title = await parse_tome_title(link + str(offset-1), session)

    tome_epub.set_identifier(str(tome_num))
    tome_epub.set_title(tome_title)
    tome_epub.set_language("ru")
    tome_epub.add_author("Ranoparse")

    chapters: list[EpubHtml] = await tqdm_asyncio.gather(
        *tasks, 
        desc=f"Том №{tome_num}📖",
        leave=False,
        position=tome_num,
        ascii=" ░▒▓█",
        bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
    ) # type: ignore
    
    for chapter in chapters:
        tome_epub.add_item(chapter)
        tome_epub.toc.append(chapter)
        tome_epub.spine.append(chapter) # type: ignore

    tome_epub.add_item(EpubNcx(uid='ncx', file_name='toc.ncx'))

    return tome_epub


async def make_chapter(tome: EpubBook, link: str, session: aiohttp.ClientSession) -> EpubHtml:
    chapter_text, img_ids = await parse_chapter(link, session)
    chapter_title = await parse_chapter_title(link, session)

    chapter_epub = EpubHtml(
        title=chapter_title,
        file_name=f"{chapter_title}.html",
        lang="ru"
    )
    chapter_epub.set_content(chapter_text)

    for img_id in img_ids:
        async with aiofiles.open(IMAGES_SAVE_PATH + img_id + ".jpg", "rb") as img:
            img_item = EpubImage(
                file_name=IMAGES_SAVE_PATH + img_id + ".jpg",
                media_type="image/jpeg",
                content=await img.read()
            )
            tome.add_item(img_item)

    return chapter_epub


async def ping(link: str, session: aiohttp.ClientSession) -> aiohttp.ClientResponse:
    async with session.get(link) as resp:
        return resp
