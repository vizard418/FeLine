#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.local import Local
from lib.gemini import Gemini
from lib.models import Models
from lib.cmdparser import Cmdparser

from typing import Union
from typing import Generator
from typing import Optional

class Engine:
    def __init__(self):
        self.local = Local()
        self.client = Gemini()
        self.cmdparser = Cmdparser()


    def application_setup(self) ->Union[bool, Exception]:
        """
        Performs essential application setup.
        Returns:
            True if all setup steps succeed, the Exception object otherwise.
        """
        try:
            self.local.setup_dirs()
            return True

        except Exception as e:
            return e


    def application_clear(self) ->Union[bool, Exception]:
        """
        Performs application cleanup, including clearing input history.
        Exits the application immediately if a critical exception occurs during cleanup.
        """
        try:
            self.local.clear_input_hist()
            return True

        except Exception as e:
            return e


    def get_hist_path(self) ->str:
        """
        Retrieves the file path for the input history persistence.
        Returns:
            str: The full path to the input history file.
        """
        return self.local.get_hist_path()


    def get_shell_commands(self, chat_text:str) ->Generator[str, None, None]:
        """
        Parses user input for shell commands and yields them.
        The generator separates and yields commands found using cmdparser.
        Args:
            chat_text (str): The input text string potentially containing
                shell commands.
        Yields:
            str: A single command extracted from the user input.
        """
        commands = self.cmdparser.getcmd(chat_text)

        for i in commands:
            yield i


    def get_image_file(self, chat_text:str) ->Union[str, Exception]:
        """
        Extracts the path or URL of an image file from the user input.
        Returns:
            str: The image file path/URL, or an empty string if not found.
        """
        try:
            image_file = self.cmdparser.getimg(chat_text)
            return image_file
        except Exception as e:
            return e

    def get_response(self, contents: iter):
        """
        Retrieves the streaming response from the chat client.
        Raises:
            Exception: If an error occurs during the stream creation.
        """
        response = self.client.get_chat_stream(contents)
        return response


    def set_model(self, kw_model:str) ->bool:
        model = Models.availables.get(kw_model)

        if model:
            self.client.model = model
            return True
        else:
            return False
