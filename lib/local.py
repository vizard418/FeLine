#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from pathlib import Path
from sys import platform

class Local:
    def __init__(self):
        self.app_name = 'FeLine'
        self.hist_file = '.history'

    def get_cache_dir(self) ->Path:
        """
        Retrieves the user's cache directory path, adapted for Windows, Linux, and macOS.
        Returns: A Path object representing the cache directory path.
        """

        home_dir = Path.home()

        if platform == "win32":
            cache_path = home_dir / 'AppData' / '.cache' / self.app_name

        elif platform == "darwin":
            cache_path = home_dir / 'Library' / 'Caches' / self.app_name

        else:
            cache_path = home_dir / '.cache' / self.app_name

        return cache_path


    def get_hist_path(self) ->Path:
        """
        Returns the full file path for the input history file.
        """
        return self.get_cache_dir() / self.hist_file


    def setup_dirs(self) ->None:
        """
        Creates the application's cache directory and the input history file
        if they do not already exist.
        Raises:
            OSError: If directory or file creation fails.
        """
        cache_dir = self.get_cache_dir()
        hist_file = self.get_hist_path()

        # Creates the directory and parents if necessary
        cache_dir.mkdir(parents=True, exist_ok=True)
        # Creates the file if it doesn't exist
        hist_file.touch()


    def clear_input_hist(self) ->None:
        """
        Clears (empties) the content of the input history file.
        Raises:
            IOError: If opening or writing to the file fails.
        """
        hist_file = self.get_hist_path()

        with open(hist_file, 'w') as f:
            pass
