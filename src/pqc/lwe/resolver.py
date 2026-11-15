"""Rotura de clave LWE: recuperar el vector de secretos s."""
from __future__ import annotations

from ..lector_tareas import TareaLWE
from .fuerza_bruta import fuerza_bruta

# Maximo de intentos de la fuerza bruta: (2*error_max + 1)^n. Con 10^5 tarda como mucho ~2 s.
MAX_INTENTOS = 10**5


def romper_clave(tarea: TareaLWE) -> list[int]:
    """Recupera s tal que A s + e = b (mod q), con e pequeno.

    Convenio (Tema 11 y Ejemplo 4 del enunciado): b = A s + e, luego e = b - A s (centrado).

    Probamos la fuerza bruta con error_max = 0, 1, 2, ... Asi, si no hay error (Tier0T01/T02),
    sale a la primera y es simplemente resolver el sistema con la inversa modulo q.
    Paramos cuando el numero de intentos pasa de MAX_INTENTOS: esas tareas (n grande o error
    grande) necesitan el ataque de celosia (ataque_celosia.py).
    """
    error_max = 0
    while (2 * error_max + 1) ** tarea.n <= MAX_INTENTOS:
        s = fuerza_bruta(tarea, error_max)
        if s is not None:
            return s
        error_max += 1
    raise NotImplementedError("Fuerza bruta demasiado cara: falta el ataque de celosia")
