#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from colorama import Style, Fore
from functools import wraps
from typing import Callable, Any


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

def colored_output(color_code: str, reset_after_print: bool = True) -> Callable:
    """Decorator to apply color before and reset after a print function."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                print(color_code, end='')
                return func(*args, **kwargs)
            finally:
                if reset_after_print:
                    print(Style.RESET_ALL, end='')
        return wrapper
    return decorator



class Console:
    """Handles all console output operations."""

    @colored_output(Fore.GREEN)
    def print_banner(self, model_name:str='') ->None:
        """
        Prints the ASCII application banner, including the selected model name.
        Args:
            model_name (str): The name of the model currently in use.
        """
        print(APP_BANNER % model_name)


    @colored_output(Fore.RED)
    def print_error(self, message:str='') ->None:
        """
        Prints a standardized error message in red.
        Args:
            message (str): The error details to display.
        """
        print('[ERROR]'+ Style.RESET_ALL, message)


    @colored_output(Fore.CYAN)
    def print_info(self, message:str='') ->None:
        """
        Prints a standardized system information message in green.
        Args:
            message (str): The informational details to display.
        """
        print('[INFO]'+ Style.RESET_ALL, message)


    @colored_output(Fore.GREEN)
    def print_user(self):
        """
        Prints the user's turn prompt and the exit instruction.
        """
        message = '**Press Return 2 times to exit**'
        print('\n[USER]' + Style.RESET_ALL + Style.DIM, message)


    @colored_output(Fore.CYAN)
    def print_command(self, message:str='') ->None:
        """
        Prints a command execution message in cyan.
        Args:
            message (str): The command message to display.
        """
        print('[SHELL]' + Style.RESET_ALL + Style.DIM, message)


    @colored_output(Fore.CYAN)
    def print_image(self, message:str='') ->None:
        """
        Prints a status message regarding an image resource in cyan.
        Args:
            message (str): The message indicating the image status (e.g., loaded).
        """
        print('[IMAGE]' + Style.RESET_ALL + Style.DIM, message)


    @colored_output(Fore.YELLOW)
    def print_feline(self):
        """
        Prints the feline's turn prompt and the exit instruction.
        """
        print('\n[FELINE]' + Style.RESET_ALL)
