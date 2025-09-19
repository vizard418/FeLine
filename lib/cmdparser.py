#!/usr/bin/env python3
# coding: utf-8 -*-

from re import findall, split, search
from subprocess import check_output, STDOUT

class CmdParser:
    def __init__(self):
        self.commands = []
        self.expands = []

    def getcmd(self, text:str) ->list[str]:
        # finds all $(...) blocks in the text
        matches = findall(r'\$\(([^)]*)\)', text)

        # splits chained commands by &&, ; or ||
        for match in matches:
            parts = split(r'\s*(?:&&|\|\||;)\s*', match)

            self.commands.extend(parts)
        return self.commands


    def getexpand(self, command: str) -> str:
        output = check_output(command, shell=True, text=True, stderr=STDOUT).strip()
        self.expands.append(output)
        return output

    def insert_expand(self, text:str):
        self.expands.append(text)

    def getimg(self, text:str) -> str:
        match = search(r'\$\[([^\]]+)\]', text)
        return match.group(1) if match else ''

