"""Busqueda exacta de SVP / CVP (fuerza bruta acotada, Fincke-Pohst / Schnorr-Euchner)."""
from __future__ import annotations

import numpy as np


def enumerate_short(B: np.ndarray, target: np.ndarray | None = None):
    """SVP si target es None, CVP si no."""
    raise NotImplementedError  # TODO
