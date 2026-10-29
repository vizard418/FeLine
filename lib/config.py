import configparser
import os
from pathlib import Path


class Config:
    """Gestiona la configuracion global y de modelos."""

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.config_file = self.base_dir / "config" / "config.ini"
        self.app_dirs = self._get_app_dirs()
        self.user_config = self.load_config()
        self._ensure_app_dirs()

    def _get_app_dirs(self) -> dict:
        """Determina las rutas de configuracion y datos segun el SO."""
        if os.name == "nt":
            appdata = Path(
                os.environ.get(
                    "APPDATA", Path.home() / "AppData" / "Roaming"
                )
            )
            localappdata = Path(
                os.environ.get(
                    "LOCALAPPDATA", Path.home() / "AppData" / "Local"
                )
            )
            config_dir = appdata / "FeLine"
            return {
                "chats_db": localappdata / "FeLine" / "chats.db",
                "prompt_history": localappdata / "FeLine" / ".prompt_history",
                "default_context": config_dir / "default_context.txt",
                "user_context": config_dir / "user_context.txt",
                "instructions": config_dir / "instructions.txt",
                "models_ini": config_dir / "models.ini",
                "theme_ini": config_dir / "theme.ini",
            }
        elif os.sys.platform == "darwin":
            support = (
                Path.home() / "Library" / "Application Support" / "FeLine"
            )
            cache = Path.home() / "Library" / "Caches" / "FeLine"
            return {
                "chats_db": support / "chats.db",
                "prompt_history": cache / ".prompt_history",
                "default_context": support / "default_context.txt",
                "user_context": support / "user_context.txt",
                "instructions": support / "instructions.txt",
                "models_ini": support / "models.ini",
                "theme_ini": support / "theme.ini",
            }
        else:
            xdg_data = Path(
                os.environ.get(
                    "XDG_DATA_HOME", Path.home() / ".local" / "share"
                )
            )
            xdg_cache = Path(
                os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
            )
            xdg_config = Path(
                os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
            )
            config_dir = xdg_config / "feline"
            return {
                "chats_db": xdg_data / "feline" / "chats.db",
                "prompt_history": xdg_cache / "feline" / ".prompt_history",
                "default_context": config_dir / "default_context.txt",
                "user_context": config_dir / "user_context.txt",
                "instructions": config_dir / "instructions.txt",
                "models_ini": config_dir / "models.ini",
                "theme_ini": config_dir / "theme.ini",
            }

    def load_config(self) -> configparser.ConfigParser:
        """Lee el archivo config.ini o lo crea si no existe."""
        config = configparser.ConfigParser()

        if not self.config_file.exists():
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            config["paths"] = {
                key: str(path) for key, path in self.app_dirs.items()
            }
            with open(self.config_file, "w", encoding="utf-8") as f:
                config.write(f)
        else:
            config.read(self.config_file, encoding="utf-8")

        return config

    def _ensure_app_dirs(self) -> None:
        """Crea los directorios padre para las rutas configuradas."""
        for path in self.app_dirs.values():
            Path(path).parent.mkdir(
                parents=True, exist_ok=True
            )

    def load_models_config(self) -> configparser.ConfigParser:
        """Carga models.ini exclusivamente desde el proyecto."""
        project_models_path = self.base_dir / "config" / "models.ini"
        config = configparser.ConfigParser()
        if project_models_path.exists():
            config.read(project_models_path, encoding="utf-8")
        return config

    def set_default_model(self, model_name: str) -> None:
        """Actualiza el modelo por defecto en el archivo del usuario."""
        user_models_path = self.app_dirs["models_ini"]
        config = configparser.ConfigParser()
        if user_models_path.exists():
            config.read(user_models_path, encoding="utf-8")

        if "models" not in config:
            config["models"] = {}

        config["models"]["default"] = model_name

        user_models_path.parent.mkdir(parents=True, exist_ok=True)
        with open(user_models_path, "w", encoding="utf-8") as f:
            config.write(f)

    def get_default_model(self) -> str:
        """Obtiene el modelo por defecto desde la configuracion de usuario."""
        user_models_path = self.app_dirs["models_ini"]
        config = configparser.ConfigParser()
        if user_models_path.exists():
            config.read(user_models_path, encoding="utf-8")
            return config.get("models", "default", fallback="gemini-lite")
        return "gemini-lite"

    def get_theme_scheme(self) -> str:
        """Obtiene el esquema guardado en el archivo theme.ini del usuario."""
        from lib.themes import DEFAULT_THEME, AVAILABLE_THEMES

        theme_path = self.app_dirs["theme_ini"]
        config = configparser.ConfigParser()

        if theme_path.exists():
            config.read(theme_path, encoding="utf-8")
        else:
            config["theme"] = {"scheme": DEFAULT_THEME}
            theme_path.parent.mkdir(parents=True, exist_ok=True)
            with open(theme_path, "w", encoding="utf-8") as file:
                config.write(file)

        scheme = config.get("theme", "scheme", fallback=DEFAULT_THEME).lower()
        if scheme not in AVAILABLE_THEMES:
            return DEFAULT_THEME
        return scheme

    def set_theme_scheme(self, scheme: str) -> None:
        """Guarda el esquema visual seleccionado por el usuario."""
        from lib.themes import AVAILABLE_THEMES

        scheme = scheme.lower()
        if scheme not in AVAILABLE_THEMES:
            available = ", ".join(AVAILABLE_THEMES)
            raise ValueError(f"Unknown theme '{scheme}'. Available themes: {available}")

        theme_path = self.app_dirs["theme_ini"]
        config = configparser.ConfigParser()
        if theme_path.exists():
            config.read(theme_path, encoding="utf-8")

        if "theme" not in config:
            config["theme"] = {}
        config["theme"]["scheme"] = scheme

        theme_path.parent.mkdir(parents=True, exist_ok=True)
        with open(theme_path, "w", encoding="utf-8") as file:
            config.write(file)
