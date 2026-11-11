"""Gram-Schmidt de una base. Base comun de LLL, Babai y enumeracion.

Idea: a partir de los vectores de la base b_0, b_1, ... construimos vectores b*_0, b*_1, ...
PERPENDICULARES entre si. A cada b_i le quitamos su "sombra" (proyeccion) sobre los b*
anteriores; lo que queda es perpendicular a todos ellos.

Ejemplo (base privada del enunciado), B = [[3, 1], [-1, 4]]:
  b*_0 = (3, 1)                                       ||b*_0||^2 = 10
  mu_10 = <(-1, 4), (3, 1)> / 10 = 1/10
  b*_1 = (-1, 4) - 1/10 * (3, 1) = (-13/10, 39/10)    ||b*_1||^2 = 169/10
"""
from __future__ import annotations

from fractions import Fraction

from ..matrices import Matriz, escalar_por_vector, norma2, producto_escalar, resta_vectores


def gso(B: Matriz) -> tuple[Matriz, list[Fraction], Matriz]:
    """Devuelve (mu, normas2, Bstar), todo con fracciones exactas:
      Bstar[i]   = b*_i = b_i - suma de mu[i][j] * b*_j   (para j < i)
      mu[i][j]   = <b_i, b*_j> / ||b*_j||^2               (cuanto de b*_j hay en b_i)
      normas2[i] = ||b*_i||^2
    """
    n = len(B)
    mu = [[Fraction(0)] * n for _ in range(n)]
    Bstar = []
    normas2 = []

    for i in range(n):
        v = [Fraction(x) for x in B[i]]                   # empezamos con una copia de b_i
        for j in range(i):
            mu[i][j] = producto_escalar(B[i], Bstar[j]) / normas2[j]
            v = resta_vectores(v, escalar_por_vector(mu[i][j], Bstar[j]))   # quitamos la sombra sobre b*_j
        mu[i][i] = Fraction(1)                            # asi se cumple B = mu * Bstar

        norma = norma2(v)
        if norma == 0:
            raise ValueError(f"Los vectores no son independientes (b*_{i} = 0)")
        Bstar.append(v)
        normas2.append(norma)

    return mu, normas2, Bstar
