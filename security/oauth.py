"""OAuth 2.0 + PKCE para Google y Microsoft.

- Timeout en todas las llamadas salientes.
- Límite de tamaño de respuesta para evitar DoS por respuesta gigante.
- Validación de que access_token sea un string no vacío antes de usarlo
  en cabeceras.
"""

import base64
import hashlib
import json
import secrets
import urllib.error
import urllib.parse
import urllib.request

import config


PROVIDERS = {
    "google": {
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://openidconnect.googleapis.com/v1/userinfo",
        "scope": "openid email profile",
    },
    "microsoft": {
        "auth_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "userinfo_url": "https://graph.microsoft.com/oidc/userinfo",
        "scope": "openid email profile",
    },
}

_TIMEOUT = 15
_MAX_RESPONSE_BYTES = 64 * 1024
_MAX_TOKEN_LEN = 4096


def is_configured(provider: str) -> bool:
    if provider == "google":
        return bool(config.GOOGLE_CLIENT_ID and config.GOOGLE_CLIENT_SECRET)
    if provider == "microsoft":
        return bool(config.MICROSOFT_CLIENT_ID and config.MICROSOFT_CLIENT_SECRET)
    return False


def _client(provider: str) -> tuple[str, str]:
    if provider == "google":
        return config.GOOGLE_CLIENT_ID, config.GOOGLE_CLIENT_SECRET
    if provider == "microsoft":
        return config.MICROSOFT_CLIENT_ID, config.MICROSOFT_CLIENT_SECRET
    return "", ""


def _read_json(resp) -> dict:
    """Lee como máximo MAX_RESPONSE_BYTES y parsea JSON."""
    data = resp.read(_MAX_RESPONSE_BYTES)
    if not data:
        raise ValueError("Respuesta vacía del proveedor")
    try:
        parsed = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Respuesta JSON inválida del proveedor") from exc
    if not isinstance(parsed, dict):
        raise ValueError("Respuesta del proveedor no es un objeto")
    return parsed


def generate_pkce() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
        .rstrip(b"=")
        .decode("ascii")
    )
    return verifier, challenge


def build_authorize_url(
    provider: str, redirect_uri: str, state: str, challenge: str
) -> str:
    p = PROVIDERS[provider]
    cid, _ = _client(provider)
    params = {
        "client_id": cid,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": p["scope"],
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "select_account",
    }
    return p["auth_url"] + "?" + urllib.parse.urlencode(params)


def exchange_code(provider: str, code: str, redirect_uri: str, verifier: str) -> dict:
    p = PROVIDERS[provider]
    cid, csecret = _client(provider)
    body = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": cid,
            "client_secret": csecret,
            "code_verifier": verifier,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        p["token_url"],
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return _read_json(resp)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ValueError("Fallo al contactar el endpoint de tokens") from exc


def fetch_userinfo(provider: str, access_token: str) -> dict:
    if not access_token or not isinstance(access_token, str):
        raise ValueError("access_token vacío o inválido")
    if len(access_token) > _MAX_TOKEN_LEN:
        raise ValueError("access_token demasiado largo")
    if "\r" in access_token or "\n" in access_token:
        raise ValueError("access_token contiene caracteres no permitidos")

    p = PROVIDERS[provider]
    req = urllib.request.Request(
        p["userinfo_url"],
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return _read_json(resp)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise ValueError("Fallo al contactar el endpoint de userinfo") from exc