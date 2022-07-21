import os
import re


def find_comic_in_folder() -> str:
    """
    Find comic in folder. If file exist - return filename
    """
    files_in_folder = os.listdir('.')

    for file in files_in_folder:
        if re.search('.png', file) or re.search('.jpg', file):
            return file


def delete_comic_from_folder() -> None:
    """
    Delete comic from folder
    """
    comic = find_comic_in_folder()
    os.remove(f'{comic}')
