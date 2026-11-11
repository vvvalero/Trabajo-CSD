"""Algoritmos de Babai: dado un punto t, encontrar un punto de la celosia cercano (CVP aproximado).

Los dos funcionan bien solo si la base es buena (casi perpendicular). Con la base publica de GGH
fallan; con la base reducida por LLL suelen acertar. Por eso el ataque a GGH es: LLL y despues Babai.
Ninguno garantiza el punto MAS cercano: para eso hace falta la enumeracion.

Ejemplo (enunciado, Ejemplos 1-3): c = (43, 176)
  - con la base privada [[3, 1], [-1, 4]]          -> (44, 175)  correcto
  - con la base publica [[5, 19], [3, 14]]         -> (45, 184)  incorrecto
  - con la publica reducida por LLL                -> (44, 175)  correcto
"""
from __future__ import annotations

from ..matrices import (
    Matriz,
    Vector,
    escalar_por_vector,
    inversa,
    producto_escalar,
    redondeo,
    redondeo_vector,
    resta_vectores,
    vector_por_matriz,
)
from .gso import gso


def babai_redondeo(B: Matriz, t: Vector) -> list[int]:
    """Redondeo de Babai: es el descifrado de GGH (Ejemplo 3 del enunciado).

    Escribimos t en coordenadas de la base, redondeamos TODAS las coordenadas a la vez y
    volvemos a multiplicar por la base. B debe ser cuadrada.
    """
    coordenadas = vector_por_matriz(t, inversa(B))      # t = coordenadas * B (con fracciones)
    x = redondeo_vector(coordenadas)                    # coordenadas enteras mas cercanas
    return vector_por_matriz(x, B)                      # el punto de la celosia x * B


def babai_plano_cercano(B: Matriz, t: Vector) -> list[int]:
    """Plano mas cercano de Babai: como el redondeo, pero coordenada a coordenada.

    Empezamos por el ultimo vector y vamos hacia el primero. En cada paso miramos cuantas veces
    cabe b_i en lo que queda por aproximar (proyectando sobre b*_i), redondeamos, y restamos
    ese multiplo de b_i. Asi cada redondeo tiene en cuenta los anteriores.
    Con una base reducida por LLL, el punto esta como mucho a 2^(n/2) veces la distancia minima.
    """
    _, normas2, Bstar = gso(B)
    n = len(B)
    x = [0] * n
    resto = list(t)                                     # lo que queda por aproximar
    for i in range(n - 1, -1, -1):
        x[i] = redondeo(producto_escalar(resto, Bstar[i]) / normas2[i])
        resto = resta_vectores(resto, escalar_por_vector(x[i], B[i]))
    return vector_por_matriz(x, B)                      # el punto de la celosia x * B
