#!/usr/bin/env python3
# coding: utf-8 -*-

from pathlib import Path
from os import name as osname

class Storage:
    def __init__(self):
        if osname == 'nt':
            self.localdir = Path.home() / 'AppData' / 'Local' / 'FeLine'
        else:
            self.localdir = Path.home() / '.cache' / 'FeLine'

        self.input_filehistory = self.localdir / '.input-history'


    def check_local(self):
        self.localdir.mkdir(parents=True, exist_ok=True)


    def clear_history(self) ->bool:
        try:
            with open(self.input_filehistory, 'w') as f:
                return True
        except:
            return False

