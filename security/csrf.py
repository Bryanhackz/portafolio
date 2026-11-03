"""CSRF double-submit firmado con HMAC-SHA256.

El token se firma con SECRET_KEY y viaja en cookie no-HttpOnly
(SameSite=Strict). El cliente lo reenvía como header `X-CSRF-Token` o
campo `_csrf`. El servidor rechaza tokens no firmados, lo que cierra el
vector de cookie injection por subdominio.
"""

import hashlib
import hmac
import secrets

import config


def _sign(raw: str) -> str:
    return hmac.new(
        config.SECRET_KEY.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256
    ).hexdigest()[:32]


def new_token() -> str:
    raw = secrets.token_urlsafe(32)
    return f"{raw}.{_sign(raw)}"


def _verify_sig(token: str) -> bool:
    if "." not in token:
        return False
    raw, _, sig = token.rpartition(".")
    if not raw or not sig:
        return False
    if len(raw) > 128 or len(sig) > 128:
        return False
    return hmac.compare_digest(sig, _sign(raw))


def token_matches(cookie_token: str | None, submitted: str | None) -> bool:
    if not cookie_token or not submitted:
        return False
    if len(cookie_token) > 256 or len(submitted) > 256:
        return False
    if not _verify_sig(cookie_token):
        return False
    if not _verify_sig(submitted):
        return False
    return hmac.compare_digest(cookie_token, submitted)


def csrf_cookie_header(token: str) -> str:
    parts = [
        f"{config.CSRF_COOKIE}={token}",
        "Path=/",
        "SameSite=Strict",
        f"Max-Age={config.SESSION_TTL}",
    ]
    if config.IS_PRODUCTION:
        parts.append("Secure")
    return "; ".join(parts)