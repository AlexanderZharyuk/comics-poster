import os

from typing import NamedTuple
from urllib.parse import urlparse

import requests

from dotenv import load_dotenv


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


def get_url_for_comic_upload(group_id: str, vk_token: str) -> str:
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    api_version = 5.131
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': api_version
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    api_response = response.json()

    return api_response['response']['upload_url']


class UploadComicResponse(NamedTuple):
    server: str
    photo: str
    hash: str


def upload_comic_to_server(group_id: str, vk_token: str,
                           upload_url: str) -> UploadComicResponse:
    api_version = 5.131
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': api_version
    }

    files_in_folder = os.listdir('.')
    for file in files_in_folder:
        if file.index('.png'):
            comic = file
            break

    with open(comic, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(url=upload_url, files=files, params=params)
        response.raise_for_status()
        api_response = response.json()

        server = api_response['server']
        photo = api_response['photo']
        hash = api_response['hash']

        return UploadComicResponse(server=server, photo=photo, hash=hash)


def save_comic_to_server(group_id: str, vk_token: str, photo: str,
                         server: str, hash: str) -> str:
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    api_version = 5.131
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'v': api_version
    }

    response = requests.post(url=url, params=params)
    response.raise_for_status()
    api_response = response.json()

    owner_id = api_response['response'][0]['owner_id']
    media_id = api_response['response'][0]['id']

    attachment = f'photo{owner_id}_{media_id}'

    return attachment


def post_comic_on_wall(group_id: str, vk_token: str, message: str,
                       attachments: str) -> None:
    url = 'https://api.vk.com/method/wall.post'
    api_version = 5.131
    params = {
        'access_token': vk_token,
        'message': message,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': attachments,
        'v': api_version
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()


def main() -> None:
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']
    vk_group_id = os.environ['GROUP_ID']

    url = 'https://xkcd.com/353/info.0.json'
    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()

    download_comic(service_response=service_response)
    comment_by_author = get_author_comment(service_response=service_response)

    upload_url = get_url_for_comic_upload(
        group_id=vk_group_id,
        vk_token=access_token
    )
    upload_response = upload_comic_to_server(
        group_id=vk_group_id,
        vk_token=access_token,
        upload_url=upload_url
    )
    attachment = save_comic_to_server(
        group_id=vk_group_id,
        vk_token=access_token,
        server=upload_response.server,
        photo=upload_response.photo,
        hash=upload_response.hash
    )
    post_comic_on_wall(
        group_id=vk_group_id,
        vk_token=access_token,
        message=comment_by_author,
        attachments=attachment
    )


if __name__ == '__main__':
    main()
