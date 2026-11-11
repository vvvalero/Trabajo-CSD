"""Fuerza bruta para SVP/CVP en dimension pequena (defender por que es viable)."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def fuerza_bruta(base: Matriz, objetivo: Vector | None, cota: int) -> list[int]:
    """Probar todos los coeficientes enteros en [-cota, cota]^n. Coste (2*cota+1)^n."""
    raise NotImplementedError  # TODO
