"""Repositorio de proyectos del portafolio."""

from contextlib import closing

from data import db


def list_published() -> list[dict]:
    with closing(db.connect()) as conn:
        rows = conn.execute(
            "SELECT * FROM projects WHERE published = 1 ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


def list_all() -> list[dict]:
    with closing(db.connect()) as conn:
        rows = conn.execute("SELECT * FROM projects ORDER BY id").fetchall()
        return [dict(r) for r in rows]


def get_by_slug(slug: str) -> dict | None:
    with closing(db.connect()) as conn:
        row = conn.execute(
            "SELECT * FROM projects WHERE slug = ?", (slug,)
        ).fetchone()
        return dict(row) if row else None


def get(project_id: int) -> dict | None:
    with closing(db.connect()) as conn:
        row = conn.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        return dict(row) if row else None


def create(data: dict, owner_id: int | None) -> int:
    with closing(db.connect()) as conn:
        cur = conn.execute(
            "INSERT INTO projects (slug, title, category, challenge, solution, result, owner_id, published)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data["slug"],
                data["title"],
                data["category"],
                data["challenge"],
                data["solution"],
                data["result"],
                owner_id,
                int(data.get("published", 1)),
            ),
        )
        conn.commit()
        return int(cur.lastrowid)


def update(project_id: int, data: dict) -> None:
    with closing(db.connect()) as conn:
        conn.execute(
            "UPDATE projects SET slug=?, title=?, category=?, challenge=?, solution=?, result=?, published=?"
            " WHERE id=?",
            (
                data["slug"],
                data["title"],
                data["category"],
                data["challenge"],
                data["solution"],
                data["result"],
                int(data.get("published", 1)),
                project_id,
            ),
        )
        conn.commit()


def delete(project_id: int) -> None:
    with closing(db.connect()) as conn:
        conn.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()