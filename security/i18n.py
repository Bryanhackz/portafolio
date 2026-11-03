"""Selección de idioma a partir de Accept-Language.

Bounded: el header se trunca y el número de partes se limita para evitar
DoS por headers gigantes. Solo se aceptan calidades en (0, 1].
"""

SUPPORTED_LANGUAGES = ("en", "es", "it", "pt", "fr", "zh", "ja", "ko")
DEFAULT_LANGUAGE = "en"

_MAX_HEADER_LEN = 1024
_MAX_PARTS = 32
_MAX_TAG_LEN = 32


def parse_accept_language(header: str) -> list[str]:
    """Parsea Accept-Language y devuelve tags ordenados por calidad (q).

    - Ignora tags vacíos, demasiado largos o con q<=0.
    - Desempata por orden de aparición.
    """
    if not header or len(header) > _MAX_HEADER_LEN:
        return []

    langs: list[tuple[float, int, str]] = []
    for index, part in enumerate(header.split(",")[:_MAX_PARTS]):
        tag, _, params = part.strip().partition(";")
        tag = tag.strip()
        if not tag or len(tag) > _MAX_TAG_LEN:
            continue

        quality = 1.0
        for param in params.split(";"):
            key, _, value = param.strip().partition("=")
            if key.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
                break

        if 0 < quality <= 1:
            langs.append((-quality, index, tag))

    return [tag for _, _, tag in sorted(langs)]


def pick_language(header: str, default: str = DEFAULT_LANGUAGE) -> str:
    """Devuelve el mejor idioma soportado según la cabecera."""
    supported = {lang.lower(): lang for lang in SUPPORTED_LANGUAGES}

    for tag in parse_accept_language(header):
        normalized = tag.lower()
        if normalized in supported:
            return supported[normalized]

        base = normalized.split("-")[0]
        if base in supported:
            return supported[base]

    return default