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
        """Carga models.ini del usuario o lo replica desde el proyecto."""
        project_models_path = self.base_dir / "config" / "models.ini"
        user_models_path = self.app_dirs["models_ini"]

        if not user_models_path.exists() and project_models_path.exists():
            content = project_models_path.read_text(encoding="utf-8")
            user_models_path.write_text(content, encoding="utf-8")

        config = configparser.ConfigParser()
        target_path = (
            user_models_path
            if user_models_path.exists()
            else project_models_path
        )
        config.read(target_path, encoding="utf-8")
        return config

    def set_default_model(self, model_name: str) -> None:
        """Actualiza el modelo por defecto en el models.ini del usuario."""
        user_models_path = self.app_dirs["models_ini"]
        config = self.load_models_config()

        if "models" not in config:
            config["models"] = {}

        config["models"]["default"] = model_name

        with open(user_models_path, "w", encoding="utf-8") as f:
            config.write(f)


    def get_default_model(self) -> str:
        """Obtiene el modelo por defecto desde la configuracion."""
        config = self.load_models_config()
        return config.get("models", "default", fallback="gemini-lite")
