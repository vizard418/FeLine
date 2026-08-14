#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from lib.argparser import Argparser
from lib.printer import Printer
from lib.models import Models
from lib.engine import Engine
from lib.chatty import Chatty


class Main:
    """Main application controller."""

    def __init__(self, *args, **kwargs):
        """Initialize main components and shared instances."""
        self.args = args[0] if args else None
        self.printer = Printer()
        self.engine = Engine()
        self.chatty = Chatty()


    def execute(self):
        """Execute the main program flow."""
        # App say hello
        model = Models.availables.get(self.args.model)
        self.printer.banner(model)

        self.run_setup()
        self.cleanup()

        # Set client model
        self.engine.client.model = model

        # main chat
        self.run_chat()

        # App say goodbye
        self.printer.feline()
        self.printer.goodbye()


    def run_setup(self) ->bool:
        """Create application filesystem"""
        if self.args:
            message = 'Checking File System...'
            result = self.engine.app_build()

            if result is True:
                self.printer.system_ok(message)
                return True
            else:
                self.printer.system_err(message)
                return False


    def cleanup(self) ->bool:
        """Clear local files if '--clear' argument is set."""
        if self.args and self.args.clear:
            message = 'Application cleanup...'
            result = self.engine.app_clear()

            if result is True:
                self.printer.system_ok(message)
                return True
            else:
                self.printer.system_err(message)
                return False
        return False


    def run_chat(self) -> None:
        """Run the main chat loop; repeat while '--interactive' flag is set."""
        if not (self.args.message or self.args.interactive):
            return

        chat_loop = True
        while chat_loop:
            chat_loop = self.args.interactive

            self.printer.user()
            prompt_input = self.get_prompt_input()
            if not prompt_input:
                break

            image_data = self.get_image_data(prompt_input)
            command_expands = self.get_expands(prompt_input)

            prompt_contents = [prompt_input]
            prompt_contents.extend(command_expands)

            if image_data is not None:
                prompt_contents.append(image_data)

            chat_response = self.get_response(prompt_contents)

            if chat_response:
                self.engine.add_to_history(chat_response)
                self.printer.print_response(chat_response)


    def get_prompt_input(self) -> str:
        """Obtain user input (CLI or interactive) and log it in history only if needed."""
        prompt_input = ''

        if self.args.message:
            # Use message from CLI argument for the first turn.
            prompt_input = self.args.message.rstrip()

            # Clear message to prevent reuse in interactive loop.
            self.args.message = ''

            print('>', prompt_input)

            # Manually log to history (interactive mode handles it automatically).
            result = self.engine.add_to_history(prompt_input)
            if isinstance(result, Exception):
                self.printer.system_warning(result)

        else:
            # Get multi-line input from the interactive console.
            filehistory = self.engine.cache.filehistory
            prompt_input = self.chatty.multiline_input(filehistory).rstrip('\n')

        return prompt_input.rstrip()


    def get_expands(self, prompt_text:str) ->'List[str]':
        """Execute shell commands from input and collect successful outputs."""
        expands = []
        for cmd, result in self.engine.handle_cmd(prompt_text):
            if isinstance(result, str):
                self.printer.system_info(cmd)
                expands.append(result)
            else:
                self.printer.system_warning(cmd)
        return expands


    def get_image_data(self, prompt_text: str) -> 'Optional[PIL.Image.Image]':
        """Resolve image resource from input; print warning if invalid, return valid image or None."""
        image_file, image_data = self.engine.handle_img(prompt_text)

        if isinstance(image_data, Exception):
            if image_file is not None:
                self.printer.system_warning(image_file)
            return None

        if image_file is not None and image_data is not None:
            self.printer.system_info(image_file)
        return image_data


    def get_response(self, contents: 'Iterable[Union[str, PIL.Image.Image]]') -> 'Optional[str]':
        """Stream model response; render Markdown paragraph by paragraph."""
        try:
            response = self.engine.get_response(contents)
            response_chunks = ''

            if response: self.printer.feline()

            for chunk in response:
                text = chunk.text
                response_chunks += text
                print(text, end='', flush=True)

            print()
            return response_chunks

        except Exception as e:
            self.printer.system_warning(e)
            return None


if __name__ == '__main__':
    parser = Argparser()
    args = parser.parse_args()

    app = Main(args)
    app.execute()
