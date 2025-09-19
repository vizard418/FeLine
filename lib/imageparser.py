#!/usr/bin/env python3
# coding: utf-8 -*-

from PIL import Image
from requests import get as r_get
from urllib.parse import urlparse
from io import BytesIO


class ImageParser():
    def __init__(self):
        self.image_data = None

    def image_resolve(self, source:str) ->None:
        if urlparse(source).scheme:
            request = r_get(source)
            self.image_data = Image.open(BytesIO(request.content))

        else:
            self.image_data = Image.open(source)

