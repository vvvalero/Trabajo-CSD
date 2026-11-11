"""Reduccion LLL. Util para: base publica GGH -> base 'buena', celosias q-arias de LWE."""
from __future__ import annotations

from fractions import Fraction

from ..matrices import Matriz


def lll(B: Matriz, delta: Fraction = Fraction(99, 100)) -> list[list[int]]:
    """Base LLL-reducida (filas enteras) de la misma celosia que B. Exacto (Fraction)."""
    raise NotImplementedError  # TODO
