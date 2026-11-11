"""Fuerza bruta para SVP/CVP en dimension pequena (defender por que es viable)."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def brute_force(basis: Matriz, target: Vector | None, bound: int) -> list[int]:
    """Probar coeficientes enteros en [-bound, bound]^n. Coste (2*bound+1)^n."""
    raise NotImplementedError  # TODO
