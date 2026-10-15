import sqlite3
from pathlib import Path


class Database:
    """Gestiona la persistencia de chats y mensajes."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Inicializa las tablas necesarias en la base de datos."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    model TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id INTEGER,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (chat_id) REFERENCES conversations (id)
                )
                """
            )
            conn.commit()

    def create_conversation(
        self, title: str, model: str
    ) -> int:
        """Crea un nuevo chat y devuelve su ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO conversations (title, model)
                VALUES (?, ?)
                """,
                (title, model),
            )
            conn.commit()
            return cursor.lastrowid

    def add_message(self, chat_id: int, role: str, content: str):
        """Agrega un mensaje a un chat."""
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO messages (chat_id, role, content)
                VALUES (?, ?, ?)
                """,
                (chat_id, role, content),
            )
            conn.commit()

    def get_chat_history(self, chat_id: int, limit: int = 10) -> list:
        """Devuelve los ultimos mensajes de un chat."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT role, content FROM messages
                WHERE chat_id = ?
                ORDER BY id ASC
                LIMIT ?
                """,
                (chat_id, limit),
            )
            return [dict(row) for row in cursor.fetchall()]


    def get_conversations(self) -> list:
        """Devuelve todas las conversaciones guardadas."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, title, model, created_at 
                FROM conversations
                ORDER BY id DESC
                """
            )
            return [dict(row) for row in cursor.fetchall()]


    def clear_all(self):
        """Elimina todos los datos de la base de datos."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM messages")
            conn.execute("DELETE FROM conversations")
            conn.commit()

    def get_all_chat_messages(self, chat_id: int) -> list:
        """Devuelve todos los mensajes de un chat específico."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT role, content FROM messages
                WHERE chat_id = ?
                ORDER BY id ASC
                """,
                (chat_id,),
            )
            return [dict(row) for row in cursor.fetchall()]
