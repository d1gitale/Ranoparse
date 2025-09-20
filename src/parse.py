import logging
from io import BytesIO

import aiofiles
import aiohttp
from aiohttp.web import HTTPException
from bs4 import BeautifulSoup
from PIL import Image


API_ROUTE = "https://ranobehub.org/api/media/"
IMAGES_SAVE_PATH = "images/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"


async def parse_chapter(link: str, session: aiohttp.ClientSession) -> str:
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        content = soup.select(
            "div.ui.text.container[data-container] > *", 
        )
        chapter_content = ""
        for child in content:
            if child.name == "p":
                if (img := child.find("img")) is not None:
                    img_id: str = img.get("data-media-id") # type: ignore
                    await download_image(session, API_ROUTE + img_id, IMAGES_SAVE_PATH + img_id + ".jpg")
                    img["src"] = IMAGES_SAVE_PATH + img_id + ".jpg" # type: ignore
                    del img["data-media-id"] # type: ignore
                    chapter_content += str(img).strip()
                else:
                    chapter_content += str(child).strip()
            elif child.name == "h3":
                chapter_content += str(child).strip()

        return chapter_content


async def parse_chapter_title(link: str, session: aiohttp.ClientSession) -> str:
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        title = soup.find(
            "h1", 
            class_=["ui", "header"],
            attrs={"data-id": True, "data-url": True}
        )
        if title is None:
            return "None"
        return title.text


async def parse_tome_title(link: str, session: aiohttp.ClientSession) -> str:
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        title = soup.find_all("span", attrs={"itemprop": "name"})[-1]
        return title.text


async def parse_ranobe_title(link: str, session: aiohttp.ClientSession) -> str:
    async with session.get(link) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")
        title = soup.select_one("h1.ui.huge.header")
        if title is not None:
            return title.text
        else:
            return "None"


async def download_image(session: aiohttp.ClientSession, img_url: str, save_path: str):
    try:
        async with session.get(img_url, headers={"User-Agent": USER_AGENT}) as response:
            if response.status == 200:
                with Image.open(BytesIO(await response.read())) as img:
                    if img.mode in ('RGBA', 'LA', 'P'):
                        rgb_img = img.convert('RGB')
                    else:
                        rgb_img = img

                    jpg_buf = BytesIO()
                    rgb_img.save(jpg_buf, "JPEG", quality=85)

                    async with aiofiles.open(save_path, "wb") as img:
                        await img.write(jpg_buf.getvalue())

                return save_path
    except HTTPException as e:
        logging.error(f"{img_url}: {e}")
    return None