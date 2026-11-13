"""Punto de entrada GGH: resolver una tarea SVP / CVP."""
from __future__ import annotations

from ..lector_tareas import TareaGGH
from ..celosias import enumeracion, lll
from .celosia_modular import base_modular


def solve(tarea: TareaGGH) -> list[int]:
    """Devuelve el punto solucion (SVP: vector mas corto; CVP: punto de la celosia mas cercano).

    LLL reduce la base sin cambiar la celosia y la enumeracion certifica el optimo.
    Babai proporciona la cota inicial para CVP dentro de la enumeracion. El ataque
    aproximado sigue disponible en reduccion_babai.py para poder comparar.
    Las tareas con "reduccion modulo n" (Tier3) cambian antes la base (celosia_modular.py).
    """
    base = tarea.base
    if tarea.modulo:
        base = base_modular(base, tarea.modulo)
    return enumeracion(lll(base), tarea.objetivo)
