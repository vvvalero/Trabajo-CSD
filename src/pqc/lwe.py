"""LWE y Ring-LWE: rotura de clave y criptoanalisis de criptogramas. ESQUELETO."""
from __future__ import annotations

from .tasks import LWETask


def break_key(task: LWETask) -> list[int]:
    """Recupera el vector de secretos s tal que A s + e = b (mod q), con e pequeno.

    Ideas: Tier0 pocas incognitas/ruido bajo -> Gauss / fuerza bruta sobre el ruido;
    Tier1 fuerza bruta; Tier2/3 -> reduccion de celosia (q-ary lattice, embedding de Kannan).
    """
    raise NotImplementedError  # TODO


def decrypt_bit(task: LWETask, s: list[int]) -> int:
    """R = C . s mod q; bit 0 si R cerca de B, bit 1 si cerca de B + q/2 (ver Ejemplo 6)."""
    raise NotImplementedError  # TODO


def break_ring_key(task: LWETask) -> list[int]:
    """Ring-LWE en Z_q[x]/(x^n + 1):  b = a*s + e. Recuperar s."""
    raise NotImplementedError  # TODO


def decrypt_ring(task: LWETask, s: list[int]) -> list[int]:
    """Palabra de bits a partir de (c1, c2):  c2 - c1*s  ~  bit * q/2."""
    raise NotImplementedError  # TODO
