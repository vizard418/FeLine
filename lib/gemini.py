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
            max_iterations = 10

            for iteration in range(max_iterations + 1):
                response = self.client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=config,
                )

                if not response.function_calls:
                    return response.text if response.text else "Error: Model returned an empty response."

                if iteration == max_iterations:
                    return "Tool execution limit reached. Please refine your request."

                contents.append(response.candidates[0].content)

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

            return "Tool execution limit reached."
        except Exception as e:
            return f"API Error: {str(e)}"
