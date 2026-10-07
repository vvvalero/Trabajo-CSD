"""Punto de entrada GGH: resolver una tarea SVP / CVP."""
from __future__ import annotations

from ..tareas import GGHTask


def solve(task: GGHTask) -> list[int]:
    """Devuelve el vector solucion (SVP: vector mas corto; CVP: punto de la celosia mas cercano).

    Elegir estrategia segun la tarea (ver README):
      Tier0    bases (casi) ortogonales -> reduccion_babai.py basta
      Tier1/2  dimension pequena -> fuerza_bruta.py o enumeracion; comparar con LLL + Babai
      Tier3    'Reduccion modulo n' -> celosia_modular.py (ver punto abierto del README)
    """
    raise NotImplementedError  # TODO
