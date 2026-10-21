import json
from openai import OpenAI
from lib.tools import run_command


class OpenAIHandler:
    """Gestiona la comunicacion y el function calling con modelos compatibles con OpenAI/Groq."""

    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def generate(self, model: str, prompt: str) -> str:
        try:
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "run_command",
                        "description": "USE THIS TOOL to execute local shell commands when needed for system status, files or configuration.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "command": {
                                    "type": "string",
                                    "description": "The exact shell command to execute."
                                }
                            },
                            "required": ["command"],
                        },
                    },
                }
            ]

            messages = [{"role": "user", "content": prompt}]

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
            )

            response_message = response.choices[0].message

            if response_message.tool_calls:
                # Anexa el mensaje completo del asistente que contiene las llamadas a herramientas
                messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    if tool_call.function.name == "run_command":
                        args = json.loads(tool_call.function.arguments)
                        tool_output = run_command(args.get("command", ""))

                        messages.append({
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": "run_command",
                            "content": tool_output,
                        })

                second_response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                )

                content = second_response.choices[0].message.content
                if content:
                    return content

                # Si el mensaje viene vacio pero hay tool_calls secundarias o contenido alternativo
                return "[La herramienta se ejecuto correctamente, pero el modelo no retorno texto adicional]"

            content = response_message.content
            return content if content else "Error: Model returned an empty response."
        except Exception as e:
            return f"API Error: {str(e)}"
