#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from lib.models import Models

class ArgParser(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.prog = 'FeLine'
        self.description = 'Interactive CLI AI tool'

        self.add_argument(
            'message',
            nargs='?',
            type=str,
            default='',
            help='Send message to the prompt.'
        )

        self.add_argument(
            '--interactive', '-i',
            action='store_true',
            default=False,
            required=False,
            help='Launch interactive chat mode.'
        )

        self.add_argument(
            '--clear', '-cls',
            action='store_true',
            default=False,
            required=False,
            help='Clear history.'
        )

        self.add_argument(
            '--model', '-m',
            type = str,
            choices = Models.availables,
            default = Models.default,
            required = False,
            help = 'Selecting a specific model based on needs'
        )

