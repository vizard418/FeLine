import re
from os import environ
from google import genai
from openai import OpenAI
from lib.tools import parse_commands, run_command


class Engine:
    """Gestiona comandos, contexto y conexion con modelos."""

    def __init__(self):
        self.model = None
        self.prompt_message = ""
        self.api_key = None
        self.context = ""

    def config_api_key(self) -> str | None:
        """Establece la api key correspondiente al modelo seleccionado."""
        if "gemini" in self.model:
            self.api_key = environ.get("GEMINI_API_KEY")
            return self.api_key

        elif "gpt" in self.model:
            self.api_key = environ.get("OPENAI_API_KEY")
            return self.api_key

    def build_prompt_message(self, text: str) -> str:
        """Construye el mensaje procesando los comandos."""
        if not text:
            return text

        commands = parse_commands(text)
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

        # Si hay contexto previo, lo anteponemos al mensaje procesado
        if self.context:
            return f"{self.context}\nUser: {processed_text}"

        return processed_text

    def generate(self, prompt: str) -> str:
        """Genera una respuesta usando el cliente de IA."""
        if "gemini" in self.model:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(model=self.model,
                contents=prompt,)

            return response.text

        if "gpt" in self.model or "openai" in self.model:
            client = OpenAI(api_key=self.api_key,
                base_url="https://api.groq.com/openai/v1",)

            response = client.chat.completions.create(model=self.model,
                messages=[ {"role": "user", "content": prompt,} ],)

            return (response.choices[0].message.content)
        raise ValueError(f"Modelo no soportado: {self.model}")
