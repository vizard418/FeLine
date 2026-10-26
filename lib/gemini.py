from google import genai
from google.genai import types
from lib.tools import run_command, AVAILABLE_TOOLS


class GeminiHandler:
    """Gestiona la comunicacion y el function calling con modelos Gemini."""

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate(self, model: str, prompt: str) -> str:
        try:
            config = types.GenerateContentConfig(
                tools=AVAILABLE_TOOLS,
                temperature=0.3
            )

            chat = self.client.chats.create(
                model=model,
                config=config
            )

            response = chat.send_message(prompt)
            max_iterations = 10
            iteration = 0

            while response.function_calls and iteration < max_iterations:
                iteration += 1
                parts = []
                for function_call in response.function_calls:
                    name = function_call.name
                    args = function_call.args
                    tool_output = ""

                    if name == "run_command":
                        try:
                            tool_output = run_command(args.get("command", ""))
                        except Exception as e:
                            tool_output = f"Tool error: {e}"
                    else:
                        tool_output = f"Unknown tool: {name}"

                    parts.append(
                        types.Part.from_function_response(
                            name=name,
                            response={"result": tool_output}
                        )
                    )

                response = chat.send_message(parts)

            if response.text:
                return response.text
            return "Error: Model returned an empty response."

        except Exception as e:
            return f"API Error: {str(e)}"
