import asyncio
import json
from functools import reduce
from itertools import chain
from operator import truediv
from pathlib import Path

import aiofiles
import aiohttp

from config import config


def get_relative_paths(obj, acc=None):
    acc = [] if acc is None else acc
    return chain.from_iterable(
        [
            get_relative_paths(v, acc + [k])
            if not isinstance(v, str)
            else [[*acc, k, v]]
            for k, v in obj.items()
        ]
    )


def get_full_file_path(fragments, root='.'):
    return reduce(truediv, fragments, Path(root)).resolve()


def get_url(fragments, base_url):
    return '/'.join([base_url, *fragments])


async def get_file(path, session, main_url, output_dir):
    url = get_url(path, main_url)
    file_path = get_full_file_path(path, output_dir)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)

    async with session.get(url) as response:
        content = await response.read()

    async with aiofiles.open(file_path, 'ab') as f:
        await f.write(content)


async def run():
    async with aiofiles.open(config['schema_file'], 'r') as f:
        schemas = await f.read()

    schemas = json.loads(schemas)

    paths = get_relative_paths(schemas)

    async with aiohttp.ClientSession() as session:
        for f in asyncio.as_completed(
            [
                get_file(path, session, config['main_url'], config['output_dir'])
                for path in paths
            ]
        ):
            await f


def main():
    asyncio.run(run())


if __name__ == '__main__':
    main()
