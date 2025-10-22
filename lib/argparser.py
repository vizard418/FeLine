#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from argparse import ArgumentParser
from lib.models import Models


class Argparser(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.prog = 'FeLine'
        self.description = 'A command-line client for AI models'

        self.add_argument(
            'message',
            nargs='?',
            type=str,
            default='',
            help='The message to send to the AI model.'
        )

        self.add_argument(
            '--interactive', '-i',
            action='store_true',
            default=False,
            required=False,
            help='Enable interactive chat mode.'
        )

        self.add_argument(
            '--clear',
            action='store_true',
            default=False,
            required=False,
            help='Clear the conversation history.'
        )

        self.add_argument(
            '--model', '-m',
            type=str,
            choices=Models.availables,
            default=Models.default,
            required=False,
            help='Specify the AI model to use.'
        )

        self.add_argument(
            '--role', '-r',
            type=str,
            default='',
            required=False,
            help='Set a system role for the conversation.'
        )

        self.add_argument(
            '--verbose', '-v',
            action='store_true',
            default=False,
            required=False,
            help='Enable verbose output for debugging.'
        )
