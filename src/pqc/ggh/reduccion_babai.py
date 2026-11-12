"""Ataque clasico a GGH: reducir la base publica con LLL y resolver el CVP con Babai.

La base publica es "mala" (vectores largos y casi paralelos) y con ella Babai falla.
LLL la convierte en una base buena de la MISMA celosia, y con esa Babai suele acertar.

Ejemplo (enunciado, Ejemplos 1-3): base publica [[5, 19], [3, 14]] y c = (43, 176)
  - LLL da la base [[-3, -1], [1, -4]]: es la base privada [[3, 1], [-1, 4]] cambiada de signo
  - Babai con esa base da (44, 175), que es el mensaje cifrado
"""
from __future__ import annotations

from ..celosias import babai_plano_cercano, lll
from ..matrices import Matriz, Vector, norma2


def ataque(base: Matriz, objetivo: Vector | None) -> list[int]:
    """SVP si objetivo es None, CVP si no.

    SVP: tras LLL, el vector mas corto de la base reducida (suele ser el primero, pero LLL
         no lo garantiza, asi que cogemos el minimo).
    CVP: Babai (plano mas cercano) con la base reducida.
    Ninguno de los dos garantiza el optimo; para eso hace falta la enumeracion.
    Ejemplo: en Tier02T03 Babai da un punto a distancia^2 186, y existe uno a 155.
    """
    R = lll(base)
    if objetivo is None:
        return min(R, key=norma2)
    # Plano mas cercano y no redondeo: en Tier02T03 queda a 186 en vez de 187 (ver test_babai.py).
    return babai_plano_cercano(R, objetivo)
