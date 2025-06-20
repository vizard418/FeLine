#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.genai import Client
from google.genai import types

class Gemini(Client):

    API_VARNAME = 'GEMINI_API_KEY'

    AVAILABLE_MODELS = {
        'flash' : 'gemini-2.0-flash',
        'lite' : 'gemini-2.0-flash-lite',
        'preview' : 'gemini-2.5-flash-preview-05-20'
    }

    DEFAULT_MODEL = AVAILABLE_MODELS['lite']


    def __init__(self, api:str):
        super().__init__(api_key=api)

        self.model = self.DEFAULT_MODEL
        self.chat = None


    def get_chat_stream(self, message:str):
        if not self.chat:
            self.chat = self.chats.create(model=self.model)

        return self.chat.send_message_stream(message)


    def generate_speech(self, text:str):
        response = self.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text, config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Kore',
                        )
                    )
                ),
            )
        )

        data = response.candidates[0].content.parts[0].inline_data.data
        return data

