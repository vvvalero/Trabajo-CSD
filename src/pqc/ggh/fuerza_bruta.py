"""Fuerza bruta para SVP/CVP en dimension pequena (defender por que es viable)."""
from __future__ import annotations

import numpy as np


def brute_force(basis: np.ndarray, target: np.ndarray | None, bound: int) -> np.ndarray:
    """Probar coeficientes enteros en [-bound, bound]^n. Coste (2*bound+1)^n."""
    raise NotImplementedError  # TODO
