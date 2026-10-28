import re
from os import environ

from lib.tools import parse_commands, run_command
from lib.gemini import GeminiHandler
from lib.openai import OpenAIHandler


class Engine:
    """Orquestador principal que delega las peticiones segun el modelo activo."""

    def __init__(self):
        self.model = None
        self.prompt_message = ""
        self.api_key = None
        self.context = ""
        self.allow_function_calling = True

    def config_api_key(self) -> str | None:
        """Establece la api key correspondiente al modelo seleccionado."""
        if "gemini" in self.model:
            self.api_key = environ.get("GEMINI_API_KEY")
            return self.api_key

        elif "gpt" in self.model or "openai" in self.model:
            self.api_key = environ.get("OPENAI_API_KEY")
            return self.api_key

    def build_prompt_message(self, text: str) -> str:
        """Construye el mensaje procesando los comandos estaticos."""
        if not text:
            return text

        commands = parse_commands(text)

        # Evitar que el proveedor vuelva a ejecutar comandos explicitos
        self.allow_function_calling = not bool(commands)

        processed_text = text

        for cmd in commands:
            output = run_command(cmd)
            replacement = f"\n# OUTPUT: {cmd}\n{output}\n"
            processed_text = re.sub(
                r"@(?:cmd|command)\("
                + re.escape(cmd)
                + r"\)",
                replacement,
                processed_text,
                count=1,
            )

        if self.context:
            return f"{self.context}\nUser: {processed_text}"

        return processed_text

    def generate(self, prompt: str) -> str:
        """Delega la generacion de respuesta al manejador correspondiente."""
        if "gemini" in self.model:
            handler = GeminiHandler(self.api_key)
            return handler.generate(
                self.model,
                prompt,
                allow_tools=self.allow_function_calling,
            )

        if "gpt" in self.model or "openai" in self.model:
            handler = OpenAIHandler(self.api_key)
            return handler.generate(
                self.model,
                prompt,
                allow_tools=self.allow_function_calling,
            )

        raise ValueError(f"Model not supported: {self.model}")
