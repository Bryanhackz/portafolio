"""Router WSGI: aplica headers, gestiona sesión y CSRF, despacha a handlers."""

import mimetypes
from urllib.parse import parse_qs

import config
from data.repositories import users
from security import csrf as csrf_mod, headers as security_headers, session as session_mod
from handlers import admin, api_auth, api_contact, health, pages, seo
from handlers._types import Request, Response


_SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}
_CSRF_EXEMPT_PATHS = {
    "/auth/google/callback",
    "/auth/microsoft/callback",
}


def _parse_cookies(header: str) -> dict[str, str]:
    out: dict[str, str] = {}
    if not header:
        return out
    for part in header.split(";"):
        if "=" not in part:
            continue
        key, _, value = part.partition("=")
        out[key.strip()] = value.strip()
    return out


def _read_body(environ) -> bytes:
    try:
        length = int(environ.get("CONTENT_LENGTH", "0") or 0)
    except ValueError:
        length = 0
    if length <= 0:
        return b""
    length = min(length, config.MAX_BODY_BYTES)
    return environ["wsgi.input"].read(length)


def _match_pattern(pattern: str, path: str) -> dict | None:
    if "<" not in pattern:
        return {} if pattern == path else None
    parts_p = pattern.split("/")
    parts_x = path.split("/")
    if len(parts_p) != len(parts_x):
        return None
    params: dict[str, str] = {}
    for pp, px in zip(parts_p, parts_x):
        if pp.startswith("<") and pp.endswith(">"):
            params[pp[1:-1]] = px
        elif pp != px:
            return None
    return params


_ROUTES = [
    ("GET", "/", pages.index),
    ("GET", "/index.html", pages.index),
    ("GET", "/legal", pages.legal),
    ("GET", "/admin", admin.dashboard),
    ("GET", "/admin.html", admin.dashboard),
    ("GET", "/admin/login", admin.login_page),
    ("POST", "/admin/login", admin.login_submit),
    ("POST", "/admin/logout", admin.logout),
    ("POST", "/api/contact", api_contact.submit),
    ("GET", "/auth/<provider>", api_auth.start),
    ("GET", "/auth/<provider>/callback", api_auth.callback),
    ("GET", "/sitemap.xml", seo.sitemap),
    ("GET", "/robots.txt", seo.robots),
    ("GET", "/llms.txt", seo.llms_txt),
    ("GET", "/health", health.check),
    ("GET", "/api/admin/projects", admin.api_projects_list),
    ("POST", "/api/admin/projects", admin.api_projects_create),
    ("PUT", "/api/admin/projects/<project_id>", admin.api_projects_update),
    ("DELETE", "/api/admin/projects/<project_id>", admin.api_projects_delete),
    ("GET", "/api/admin/messages", admin.api_messages_list),
    ("POST", "/api/admin/messages/<message_id>/read", admin.api_messages_read),
    ("DELETE", "/api/admin/messages/<message_id>", admin.api_messages_delete),
]


def _dispatch(method: str, path: str, request: Request) -> Response | None:
    for route_method, pattern, handler in _ROUTES:
        if route_method != method:
            continue
        params = _match_pattern(pattern, path)
        if params is None:
            continue
        return handler(request, **params)
    return None


def _serve_static(path: str) -> Response | None:
    rel = path.lstrip("/")
    if not rel:
        return None
    if ".." in rel.split("/") or ".." in rel.split("\\") or rel.startswith("."):
        return None
    target = (config.FRONTEND_DIR / rel).resolve()
    try:
        target.relative_to(config.FRONTEND_DIR.resolve())
    except ValueError:
        return None
    if not target.is_file():
        return None
    ctype = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
    if ctype.startswith("text/") or ctype in (
        "application/javascript",
        "application/json",
    ):
        ctype += "; charset=utf-8"
    return Response(body=target.read_bytes(), content_type=ctype)


def _validate_csrf(request: Request) -> bool:
    if request.method in _SAFE_METHODS:
        return True
    if request.path in _CSRF_EXEMPT_PATHS:
        return True
    cookie_token = request.cookies.get(config.CSRF_COOKIE)
    submitted = (
        request.headers.get("X_CSRF_TOKEN")
        or request.headers.get("HTTP_X_CSRF_TOKEN")
        or request.form.get("_csrf")
    )
    return csrf_mod.token_matches(cookie_token, submitted)


def _status_text(status: int) -> str:
    return {
        200: "OK", 201: "Created", 204: "No Content", 302: "Found",
        400: "Bad Request", 401: "Unauthorized", 403: "Forbidden",
        404: "Not Found", 405: "Method Not Allowed", 413: "Payload Too Large",
        429: "Too Many Requests", 500: "Internal Server Error",
    }.get(status, "OK")


def _build_headers(environ) -> dict[str, str]:
    headers: dict[str, str] = {}
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            headers[k[5:]] = v
        elif k in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            headers[k] = v
    return headers


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET").upper()
    path = environ.get("PATH_INFO", "/") or "/"
    query = parse_qs(environ.get("QUERY_STRING", ""), keep_blank_values=True)
    headers = _build_headers(environ)
    cookies = _parse_cookies(environ.get("HTTP_COOKIE", ""))
    body = _read_body(environ)
    remote_addr = environ.get("REMOTE_ADDR", "0.0.0.0")

    csrf_token = cookies.get(config.CSRF_COOKIE) or csrf_mod.new_token()

    actor = None
    payload = session_mod.verify_token(cookies.get(config.SESSION_COOKIE))
    if payload:
        user = users.get(payload["uid"])
        if user:
            actor = {
                "user_id": int(user["id"]),
                "email": user["email"],
                "role": user["role"],
            }

    request = Request(
        method=method,
        path=path,
        query=query,
        headers=headers,
        cookies=cookies,
        body=body,
        remote_addr=remote_addr,
        actor=actor,
        csrf_token=csrf_token,
    )

    if not _validate_csrf(request):
        response = Response(
            status=403,
            body=b"<h1>403 CSRF</h1>",
            content_type="text/html; charset=utf-8",
        )
    else:
        try:
            response = _dispatch(method, path, request)
        except Exception:
            import traceback
            if not config.IS_PRODUCTION:
                traceback.print_exc()
            response = Response(
                status=500,
                body=b"<h1>500</h1>",
                content_type="text/html; charset=utf-8",
            )
        if response is None:
            response = _serve_static(path)
        if response is None:
            response = pages.not_found(request)

    out_headers = security_headers.base_headers()
    out_headers.append(("Content-Type", response.content_type))
    out_headers.append(("Content-Length", str(len(response.body))))
    if response.status == 429:
        out_headers.append(("Retry-After", "60"))
    if response.extra_headers:
        out_headers.extend(response.extra_headers)

    if response.content_type.startswith("text/html"):
        if config.CSRF_COOKIE not in cookies:
            out_headers.append(("Set-Cookie", csrf_mod.csrf_cookie_header(csrf_token)))

    start_response(f"{response.status} {_status_text(response.status)}", out_headers)
    return [response.body]