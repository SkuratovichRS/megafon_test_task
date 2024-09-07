import sqlite3


class Database:
    def __init__(self, filename: str):
        self._connection = sqlite3.connect(filename)

    def create_table(self) -> None:
        cursor = self._connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self._connection.commit()

    def save_message(self, message: str) -> None:
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO messages (message) VALUES (?)", (message,))
        self._connection.commit()
