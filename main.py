#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from lib.argparser import Argparser
from lib.engine import Engine
from lib.console import Console

from sys import stdout
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory


class Main:
    def __init__(self, *args, **kwargs):
        self.args = args[0] if args else None
        self.console = Console()
        self.engine = Engine()

        self.filehistory = FileHistory(self.engine.get_hist_path())


    def _print_verbose(self, detail:any) -> None:
        """
        Checks for the --verbose flag and prints  detail if set.
        """
        if self.args and self.args.verbose:
            print(detail)


    def execute(self) ->None:
        """
        Initializes the application workflow, including setup, optional cleanup, 
        and the primary execution based on command-line arguments.
        """
        # Handle case where no arguments are present
        if not self.args: return

        self.console.print_banner(self.args.model)
        self._handle_application_setup()
        self.engine.set_model(self.args.model)

        if self.args.clear:
            self._handle_application_cleanup()

        if self.args.message or self.args.interactive:
            self._run_chat()


    def _handle_application_setup(self) -> bool:
        """
        Calls the setup, handles the result, and prints the outcome.
        Returns: True if setup succeeded, False otherwise.
        """
        setup_result = self.engine.application_setup()

        if setup_result is True:
            self.console.print_info('Local files... [OK]')
            return True
        else:
            self.console.print_error('Local files setup failed.')
            self._print_verbose(setup_result)
            return False


    def _handle_application_cleanup(self) -> bool:
        """
        Calls the clear action, handles the result, and prints the outcome.
        Returns: True if cleanup succeeded, False otherwise.
        """
        cleanup_result = self.engine.application_clear()

        if cleanup_result is True:
            self.console.print_info('Application data cleanup... [OK]')
            return True
        else:
            self.console.print_error('Application data cleanup failed.')
            self._print_verbose(cleanup_result)
            return False


    def _run_chat(self):
        """
        Runs the main chat loop.
        The loop executes at least once and continues if the '--interactive'
        argument is set.
        """
        # The chat must run at least once
        chat_loop = True

        while chat_loop:
            # Continue the loop only if the '--interactive' flag is present.
            chat_loop = self.args.interactive

            # Display user prompt and get input.
            self.console.print_user()
            user_input = self._get_user_input()

            if user_input:
                cmd_expands = self._handle_cmd(user_input)
                img_data = self._handle_img(user_input)

                contents = [user_input]

                if len(cmd_expands) > 0:
                    contents =[f'{user_input}\n{cmd_expands}']

                if img_data:
                    contents.append(img_data)

                response = self._chat_response(contents)
                if response: self.filehistory.append_string(response)

            else:
                break


    def _get_user_input(self) ->str:
        """
        Retrieves user input, prioritizing the command-line message argument 
        over interactive multiline input.
        Returns:
            str: The sanitized user input.
        """
        user_input = ''

        if self.args.message:
            # Use message from CLI argument for the first turn.
            user_input = self.args.message
            # Clear message to prevent reuse in interactive loop.
            self.args.message = ''
            print('>', user_input)

            self.filehistory.append_string(user_input.rstrip())

        else:
            # Get multi-line input from the interactive console.
            user_input = self._get_input_multiline()

        return user_input.rstrip()


    def _get_input_multiline(self) -> str:
        """
        Collects multi-line input, exiting on two consecutive empty lines.
        The implementation uses prompt_toolkit for line editing and history.
        Returns:
            str: The complete multi-line string input.
        """
        multiline = ''
        count_whitelines = 0

        while True:
            line = prompt('> ', history=self.filehistory)

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


    def _handle_cmd(self, chat_text:str) ->list[str]:
        """
        Processes shell commands found in user input and returns their output.
        The method extracts commands, executes them, prints output/errors,
        and collects successful command outputs.
        Args:
            chat_text (str): The raw input string
                potentially containing commands.
        Returns:
            list[str]: A list of successful command outputs (strings).
        """
        # Shell subprocess
        shell_commands = self.engine.get_shell_commands(chat_text)
        command_expands = []

        for cmd in shell_commands:
            expand = self.engine.cmdparser.getexpand(cmd)

            if isinstance(expand, str):
                self.console.print_command(cmd)
                command_expands.append(expand)
                self._print_verbose(expand)
            else:
                self.console.print_error(expand)

        return command_expands


    def _handle_img(self, chat_text:str) ->'Optional[bytes]':
        """
        Processes user input to extract and resolve image data.
        Checks if the engine returns an image path (str) or an error
        (Exception). Prints the image or the error to the console.
        Args:
            chat_text (str): The user input containing the image command.
        Returns:
            Optional[bytes]: The resolved image data on success, or None
                if image extraction failed.
        """
        # Image process
        image_file = self.engine.get_image_file(chat_text)
        image_data = None

        if isinstance(image_file, Exception):
            self.console.print_error(image_file)

        elif image_file:
            self.console.print_image(image_file)
            image_data = self.engine.cmdparser.image_resolve(image_file)
            self._print_verbose(image_data)
        return image_data


    def _chat_response(self, contents: iter) -> 'Optional[str]':
        """
        Retrieves and processes the streaming response from the engine.
        Prints the response chunk by chunk and returns the full text
        or handles and prints any error encountered.
        Args:
            contents (iter): The prompt contents to send to the engine.
        Returns:
            Optional[str]: The full response text on success, otherwise None.
        """
        response_chunks = ''

        try:
            response = self.engine.get_response(contents)
            self.console.print_feline()

            for chunk in response:
                text = chunk.text
                print(text, end='')
                response_chunks += text

            return response_chunks
        except Exception as e:
            self.console.print_error(e)
            return


if __name__ == '__main__':
    parser = Argparser()
    arguments = parser.parse_args()

    app = Main(arguments)
    app.execute()
