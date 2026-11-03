"""Tipos HTTP internos: Request, Response y helper de redirección."""

import json
from dataclasses import dataclass, field
from urllib.parse import parse_qs


@dataclass
class Request:
    method: str
    path: str
    query: dict
    headers: dict
    cookies: dict
    body: bytes
    remote_addr: str
    actor: dict | None = None
    csrf_token: str = ""

    @property
    def form(self) -> dict:
        ctype = self.headers.get("CONTENT_TYPE", "")
        if "application/x-www-form-urlencoded" not in ctype:
            return {}
        text = self.body.decode("utf-8", "replace")
        return {k: v[0] for k, v in parse_qs(text, keep_blank_values=True).items()}

    @property
    def json_data(self):
        ctype = self.headers.get("CONTENT_TYPE", "")
        if "application/json" not in ctype:
            return {}
        try:
            return json.loads(self.body.decode("utf-8"))
        except (ValueError, TypeError):
            return {}


@dataclass
class Response:
    status: int = 200
    body: bytes = b""
    content_type: str = "text/html; charset=utf-8"
    extra_headers: list[tuple[str, str]] = field(default_factory=list)


def redirect(location: str, extra_headers: list[tuple[str, str]] | None = None) -> Response:
    headers = [("Location", location)]
    if extra_headers:
        headers.extend(extra_headers)
    return Response(status=302, body=b"", extra_headers=headers)


def json_response(payload, status: int = 200) -> Response:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return Response(status=status, body=body, content_type="application/json; charset=utf-8")