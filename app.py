import sys
import aiohttp
import asyncio
import logging

from src.parse import parse


BASE_URL = "https://ranobehub.org/ranobe/"


async def make_tome(link, session):
    pass


async def make_chapter(link, session):
    pass


async def ping(link, session: aiohttp.ClientSession):
    async with session.get(link) as resp:
        return resp


async def main(ranobe_id: str):
    ranobe_link = BASE_URL + ranobe_id + "/"
    async with aiohttp.ClientSession() as session:
        tasks = []
        count = 1

        while (resp := await ping(ranobe_link + str(count) + "/1", session)).status != 404:
            tome_link = ranobe_link + str(count) + "/" 
            count += 1
            if 300 < resp.status < 500:
                logging.warning(f" {tome_link} - {resp.status}: {resp.reason}")
                exit(2)
                
            tasks.append(make_tome(tome_link, session))
            print(tome_link)

        if not tasks:
            logging.error("Сервер недоступен")
            exit(3)

        await asyncio.gather(*tasks)


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
