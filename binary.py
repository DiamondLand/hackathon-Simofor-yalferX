from base64 import b16encode as enc64
from base64 import b16decode as dec64
from io import BytesIO
from PIL import Image

import configparser

config = configparser.ConfigParser()
config.read("settings.ini")


async def enc64(photo):
    binary = enc64(photo.read())
    return binary


async def dec64(binary):
    image = BytesIO(dec64(binary))
    pillow = Image.open(image)
    return pillow
