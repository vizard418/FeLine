#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from sys import stdout
from prompt_toolkit import prompt


class Chatty:
    def multiline_input(self, filehistory:'FileHistory')->str:
        """
        Collects multi-line input, exiting on two consecutive empty lines.
        The implementation uses prompt_toolkit for line editing and history.
        Arg: FileHistory object.
        Returns The complete multi-line string input (str).
        """
        multiline = ''
        count_whitelines = 0

        while True:
            line = prompt('> ', history=filehistory)

            if line == '':
                count_whitelines += 1

                # Exit condition: two consecutive empty lines.
                if count_whitelines >= 2:
                    # Use ANSI codes to clean up the last empty line from view.
                    stdout.write('\x1b[1A') # Move cursor up one line
                    stdout.write('\x1b[2K') # Clear the current line
                    break
            else:
                # Reset counter on non-empty input.
                count_whitelines = 0

            multiline += line + '\n'
        return multiline
