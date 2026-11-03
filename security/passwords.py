"""Hashing de contraseñas con scrypt. Comparación en tiempo constante.

Parámetros actuales: N=2**15, r=8, p=1, dklen=64.
Coste aproximado: ~50-100 ms por hash en hardware moderno. Ajusta N si
necesitas más margen, teniendo en cuenta que `n` debe ser potencia de 2.
"""

import hashlib
import hmac
import secrets

_N = 2 ** 15
_R = 8
_P = 1
_DKLEN = 64
_MAX_PASSWORD_LEN = 1024


def hash_password(password: str) -> str:
    if not isinstance(password, str) or not password:
        raise ValueError("La contraseña debe ser un string no vacío")
    if len(password) > _MAX_PASSWORD_LEN:
        raise ValueError("La contraseña excede el tamaño máximo")
    salt = secrets.token_bytes(16)
    dk = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=_N,
        r=_R,
        p=_P,
        dklen=_DKLEN,
    )
    return f"scrypt${_N}${_R}${_P}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    if not stored or not stored.startswith("scrypt$"):
        return False
    if not isinstance(password, str) or len(password) > _MAX_PASSWORD_LEN:
        return False
    try:
        _, n, r, p, salt_hex, dk_hex = stored.split("$")
        n_i, r_i, p_i = int(n), int(r), int(p)
        # Rechaza parámetros fuera de rango razonable (defensa contra
        # hashes almacenados que intenten forzar costes excesivos).
        if not (2 ** 10 <= n_i <= 2 ** 20):
            return False
        if not (1 <= r_i <= 32) or not (1 <= p_i <= 16):
            return False
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(dk_hex)
        if len(salt) < 8 or len(expected) < 32:
            return False
        actual = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n_i,
            r=r_i,
            p=p_i,
            dklen=len(expected),
        )
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False