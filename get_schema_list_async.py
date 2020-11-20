import asyncio
import json

import aiofiles
import aiohttp

from config import config
from utils import async_callback


async def crawl(session, url):
    async with session.get(url) as response:
        content = await response.json()

    if (file := get_schema_file(content)) :
        return file[0]

    results = {}
    for f in asyncio.as_completed(
        [
            async_callback(
                crawl(session, f"{url}/{x}"), (lambda x: (lambda f: (x, f)))(x)
            )
            for x in get_directories(content)
        ]
    ):
        k, v = await f
        results[k] = v

    return results


def get_directories(directory):
    return [x['name'] for x in directory if x['type'] == 'directory']


def get_schema_file(directory):
    return [
        x['name']
        for x in directory
        if x['type'] == 'file' and x['name'] == 'current.yaml'
    ]


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        schemas = await crawl(session, url)

    return schemas


async def main():
    schemas = await fetch(config['main_url'])

    async with aiofiles.open(config['schema_file'], 'w') as f:
        await f.write(json.dumps(schemas))


if __name__ == '__main__':
    asyncio.run(main())
