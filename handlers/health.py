"""Endpoint de salud para monitoreo."""

from data import db
from handlers._types import Request, Response, json_response


def check(request: Request) -> Response:
    try:
        with db.connect() as conn:
            conn.execute("SELECT 1").fetchone()
        return json_response({"ok": True})
    except Exception:
        return json_response({"ok": False}, status=500)