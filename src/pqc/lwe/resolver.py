"""Rotura de clave LWE: recuperar el vector de secretos s."""
from __future__ import annotations

from ..tasks import LWETask


def break_key(task: LWETask) -> list[int]:
    """Recupera s tal que A s + e = b (mod q), con e pequeno.

    Elegir estrategia segun la tarea (ver README):
      Tier0  pocas incognitas / ruido bajo -> gauss.py o fuerza_bruta.py
      Tier1  fuerza bruta (talla reducida)
      Tier2/3  ataque_celosia.py (el sistema se plantea como celosia)
    """
    raise NotImplementedError  # TODO
