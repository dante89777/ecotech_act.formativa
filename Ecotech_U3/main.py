import sys

import requests
from getpass import getpass

from api_clima import ErrorApi, obtener_clima_por_ciudad
from login import autenticar

MAX_INTENTOS = 3
CIUDAD_POR_DEFECTO = "Santiago"


def pedir_clave():
    if sys.stdin.isatty():
        try:
            return getpass("Clave: ")
        except Exception:
            pass
    return input("Clave: ")


def iniciar_sesion():
    for intento in range(1, MAX_INTENTOS + 1):
        usuario = input("Usuario: ").strip()
        clave = pedir_clave()
        if autenticar(usuario, clave):
            print("Acceso concedido")
            return True
        restantes = MAX_INTENTOS - intento
        print(f"Acceso denegado. Intentos restantes: {restantes}")
    return False


def consultar_clima():
    ciudad = input(f"Ciudad (Enter para {CIUDAD_POR_DEFECTO}): ").strip() or CIUDAD_POR_DEFECTO
    nombre, temperatura = obtener_clima_por_ciudad(ciudad)
    print(f"Temperatura actual en {nombre}: {temperatura} °C")


def main():
    if not iniciar_sesion():
        print("Se agotaron los intentos.")
        return
    try:
        consultar_clima()
    except ValueError as error:
        print(f"Entrada invalida: {error}")
    except ErrorApi as error:
        print(f"Error de la API: {error}")
    except requests.RequestException as error:
        print(f"Error de conexion: {error}")


if __name__ == "__main__":
    main()
