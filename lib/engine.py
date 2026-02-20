#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from lib.cache import Cache
from lib.gemini import Gemini
from lib.cmdparser import Cmdparser

class Engine:
    """Application core logic handler."""

    def __init__(self):
        self.cache = Cache()
        self.client = Gemini()
        self.cmdparser = Cmdparser()


    def app_build(self) ->'Union[bool, Exception]':
        """Create required cache and history files."""
        try:
            self.cache.setup_cache()
            self.cache.get_hist_filepath().touch()
            return True

        except Exception as e:
            return e


    def app_clear(self) ->'Union[bool, Exception]':
        """Clear application cache and history files."""
        result = self.cache.clear_history()
        return result


    def add_to_history(self, entry:str) -> 'Union[bool, Exception]':
        """Append entry to history; return True, False, or Exception."""
        if entry:
            return self.cache.append_history(entry)
        else:
            return False


    def handle_cmd(self, prompt_text:str) ->"Iterator[Tuple[str, Union[str, Exception]]]":
        """Extract, execute, and yield shell commands with their results."""
        for cmd in self.cmdparser.getcmd(prompt_text):
            result = self.cmdparser.getexpand(cmd)
            yield (cmd, result)


    def handle_img(self, prompt_text: str) -> 'Tuple[Optional[str], Union[PIL.Image.Image, Exception, None]]':
        """Extract and resolve image resource from user input."""
        img_resource = self.cmdparser.getimg(prompt_text)
        result = None

        if img_resource:
            try:
                result = self.cmdparser.image_resolve(img_resource)
            except Exception as e:
                result = e

        return img_resource, result


    def get_response(self, contents: 'List[Union[str, PIL.Image.Image]]') -> 'Generator[str]':
        """Stream model response from text or image input contents."""
        response = self.client.get_chat_stream(contents)
        return response
