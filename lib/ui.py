from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import ANSI
from lib.pager import Pager

class UI:
    """Gestiona la interfaz de usuario en consola."""

    def __init__(self, filehistory: Path) -> None:
        self.filehistory = FileHistory(str(filehistory))
        self.pager = Pager()

    def print_welcome(self, current_model: str) -> None:
        print(
            "\033[1mFeLine:\033[0m "
            "Minimalist CLI client for generative AI models."
        )
        print(f"\033[1mCurrent Model:\033[0m {current_model}")

    def print_info(self, message:str) -> None:
        print(f"\033[1mSystem:\033[0m {message}")


    def print_models(self, models: dict) -> None:
        """Imprime los modelos disponibles."""
        print("\033[1mAvailable Models:\033[0m")
        for key, model in models.items():
            print(f"  \033[1m{key}\033[0m: {model}")


    def print_chats(self, chats: list) -> None:
        """Imprime la lista de chats almacenados."""
        print("\033[1mSaved Chats:\033[0m")
        if not chats:
            print("  No chats found.")
            return
        for chat in chats:
            print(
                f"  \033[1m[{chat['id']}]\033[0m {chat['title']} "
                f"(\033[36m{chat['model']}\033[0m) - {chat['created_at']}"
            )


    def print_user_flag(self, username: str) -> None:
        print(f"\n\033[1m[{username}]\033[0m")


    def print_user_message(self, message: str) -> None:
        print(f"\033[1m>\033[0m {message}\n\033[1m>\033[0m\n")

    def get_multiline_input(self) -> str | None:
        lines = []
        empty_lines = 0

        while True:
            try:
                line = prompt(
                    ANSI("\033[1m>\033[0m "),
                    history=self.filehistory
                )
            except (KeyboardInterrupt, EOFError):
                print()
                return None

            if not line:
                empty_lines += 1
                if empty_lines >= 2:
                    break
            else:
                empty_lines = 0
            lines.append(line)

        while lines and not lines[-1]:
            lines.pop()
        return "\n".join(lines).strip()

    def print_chat_messages(self, messages: list):
        """Formatea los mensajes de un chat para pasarlos al paginador."""
        formatted_output = []
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_output.append(f"--- [{role}] ---")
            formatted_output.append(msg["content"])
            formatted_output.append("\n")

        self.pager.show_text("\n".join(formatted_output))

    def print_assistant_message(self, text: str):
        """Muestra la respuesta generada por el asistente."""
        if text.startswith("API Error:"):
            self.print_error(text.removeprefix("API Error:").strip())
            return

        if text.startswith("Error:"):
            self.print_error(text.removeprefix("Error:").strip())
            return

        if text.startswith("Tool execution limit reached"):
            self.print_diagnostic(
                "Tool limit reached",
                text,
            )
            return

        output = f"--- FeLine Response ---\n\n{text}"
        self.pager.show_text(output)

    def print_diagnostic(self, title: str, message: str):
        """Muestra un diagnostico breve."""
        print(f"\n\033[1m[FeLine] {title}\033[0m")
        print(message)

    def print_error(self, err_msg: str):
        """Muestra un mensaje de error formateado."""
        print(f"\n\033[1;31m[FeLine Error]\033[0m {err_msg}")
