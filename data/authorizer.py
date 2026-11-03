"""Autorización centralizada que emula Row Level Security."""


class Unauthorized(Exception):
    pass


class Forbidden(Exception):
    pass


def require_authenticated(actor: dict | None) -> dict:
    if not actor or not actor.get("user_id"):
        raise Unauthorized()
    return actor


def require_admin(actor: dict | None) -> dict:
    actor = require_authenticated(actor)
    if actor.get("role") != "admin":
        raise Forbidden()
    return actor


def can_read_project(actor: dict | None, project: dict) -> bool:
    if project.get("published"):
        return True
    return bool(actor and actor.get("role") == "admin")


def can_write_project(actor: dict | None) -> bool:
    return bool(actor and actor.get("role") == "admin")


def can_read_messages(actor: dict | None) -> bool:
    return bool(actor and actor.get("role") == "admin")