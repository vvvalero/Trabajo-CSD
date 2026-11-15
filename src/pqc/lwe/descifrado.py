"""Descifrado de un bit con LWE (Ejemplo 6 del enunciado)."""
from __future__ import annotations

from ..lector_tareas import TareaLWE
from ..matrices import centrado, producto_escalar


def descifrar_bit(tarea: TareaLWE, s: list[int]) -> int:
    """Bit cifrado en el criptograma (coeficientes C, termino independiente B), conocido el secreto s.

    El criptograma es la suma de algunas ecuaciones de la clave publica, y si el bit es 1 se le
    suma ademas q/2 (redondeado hacia abajo) al termino independiente B. Con el secreto
    calculamos el valor "real", sin errores: R = C . s mod q. Entonces:
      - bit 0: B = R + (suma de errores)        -> B - R esta cerca de 0
      - bit 1: B = R + (suma de errores) + q/2  -> B - R esta cerca de q/2
    Miramos d = B - R centrado (entre -q/2 y q/2). Si |d| es menor que q/4 (la mitad del
    camino entre 0 y q/2) el bit es 0, y si no, 1.

    Ejemplo 6 (q = 71, s = (4, 70, 0, 3)), primer criptograma (0, 41, 32, 53) ~ 9:
      R = 47, d = 9 - 47 = -38, que centrado es 33. 33 no es menor que 71/4 = 17,75 -> bit 1.
    """
    C, B = tarea.criptograma
    R = producto_escalar(C, s) % tarea.q
    d = centrado(B - R, tarea.q)
    if abs(d) < tarea.q / 4:
        return 0
    return 1
