"""Headers de seguridad aplicados a todas las respuestas."""

import config


CSP = (
    "default-src 'self'; "
    "script-src 'self' https://www.googletagmanager.com; "
    "style-src 'self'; "
    "img-src 'self' data: https://www.google-analytics.com; "
    "connect-src 'self' https://www.google-analytics.com https://analytics.google.com; "
    "font-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    "form-action 'self'; "
    "object-src 'none'"
)


def base_headers() -> list[tuple[str, str]]:
    headers = [
        ("Content-Security-Policy", CSP),
        ("X-Content-Type-Options", "nosniff"),
        ("X-Frame-Options", "DENY"),
        ("Referrer-Policy", "strict-origin-when-cross-origin"),
        ("Permissions-Policy", "geolocation=(), camera=(), microphone=()"),
        ("Cross-Origin-Opener-Policy", "same-origin"),
    ]
    if config.IS_PRODUCTION:
        headers.append(
            ("Strict-Transport-Security", "max-age=31536000; includeSubDomains; preload")
        )
    return headers