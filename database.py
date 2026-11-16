import sqlite3


class TriangleDB:
    def __init__(self, db_path: str = ":memory:"):
        # :memory: — БД в оперативной памяти (идеально для тестов).
        # Для реальной работы можно передать "triangles.db".
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL,
                b REAL,
                c REAL,
                triangle_type TEXT,
                error_message TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        self.conn.commit()

    def add(self, a: float, b: float, c: float, ttype, err):
        # INSERT OR REPLACE — если запись с такими сторонами уже есть,
        # она перезапишется (полезно при повторных вызовах).
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (a, b, c, ttype, err),
        )
        self.conn.commit()

    def get(self, a: float, b: float, c: float):
        # Возвращает кортеж (ttype, err) или None, если записи нет.
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE a=? AND b=? AND c=?",
            (a, b, c),
        )
        return cur.fetchone()

    def delete(self, a: float, b: float, c: float):
        self.conn.execute(
            "DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c)
        )
        self.conn.commit()