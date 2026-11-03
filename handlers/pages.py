import config
from security.i18n import pick_language
from security.sanitize import safe
from handlers._types import Request, Response


def _render(filename: str, context: dict) -> bytes:
    html = (config.FRONTEND_DIR / filename).read_text(encoding="utf-8")
    for key, value in context.items():
        html = html.replace("{{" + key + "}}", safe(value))
    return html.encode("utf-8")


def _base_context(request: Request) -> dict:
    accept_language = request.headers.get("ACCEPT_LANGUAGE", "")
    detected_lang = pick_language(accept_language)

    return {
        "CSRF_TOKEN": request.csrf_token,
        "SITE_URL": config.SITE_URL,
        "SITE_NAME": config.SITE_NAME,
        "EMAIL": config.EMAIL,
        "LINKEDIN": config.LINKEDIN,
        "GITHUB": config.GITHUB,
        "INSTAGRAM": config.INSTAGRAM,
        "FACEBOOK": config.FACEBOOK,
        "DETECTED_LANG": detected_lang,
    }


def index(request: Request) -> Response:
    ctx = _base_context(request)
    return Response(body=_render("index.html", ctx))


def legal(request: Request) -> Response:
    return Response(body=_render("legal.html", _base_context(request)))


def not_found(request: Request) -> Response:
    try:
        body = (config.FRONTEND_DIR / "404.html").read_bytes()
    except FileNotFoundError:
        body = b"<h1>404</h1>"
    return Response(status=404, body=body)