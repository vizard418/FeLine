from getpass import getuser
from pathlib import Path

from lib.ui import UI
from lib.config import Config
from lib.database import Database
from lib.engine import Engine


class Application:
    """Gestiona el ciclo de vida principal de la aplicacion."""

    def __init__(self, *args, **kwargs):
        self.args = args[0] if args else None
        self.config_manager = Config()
        self.config = self.config_manager.load_models_config()

        paths = self.config_manager.user_config["paths"]
        self.history_path = Path(paths["prompt_history"])
        chats_db_path = Path(paths["chats_db"])

        self.db = Database(chats_db_path)
        self.ui = UI(self.history_path)
        self.engine = Engine()
        self.current_chat_id = None

    def run(self):
        # Establece el modelo predeterminado
        if self.args.model_config:
            self.config_manager.set_default_model(self.args.model_config)
            self.ui.print_info(f"Default model updated to '{self.args.model_config}'")
            return

        # Limpiar archivos locales y base de datos
        if self.args.purge:
            self.history_path.write_text("", encoding="utf-8")
            self.db.clear_all()
            self.ui.print_info("Application cache cleared")
            return

        # Mostrar modelos disponibles
        if self.args.show_models:
            models_dict = dict(self.config["availables"]) if "availables" in self.config else {}
            self.ui.print_models(models_dict)
            return

        # Mostrar chats guardados
        if self.args.show_chats:
            chats = self.db.get_conversations()
            self.ui.print_chats(chats)
            return

        # Mostrar mensajes de un chat especifico
        if self.args.show_chat:
            messages = self.db.get_all_chat_messages(self.args.show_chat)
            if not messages:
                self.ui.print_error(f"No messages found for chat ID {chat_id}")
            else:
                self.ui.print_chat_messages(messages)
            return

        # Asignar modelo al motor de ejecucion
        if self.args.model:
            self.engine.model = self.config["availables"].get(self.args.model)
        else:
            default_keyword = self.config_manager.get_default_model()
            self.engine.model = self.config["availables"].get(default_keyword, default_keyword)

        # Asignacion de api correspondiente al modelo seleccionado
        self.engine.api_key = self.engine.get_api_key()

        # Reanudar chat anterior si se proporciona --resume-chat
        if hasattr(self.args, "resume_chat") and self.args.resume_chat:
            self.current_chat_id = self.args.resume_chat
            history = self.db.get_chat_history(self.current_chat_id, limit=5)
            # Construir contexto plano con las ultimas 5 interacciones
            self.engine.context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

        # Imprime un saludo al ejecutar aplicacion usando el modelo resuelto
        self.ui.print_welcome(self.engine.model)

        # Inicio de chat interactivo o one-shot
        if self.args.interactive:
            while True:
                self.ui.print_user_flag(getuser())

                if self.args.message:
                    user_message = self.args.message
                    self.ui.print_user_message(user_message)
                    self.args.message = ""
                else:
                    user_message = self.ui.get_multiline_input()

                if not user_message.strip():
                    break

                # Procesar mensaje y comandos
                self.engine.prompt_message = self.engine.build_prompt_message(user_message)

                # Crear chat nuevo si no existe pasando el titulo y el modelo
                if not self.current_chat_id:
                    title = user_message[:30].strip()
                    self.current_chat_id = self.db.create_conversation(title, self.engine.model)

                # Guardar mensaje del usuario en DB
                self.db.add_message(self.current_chat_id, "user", self.engine.prompt_message)

                # Generar respuesta y mostrarla
                response = self.engine.generate(self.engine.prompt_message)
                self.ui.print_assistant_message(response)

                # Guardar respuesta del asistente en DB
                self.db.add_message(self.current_chat_id, "assistant", response)

        elif self.args.message:
            self.ui.print_user_flag(getuser())
            self.ui.print_user_message(self.args.message)

            self.engine.prompt_message = self.engine.build_prompt_message(self.args.message)

            if not self.current_chat_id:
                title = self.args.message[:30].strip()
                self.current_chat_id = self.db.create_conversation(title, self.engine.model)

            self.db.add_message(self.current_chat_id, "user", self.engine.prompt_message)

            response = self.engine.generate(self.engine.prompt_message)
            self.ui.print_assistant_message(response)

            self.db.add_message(self.current_chat_id, "assistant", response)
