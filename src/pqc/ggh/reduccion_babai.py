"""Ataque clasico a GGH: reducir la base publica con LLL y resolver el CVP con Babai."""
from __future__ import annotations

import numpy as np


def attack(basis: np.ndarray, target: np.ndarray | None) -> np.ndarray:
    """SVP si target es None, CVP si no. Usa pqc.celosias (lll, babai, enumeracion)."""
    raise NotImplementedError  # TODO
