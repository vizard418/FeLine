from pathlib import Path
from re import search

from prompt_toolkit import prompt, print_formatted_text
from prompt_toolkit.formatted_text import ANSI, HTML
from prompt_toolkit.history import FileHistory
from prompt_toolkit.completion import Completer, PathCompleter
from prompt_toolkit.document import Document

from lib.pager import Pager
from lib.themes import get_theme, get_ui_style


class UI:
    """Gestiona la interfaz de usuario en consola."""

    def __init__(self, filehistory: Path, scheme: str = "nord") -> None:
        self.filehistory = FileHistory(str(filehistory))
        self.scheme = scheme
        self.theme = get_theme(scheme)
        self.style = get_ui_style(scheme)
        self.pager = Pager(scheme)

    def _print(self, content: str) -> None:
        print_formatted_text(HTML(content), style=self.style)

    def print_welcome(self, current_model: str) -> None:
        self._print("")
        self._print(" <brand>◆ FeLine</brand> <muted>/ Minimal AI client</muted>")
        self._print(" <muted>────────────────────────────────────────────</muted>")
        self._print(f" <muted>Model</muted>  <model>{self._escape(current_model)}</model>")
        self._print(f" <muted>Theme</muted>  <brand>{self._escape(self.scheme)}</brand>")
        self._print(" <muted>Enter twice to send · Ctrl+C to cancel</muted>")
        self._print("")

    def print_info(self, message: str) -> None:
        self._print(f" <success>●</success> <muted>System</muted>  {self._escape(message)}")

    def print_models(self, models: dict) -> None:
        self._print("")
        self._print(" <brand>Available models</brand>")
        self._print(" <muted>────────────────────────────────────────────</muted>")
        if not models:
            self._print(" <muted>No models configured.</muted>")
            return
        for key, model in models.items():
            self._print(f" <brand>›</brand> <b>{self._escape(str(key))}</b>  <muted>{self._escape(str(model))}</muted>")

    def print_chats(self, chats: list) -> None:
        self._print("")
        self._print(" <brand>Saved conversations</brand>")
        self._print(" <muted>────────────────────────────────────────────</muted>")
        if not chats:
            self._print(" <muted>No saved conversations yet.</muted>")
            return
        for chat in chats:
            chat_id = self._escape(str(chat["id"]))
            title = self._escape(str(chat["title"]))
            model = self._escape(str(chat["model"]))
            created_at = self._escape(str(chat["created_at"]))
            self._print(f" <brand>#{chat_id}</brand>  <b>{title}</b>")
            self._print(f"    <model>{model}</model>  <muted>{created_at}</muted>")

    def print_user_flag(self, username: str) -> None:
        self._print(f"\n <user>● {self._escape(username)}</user>")

    def print_user_message(self, message: str) -> None:
        self._print(" <user>❯ You</user>")
        print(message)
        print()

    def get_multiline_input(self) -> str | None:
        lines = []
        empty_lines = 0

        # Habilitar autocompletado de rutas
        path_completer = HybridPathCompleter()

        while True:
            try:
                line = prompt(
                    ANSI("\033[1m❯ \033[0m"),
                    history=self.filehistory,
                    style=self.style,
                    completer=path_completer,
                    complete_while_typing=True,
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
        self.pager.show_text("\n".join(formatted_output), title="Saved conversation")

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
        self._print(f"\n <warning>! FeLine / {self._escape(title)}</warning>")
        print(message)

    def print_error(self, err_msg: str) -> None:
        self._print(f"\n <error>✕ FeLine</error>  {self._escape(err_msg)}")

    @staticmethod
    def _escape(value: str) -> str:
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

class HybridPathCompleter(Completer):
    """Permite autocompletar rutas de archivos y directorios de forma hibrida."""

    def __init__(self):
        self.path_completer = PathCompleter(expanduser=True)

    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor

        # Detectar si el cursor se encuentra dentro de un bloque @cmd(...) o @command(...)
        if "@cmd(" in text_before_cursor or "@command(" in text_before_cursor:
            last_cmd_idx = max(
                text_before_cursor.rfind("@cmd("),
                text_before_cursor.rfind("@command("),
            )
            open_paren_idx = text_before_cursor.find("(", last_cmd_idx)

            if open_paren_idx != -1 and text_before_cursor.rfind(")") < open_paren_idx:
                # Extraer todo el contenido escrito dentro del comando hasta el cursor
                inner_text = text_before_cursor[open_paren_idx + 1 :]

                # Aislar la ultima palabra o argumento separado por espacios u operadores (ej. pipes)
                tokens = search(r"([^\s]+)$", inner_text)
                if tokens:
                    path_part = tokens.group(1)
                    temp_doc = Document(path_part, cursor_position=len(path_part))

                    for comp in self.path_completer.get_completions(temp_doc, complete_event):
                        yield comp
                return

        # Aplicar comportamiento por defecto para autocompletar rutas directas
        match = search(r"[~\/\.\w\-]+$", text_before_cursor)
        if match:
            word = match.group(0)
            if word.startswith("~") or word.startswith("/") or word.startswith("./"):
                for comp in self.path_completer.get_completions(document, complete_event):
                    yield comp
