"""Repositorio de mensajes de contacto."""

from contextlib import closing

from data import db


def create(name: str, email: str, body: str) -> int:
    with closing(db.connect()) as conn:
        cur = conn.execute(
            "INSERT INTO messages (name, email, body) VALUES (?, ?, ?)",
            (name, email, body),
        )
        conn.commit()
        return int(cur.lastrowid)


def list_all() -> list[dict]:
    with closing(db.connect()) as conn:
        rows = conn.execute(
            "SELECT * FROM messages ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def mark_read(message_id: int) -> None:
    with closing(db.connect()) as conn:
        conn.execute("UPDATE messages SET read = 1 WHERE id = ?", (message_id,))
        conn.commit()


def delete(message_id: int) -> None:
    with closing(db.connect()) as conn:
        conn.execute("DELETE FROM messages WHERE id = ?", (message_id,))
        conn.commit()