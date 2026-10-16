import hashlib
import os

ITERACIONES = 200_000
LARGO_SALT = 16


def crear_credencial(clave, salt=None):
    if salt is None:
        salt = os.urandom(LARGO_SALT)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    hash_clave = hashlib.pbkdf2_hmac("sha256", clave.encode("utf-8"), salt, ITERACIONES)
    return {"salt": salt.hex(), "hash": hash_clave.hex()}


def imprimir_credencial(usuario, clave):
    credencial = crear_credencial(clave)
    print(f'    "{usuario}": {{"salt": "{credencial["salt"]}", "hash": "{credencial["hash"]}"}},')


usuarios = {
    "admin": {
        "salt": "bdd2fa7f28b223812f67c749e2ec6007",
        "hash": "45c4897a5d77b871e4d6c3caa30b935c6de6da3c7169b4a46cad4df92de0260e",
    },
}


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 3:
        imprimir_credencial(sys.argv[1], sys.argv[2])
    else:
        print("Uso: python usuarios.py <usuario> <clave>")
