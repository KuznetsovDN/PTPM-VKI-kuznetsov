import sqlite3


class DatabaseRepository:
    NAME_MAX = 256
    MESSAGE_MAX = 8096

    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row  # удобно превращать в dict
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                CHECK (length(name) <= 256),
                CHECK (length(message) <= 8096)
            )
        """)
        self.conn.commit()

    # ---------- внутренняя валидация ----------
    @staticmethod
    def _validate_id(comment_id):
        if not isinstance(comment_id, int):
            raise ValueError("comment_id должен быть int")

    @staticmethod
    def _validate_name(username):
        if not isinstance(username, str):
            raise ValueError("name должен быть строкой")
        if len(username) > DatabaseRepository.NAME_MAX:
            raise ValueError(f"name длиннее {DatabaseRepository.NAME_MAX} символов")

    @staticmethod
    def _validate_message(message):
        if not isinstance(message, str):
            raise ValueError("message должен быть строкой")
        if len(message) > DatabaseRepository.MESSAGE_MAX:
            raise ValueError(f"message длиннее {DatabaseRepository.MESSAGE_MAX} символов")

    # ---------- публичные методы ----------
    def get_by_id(self, comment_id: int):
        self._validate_id(comment_id)
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE id=?", (comment_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None

    def get_by_name(self, username: str):
        self._validate_name(username)
        cur = self.conn.execute(
            "SELECT id, name, message FROM comments WHERE name=?", (username,)
        )
        return [dict(r) for r in cur.fetchall()]

    def add(self, comment_id: int, username: str, message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_name(username)
        self._validate_message(message)
        try:
            self.conn.execute(
                "INSERT INTO comments (id, name, message) VALUES (?, ?, ?)",
                (comment_id, username, message),
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            # дубликат ID и т.п.
            raise ValueError(f"Нарушение целостности: {e}")

    def update(self, comment_id: int, new_message: str) -> bool:
        self._validate_id(comment_id)
        self._validate_message(new_message)
        cur = self.conn.execute(
            "UPDATE comments SET message=? WHERE id=?", (new_message, comment_id)
        )
        self.conn.commit()
        return cur.rowcount > 0  # False, если запись не найдена

    def delete(self, comment_id: int) -> bool:
        self._validate_id(comment_id)
        cur = self.conn.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        self.conn.commit()
        return cur.rowcount > 0