"""Validación manual de entrada con esquemas declarativos.

- Acepta solo strings en los campos declarados.
- Rechaza campos ausentes si `required=True`.
- `min_len` y `max_len` acotados.
- Validación de email reforzada (longitud RFC, un solo @, dominio con punto).
- `one_of` para listas cerradas.
"""

from dataclasses import dataclass


class ValidationError(Exception):
    def __init__(self, errors: dict[str, str]):
        super().__init__("Datos inválidos")
        self.errors = errors


@dataclass
class Field:
    name: str
    required: bool = True
    min_len: int = 0
    max_len: int = 500
    email: bool = False
    one_of: tuple[str, ...] | None = None
    strip: bool = True


def _is_email(value: str) -> bool:
    if not value or len(value) > 254:
        return False
    if value.count("@") != 1:
        return False
    local, domain = value.rsplit("@", 1)
    if not local or not domain:
        return False
    if len(local) > 64:
        return False
    if "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith("."):
        return False
    if ".." in domain:
        return False
    return True


def validate(data: dict, fields: list[Field]) -> dict:
    if not isinstance(data, dict):
        raise ValidationError({"_": "Payload inválido"})

    out: dict = {}
    errors: dict = {}
    for f in fields:
        raw = data.get(f.name)
        if raw is None:
            if f.required:
                errors[f.name] = "Campo requerido"
            continue
        if not isinstance(raw, str):
            errors[f.name] = "Tipo inválido"
            continue

        value = raw.strip() if f.strip else raw
        if not value:
            if f.required:
                errors[f.name] = "Campo requerido"
            continue
        if len(value) < f.min_len:
            errors[f.name] = f"Debe tener al menos {f.min_len} caracteres"
            continue
        if len(value) > f.max_len:
            errors[f.name] = f"No puede exceder {f.max_len} caracteres"
            continue
        if f.email and not _is_email(value):
            errors[f.name] = "Correo inválido"
            continue
        if f.one_of is not None and value not in f.one_of:
            errors[f.name] = "Valor no permitido"
            continue
        out[f.name] = value
    if errors:
        raise ValidationError(errors)
    return out