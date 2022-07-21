import os

from urllib.parse import urlparse

import requests


def get_service_response(url: str) -> dict:
    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()

    return service_response


def get_comics_url(service_response: dict) -> str:
    comic_url = service_response['img']
    return comic_url


def get_comics_extension(service_response: dict) -> str:
    comic_url = service_response['img']
    comic_path = urlparse(url=comic_url).path

    return os.path.splitext(comic_path)[-1]


def get_comics_filename(service_response: dict) -> str:
    comic_name = service_response['title']
    comic_extension = get_comics_extension(service_response=service_response)
    filename = f'{comic_name}{comic_extension}'

    return filename


def download_comics() -> None:
    download_folder = 'images'
    os.makedirs(download_folder, exist_ok=True)

    url = 'https://xkcd.com/353/info.0.json'
    service_response = get_service_response(url=url)
    comic_url = get_comics_url(service_response=service_response)

    response = requests.get(url=comic_url)
    response.raise_for_status()

    comic = response.content
    comic_name = get_comics_filename(service_response=service_response)
    comic_path = os.path.join(download_folder, comic_name)

    with open(comic_path, 'wb') as comics_file:
        comics_file.write(comic)


if __name__ == '__main__':
    download_comics()
