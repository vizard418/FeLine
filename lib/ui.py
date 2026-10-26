from pathlib import Path

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.formatted_text import ANSI, HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from lib.pager import Pager


class UI:
    """Gestiona la interfaz de usuario en consola."""

    def __init__(self, filehistory: Path) -> None:
        self.filehistory = FileHistory(str(filehistory))
        self.pager = Pager()
        self.style = Style.from_dict({
            "brand": "bold #7C9DFF",
            "muted": "#7F8798",
            "success": "#8BD5A1",
            "warning": "#F5C97A",
            "error": "bold #FF7B86",
            "user": "bold #9AD7FF",
            "assistant": "bold #B9A0FF",
            "model": "bold #D7C8FF",
            "prompt": "bold #7C9DFF",
        })

    def _print(self, content: str) -> None:
        print_formatted_text(HTML(content), style=self.style)

    def print_welcome(self, current_model: str) -> None:
        self._print("")
        self._print(
            " <brand>◆ FeLine</brand> "
            "<muted>/ Minimal AI client</muted>"
        )
        self._print(
            " <muted>────────────────────────────────────────────</muted>"
        )
        self._print(
            f" <muted>Model</muted>  "
            f"<model>{self._escape(current_model)}</model>"
        )
        self._print(
            " <muted>Enter twice to send · Ctrl+C to cancel</muted>"
        )
        self._print("")

    def print_info(self, message: str) -> None:
        self._print(
            f" <success>●</success> <muted>System</muted>  "
            f"{self._escape(message)}"
        )

    def print_models(self, models: dict) -> None:
        self._print("")
        self._print(" <brand>Available models</brand>")
        self._print(
            " <muted>────────────────────────────────────────────</muted>"
        )

        if not models:
            self._print(" <muted>No models configured.</muted>")
            return

        for key, model in models.items():
            self._print(
                f" <brand>›</brand> "
                f"<b>{self._escape(str(key))}</b>  "
                f"<muted>{self._escape(str(model))}</muted>"
            )

    def print_chats(self, chats: list) -> None:
        self._print("")
        self._print(" <brand>Saved conversations</brand>")
        self._print(
            " <muted>────────────────────────────────────────────</muted>"
        )

        if not chats:
            self._print(" <muted>No saved conversations yet.</muted>")
            return

        for chat in chats:
            chat_id = self._escape(str(chat["id"]))
            title = self._escape(str(chat["title"]))
            model = self._escape(str(chat["model"]))
            created_at = self._escape(str(chat["created_at"]))

            self._print(f" <brand>#{chat_id}</brand>  <b>{title}</b>")
            self._print(
                f"    <model>{model}</model>  "
                f"<muted>{created_at}</muted>"
            )

    def print_user_flag(self, username: str) -> None:
        self._print(f"\n <user>● {self._escape(username)}</user>")

    def print_user_message(self, message: str) -> None:
        self._print(" <user>❯ You</user>")
        print(message)
        print()

    def get_multiline_input(self) -> str | None:
        lines = []
        empty_lines = 0

        while True:
            try:
                line = prompt(
                    ANSI("\033[1;34m❯ \033[0m"),
                    history=self.filehistory,
                    style=self.style,
                    prompt_continuation="  ",
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

    def print_chat_messages(self, messages: list) -> None:
        formatted_output = []

        for msg in messages:
            role = "You" if msg["role"] == "user" else "FeLine"
            formatted_output.append(f"--- {role} ---")
            formatted_output.append(msg["content"])
            formatted_output.append("")

        self.pager.show_text("\n".join(formatted_output))

    def print_assistant_message(self, text: str) -> None:
        if text.startswith("API Error:"):
            self.print_error(text.removeprefix("API Error:").strip())
            return

        if text.startswith("Error:"):
            self.print_error(text.removeprefix("Error:").strip())
            return

        if text.startswith("Tool execution limit reached"):
            self.print_diagnostic("Tool limit reached", text)
            return

        self.pager.show_text(text, title="FeLine response")

    def print_diagnostic(self, title: str, message: str) -> None:
        self._print(
            f"\n <warning>! FeLine / {self._escape(title)}</warning>"
        )
        print(message)

    def print_error(self, err_msg: str) -> None:
        self._print(
            f"\n <error>✕ FeLine</error>  {self._escape(err_msg)}"
        )

    @staticmethod
    def _escape(value: str) -> str:
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
