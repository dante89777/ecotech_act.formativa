import re

import requests

TIMEOUT = 8
URL_GEOCODIFICACION = "https://geocoding-api.open-meteo.com/v1/search"
URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
PATRON_CIUDAD = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s.'-]{2,50}$")


class ErrorApi(Exception):
    pass


def validar_ciudad(ciudad):
    ciudad = (ciudad or "").strip()
    if not PATRON_CIUDAD.match(ciudad):
        raise ValueError("El nombre de la ciudad contiene caracteres no permitidos.")
    return ciudad


def obtener_coordenadas(ciudad):
    ciudad = validar_ciudad(ciudad)
    respuesta = requests.get(
        URL_GEOCODIFICACION,
        params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    resultados = respuesta.json().get("results")
    if not resultados:
        raise ErrorApi(f"No se encontro la ciudad '{ciudad}'.")
    lugar = resultados[0]
    return lugar["latitude"], lugar["longitude"], lugar["name"]


def obtener_temperatura(latitud=-36.82, longitud=-73.05):
    respuesta = requests.get(
        URL_CLIMA,
        params={
            "latitude": latitud,
            "longitude": longitud,
            "current": "temperature_2m",
        },
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    datos = respuesta.json()
    return datos["current"]["temperature_2m"]


def obtener_clima_por_ciudad(ciudad):
    latitud, longitud, nombre = obtener_coordenadas(ciudad)
    temperatura = obtener_temperatura(latitud, longitud)
    return nombre, temperatura
