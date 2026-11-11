"""Fuerza bruta: probar los posibles errores y comprobar que el resto de ecuaciones cuadra."""
from __future__ import annotations

from ..lector_tareas import TareaLWE


def fuerza_bruta(tarea: TareaLWE, error_max: int) -> list[int] | None:
    """Idea: elegir n ecuaciones, probar e en [-error_max, error_max]^n, despejar s y
    comprobar que el resto de ecuaciones salen con error acotado. Coste (2*error_max+1)^n."""
    raise NotImplementedError  # TODO
