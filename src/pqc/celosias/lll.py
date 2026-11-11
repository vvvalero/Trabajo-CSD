"""Reduccion LLL (Lenstra-Lenstra-Lovasz).

Convierte una base en otra de la MISMA celosia con vectores cortos y casi perpendiculares.
Es lo que necesita el atacante de GGH: pasar de la base publica (mala) a una base buena.

Recorremos los vectores uno a uno (k = 1, 2, ...) y con cada b_k hacemos dos cosas:
  1) Reduccion de tamano: si b_k se parece demasiado a un b_j anterior (|mu| > 1/2),
     le restamos b_j un numero entero de veces.
  2) Condicion de Lovasz: si b_k aporta poco "de nuevo" (||b*_k||^2) comparado con b_(k-1),
     estan mal ordenados: los intercambiamos y volvemos un paso atras. Si no, pasamos al siguiente.

Las dos decisiones usan mu y normas2, que salen de gso. Por eso llamamos a gso cada vez que la
base cambia.
"""
from __future__ import annotations

from fractions import Fraction

from ..matrices import Matriz, escalar_por_vector, redondeo, resta_vectores
from .gso import gso


def lll(B: Matriz, delta: Fraction = Fraction(99, 100)) -> list[list[int]]:
    """Devuelve una base LLL-reducida de la misma celosia que B (B con coordenadas enteras).

    delta (entre 1/4 y 1) indica cuanto se exige en la condicion de Lovasz.
    """
    if not Fraction(1, 4) < delta <= 1:
        raise ValueError("delta debe estar entre 1/4 y 1")

    b = [list(fila) for fila in B]          # copia, para no modificar la base original
    k = 1
    while k < len(b):
        # Para decidir sobre b_k solo intervienen b_0, ..., b_k: calculamos gso solo de esos.
        mu, normas2, _ = gso(b[:k + 1])

        # 1) Reduccion de tamano (de j = k-1 hacia atras)
        for j in range(k - 1, -1, -1):
            r = redondeo(mu[k][j])
            if r != 0:
                b[k] = resta_vectores(b[k], escalar_por_vector(r, b[j]))
                mu, normas2, _ = gso(b[:k + 1])     # b_k ha cambiado: recalculamos

        # 2) Condicion de Lovasz
        if normas2[k] >= (delta - mu[k][k - 1] ** 2) * normas2[k - 1]:
            k += 1                                  # bien ordenados: siguiente vector
        else:
            b[k], b[k - 1] = b[k - 1], b[k]         # mal ordenados: intercambiar y retroceder
            k = max(k - 1, 1)
    return b
