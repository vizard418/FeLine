from openai import OpenAI


class OllamaHandler:
    """Gestiona la comunicacion con modelos locales en Ollama sin function calling."""

    def __init__(self, api_key: str | None = None):
        self.client = OpenAI(
            api_key=api_key or "ollama",
            base_url="http://localhost:11434/v1",
        )

    def generate(self, model: str, prompt: str) -> str:
        try:
            messages = [{"role": "user", "content": prompt}]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
            )

            content = response.choices[0].message.content
            return content if content else "Error: Model returned an empty response."

        except Exception as e:
            return f"API Error: {str(e)}"
