import sys
from pathlib import Path
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.history import FileHistory
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.styles import Style

class UI:
    """Gestiona la interfaz de usuario en consola."""

    def __init__(self, filehistory: Path) -> None:
        self.filehistory = FileHistory(str(filehistory))


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


    def print_assistant_message(self, text: str):
        """Muestra la respuesta generada por el asistente."""
        self.show_paged_text(text)


    def show_paged_text(self, text: str):
        """Muestra texto navegable y lo deja en la terminal al salir."""
        if not text:
            return

        if not sys.stdin.isatty() or not sys.stdout.isatty():
            print(text)
            return

        bindings = KeyBindings()
        content_lines = max(1, len(text.splitlines()))
        pane = ScrollablePane(
            Window(
                FormattedTextControl(text),
                wrap_lines=True,
            ),
            keep_cursor_visible=False,
            keep_focused_window_visible=False,
            show_scrollbar=True,
        )

        @bindings.add("q")
        @bindings.add("escape")
        def _exit_pager(event):
            event.app.exit()

        @bindings.add("c-c")
        def _interrupt_pager(event):
            event.app.exit()

        @bindings.add("up")
        @bindings.add("k")
        def _scroll_up(event):
            pane.vertical_scroll = max(0, pane.vertical_scroll - 1)
            event.app.invalidate()

        @bindings.add("down")
        @bindings.add("j")
        def _scroll_down(event):
            pane.vertical_scroll = min(
                content_lines, pane.vertical_scroll + 1
            )
            event.app.invalidate()

        @bindings.add("pageup")
        @bindings.add("b")
        @bindings.add("c-b")
        def _page_up(event):
            page_size = max(1, event.app.output.get_size().rows - 2)
            pane.vertical_scroll = max(0, pane.vertical_scroll - page_size)
            event.app.invalidate()

        @bindings.add("pagedown")
        @bindings.add("f")
        @bindings.add("c-f")
        @bindings.add("space")
        def _page_down(event):
            page_size = max(1, event.app.output.get_size().rows - 2)
            pane.vertical_scroll = min(
                content_lines, pane.vertical_scroll + page_size
            )
            event.app.invalidate()

        @bindings.add("u")
        @bindings.add("c-u")
        def _half_page_up(event):
            page_size = max(1, (event.app.output.get_size().rows - 2) // 2)
            pane.vertical_scroll = max(0, pane.vertical_scroll - page_size)
            event.app.invalidate()

        @bindings.add("d")
        @bindings.add("c-d")
        def _half_page_down(event):
            page_size = max(1, (event.app.output.get_size().rows - 2) // 2)
            pane.vertical_scroll = min(
                content_lines, pane.vertical_scroll + page_size
            )
            event.app.invalidate()

        @bindings.add("g")
        def _go_to_top(event):
            pane.vertical_scroll = 0
            event.app.invalidate()

        @bindings.add("G")
        def _go_to_bottom(event):
            pane.vertical_scroll = content_lines
            event.app.invalidate()

        footer = Window(
            FormattedTextControl(" ↑/k, ↓/j scroll  PgUp/PgDn/Space page  g/G top/bottom  q quit "),
            height=1,
            style="class:status",
        )
        app = Application(
            layout=Layout(HSplit([pane, footer])),
            key_bindings=bindings,
            full_screen=False,
            mouse_support=True,
            style=Style.from_dict({
                "scrollbar.background": "bg:#444444",
                "status": "reverse",
            }),
        )
        app.run()
        print(text)

    def print_chat_messages(self, messages: list):
        """Formatea los mensajes de un chat para pasarlos al paginador."""
        formatted_output = []
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_output.append(f"--- [{role}] ---")
            formatted_output.append(msg["content"])
            formatted_output.append("\n")

        self.show_paged_text("\n".join(formatted_output))


    def print_error(self, err_msg: str):
        """Muestra un mensaje de error formateado."""
        print(f"\n[FeLine Error] {err_msg}")
