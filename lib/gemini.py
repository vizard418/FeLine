#!/usr/bin/env python
# coding: utf-8 -*-

from google.genai import Client

class Gemini(Client):
    AVAILABLE_MODELS = {
        'lite' : 'gemini-2.0-flash-lite',
        'flash' : 'gemini-2.0-flash',
        'preview' : 'gemini-2.5-flash-preview-05-20'
    }

    DEFAULT_MODEL = 'lite'

    def __init__(self):
        super().__init__()

        self.model = ''
        self.chat_stream = None

    
    def get_chat_stream(self, contents):
        if not self.chat_stream:
            self.chat_stream = self.chats.create(model=self.model)
        
        return self.chat_stream.send_message_stream(contents)
    