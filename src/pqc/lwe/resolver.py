"""Rotura de clave LWE: recuperar el vector de secretos s."""
from __future__ import annotations

from ..tareas import LWETask


def break_key(task: LWETask) -> list[int]:
    """Recupera s tal que A s + e = b (mod q), con e pequeno.

    Convenio (Tema 11 y Ejemplo 4 del enunciado): b = A s + e, luego e = b - A s (centrado en (-q/2, q/2]).

    Elegir estrategia segun la tarea (ver README):
      Tier0  pocas incognitas / ruido bajo -> gauss.py o fuerza_bruta.py
      Tier1  fuerza bruta (talla reducida)
      Tier2/3  ataque_celosia.py (el sistema se plantea como celosia)
    """
    raise NotImplementedError  # TODO
