"""Gram-Schmidt de una base. Base comun de LLL, Babai, enumeracion y BKZ.

Convenio: base = lista de filas (int o Fraction), un vector por FILA. Aritmetica exacta con Fraction.
"""
from __future__ import annotations

from ..matrices import Matriz


def gso(B: Matriz) -> tuple[Matriz, list, Matriz]:
    """Devolver (mu, norms2, Bstar), todo en Fraction:
      Bstar[i]  = b*_i = b_i - sum_{j<i} mu[i][j] * b*_j
      mu[i][j]  = <b_i, b*_j> / ||b*_j||^2   (para j < i)
      norms2[i] = ||b*_i||^2
    """
    raise NotImplementedError  # TODO
