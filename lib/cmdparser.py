#!/usr/bin/env python3
# coding: utf-8 -*-

from re import findall, split, search
from subprocess import check_output, STDOUT
from PIL import Image
from requests import get as r_get
from urllib.parse import urlparse
from io import BytesIO


class Cmdparser:
    def getcmd(self, text:str) ->list[str]:
        """
        Extracts shell commands enclosed in $() from the input text.
        Chained commands (using &&, ||, or ;) are split into separate strings.
        Args:
            text (str): The raw user input string.
        Returns:
            list[str]: A list of individual shell commands.
        """
        commands = []
        # finds all $(...) blocks in the text
        matches = findall(r'\$\(([^)]*)\)', text)

        # splits chained commands by &&, ; or ||
        for match in matches:
            parts = split(r'\s*(?:&&|\|\||;)\s*', match)
            commands.extend(parts)
        return commands


    def getexpand(self, command: str) ->'Union[str, Exception]':
        """
        Executes a single shell command and returns the stripped output.
        Args:
            command (str): The shell command string to execute.
        Returns:
            str: The output of the executed command.
        """
        try:
            output = check_output(
                command, shell=True, text=True, stderr=STDOUT
            )
            return output.strip()

        except Exception as e:
            return e


    def getimg(self, text:str) -> str:
        """
        Extracts an image file path or URL enclosed in $[] from the input text.
        Args:
            text (str): The raw user input string.
        Returns:
            str: The path/URL, or an empty string if the pattern is not found.
        """
        match = search(r'\$\[([^\]]+)\]', text)
        return match.group(1) if match else ''


    def image_resolve(self, source:str) ->bytes:
        """
        Resolves an image source (URL or local path) into a PIL Image object.
        Args:
            source (str): The image URL or local file path.
        Returns:
            Image.Image: The loaded PIL Image object.
        """
        if urlparse(source).scheme:
            request = r_get(source)
            return Image.open(BytesIO(request.content))
        else:
            return Image.open(source)
