import os
import re


def find_comic_in_folder() -> str:
    files_in_folder = os.listdir('.')
    for file in files_in_folder:
        if re.search('.png', file) or re.search('.jpg', file):
            return file


def delete_comic_from_folder() -> None:
    comic = find_comic_in_folder()
    os.remove(f'{comic}')
