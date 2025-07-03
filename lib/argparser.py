#!/usr/bin/env python
# coding: utf-8 -*-

from argparse import ArgumentParser

class ArgParser(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.prog = 'FeLine'
        self.description = 'Interactive CLI AI tool'

        self.add_argument(
            'message',
            nargs='?',
            type=str,
            default=None,
            help='Send message to the prompt.'
        )

        self.add_argument(
            '--interactive', '-it',
            action='store_true',
            default=False,
            required=False,
            help='Start interactive chat mode.'
        )

        self.add_argument(
            '--clear',
            action='store_true',
            default=False,
            required=False,
            help='Clear history.'
                )
    

    def set_arg_models(self, availables, default):
        self.add_argument(
            '--model', '-m',
            type=str,
            choices=availables,
            default=default,
            required=False,
            help='Switch to a specific model.'
        )

