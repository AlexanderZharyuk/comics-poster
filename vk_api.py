from typing import NamedTuple

import requests

from general_functions import find_comic_in_folder


API_VERSION = 5.131


class UploadComicResponse(NamedTuple):
    server: str
    photo: str
    hash: str


def get_url_for_comic_upload(group_id: str, vk_token: str) -> str:
    """
    Return upload url for upload photos
    """
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': API_VERSION
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    api_response = response.json()

    return api_response['response']['upload_url']


def upload_comic_to_server(group_id: str, vk_token: str,
                           upload_url: str) -> UploadComicResponse:
    """
    Return info about uploaded image.
    Information like hash, server and photo_url
    """
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': API_VERSION
    }

    comic = find_comic_in_folder()
    with open(comic, 'rb') as upload_file:
        files = {
            'photo': upload_file,
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
    """
    Save comic to VK-servers and return attachment for post this comic on wall
    """
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'server': server,
        'photo': photo,
        'hash': hash,
        'v': API_VERSION
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
    """
    Post comic on wall in VK community
    """
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_token,
        'message': message,
        'owner_id': f'-{group_id}',
        'from_group': 1,
        'attachments': attachments,
        'v': API_VERSION
    }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
