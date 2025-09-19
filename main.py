#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.argparser import ArgParser
from lib.engine import Engine
from lib.models import Models


class FeLine(Engine):

    def __init__(self):
        super().__init__()


    def execute(self):
        self.prompt.print_styled_banner()
        self.prompt.print_client_model(self.client.model)
        self.storage.check_local()
        self.run_chat()


    def run_chat(self):
        # turn based chat
        chat_loop = True

        while chat_loop:
            chat_loop = self.prompt.interactive

            # break loop of no prompt entered
            if not self.prompt.get_multiline_prompt():
                break

            self.cmd_handle()
            self.img_handle()
            self.show_response()
            self.clear_contents()


    def cmd_handle(self):
        user_input = self.prompt.user_input
        shell_commands = self.cmdparser.getcmd(user_input)

        for cmd in shell_commands:
            # command output
            cmd_output = ''

            try:
                # exec subprocess
                cmd_output = self.cmdparser.getexpand(cmd)
                self.prompt.print_styled_command('SHELL', f'`{cmd}`')

            except Exception as e:
                # print error
                cmd_output = f'{e}'
                self.prompt.print_error(f'{e}')

            # store result of command execution
            self.cmdparser.insert_expand(cmd_output)


    def img_handle(self) -> None:
        user_input = self.prompt.user_input
        image_resource = self.cmdparser.getimg(user_input)

        if image_resource:
            try:
                # get image from URL or local file
                self.imageparser.image_resolve(image_resource)
                self.prompt.print_styled_command('IMAGE', f'{image_resource}')

            except Exception as e:
                # print error
                self.prompt.print_error(f'{e}')


    def show_response(self):
        self.prompt.print_response_header()
        response = self.get_client_response()

        for chunk in response:
            print(chunk.text, end='')
        print()


if __name__ == '__main__':
    # agent initialize
    feline = FeLine()

    # process arguments
    parser = ArgParser()
    args = parser.parse_args()

    # clear application history
    if args.clear:
        feline.storage.clear_history()

    # command-line chat
    if args.message or args.interactive:

        feline.prompt.user_input= args.message
        feline.prompt.interactive = args.interactive
        feline.client.model = Models.availables[args.model]

        feline.execute()

    else:
        parser.print_help()

