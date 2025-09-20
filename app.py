import sys
import os
import shutil
import asyncio
import logging

import aiohttp
import pypub
from tqdm.asyncio import tqdm_asyncio
from aiohttp.web import HTTPException

from src.helpers import ping, make_tome, IMAGES_SAVE_PATH
from src.parse import parse_ranobe_title


BASE_URL = "https://ranobehub.org/ranobe/"


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

        if not os.path.exists(IMAGES_SAVE_PATH):
            os.mkdir(IMAGES_SAVE_PATH)

        tomes: list[pypub.Epub] = await tqdm_asyncio.gather(
            *tasks, 
            desc="Создание томов📚",
            position=0,
            ascii=" ░▒▓█",
            bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt}"
        )
        ranobe_title = await parse_ranobe_title(ranobe_link, session)
        save_path = f"{open("env.txt").read()}/{ranobe_title}"

        if not os.path.exists(save_path):
            os.mkdir(save_path)

        for tome in tomes:
            tome.create(f"{save_path}/{tome.title}.epub")


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
    
    try:
        asyncio.run(main(ranobe_id))
    finally:
        shutil.rmtree(IMAGES_SAVE_PATH)
