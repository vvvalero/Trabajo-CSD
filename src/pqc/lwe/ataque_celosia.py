"""Ataque a LWE por reduccion de celosias: el sistema con ruido se plantea como un CVP.

Usa los algoritmos genericos de pqc.celosias (LLL, Babai, enumeracion).
"""
from __future__ import annotations

from ..tareas import LWETask


def sistema_a_celosia(task: LWETask):
    """Construye la base de la celosia (q-ary) asociada al sistema. Devolver (base, objetivo)."""
    raise NotImplementedError  # TODO


def attack(task: LWETask) -> list[int]:
    """Resuelve el CVP y devuelve el vector de secretos."""
    raise NotImplementedError  # TODO
