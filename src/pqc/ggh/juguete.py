"""GGH de juguete (seccion 2.1 del enunciado): generar claves, cifrar y descifrar.

Sirve para crear ejemplos propios con los que probar los ataques y medir tiempos.
"""
from __future__ import annotations

import random

from ..matrices import (
    es_entera,
    identidad,
    inversa,
    producto_matrices,
    redondeo_vector,
    suma_vectores,
    vector_por_matriz,
)


def _unimodular_aleatoria(n: int, rng: random.Random, pasos: int, k_max: int):
    """Matriz con determinante +-1, hecha a partir de la identidad con operaciones de filas.

    En cada paso: o se intercambian dos filas, o a una fila se le suma k veces otra.
    Ninguna de las dos operaciones cambia el valor absoluto del determinante, asi que
    el resultado sigue teniendo determinante +-1 (es unimodular).
    """
    U = identidad(n)
    for _ in range(pasos):
        i, j = rng.sample(range(n), 2)
        if rng.random() < 0.1:
            U[i], U[j] = U[j], U[i]
        else:
            k = rng.choice([c for c in range(-k_max, k_max + 1) if c != 0])
            U[i] = [a + k * b for a, b in zip(U[i], U[j])]
    return U


def generar_claves(n: int, semilla: int | None = None, diag: int = 50, fuera: int = 3,
                   pasos: int | None = None):
    """Devuelve (B, U, B_pub): clave privada (B, U) y clave publica B_pub = U B.

    B: base "buena", casi ortogonal: diagonal grande (entre diag y 2*diag) y el resto pequeno
       (entre -fuera y fuera). Si diag > n*fuera, la diagonal domina y det(B) != 0.
    U: matriz unimodular con numeros grandes, para que B_pub sea una base "mala" de la misma celosia.
    La misma semilla da siempre las mismas claves.
    """
    if n < 2 or diag <= n * fuera:
        raise ValueError("Hace falta n >= 2 y diag > n*fuera (para que det(B) != 0)")
    rng = random.Random(semilla)
    B = [[rng.randint(diag, 2 * diag) if i == j else rng.randint(-fuera, fuera) for j in range(n)]
         for i in range(n)]
    U = _unimodular_aleatoria(n, rng, pasos if pasos is not None else 4 * n * n, k_max=2)
    return B, U, producto_matrices(U, B)


def cifrar(x, B_pub, e):
    """c = x B_pub + e  (mensaje x, error pequeno e)."""
    if not len(x) == len(e) == len(B_pub):
        raise ValueError("x, e y la base deben tener la misma dimension")
    return suma_vectores(vector_por_matriz(x, B_pub), e)


def descifrar(c, B, U):
    """Descifrado legitimo: y = redondeo(c B^-1) y despues x = y U^-1.

    Funciona si el error es pequeno: c B^-1 = x U + e B^-1, y el redondeo elimina e B^-1.
    """
    y = redondeo_vector(vector_por_matriz(c, inversa(B)))
    x = vector_por_matriz(y, inversa(U))
    if not es_entera(x):
        raise ValueError("x no es entero: error demasiado grande o claves incoherentes")
    return [int(v) for v in x]
