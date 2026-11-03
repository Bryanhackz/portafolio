"""Bootstrap: aplica migraciones, crea el admin si procede y arranca el servidor."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import config
from data.db import migrate
from data.repositories import users


def bootstrap_admin() -> None:
    if not config.ADMIN_PASSWORD:
        print("ADMIN_PASSWORD no definido: se omite el bootstrap del admin.")
        return
    if users.find_by_email(config.ADMIN_EMAIL):
        print(f"Admin ya existe: {config.ADMIN_EMAIL}")
        return
    users.create(
        email=config.ADMIN_EMAIL,
        name="Administrador",
        password=config.ADMIN_PASSWORD,
        role="admin",
    )
    print(f"Admin creado: {config.ADMIN_EMAIL}")


def main() -> None:
    migrate()
    bootstrap_admin()
    from server import main as serve

    serve()


if __name__ == "__main__":
    main()