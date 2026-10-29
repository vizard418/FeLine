import sys

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, Layout, ScrollablePane, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style

from lib.themes import get_theme


class Pager:
    """Muestra texto navegable y conserva la salida al salir."""

    def __init__(self, scheme: str = "nord") -> None:
        self.scheme = scheme
        self.theme = get_theme(scheme)

    def show_text(self, text: str, title: str = "FeLine") -> None:
        if not text:
            return

        if not sys.stdin.isatty() or not sys.stdout.isatty():
            print(text)
            return

        bindings = KeyBindings()
        content_lines = max(1, len(text.splitlines()))

        content_window = Window(
            FormattedTextControl(text),
            wrap_lines=True,
            style="class:content",
        )

        pane = ScrollablePane(
            content_window,
            height=20,
            keep_cursor_visible=False,
            keep_focused_window_visible=False,
            show_scrollbar=True,
        )

        pane.vertical_scroll = 0

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
            pane.vertical_scroll = min(content_lines, pane.vertical_scroll + 1)
            event.app.invalidate()

        @bindings.add("pageup")
        @bindings.add("b")
        @bindings.add("c-b")
        def _page_up(event):
            page_size = max(1, event.app.output.get_size().rows - 3)
            pane.vertical_scroll = max(0, pane.vertical_scroll - page_size)
            event.app.invalidate()

        @bindings.add("pagedown")
        @bindings.add("f")
        @bindings.add("c-f")
        @bindings.add("space")
        def _page_down(event):
            page_size = max(1, event.app.output.get_size().rows - 3)
            pane.vertical_scroll = min(content_lines, pane.vertical_scroll + page_size)
            event.app.invalidate()

        @bindings.add("g")
        def _go_to_top(event):
            pane.vertical_scroll = 0
            event.app.invalidate()

        @bindings.add("G")
        def _go_to_bottom(event):
            pane.vertical_scroll = content_lines
            event.app.invalidate()

        header = Window(
            FormattedTextControl([("class:brand", f" ◆ {title} ")]),
            height=1,
            style="class:header",
        )
        footer = Window(
            FormattedTextControl(
                " ↑/k ↓/j scroll   PgUp/PgDn page   g/G top/bottom   q close "
            ),
            height=1,
            style="class:status",
        )

        app = Application(
            layout=Layout(HSplit([header, pane, footer]), focused_element=content_window),
            key_bindings=bindings,
            full_screen=False,
            mouse_support=True,
            erase_when_done=False,
            style=Style.from_dict({
                "header": f"bg:{self.theme['header_bg']}",
                "brand": self.theme["brand"],
                "content": self.theme["content"],
                "status": f"bg:{self.theme['status_bg']} {self.theme['status_fg']}",
                "scrollbar.background": f"bg:{self.theme['scrollbar_bg']}",
                "scrollbar.button": f"bg:{self.theme['scrollbar_button']}",
            }),
        )
        app.run()
