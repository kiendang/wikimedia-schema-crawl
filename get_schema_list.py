import json
from pathlib import Path

import requests

from config import config


def crawl(session, url):
    content = session.get(url).json()

    return (
        file[0]
        if (file := get_schema_file(content))
        else {x: crawl(session, f"{url}/{x}") for x in get_directories(content)}
    )


def get_directories(directory):
    return [x['name'] for x in directory if x['type'] == 'directory']


def get_schema_file(directory):
    return [
        x['name']
        for x in directory
        if x['type'] == 'file' and x['name'] == 'current.yaml'
    ]


def fetch(url):
    with requests.Session() as session:
        schemas = crawl(session, url)

    return schemas


def main():
    schemas = fetch(config['main_url'])
    Path(config['schema_file']).write_text(json.dumps(schemas))


if __name__ == '__main__':
    main()
