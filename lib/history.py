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
    def clear_input() ->bool:
        try:
            with open(History.INPUT_HISTORY, 'w') as f:
                return True
        except:
            return False


    @staticmethod
    def delete_wav() ->bool:
        try:
            wav_dir = History.DIR_CACHE
            wav_files = [x for x in listdir(wav_dir) if x.endswith('.wav')]

        except:
            return False

        else:
            for f in wav_files:
                filepath = joinpath(wav_dir, f)
                removefile(filepath)
            return True

