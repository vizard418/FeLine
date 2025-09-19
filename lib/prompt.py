#!/usr/bin/env python3
# coding: utf-8 -*-

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from sys import stdout
from colorama import Fore, Style


class Prompt:
    def __init__(self, filehistory):
        self.filehistory = FileHistory(filehistory)

        self.user_input = ''
        self.interactive = False


    def get_multiline_prompt(self) -> str:
        if not self.user_input:
            self.print_styled_input()
            self.user_input = self.input_multiline()

        else:
            self.print_styled_input(self.user_input)
            self.filehistory.append_string(self.user_input)
        return self.user_input


    def input_multiline(self) -> str:
        multiline = ''
        count_whitelines = 0

        while True:
            line = prompt('$> ', history=self.filehistory)

            if line == '':
                count_whitelines += 1

                if count_whitelines >= 2:
                    stdout.write('\x1b[1A')
                    stdout.write('\x1b[2K')
                    break

            else:
                count_whitelines = 0

            multiline += line + '\n'
        return multiline.rstrip()


    def print_styled_banner(self):
        banner_message = '  FeLine - Imagination is the only limit'
        print(Style.BRIGHT + Fore.YELLOW + banner_message + Style.RESET_ALL)


    def print_client_model(self, modelname:str) -> None:
        print(Style.DIM + f'► Current LLM model: {modelname}' + Style.RESET_ALL)


    def print_styled_input(self, message:str='') -> None:
        print(Style.BRIGHT)
        print(Fore.GREEN + '  [User]' + Style.RESET_ALL, end= ' ')
        print('**Press Return 2 times to exit**')

        if message:
            print('$> ', message)
            print('$> ')


    def print_error(self, error_msg:str) -> None:
        print(Style.BRIGHT + Fore.RED + '  [Error!]' + Style.RESET_ALL, error_msg)


    def print_debug(self, any:object) -> None:
        print(Style.BRIGHT + Fore.RED + '  [Debug]' + Style.RESET_ALL, any)


    def print_response_header(self):
        print(Style.BRIGHT + Fore.YELLOW + '  [FeLine]' + Style.RESET_ALL)


    def print_styled_command(self, head:str, message:str) -> None:
        print(Style.BRIGHT + Fore.GREEN + f'  [{head}]' + Style.RESET_ALL, message)
