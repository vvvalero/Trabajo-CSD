"""Busqueda exacta de SVP / CVP (fuerza bruta acotada, Fincke-Pohst / Schnorr-Euchner)."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def enumerate_short(B: Matriz, target: Vector | None = None) -> list[int]:
    """SVP si target es None, CVP si no. Devuelve el vector de la celosia optimo."""
    raise NotImplementedError  # TODO
