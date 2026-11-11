"""Ataque clasico a GGH: reducir la base publica con LLL y resolver el CVP con Babai."""
from __future__ import annotations

from ..matrices import Matriz, Vector


def ataque(base: Matriz, objetivo: Vector | None) -> list[int]:
    """SVP si objetivo es None, CVP si no. Usa pqc.celosias (lll, babai, enumeracion)."""
    raise NotImplementedError  # TODO
