"""Endpoint POST /api/contact con validación y rate limiting."""

from data.repositories import messages
from security import rate_limit, validation
from handlers._types import Request, Response, json_response


_FIELDS = [
    validation.Field("name", required=True, min_len=2, max_len=80),
    validation.Field("email", required=True, email=True, max_len=120),
    validation.Field("body", required=True, min_len=10, max_len=2000),
]


def submit(request: Request) -> Response:
    if not rate_limit.contact_limiter.allow(request.remote_addr):
        return json_response(
            {"ok": False, "error": "Demasiadas solicitudes. Intenta en un minuto."},
            status=429,
        )
    try:
        data = validation.validate(request.json_data or request.form, _FIELDS)
    except validation.ValidationError as exc:
        return json_response({"ok": False, "errors": exc.errors}, status=400)
    messages.create(data["name"], data["email"], data["body"])
    return json_response({"ok": True})