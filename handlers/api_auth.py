"""OAuth 2.0 con PKCE. Cada callback verifica state y crea sesión firmada."""

import secrets
from contextlib import closing
from datetime import datetime, timezone

import config
from data import db
from data.repositories import users
from security import oauth, session as session_mod
from handlers._types import Request, Response, redirect


def _save_state(state: str, provider: str, verifier: str, redirect_uri: str) -> None:
    with closing(db.connect()) as conn:
        conn.execute(
            "DELETE FROM oauth_states WHERE created_at < datetime('now', ?)",
            (f"-{config.OAUTH_STATE_TTL} seconds",),
        )
        conn.execute(
            "INSERT OR REPLACE INTO oauth_states (state, provider, code_verifier, redirect_uri)"
            " VALUES (?, ?, ?, ?)",
            (state, provider, verifier, redirect_uri),
        )
        conn.commit()


def _is_expired(created_at: str) -> bool:
    try:
        created = datetime.fromisoformat(created_at.replace(" ", "T"))
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return True
    age = (datetime.now(timezone.utc) - created).total_seconds()
    return age > config.OAUTH_STATE_TTL


def _consume_state(state: str) -> dict | None:
    with closing(db.connect()) as conn:
        conn.execute("BEGIN IMMEDIATE")
        try:
            row = conn.execute(
                "SELECT * FROM oauth_states WHERE state = ?", (state,)
            ).fetchone()
            if not row:
                conn.rollback()
                return None
            if _is_expired(row["created_at"]):
                conn.execute("DELETE FROM oauth_states WHERE state = ?", (state,))
                conn.commit()
                return None
            conn.execute("DELETE FROM oauth_states WHERE state = ?", (state,))
            conn.commit()
            return dict(row)
        except Exception:
            conn.rollback()
            raise


def start(request: Request, provider: str) -> Response:
    if provider not in oauth.PROVIDERS or not oauth.is_configured(provider):
        return redirect("/admin/login?error=oauth_no_configurado")
    redirect_uri = f"{config.OAUTH_REDIRECT_BASE}/auth/{provider}/callback"
    verifier, challenge = oauth.generate_pkce()
    state = secrets.token_urlsafe(32)
    _save_state(state, provider, verifier, redirect_uri)
    return redirect(oauth.build_authorize_url(provider, redirect_uri, state, challenge))


def callback(request: Request, provider: str) -> Response:
    if provider not in oauth.PROVIDERS:
        return redirect("/admin/login?error=proveedor_invalido")
    code = request.query.get("code", [""])[0]
    state = request.query.get("state", [""])[0]
    if not code or not state:
        return redirect("/admin/login?error=oauth_respuesta_invalida")
    entry = _consume_state(state)
    if not entry or entry["provider"] != provider:
        return redirect("/admin/login?error=oauth_state_invalido")
    try:
        tokens = oauth.exchange_code(
            provider, code, entry["redirect_uri"], entry["code_verifier"]
        )
        info = oauth.fetch_userinfo(provider, tokens.get("access_token", ""))
    except Exception:
        return redirect("/admin/login?error=oauth_intercambio")
    email = (info.get("email") or "").lower().strip()
    sub = info.get("sub") or ""
    if not email or not sub:
        return redirect("/admin/login?error=oauth_sin_email")
    if info.get("email_verified") is False:
        return redirect("/admin/login?error=oauth_email_no_verificado")
    role = "admin" if email in config.ADMIN_EMAILS else "user"
    user_id = users.upsert_oauth(email, info.get("name", ""), provider, sub, role=role)
    token = session_mod.create_token(user_id)
    return redirect(
        "/admin",
        extra_headers=[("Set-Cookie", session_mod.session_cookie_header(token))],
    )