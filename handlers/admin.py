"""Panel de administración y endpoints JSON para proyectos y mensajes."""

import config
from data import authorizer
from data.repositories import messages, projects, users
from security import rate_limit, session as session_mod, validation
from security.sanitize import safe
from handlers._types import Request, Response, json_response, redirect


LOGIN_HTML = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Acceso administrativo</title>
<link rel="stylesheet" href="/css/tokens.css">
<link rel="stylesheet" href="/css/base.css">
<link rel="stylesheet" href="/css/components.css">
<link rel="stylesheet" href="/css/pages/admin.css">
</head>
<body class="login-page">
<main class="login-card">
<h1>Acceso administrativo</h1>
<p class="login-note">Ingresa con tu cuenta autorizada.</p>
{error}
<form method="post" action="/admin/login" class="login-form">
<input type="hidden" name="_csrf" value="{csrf}">
<label>Correo<input type="email" name="email" required autocomplete="username"></label>
<label>Contraseña<input type="password" name="password" required autocomplete="current-password"></label>
<button type="submit" class="btn btn-primary">Entrar</button>
</form>
<div class="login-oauth">
<a class="btn btn-ghost" href="/auth/google">Continuar con Google</a>
<a class="btn btn-ghost" href="/auth/microsoft">Continuar con Microsoft</a>
</div>
</main>
</body>
</html>"""


_PROJECT_FIELDS = [
    validation.Field("slug", required=True, min_len=2, max_len=80),
    validation.Field("title", required=True, min_len=2, max_len=120),
    validation.Field("category", required=True, min_len=2, max_len=60),
    validation.Field("challenge", required=True, min_len=10, max_len=2000),
    validation.Field("solution", required=True, min_len=10, max_len=2000),
    validation.Field("result", required=True, min_len=10, max_len=2000),
]


def _render_login(request: Request, error: str = "") -> Response:
    error_html = f'<p class="login-error">{safe(error)}</p>' if error else ""
    body = (
        LOGIN_HTML.replace("{csrf}", safe(request.csrf_token))
        .replace("{error}", error_html)
        .encode("utf-8")
    )
    return Response(body=body)


def login_page(request: Request) -> Response:
    if request.actor:
        return redirect("/admin")
    return _render_login(request)


def login_submit(request: Request) -> Response:
    if not rate_limit.login_limiter.allow(request.remote_addr):
        return _render_login(request, "Demasiados intentos. Espera unos minutos.")
    form = request.form
    email = (form.get("email") or "").strip()
    password = form.get("password") or ""
    user = users.verify_credentials(email, password)
    if not user:
        return _render_login(request, "Credenciales incorrectas.")
    if user.get("role") != "admin":
        return _render_login(request, "Esta cuenta no tiene acceso administrativo.")
    token = session_mod.create_token(int(user["id"]))
    return redirect(
        "/admin",
        extra_headers=[("Set-Cookie", session_mod.session_cookie_header(token))],
    )


def logout(request: Request) -> Response:
    return redirect(
        "/admin/login",
        extra_headers=[("Set-Cookie", session_mod.clear_session_cookie_header())],
    )


def dashboard(request: Request) -> Response:
    if not request.actor:
        return redirect("/admin/login")
    if request.actor.get("role") != "admin":
        return redirect("/admin/login?error=sin_permiso")
    html = (config.FRONTEND_DIR / "admin.html").read_text(encoding="utf-8")
    html = html.replace("{{CSRF_TOKEN}}", safe(request.csrf_token))
    html = html.replace("{{USER_EMAIL}}", safe(request.actor["email"]))
    return Response(
        body=html.encode("utf-8"),
        extra_headers=[("Cache-Control", "no-store, must-revalidate")],
    )


def _require_admin(actor):
    authorizer.require_admin(actor)


def api_projects_list(request: Request) -> Response:
    try:
        _require_admin(request.actor)
    except authorizer.Unauthorized:
        return json_response({"ok": False}, status=401)
    except authorizer.Forbidden:
        return json_response({"ok": False}, status=403)
    return json_response({"ok": True, "projects": projects.list_all()})


def api_projects_create(request: Request) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    try:
        data = validation.validate(request.json_data, _PROJECT_FIELDS)
    except validation.ValidationError as exc:
        return json_response({"ok": False, "errors": exc.errors}, status=400)
    data["published"] = 1 if request.json_data.get("published", 1) else 0
    try:
        project_id = projects.create(data, request.actor["user_id"])
    except Exception:
        return json_response({"ok": False, "error": "Slug duplicado o inválido"}, status=400)
    return json_response({"ok": True, "id": project_id}, status=201)


def api_projects_update(request: Request, project_id: str) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    try:
        pid = int(project_id)
    except ValueError:
        return json_response({"ok": False, "error": "ID inválido"}, status=400)
    if not projects.get(pid):
        return json_response({"ok": False, "error": "No encontrado"}, status=404)
    try:
        data = validation.validate(request.json_data, _PROJECT_FIELDS)
    except validation.ValidationError as exc:
        return json_response({"ok": False, "errors": exc.errors}, status=400)
    data["published"] = 1 if request.json_data.get("published", 1) else 0
    try:
        projects.update(pid, data)
    except Exception:
        return json_response({"ok": False, "error": "Datos inválidos"}, status=400)
    return json_response({"ok": True})


def api_projects_delete(request: Request, project_id: str) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    try:
        pid = int(project_id)
    except ValueError:
        return json_response({"ok": False, "error": "ID inválido"}, status=400)
    projects.delete(pid)
    return json_response({"ok": True})


def api_messages_list(request: Request) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    return json_response({"ok": True, "messages": messages.list_all()})


def api_messages_read(request: Request, message_id: str) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    try:
        messages.mark_read(int(message_id))
    except ValueError:
        return json_response({"ok": False, "error": "ID inválido"}, status=400)
    return json_response({"ok": True})


def api_messages_delete(request: Request, message_id: str) -> Response:
    try:
        _require_admin(request.actor)
    except (authorizer.Unauthorized, authorizer.Forbidden):
        return json_response({"ok": False}, status=403)
    try:
        messages.delete(int(message_id))
    except ValueError:
        return json_response({"ok": False, "error": "ID inválido"}, status=400)
    return json_response({"ok": True})