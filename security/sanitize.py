"""Escapado seguro de contenido para HTML y URLs.

- `safe()`: escape HTML estándar con comillas.
- `safe_url()`: valida esquema y estructura de URL antes de escapar.
  Bloquea `javascript:`, `data:`, `vbscript:`, `file:`, protocol-relative
  (`//evil.com`) y cualquier esquema no permitido.
"""

import re
from html import escape
from urllib.parse import urlparse

_CONTROL_CHARS = re.compile(r"[\x00-\x1f\x7f]")
_ALLOWED_SCHEMES = {"http", "https", "mailto", "tel"}
_MAX_URL_LEN = 2048


def safe(value) -> str:
    if value is None:
        return ""
    return escape(str(value), quote=True)


def safe_url(value: str | None) -> str:
    if not value or not isinstance(value, str):
        return ""
    if len(value) > _MAX_URL_LEN:
        return ""
    cleaned = _CONTROL_CHARS.sub("", value.strip())
    if not cleaned:
        return ""
    try:
        parsed = urlparse(cleaned)
    except ValueError:
        return ""

    scheme = parsed.scheme.lower()
    if scheme not in _ALLOWED_SCHEMES:
        return ""
    if scheme in {"http", "https"}:
        if not parsed.netloc or "/" in parsed.netloc:
            return ""
    if scheme in {"mailto", "tel"}:
        if not parsed.path:
            return ""
    return escape(cleaned, quote=True)