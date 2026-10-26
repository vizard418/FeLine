from argparse import ArgumentParser
from pathlib import Path
from configparser import ConfigParser

from lib.themes import AVAILABLE_THEMES

class Argparser(ArgumentParser):
    def __new__(cls, *args, **kwargs):
        base_dir = Path(__file__).resolve().parent.parent

        cls.config = ConfigParser()
        cls.config.read(
            base_dir / 'config' / 'models.ini'
        )
        return super().__new__(cls)

    def __init__(self):
        super().__init__()
        self.prog = 'FeLine'
        self.description = (
            'Minimalist CLI client for generative AI models.'
        )

        self.add_argument(
            'message',
            nargs='?',
            type=str,
            default='',
            help='Input message for the prompt.'
        )

        self.add_argument(
            '--interactive', '-it',
            action='store_true',
            default=False,
            help='Start an interactive chat session.'
        )

        self.add_argument(
            '--purge',
            action='store_true',
            default=False,
            help='Purge local history and database records.'
        )

        self.add_argument(
            '--show-models',
            action='store_true',
            default=False,
            help='Show available models.'
        )

        self.add_argument(
            '--model',
            nargs='?',
            choices=list(self.config['availables'].keys()),
            help='Specify a model from the list.'
        )

        self.add_argument(
            '--model-config',
            nargs='?',
            choices=list(self.config['availables'].keys()),
            help='Configure the default model.'
        )

        self.add_argument(
            "--scheme-config",
            choices=AVAILABLE_THEMES,
            metavar="SCHEME",
            help="Configure the default UI color scheme.",
        )

        self.add_argument(
            '--resume-chat',
            type=int,
            nargs='?',
            help='Resume a conversation by specifying its ID.'
        )

        self.add_argument(
            '--show-chat',
            type=int,
            nargs='?',
            help='Show a specific conversation by its ID.'
        )

        self.add_argument(
            "--show-chats",
            action="store_true",
            help="Show saved chat conversations.",
        )

        self.add_argument(
            "--delete-chat",
            type=int,
            metavar="ID",
            help="Delete a saved conversation.",
        )

        self.add_argument(
            "--rename-chat",
            nargs=2,
            metavar=("ID", "TITLE"),
            help="Rename a saved conversation.",
        )

