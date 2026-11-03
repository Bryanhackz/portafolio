"""Repositorio de usuarios."""

from contextlib import closing

from data import db
from security import passwords


def find_by_email(email: str) -> dict | None:
    with closing(db.connect()) as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email.lower().strip(),)
        ).fetchone()
        return dict(row) if row else None


def get(user_id: int) -> dict | None:
    with closing(db.connect()) as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def create(
    email: str,
    name: str = "",
    password: str | None = None,
    provider: str | None = None,
    subject: str | None = None,
    role: str = "user",
) -> int:
    pw_hash = passwords.hash_password(password) if password else ""
    with closing(db.connect()) as conn:
        cur = conn.execute(
            "INSERT INTO users (email, name, password_hash, oauth_provider, oauth_subject, role)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (email.lower().strip(), name, pw_hash, provider, subject, role),
        )
        conn.commit()
        return int(cur.lastrowid)


def upsert_oauth(
    email: str, name: str, provider: str, subject: str, role: str = "user"
) -> int:
    existing = find_by_email(email)
    if existing:
        return int(existing["id"])
    return create(
        email=email, name=name, provider=provider, subject=subject, role=role
    )


def verify_credentials(email: str, password: str) -> dict | None:
    user = find_by_email(email)
    if not user or not user.get("password_hash"):
        return None
    if not passwords.verify_password(password, user["password_hash"]):
        return None
    return user