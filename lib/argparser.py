#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

class ArgParser(ArgumentParser):
    def __init__(self):
        super().__init__()

        self.description = 'Interactive command-line AI agent.'

        self.add_argument('message', nargs='*', default=None,
            help='Input prompt (not-required)')

        self.add_argument('--interactive', '-it', action='store_true',
            required=False, help='Interactive chat mode')

        self.add_argument('--clear', action='store_true', required=False,
            help='Clear history')

        self.add_argument('--speech', '-tts', action='store_true',
            required=False,default=False,
            help='Enable speech generation mode without requiring interactive mode.')

    def set_models(self, models:dict):
        self.add_argument('--model', '-m', type=str, choices=models, required=False,
            help='Specify model. Available: {}'.format(', '.join(models.keys())))

