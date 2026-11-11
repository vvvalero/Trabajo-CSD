"""Aproximaciones de Babai al CVP."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def babai_redondeo(B: Matriz, t: Vector) -> list[int]:
    """Redondeo de Babai (el descifrado de GGH, ver Ejemplo 3 del enunciado): redondeo(t B^-1) B."""
    raise NotImplementedError  # TODO


def babai_plano_cercano(B: Matriz, t: Vector) -> list[int]:
    """Plano mas cercano de Babai (necesita una base reducida con LLL)."""
    raise NotImplementedError  # TODO
