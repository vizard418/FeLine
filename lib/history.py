#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from os import listdir
from os.path import join as joinpath
from os import remove as removefile

class History:
    DIR_CACHE = Path.home() / '.cache' / 'feline'
    INPUT_HISTORY = DIR_CACHE / '.input_history'

    @staticmethod
    def check_dir():
        History.DIR_CACHE.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def clear_input():
        with open(History.INPUT_HISTORY, 'w') as f:
            pass

    @staticmethod
    def delete_wav():
        wav_files = [x for x in listdir(History.DIR_CACHE) if x.endswith('.wav')]

        for f in wav_files:
            filepath = joinpath(History.DIR_CACHE, f)
            removefile(filepath)

