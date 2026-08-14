#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from colorama import init
from colorama import Style
from colorama import Fore
from colorama import Back
from pydoc import pager

APP_BANNER = '''
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

    def banner(self, model:str='') ->None:
        """Print application banner with selected model name."""
        print(APP_BANNER % model)


    def system_ok(self, message:str='') ->None:
        """Print system message with OK status in green."""
        print(f'>{Style.BRIGHT} {message} [{Fore.GREEN}OK{Style.RESET_ALL}]')


    def system_err(self, message:str=''):
        """Print system message with ERROR status in red."""
        print(f'>{Style.BRIGHT} {message} [{Fore.RED}ERR{Style.RESET_ALL}]')


    def goodbye(self) ->None:
        """Print system warning message in yellow."""
        print(f'{Style.BRIGHT}¡Meow! Goodbye, human. Come back anytime.')


    def feline(self) ->None:
        """Print FeLine turn header."""
        print(f'\n{Back.WHITE}{Fore.BLACK}[FeLine]')


    def user(self) ->None:
        """Print user turn header."""
        print(f'\n{Back.WHITE}{Fore.BLACK}[User]:{Style.RESET_ALL} **Press Return 2 times to exit**')


    def system_warning(self, message:str) ->None:
        """Print farewell message when application exits."""
        print(f'> {Style.BRIGHT}{message} [{Fore.YELLOW}WARNING{Style.RESET_ALL}]')


    def system_info(self, message:str) ->None:
        """Print system information."""
        print(f'> {Style.BRIGHT}{message} [{Fore.CYAN}INFO{Style.RESET_ALL}]')

    def print_response(self, response_text:str) -> None:
        """Print text with pager."""
        pager(response_text)

