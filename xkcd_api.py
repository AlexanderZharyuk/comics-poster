import os

from urllib.parse import urlparse

import requests


def get_random_comic(comic_number: int) -> dict:
    url = f'https://xkcd.com/{comic_number}/info.0.json'

    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()

    return service_response


def get_comic_url(service_response: dict) -> str:
    comic_url = service_response['img']

    return comic_url


def get_comic_extension(service_response: dict) -> str:
    comic_url = service_response['img']
    comic_path = urlparse(url=comic_url).path

    return os.path.splitext(comic_path)[-1]


def get_comic_filename(service_response: dict) -> str:
    comic_name = service_response['title']
    comic_extension = get_comic_extension(service_response=service_response)
    filename = f'{comic_name}{comic_extension}'

    return filename


def get_author_comment(service_response: dict) -> str:
    author_comment = service_response['alt']

    return author_comment


def download_comic(service_response: dict) -> None:
    comic_url = get_comic_url(service_response=service_response)

    response = requests.get(url=comic_url)
    response.raise_for_status()

    comic = response.content
    comic_name = get_comic_filename(service_response=service_response)

    with open(comic_name, 'wb') as comics_file:
        comics_file.write(comic)
