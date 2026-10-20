import sys
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.styles import Style

class Pager:
    def show_text(self, text: str):
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
