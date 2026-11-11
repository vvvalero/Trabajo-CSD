"""Aproximaciones de Babai al CVP."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def babai_round(B: Matriz, t: Vector) -> list[int]:
    """Redondeo de Babai (el descifrado de GGH, ver Ejemplo 3 del PDF): round(t B^-1) B."""
    raise NotImplementedError  # TODO


def babai_nearest_plane(B: Matriz, t: Vector) -> list[int]:
    """Plano mas cercano de Babai (necesita base reducida)."""
    raise NotImplementedError  # TODO
