"""Busqueda exacta de SVP / CVP (Fincke-Pohst / Schnorr-Euchner)."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def enumeracion(B: Matriz, objetivo: Vector | None = None) -> list[int]:
    """SVP si objetivo es None, CVP si no. Devuelve el vector de la celosia optimo."""
    raise NotImplementedError  # TODO
