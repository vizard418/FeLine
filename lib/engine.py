#!/usr/bin/env python
# coding: utf-8 -*-

from lib.gemini import Gemini
from lib.storage import Storage
from lib.cmdparser import CmdParser
from lib.imageparser import ImageParser
from lib.prompt import Prompt


class Engine:
    def __init__(self):
        self.client = Gemini()
        self.storage = Storage()
        self.cmdparser = CmdParser()
        self.imageparser = ImageParser()
        self.prompt = Prompt(self.storage.input_filehistory)
    

    def get_client_response(self):
        prompt_text = self.prompt.multiline_prompt

        if self.cmdparser.expands:
            expands = ''.join(self.cmdparser.expands)
            prompt_text = f'Prompt: {prompt_text} Output:{expands}'
        
        contents = [prompt_text]

        if self.imageparser.image_data:
            contents.append(self.imageparser.image_data)

        return self.client.get_chat_stream(contents)
    

    def clear_contents(self) ->None:
        self.cmdparser.commands = []
        self.cmdparser.expands = []
        self.imageparser.image_data = None
        self.prompt.multiline_prompt = ''

