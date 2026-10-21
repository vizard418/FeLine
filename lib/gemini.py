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

            contents = [prompt]
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

            if response.function_calls:
                for function_call in response.function_calls:
                    name = function_call.name
                    args = function_call.args

                    tool_output = ""
                    if name == "run_command":
                        tool_output = run_command(args.get("command", ""))

                    contents.append(response.candidates[0].content)

                    contents.append(
                        types.Content(
                            role="tool",
                            parts=[
                                types.Part.from_function_response(
                                    name=name,
                                    response={"result": tool_output}
                                )
                            ]
                        )
                    )

                    final_response = self.client.models.generate_content(
                        model=model,
                        contents=contents,
                        config=config,
                    )
                    return final_response.text if final_response.text else "Error: Model returned an empty response after tool execution."

            return response.text if response.text else "Error: Model returned an empty response."
        except Exception as e:
            return f"API Error: {str(e)}"
