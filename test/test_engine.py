#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pytest
from unittest.mock import MagicMock, patch
from lib.engine import Engine

def test_engine(tmp_path):
    engine = Engine()

    # Mock Local methods
    engine.local.setup_dirs = MagicMock(return_value=True)
    engine.local.clear_input_hist = MagicMock(return_value=True)
    engine.local.get_hist_path = MagicMock(return_value=str(tmp_path / ".history"))

    # Mock Gemini client
    engine.client.get_chat_stream = MagicMock(return_value=["Hello", "World"])
    # Mock Models.availables
    from lib.models import Models
    Models.availables = {"gpt-test": "TestModel"}

    print("\n--- application_setup ---")
    result = engine.application_setup()
    print("Result:", result)

    print("\n--- application_clear ---")
    result = engine.application_clear()
    print("Result:", result)

    print("\n--- get_hist_path ---")
    hist_path = engine.get_hist_path()
    print("History file path:", hist_path)

    print("\n--- get_shell_commands ---")
    chat_text = "Run these: $(echo hello && echo world; ls || pwd)"
    for cmd in engine.get_shell_commands(chat_text):
        print("Command:", cmd)

    print("\n--- get_image_file ---")
    chat_text = "Load image $[http://example.com/image.png]"
    img_file = engine.get_image_file(chat_text)
    print("Extracted image file:", img_file)

    print("\n--- get_response ---")
    response = engine.get_response(["Some input"])
    print("Response from client:", list(response))

    print("\n--- set_model ---")
    result = engine.set_model("gpt-test")
    print("Set valid model:", result)
    result = engine.set_model("nonexistent")
    print("Set invalid model:", result)

