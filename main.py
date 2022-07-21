import os

from urllib.parse import urlparse

import requests


def get_service_response(url: str) -> dict:
    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()

    return service_response


def get_comics_url(service_response: dict) -> str:
    comics_url = service_response['img']
    return comics_url


def get_comics_extension(service_response: dict) -> str:
    comics_url = service_response['img']
    comics_path = urlparse(url=comics_url).path

    return os.path.splitext(comics_path)[-1]


def get_comics_filename(service_response: dict) -> str:
    comics_name = service_response['title']
    comics_extension = get_comics_extension(service_response=service_response)
    filename = f'{comics_name}.{comics_extension}'

    return filename


def download_comics() -> None:
    download_folder = 'images'
    os.makedirs(download_folder, exist_ok=True)

    url = 'https://xkcd.com/353/info.0.json'
    service_response = get_service_response(url=url)
    comics_url = get_comics_url(service_response=service_response)

    response = requests.get(url=comics_url)
    response.raise_for_status()

    comics = response.content
    comics_name = get_comics_filename(service_response=service_response)
    comics_path = os.path.join(download_folder, comics_name)

    with open(comics_path, 'wb') as comics_file:
        comics_file.write(comics)


if __name__ == '__main__':
    download_comics()
