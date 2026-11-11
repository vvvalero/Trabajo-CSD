"""Celosias con 'reduccion modulo n' (Tier3): la celosia es L(B) + nZ^d."""
from __future__ import annotations

from ..matrices import Matriz


def base_modular(base: Matriz, n: int) -> list[list[int]]:
    """Base de la celosia modular.
    Comprobar primero si det(B) es invertible mod n: entonces la celosia es todo Z^d."""
    raise NotImplementedError  # TODO
