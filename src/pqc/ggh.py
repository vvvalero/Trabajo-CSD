"""GGH: solver de tareas SVP/CVP + generador/cifrado/descifrado de juguete. ESQUELETO."""
from __future__ import annotations

from .tasks import GGHTask


def solve(task: GGHTask) -> list[int]:
    """Devuelve el vector solucion (SVP: vector mas corto; CVP: punto de la celosia mas cercano).

    Ideas por tier (ver README):
      Tier0  bases (casi) ortogonales -> redondeo de Babai basta
      Tier1/2  dimension pequena -> fuerza bruta / enumeracion; comparar con LLL+Babai
      Tier3  'Reduccion modulo n' -> decidir la interpretacion (ver README, punto abierto)
    """
    raise NotImplementedError  # TODO


def keygen(n: int):
    """TODO (opcional): B, U unimodular, B' = U B  (seccion 2.1 del PDF)."""
    raise NotImplementedError


def encrypt(x, B_pub, e):
    """c = x B' + e"""
    raise NotImplementedError


def decrypt(c, B_priv, U):
    """y = round(c B^-1);  x = y U^-1"""
    raise NotImplementedError
