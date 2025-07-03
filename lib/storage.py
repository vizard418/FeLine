#!/usr/bin/env python
# coding: utf-8 -*-

from pathlib import Path

class Storage:
    def __init__(self):
        self.localdir = Path.home() / '.local' / 'share' / 'FeLine'
        self.input_filehistory = self.localdir / '.input-history'

    def check_local(self):
        self.localdir.mkdir(parents=True, exist_ok=True)
    

    def clear_history(self) ->bool:
        try:
            with open(self.input_filehistory, 'w') as f:
                return True
        except:
            return False

