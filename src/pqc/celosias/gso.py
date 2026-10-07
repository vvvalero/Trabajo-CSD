"""Gram-Schmidt de una base. Base comun de LLL, Babai, enumeracion y BKZ.

Convenio: base = matriz n x m (numpy), un vector por FILA.
"""
from __future__ import annotations

import numpy as np


def gso(B: np.ndarray):
    """Devolver (mu, norms2, Bstar) con norms2[i] = ||b*_i||^2."""
    raise NotImplementedError  # TODO
