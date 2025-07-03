#!/usr/bin/env python
# coding: utf-8 -*-

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from sys import stdout
from colorama import Fore, Style


class Prompt:
    def __init__(self, filehistory):
        self.filehistory = FileHistory(filehistory)

        self.multiline_prompt = ''
        self.interactive = False

    
    def get_multiline_prompt(self) -> str:
        if not self.multiline_prompt:
            self.print_styled_input()
            self.multiline_prompt = self.input_multiline()
        
        else:
            self.print_styled_input(self.multiline_prompt)
            self.filehistory.append_string(self.multiline_prompt)
        return self.multiline_prompt

    
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
        print(Fore.YELLOW + 'FeLine · Imagination is the only limit' + Style.RESET_ALL)
    

    def print_client_model(self, modelname:str) -> None:
        print(Fore.YELLOW + f'Current LLM model: {modelname}' + Style.RESET_ALL)


    def print_styled_input(self, message:str='') -> None:
        print('\n' + Fore.GREEN + '$> [PROMPT]' + Style.RESET_ALL, end= ' ')
        print('**Press Return 2 times to exit**')
        if message:
            print('$> ', message)
            print('$> ')

    def print_error(self, error_msg:str) -> None:
        print(Fore.RED + '+ [ERROR!]' + Style.RESET_ALL, error_msg)
    

    def print_debug(self, any:object) -> None:
        print(Fore.RED + '-> [DEBUG]' + Style.RESET_ALL, any)


    def print_response_header(self):
        print(Fore.YELLOW + '-> [FELINE]' + Style.RESET_ALL)

    
    def print_styled_command(self, head:str, message:str) -> None:
        print(Fore.GREEN + f'$> [{head}]' + Style.RESET_ALL, message)
