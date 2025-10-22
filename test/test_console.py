#!/usr/env/bin python3
#-*- coding: utf-8 -*-

import pytest
from lib.console import Console

def test_console_demo_outputs():
    console = Console()

    # Banner
    console.print_banner("GPT-5")

    # Error message
    console.print_error("Something went wrong!")

    # Info message
    console.print_info("System is running smoothly.")

    # User prompt
    console.print_user()

    # Command messages
    console.print_command("ls -la /home/user")
    console.print_command("echo 'Hello World'")

    # Image messages
    console.print_image("Image loaded successfully.")
    console.print_image("Failed to load image.")

    # Feline turn
    console.print_feline()

