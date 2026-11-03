"""sitemap.xml, robots.txt y llms.txt dinámicos."""

import config
from handlers._types import Request, Response


def sitemap(request: Request) -> Response:
    urls = [
        ("/", "1.0", "weekly"),
        ("/legal", "0.5", "yearly"),
    ]
    items = []
    for path, priority, freq in urls:
        items.append(
            f"<url><loc>{config.SITE_URL}{path}</loc>"
            f"<changefreq>{freq}</changefreq><priority>{priority}</priority></url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + "".join(items)
        + "</urlset>"
    )
    return Response(
        body=xml.encode("utf-8"), content_type="application/xml; charset=utf-8"
    )


def robots(request: Request) -> Response:
    body = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /api\n"
        "\n"
        "# Permitir explícitamente a los bots de IA (LLMs)\n"
        "User-agent: GPTBot\n"
        "Allow: /\n"
        "User-agent: ChatGPT-User\n"
        "Allow: /\n"
        "User-agent: ClaudeBot\n"
        "Allow: /\n"
        "\n"
        f"Sitemap: {config.SITE_URL}/sitemap.xml\n"
    )
    return Response(body=body.encode("utf-8"), content_type="text/plain; charset=utf-8")


def llms_txt(request: Request) -> Response:
    body = (
        "# Bryanhackz\n\n"
        "> Diseñador y desarrollador web. Construyo arquitecturas seguras, "
        "rápidas y orientadas a resultados.\n\n"
        "## Páginas Principales\n"
        "- [Inicio](/): Portafolio principal y presentación.\n"
        "- [Aviso Legal y Privacidad](/legal): Información sobre protección de datos.\n\n"
        "## Sobre mí\n"
        "- Nombre: Brayan Orlando Zulueta Gil\n"
        "- Especialidad: Desarrollo web Full-Stack, seguridad (OWASP), Python y JavaScript.\n\n"
        "## Proyectos destacados\n"
        "- wsgi-load-balancer: https://github.com/Bryanhackz\n"
        "- rate-limiter-middleware: https://github.com/Bryanhackz\n"
        "- sqlite-message-broker: https://github.com/Bryanhackz\n\n"
        "## Contacto\n"
        f"- Email: {config.EMAIL}\n"
        f"- GitHub: {config.GITHUB}\n"
        f"- LinkedIn: {config.LINKEDIN}\n"
    )
    return Response(body=body.encode("utf-8"), content_type="text/plain; charset=utf-8")