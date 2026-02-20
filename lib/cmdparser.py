#!/usr/bin/env python3
# coding: utf-8 -*-

from re import findall, split, search
from subprocess import check_output, STDOUT
from PIL import Image
from requests import get as r_get
from urllib.parse import urlparse
from io import BytesIO


class Cmdparser:
    """Parse and resolve shell commands and image references in text."""

    def getcmd(self, text:str) ->'Iterator[str]':
        """Extract shell commands in $() blocks and yield individual commands."""
        # finds all $(...) blocks in the text
        matches = findall(r'\$\(([^)]*)\)', text)

        # splits chained commands by &&, ; or ||
        for match in matches:
            parts = split(r'\s*(?:&&|\|\||;)\s*', match)
            yield from parts


    def getexpand(self, command: str) ->'Union[str, Exception]':
        """Execute a shell command and return stripped output or Exception."""
        try:
            output = check_output(
                command, shell=True, text=True, stderr=STDOUT
            )
            return output.strip()

        except Exception as e:
            return e


    def getimg(self, text:str) -> 'Optional[str]':
        """Extract image path or URL in $[] from text;
        return empty string if none."""
        match = search(r'\$\[([^\]]+)\]', text)
        return match.group(1) if match else None


    def image_resolve(self, source:str) ->'PIL.Image.Image':
        """Load an image from URL or local path
        and return a PIL Image object."""
        if urlparse(source).scheme:
            request = r_get(source)
            return Image.open(BytesIO(request.content))
        else:
            return Image.open(source)
