import os
import random

import requests

from dotenv import load_dotenv

from vk_api import (get_url_for_comic_upload, upload_comic_to_server,
                    save_comic_to_server, post_comic_on_wall)
from xkcd_api import get_random_comic, download_comic, get_author_comment


def main() -> None:
    load_dotenv()
    access_token = os.environ['ACCESS_TOKEN']
    vk_group_id = os.environ['GROUP_ID']

    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url=url)
    response.raise_for_status()
    service_response = response.json()
    comics_summary = service_response['num']
    random_comic_id = random.randint(1, comics_summary)

    service_response = get_random_comic(comic_number=random_comic_id)
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
