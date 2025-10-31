#!/usr/bin/env python3
# coding: utf-8 -*-

from google.genai import Client

class Gemini(Client):
    """Manage a persistent Gemini chat session with streaming responses."""

    def __init__(self):
        """Initialize model name and persistent chat stream."""
        super().__init__()

        self.model = ''
        self.chat_stream = None


    def get_chat_stream(self, contents):
        """Send a message to the chat; return a generator of response chunks."""
        if not self.chat_stream:
            self.chat_stream = self.chats.create(model=self.model)

        return self.chat_stream.send_message_stream(contents)
