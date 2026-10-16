import hashlib
import hmac
import re

from usuarios import ITERACIONES, usuarios

PATRON_USUARIO = re.compile(r"^[A-Za-z0-9_.\-]{3,20}$")
MIN_CLAVE, MAX_CLAVE = 4, 64


def validar_usuario(usuario):
    return bool(usuario) and bool(PATRON_USUARIO.match(usuario))


def validar_clave(clave):
    return isinstance(clave, str) and MIN_CLAVE <= len(clave) <= MAX_CLAVE


def _calcular_hash(clave, salt_hex):
    salt = bytes.fromhex(salt_hex)
    return hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), salt, ITERACIONES).hex()


def autenticar(usuario, clave):
    usuario = (usuario or "").strip()
    if not validar_usuario(usuario) or not validar_clave(clave):
        return False
    credencial = usuarios.get(usuario)
    if credencial is None:
        return False
    calculado = _calcular_hash(clave, credencial["salt"])
    return hmac.compare_digest(calculado, credencial["hash"])
