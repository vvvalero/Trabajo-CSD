"""Rotura de clave LWE: recuperar el vector de secretos s."""
from __future__ import annotations

from ..lector_tareas import TareaLWE


def romper_clave(tarea: TareaLWE) -> list[int]:
    """Recupera s tal que A s + e = b (mod q), con e pequeno.

    Convenio (Tema 11 y Ejemplo 4 del enunciado): b = A s + e, luego e = b - A s (centrado).

    Elegir estrategia segun la tarea (ver README):
      Tier0    sin error -> s = inversa_mod(A, q) * b (matrices.py); con poco error -> fuerza_bruta.py
      Tier1    fuerza_bruta.py (talla reducida)
      Tier2/3  ataque_celosia.py (el sistema se plantea como celosia)
    """
    raise NotImplementedError  # TODO
