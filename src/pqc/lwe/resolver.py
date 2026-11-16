"""Rotura de clave LWE: recuperar el vector de secretos s."""
from __future__ import annotations

from ..lector_tareas import TareaLWE
from .ataque_celosia import ataque
from .fuerza_bruta import fuerza_bruta

# Maximo de intentos de la fuerza bruta: (2*error_max + 1)^n. Con 10^6 tarda como mucho ~20 s.
# Ejemplo: Tier2T03 (n = 5) necesita error_max = 6, es decir 13^5 = 371 293 intentos (con 10^5 no salia).
MAX_INTENTOS = 10**6


def romper_clave(tarea: TareaLWE) -> list[int]:
    """Recupera s tal que A s + e = b (mod q), con e pequeno.

    Convenio (Tema 11 y Ejemplo 4 del enunciado): b = A s + e, luego e = b - A s (centrado).

    Probamos la fuerza bruta con error_max = 0, 1, 2, ... Asi, si no hay error (Tier0T01/T02),
    sale a la primera y es simplemente resolver el sistema con la inversa modulo q.
    Si el numero de intentos pasaria de MAX_INTENTOS (n grande o error grande), usamos el
    ataque de celosia: el CVP en la celosia q-aria de A (ataque_celosia.py).
    """
    error_max = 0
    while (2 * error_max + 1) ** tarea.n <= MAX_INTENTOS:
        s = fuerza_bruta(tarea, error_max)
        if s is not None:
            return s
        error_max += 1
    return ataque(tarea)
