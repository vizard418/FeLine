#!/usr/bin/env python3
# coding: utf-8 -*-

from google.genai import Client

class Gemini(Client):
    def __init__(self):
        super().__init__()

        self.model = ''
        self.chat_stream = None


    def get_chat_stream(self, contents):
        if not self.chat_stream:
            self.chat_stream = self.chats.create(model=self.model)

        return self.chat_stream.send_message_stream(contents)

