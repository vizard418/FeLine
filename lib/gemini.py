#!/usr/bin/env python3
# coding: utf-8 -*-

from google.genai import Client

class Gemini(Client):
    """
    Client extension for managing a persistent Gemini chat session.
    Handles creation and reuse of a streaming chat session for messages.
    Attributes:
        model (str): The name of the model to be used.
        chat_stream (ChatStream, optional): The persistent chat session.
    """
    def __init__(self):
        super().__init__()

        self.model = ''
        self.chat_stream = None


    def get_chat_stream(self, contents):
        """
        Sends a message to the persistent chat stream.
        Initializes a new chat if necessary, then streams the response.
        Args:
            contents (list): Prompt parts (text/media) for the message.
        Returns:
            Generator: A generator yielding response chunks.
        """
        if not self.chat_stream:
            self.chat_stream = self.chats.create(model=self.model)

        return self.chat_stream.send_message_stream(contents)
