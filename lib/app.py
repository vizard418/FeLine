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

    def _handle_model_config(self) -> bool:
        """Establece modelo predeterminado en las configuraciones de usuario"""
        if self.args.model_config:
            model_config = self.args.model_config

            self.config_manager.set_default_model(model_config)
            self.ui.print_info(f"Default model updated to '{self.args.model_config}'")
            return True
        return False

    def _handle_purge(self) -> bool:
        """Limpieza de datos de usuario cache y base de datos."""
        if self.args.purge:
            self.history_path.write_text("", encoding="utf-8")
            self.db.clear_all()

            self.ui.print_info("Application cache cleared")
            return True
        return False

    def _handle_delete_chat(self) -> bool:
        """Elimina una conversacion guardada."""
        if self.args.delete_chat is None:
            return False

        chat_id = self.args.delete_chat

        if self.db.delete_conversation(chat_id):
            self.ui.print_info(f"Chat {chat_id} deleted.")
        else:
            self.ui.print_error(f"Chat {chat_id} not found.")
        return True

    def _handle_rename_chat(self) -> bool:
        """Renombra una conversacion guardada."""
        if not self.args.rename_chat:
            return False

        chat_id = int(self.args.rename_chat[0])
        title = self.args.rename_chat[1]

        if self.db.rename_conversation(chat_id, title):
            self.ui.print_info(f"Chat {chat_id} renamed.")
        else:
            self.ui.print_error(
                f"Chat {chat_id} not found or title is empty."
            )
        return True

    def _handle_show_models(self) -> bool:
        """Mostrar los modelos disponibles"""
        if self.args.show_models:
            models = dict(self.config["availables"]) if "availables" in self.config else {}
            self.ui.print_models(models)
            return True
        return False

    def _handle_show_chats(self) -> bool:
        """"Mostrar los chats guardados"""
        if self.args.show_chats:
            chats = self.db.get_conversations()
            self.ui.print_chats(chats)
            return True
        return False

    def _handle_show_chat(self) -> bool:
        """Mostrar los mensajes de un chat"""
        if self.args.show_chat:
            chat_id = self.args.show_chat
            messages = self.db.get_all_chat_messages(chat_id)

            if not messages:
                self.ui.print_error(f"No messages found for chat ID {chat_id}")
            else:
                self.ui.print_chat_messages(messages)
            return True
        return False

    def _handle_model(self) -> None:
        """Asignar modelo para conversacion actual"""
        if self.args.model:
            model_name = self.config["availables"].get(self.args.model)
            self.engine.model = model_name
            self.ui.print_info(f"Model updated to '{self.args.model}'")

        else:
            model_keyword = self.config_manager.get_default_model()
            model_name = self.config["availables"].get(model_keyword, model_keyword)
            self.engine.model = model_name

    def run(self):
        if self._handle_model_config(): return # --model-config [model_name]
        if self._handle_purge(): return # --purge
        if self._handle_delete_chat(): return # --delete-chat [chat_id]
        if self._handle_rename_chat():return # --rename-chat [chat_id] [chat_title]
        if self._handle_show_models(): return # --show-models
        if self._handle_show_chats(): return # --show-chats
        if self._handle_show_chat(): return # --show-chat [chat_id]

        self._handle_model() # --model [model_name]
        self.engine.config_api_key() # set api key

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

                # Crear chat nuevo si no existe
                if not self.current_chat_id:
                    title = user_message[:30].strip()
                    self.current_chat_id = self.db.create_conversation(
                        title,
                        self.engine.model,
                    )

                # Cargar contexto antes de agregar el mensaje actual
                self._update_context()

                # Procesar mensaje y comandos una sola vez
                self.engine.prompt_message = self.engine.build_prompt_message(user_message)

                # Guardar mensaje del usuario
                self.db.add_message(
                    self.current_chat_id,
                    "user",
                    self.engine.prompt_message,
                )

                # Generar respuesta y mostrarla
                response = self.engine.generate(self.engine.prompt_message)
                self.ui.print_assistant_message(response)

                # Guardar respuesta del asistente en DB
                self.db.add_message(self.current_chat_id, "assistant", response)

        elif self.args.message:
            self.ui.print_user_flag(getuser())
            self.ui.print_user_message(self.args.message)

            if not self.current_chat_id:
                title = self.args.message[:30].strip()
                self.current_chat_id = self.db.create_conversation(
                    title,
                    self.engine.model,
                )

            self._update_context()

            self.engine.prompt_message = self.engine.build_prompt_message(
                self.args.message
            )

            self.db.add_message(
                self.current_chat_id,
                "user",
                self.engine.prompt_message,
            )

            response = self.engine.generate(self.engine.prompt_message)
            self.ui.print_assistant_message(response)

            self.db.add_message(
                self.current_chat_id,
                "assistant",
                response,
            )

    def _update_context(self) -> None:
        """Actualiza el contexto con los mensajes recientes."""
        if not self.current_chat_id:
            self.engine.context = ""
            return

        history = self.db.get_chat_history(
            self.current_chat_id,
            limit=6,
        )

        max_chars = 1200
        context = []

        for msg in history:
            content = msg["content"]

            if len(content) > max_chars:
                content = content[:max_chars] + "..."

            context.append(f"{msg['role']}: {content}")

        self.engine.context = "\n".join(context)
