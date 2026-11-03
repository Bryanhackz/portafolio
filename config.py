"""Configuración central: carga .env, expone constantes tipadas al resto del proyecto."""

import os
import secrets as _secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"
STORAGE_DIR = BASE_DIR / "storage"
MIGRATIONS_DIR = BASE_DIR / "data" / "migrations"


def _load_env() -> None:
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


_load_env()


ENV = os.environ.get("APP_ENV", "development").lower()
IS_PRODUCTION = ENV in ("production", "prod")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if IS_PRODUCTION:
        raise RuntimeError(
            "SECRET_KEY no está definida. En producción es obligatoria. "
            "Genera una con: python -c \"import secrets;print(secrets.token_hex(32))\""
        )
    SECRET_KEY = _secrets.token_hex(32)

DB_PATH = os.environ.get("DB_PATH", str(STORAGE_DIR / "app.db"))
SESSION_COOKIE = "bozg_session"
CSRF_COOKIE = "bozg_csrf"
SESSION_TTL = 60 * 60 * 8
OAUTH_STATE_TTL = 600  # 10 minutos

SITE_URL = os.environ.get("SITE_URL", f"http://{HOST}:{PORT}")
SITE_NAME = "Brayan Orlando Zulueta Gil"

EMAIL = os.environ.get("CONTACT_EMAIL", "br4yangil006@gmail.com")
LINKEDIN = os.environ.get(
    "LINKEDIN_URL", "https://www.linkedin.com/in/brayan-gil-68b70338b"
)
GITHUB = os.environ.get("GITHUB_URL", "https://github.com/Bryanhackz")
INSTAGRAM = os.environ.get("INSTAGRAM_URL", "https://instagram.com/brayanzulueta")
FACEBOOK = os.environ.get("FACEBOOK_URL", "https://facebook.com/brayanzulueta")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
MICROSOFT_CLIENT_ID = os.environ.get("MICROSOFT_CLIENT_ID", "")
MICROSOFT_CLIENT_SECRET = os.environ.get("MICROSOFT_CLIENT_SECRET", "")
OAUTH_REDIRECT_BASE = os.environ.get("OAUTH_REDIRECT_BASE", SITE_URL)

ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
ADMIN_EMAILS = {
    e.strip().lower()
    for e in os.environ.get("ADMIN_EMAILS", "").split(",")
    if e.strip()
}
if ADMIN_EMAIL:
    ADMIN_EMAILS.add(ADMIN_EMAIL.lower().strip())

MAX_BODY_BYTES = 64 * 1024