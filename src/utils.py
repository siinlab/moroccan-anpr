import os
from enum import Enum
from os.path import dirname, join

from PIL import Image
from lgg import logger

import requests


UPLOAD_FOLDER = join(dirname(__file__), "uploads")
RESULT_FOLDER = join(dirname(__file__), "results")
DEBUG_FOLDER = join(dirname(__file__), "debug")

class ModelType(str, Enum):
    """ A class to hold the content types. """

    CARS = "cars"
    LICENSE_PLATES = "license_plates"
    LICENSE_PLATE_CHARACTERS = "license_plate_characters"
    ANPR = "anpr"


def save_uploaded_image(file) -> str:
    """ Save the uploaded file inside `uploads` folder.

    Note:
        - `uploads` folder is created if it doesn't exist.

    Args:
        file (UploadFile): The uploaded file.

    Returns:
        str: The path to the saved file.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    path = join(UPLOAD_FOLDER, file.filename)
    contents = file.file.read()
    with open(path, 'wb') as f:
        f.write(contents)

    return path