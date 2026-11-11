"""Punto de entrada GGH: resolver una tarea SVP / CVP."""
from __future__ import annotations

from ..lector_tareas import TareaGGH
from . import reduccion_babai
from .celosia_modular import base_modular


def solve(tarea: TareaGGH) -> list[int]:
    """Devuelve el punto solucion (SVP: vector mas corto; CVP: punto de la celosia mas cercano).

    Por ahora todas las tareas van por LLL + Babai (reduccion_babai.py). Cuando esten la
    enumeracion y la fuerza bruta se podra comparar y elegir.
    Las tareas con "reduccion modulo n" (Tier3) cambian antes la base (celosia_modular.py).
    """
    base = tarea.base
    if tarea.modulo:
        base = base_modular(base, tarea.modulo)
    return reduccion_babai.ataque(base, tarea.objetivo)
