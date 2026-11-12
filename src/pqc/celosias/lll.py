"""Reduccion LLL (Lenstra-Lenstra-Lovasz).

Convierte una base en otra de la MISMA celosia con vectores cortos y casi perpendiculares.
Es lo que necesita el atacante de GGH: pasar de la base publica (mala) a una base buena.

Recorremos los vectores uno a uno (k = 1, 2, ...) y con cada b_k hacemos dos cosas:
  1) Reduccion de tamano: si b_k se parece demasiado a un b_j anterior (|mu| > 1/2),
     le restamos b_j un numero entero de veces.
  2) Condicion de Lovasz: si b_k aporta poco "de nuevo" (||b*_k||^2) comparado con b_(k-1),
     estan mal ordenados: los intercambiamos y volvemos un paso atras. Si no, pasamos al siguiente.

Las dos decisiones usan mu y normas2, que salen de gso. Llamamos a gso UNA sola vez al principio;
despues, cada vez que la base cambia, actualizamos solo los valores de mu y normas2 que cambian.
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
    n = len(b)
    mu, normas2, _ = gso(b)                 # solo una vez; luego se va actualizando
    k = 1
    while k < n:
        # 1) Reduccion de tamano (de j = k-1 hacia atras)
        for j in range(k - 1, -1, -1):
            r = redondeo(mu[k][j])
            if r != 0:
                b[k] = resta_vectores(b[k], escalar_por_vector(r, b[j]))
                # Como b_k = suma de mu[k][i] * b*_i, al restarle r * b_j su coeficiente sobre
                # cada b*_i baja r * mu[j][i] (y sobre b*_j baja r, porque mu[j][j] = 1).
                # Los b* no cambian, asi que normas2 tampoco.
                # Ejemplo: mu[k][j] = 7/3 -> r = 2 -> queda 1/3.
                for i in range(j + 1):
                    mu[k][i] -= r * mu[j][i]

        # 2) Condicion de Lovasz
        m = mu[k][k - 1]
        if normas2[k] >= (delta - m ** 2) * normas2[k - 1]:
            k += 1                                  # bien ordenados: siguiente vector
        else:
            b[k], b[k - 1] = b[k - 1], b[k]         # mal ordenados: intercambiar y retroceder
            _actualizar_tras_intercambio(mu, normas2, k)
            k = max(k - 1, 1)
    return b


def _actualizar_tras_intercambio(mu: Matriz, normas2: list[Fraction], k: int) -> None:
    """Corrige mu y normas2 despues de intercambiar b_(k-1) y b_k.

    Solo cambian b*_(k-1) y b*_k; los demas b* siguen igual.
      - El nuevo b*_(k-1) es lo que el antiguo b_k aportaba de nuevo frente a b_0, ..., b_(k-2):
        b*_k + m * b*_(k-1), con m = mu[k][k-1]. Su norma2 es normas2[k] + m^2 * normas2[k-1].
      - El area del paralelogramo de b*_(k-1) y b*_k no cambia, asi que el producto de las
        dos normas2 se mantiene: de ahi sale la nueva normas2[k].
    """
    m = mu[k][k - 1]
    nueva = normas2[k] + m ** 2 * normas2[k - 1]
    mu[k][k - 1] = m * normas2[k - 1] / nueva
    normas2[k] = normas2[k - 1] * normas2[k] / nueva
    normas2[k - 1] = nueva

    # Los coeficientes de b_(k-1) y b_k sobre b*_0, ..., b*_(k-2) no cambian: solo cambian de fila.
    for j in range(k - 1):
        mu[k][j], mu[k - 1][j] = mu[k - 1][j], mu[k][j]

    # Los vectores posteriores b_i no cambian, pero ahora se miden respecto a los dos nuevos b*:
    # se recalculan sus dos coeficientes en esas direcciones.
    for i in range(k + 1, len(mu)):
        x, y = mu[i][k - 1], mu[i][k]               # coeficientes sobre los b* antiguos
        mu[i][k] = x - m * y
        mu[i][k - 1] = y + mu[k][k - 1] * mu[i][k]
