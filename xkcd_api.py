import os

from typing import NamedTuple
from urllib.parse import urlparse

import requests


class RandomComic(NamedTuple):
    comic_title: str
    comic_url: str
    comment_by_author: str


def get_comic_extension(comic_url: str) -> str:
    """
    Return comic extension
    """
    comic_path = urlparse(url=comic_url).path

    return os.path.splitext(comic_path)[-1]


def get_comic_filename(comic_name: str, comic_url: str) -> str:
    """
    Return comic filename. For example: comic.png
    """
    comic_extension = get_comic_extension(comic_url=comic_url)
    filename = f'{comic_name}{comic_extension}'

    return filename


def get_random_comic(comic_number: int) -> RandomComic:
    """
    Get random comic from xkcd-API
    """
    url = f'https://xkcd.com/{comic_number}/info.0.json'

    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()

    comic_name = service_response['title']
    comic_url = service_response['img']
    comment_by_author = service_response['alt']

    return RandomComic(
        comic_title=comic_name,
        comic_url=comic_url,
        comment_by_author=comment_by_author
    )


def download_comic(comic_url: str, comic_name: str) -> None:
    """
    Download comic to folder
    """
    response = requests.get(url=comic_url)
    response.raise_for_status()

    comic = response.content
    comic_filename = get_comic_filename(
        comic_name=comic_name,
        comic_url=comic_url
    )

    with open(comic_filename, 'wb') as comics_file:
        comics_file.write(comic)
