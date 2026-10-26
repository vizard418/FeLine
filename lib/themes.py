"""Theme definitions and style factories for the terminal UI."""

from prompt_toolkit.styles import Style


THEMES = {
    "gruvbox": {
        "brand": "bold #FABD2F",
        "muted": "#928374",
        "success": "#B8BB26",
        "warning": "#FE8019",
        "error": "bold #FB4934",
        "user": "bold #83A598",
        "assistant": "bold #D3869B",
        "model": "bold #D79921",
        "prompt": "bold #FABD2F",
        "header_bg": "#3C3836",
        "content": "#EBDBB2",
        "status_fg": "#D5C4A1",
        "status_bg": "#3C3836",
        "scrollbar_bg": "#504945",
        "scrollbar_button": "#D79921",
    },
    "nord": {
        "brand": "bold #88C0D0",
        "muted": "#7B88A1",
        "success": "#A3BE8C",
        "warning": "#EBCB8B",
        "error": "bold #BF616A",
        "user": "bold #81A1C1",
        "assistant": "bold #B48EAD",
        "model": "bold #8FBCBB",
        "prompt": "bold #88C0D0",
        "header_bg": "#2E3440",
        "content": "#D8DEE9",
        "status_fg": "#D8DEE9",
        "status_bg": "#3B4252",
        "scrollbar_bg": "#434C5E",
        "scrollbar_button": "#88C0D0",
    },
}

DEFAULT_THEME = "nord"
AVAILABLE_THEMES = tuple(THEMES)


def get_theme(name: str | None = None) -> dict:
    """Return a theme palette, falling back to the default theme."""
    theme_name = (name or DEFAULT_THEME).lower()
    if theme_name not in THEMES:
        raise ValueError(
            f"Unknown theme '{theme_name}'. Available themes: "
            f"{', '.join(AVAILABLE_THEMES)}"
        )
    return THEMES[theme_name].copy()


def get_ui_style(name: str | None = None) -> Style:
    """Build the prompt_toolkit style used by UI and input prompts."""
    theme = get_theme(name)
    return Style.from_dict({
        "brand": theme["brand"],
        "muted": theme["muted"],
        "success": theme["success"],
        "warning": theme["warning"],
        "error": theme["error"],
        "user": theme["user"],
        "assistant": theme["assistant"],
        "model": theme["model"],
        "prompt": theme["prompt"],
    })
