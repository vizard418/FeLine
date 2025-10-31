#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pathlib import Path
from sys import platform
from prompt_toolkit.history import FileHistory


class Cache():
    """Handles persistent history storage and platform-specific paths."""

    def __init__(self):
        """Initialize platform and FileHistory instance."""
        self.platform = platform
        self.filehistory = FileHistory(self.get_hist_filepath())

    def get_hist_dir(self) ->Path:
        """Return the directory path for storing history files."""
        # C:\Users\<user>\AppData\Local\FeLine
        if self.platform == "win32":
            relative = Path('AppData') / 'Local'

        # /Users/<user>/Library/Caches/FeLine
        elif self.platform == "darwin":
            relative = Path('Library') / 'Caches'

        # /home/<user>/.cache/FeLine
        elif self.platform == 'linux':
            relative = Path('.cache')

        # Fallback for others: /home/<user>/FeLine
        else:
            relative = Path()

        realdir = Path.home() / relative / 'FeLine'
        return realdir


    def get_hist_filepath(self) ->Path:
        """Return the full file path for the history file."""
        return self.get_hist_dir() / '.chat-history'


    def setup_cache(self) -> 'Union[bool, Exception]':
        """Create the history directory if it does not exist."""
        realdir = self.get_hist_dir()
        # Creates the directory and parents if necessary
        try:
            realdir.mkdir(parents=True, exist_ok=True)
            return True

        except Exception as e:
            return e


    def clear_history(self) -> 'Union[bool, Exception]':
        """Clear the content of the history file."""
        realpath = self.get_hist_filepath()
        try:
            with open(realpath, 'w') as f:
                pass
            return True
        except Exception as e:
            return e


    def append_history(self, message:str) ->'Union[bool, Exception]':
        """Append a message to persistent history; return True or Exception."""
        try:
            self.filehistory.append_string(message)
            return True
        except Exception as e:
            return e
