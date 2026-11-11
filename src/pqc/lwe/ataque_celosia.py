"""Ataque a LWE por reduccion de celosias (ataque primal): el error e es un vector corto.

Usa los algoritmos genericos de pqc.celosias (LLL, Babai, enumeracion).
"""
from __future__ import annotations

from ..lector_tareas import TareaLWE


def sistema_a_celosia(tarea: TareaLWE):
    """Construye la base de la celosia (q-aria) asociada al sistema. Devolver (base, objetivo)."""
    raise NotImplementedError  # TODO


def ataque(tarea: TareaLWE) -> list[int]:
    """Encuentra el vector corto (el error) y devuelve el vector de secretos s."""
    raise NotImplementedError  # TODO
