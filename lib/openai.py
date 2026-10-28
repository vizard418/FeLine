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

    def generate(
        self, model: str, prompt: str, allow_tools: bool = True
    ) -> str:
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
            max_iterations = 10

            for iteration in range(max_iterations + 1):
                request_args = {
                    "model": model,
                    "messages": messages,
                }

                if allow_tools:
                    request_args["tools"] = tools
                    request_args["tool_choice"] = "auto"

                response = self.client.chat.completions.create(**request_args)

                response_message = response.choices[0].message

                if not response_message.tool_calls:
                    content = response_message.content
                    return content if content else "Error: Model returned an empty response."

                if iteration == max_iterations:
                    return "Tool execution limit reached. Please refine your request."

                messages.append(response_message)

                for tool_call in response_message.tool_calls:
                    if tool_call.function.name != "run_command":
                        continue

                    args = json.loads(tool_call.function.arguments)

                    try:
                        tool_output = run_command(args.get("command", ""))
                    except Exception as e:
                        tool_output = f"Tool error: {e}"

                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": "run_command",
                        "content": tool_output,
                    })

            return "Tool execution limit reached."
        except Exception as e:
            return f"API Error: {str(e)}"
