import sys

from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, ScrollablePane
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.styles import Style


class Pager:
    """Muestra texto navegable y conserva la salida al salir."""

    def show_text(self, text: str, title: str = "FeLine") -> None:
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
                style="class:content",
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
            pane.vertical_scroll = max(
                0, pane.vertical_scroll - 1
            )
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
            page_size = max(
                1, event.app.output.get_size().rows - 3
            )
            pane.vertical_scroll = max(
                0, pane.vertical_scroll - page_size
            )
            event.app.invalidate()

        @bindings.add("pagedown")
        @bindings.add("f")
        @bindings.add("c-f")
        @bindings.add("space")
        def _page_down(event):
            page_size = max(
                1, event.app.output.get_size().rows - 3
            )
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

        header = Window(
            FormattedTextControl([
                ("class:brand", f" ◆ {title} ")
            ]),
            height=1,
            style="class:header",
        )

        footer = Window(
            FormattedTextControl(
                " ↑/k ↓/j scroll   PgUp/PgDn page   "
                "g/G top/bottom   q close "
            ),
            height=1,
            style="class:status",
        )

        app = Application(
            layout=Layout(HSplit([header, pane, footer])),
            key_bindings=bindings,
            full_screen=False,
            mouse_support=True,
            style=Style.from_dict({
                "header": "bg:#202638",
                "brand": "bold #9DB4FF",
                "content": "#D8DEEA",
                "status": "bg:#202638 #A0A8BA",
                "scrollbar.background": "bg:#30384A",
                "scrollbar.button": "bg:#7C9DFF",
            }),
        )

        app.run()
        print(text)
