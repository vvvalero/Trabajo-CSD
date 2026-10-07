"""Eliminacion gaussiana modular: resuelve el sistema cuando no hay ruido (o hay muy poco)."""
from __future__ import annotations


def solve_mod(A: list[list[int]], b: list[int], q: int) -> list[int] | None:
    """Resuelve A s = b (mod q) con A cuadrada. None si es singular."""
    raise NotImplementedError  # TODO
