"""Celosias con 'reduccion modulo n' (Tier3): la celosia es L(B) + nZ^d."""
from __future__ import annotations

import numpy as np


def base_modular(basis: np.ndarray, n: int) -> np.ndarray:
    """Base (p. ej. via forma normal de Hermite) de la celosia modular.
    Comprobar primero si det(B) es invertible mod n: entonces la celosia es todo Z^d."""
    raise NotImplementedError  # TODO
