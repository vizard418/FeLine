#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from colorama import init
from colorama import Style
from colorama import Fore
from rich.console import Console
from rich.markdown import Markdown

BANNER_ASCII = '''
███████╗███████╗██╗     ██╗███╗   ██╗███████╗
██╔════╝██╔════╝██║     ██║████╗  ██║██╔════╝
█████╗  █████╗  ██║     ██║██╔██╗ ██║█████╗
██╔══╝  ██╔══╝  ██║     ██║██║╚██╗██║██╔══╝
██║     ███████╗███████╗██║██║ ╚████║███████╗
╚═╝     ╚══════╝╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝
** Imagination Is The Limit **
** Selected Model: %s **
'''
# Initializes colorama, ensuring ANSI codes work on Windows.
init(autoreset=True)

class Printer:
    """Utility class for printing formatted output."""

    def __init__(self):
        self.console = Console()

    def banner(self, model:str='') ->None:
        """Print application banner with selected model name."""
        print(Fore.GREEN + BANNER_ASCII % model)


    def system_ok(self, message:str='') ->None:
        """Print system message with OK status in green."""
        print(Fore.CYAN + '[System]:', end=' ')
        print(Style.RESET_ALL + Style.DIM + message, end=' ')
        print(Style.RESET_ALL + Fore.GREEN + 'OK')


    def system_err(self, message:str=''):
        """Print system message with ERROR status in red."""
        print(Fore.CYAN + '[System]:', end=' ')
        print(Style.RESET_ALL + Style.DIM + message, end=' ')
        print(Style.RESET_ALL + Fore.RED + 'ERR')

    def goodbye(self) ->None:
        """Print system warning message in yellow."""
        message = '¡Meow! Goodbye, human. Come back anytime.\n'
        print(Fore.BLUE + Style.BRIGHT + message)

    def feline(self) ->None:
        """Print FeLine turn header."""
        print(Fore.YELLOW + '\n[FeLine]:')

    def user(self) ->None:
        """Print user turn header."""
        print()
        print(Fore.GREEN + '\n[User]: **Press Return 2 times to exit**')

    def system_warning(self, message:str) ->None:
        """Print farewell message when application exits."""
        print(Fore.YELLOW + '[Warning]:', message)

    def system_info(self, message:str) ->None:
        """Print system information."""
        print(Fore.CYAN + '[Info]:', message)

    def styled_text(self, text: str) -> None:
        """Render Markdown text in console with styles."""
        md = Markdown(text)
        self.console.print(md, end='')
