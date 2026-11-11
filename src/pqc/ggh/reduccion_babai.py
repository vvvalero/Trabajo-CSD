"""Ataque clasico a GGH: reducir la base publica con LLL y resolver el CVP con Babai."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def attack(basis: Matriz, target: Vector | None) -> list[int]:
    """SVP si target es None, CVP si no. Usa pqc.celosias (lll, babai, enumeracion)."""
    raise NotImplementedError  # TODO
