"""Cookies de sesión firmadas con HMAC-SHA256. Sin estado en servidor.

- Token: <payload_b64>.<hmac_hex>.
- Payload: {"uid": int, "exp": int}.
- Verificación: longitud máxima, firma constante en tiempo, expiración,
  tipo del uid.
"""

import base64
import hmac
import json
import time
from hashlib import sha256

import config


_MAX_TOKEN_LEN = 4096


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _unb64(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(data: bytes) -> str:
    return hmac.new(config.SECRET_KEY.encode("utf-8"), data, sha256).hexdigest()


def create_token(user_id: int) -> str:
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id inválido")
    payload = {"uid": user_id, "exp": int(time.time()) + config.SESSION_TTL}
    raw = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    return _b64(raw) + "." + _sign(raw)


def verify_token(token: str | None) -> dict | None:
    if not token or not isinstance(token, str):
        return None
    if len(token) > _MAX_TOKEN_LEN:
        return None
    if "." not in token:
        return None
    body, _, signature = token.rpartition(".")
    if not body or not signature or len(signature) > 128:
        return None
    try:
        raw = _unb64(body)
    except (ValueError, TypeError):
        return None
    if not hmac.compare_digest(signature, _sign(raw)):
        return None
    try:
        payload = json.loads(raw)
    except (ValueError, TypeError):
        return None
    if not isinstance(payload, dict):
        return None
    uid = payload.get("uid")
    if not isinstance(uid, int) or isinstance(uid, bool) or uid <= 0:
        return None
    exp = payload.get("exp")
    if not isinstance(exp, int) or isinstance(exp, bool):
        return None
    if exp < time.time():
        return None
    return payload


def session_cookie_header(token: str) -> str:
    parts = [
        f"{config.SESSION_COOKIE}={token}",
        "Path=/",
        "HttpOnly",
        "SameSite=Strict",
        f"Max-Age={config.SESSION_TTL}",
    ]
    if config.IS_PRODUCTION:
        parts.append("Secure")
    return "; ".join(parts)


def clear_session_cookie_header() -> str:
    parts = [
        f"{config.SESSION_COOKIE}=",
        "Path=/",
        "HttpOnly",
        "SameSite=Strict",
        "Max-Age=0",
    ]
    if config.IS_PRODUCTION:
        parts.append("Secure")
    return "; ".join(parts)