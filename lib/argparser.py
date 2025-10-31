#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from argparse import ArgumentParser
from lib.models import Models

class Argparser(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.prog = 'FeLine'
        self.description = 'Command-Line Language Models (CLILMs)'

        self.add_argument('message', nargs='?', type=str, default='',
            help='Prompt input message.')

        self.add_argument('--interactive', '-it', action='store_true',
            default=False, required=False, help='Enable interactive mode.')

        self.add_argument('--clear', action='store_true', default=False,
            required=False, help='Clear the conversation history.')

        self.add_argument('--model', '-m', type=str, choices=Models.availables,
            default=Models.default, help='Specify the AI model to use.')

        self.add_argument('--verbose', '-v', action='store_true',
            default=False, required=False, help='Debugging mode.')
