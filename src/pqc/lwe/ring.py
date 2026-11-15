"""Ring-LWE en Z_q[x]/(x^n + 1) (esquema del Tema 11)."""
from __future__ import annotations

from ..lector_tareas import TareaRingLWE
from ..matrices import (centrado_vector, inversa, matriz_por_vector, redondeo_vector, resta_vectores,
                        transpuesta)


def producto_polinomios(a: list[int], s: list[int]) -> list[int]:
    """Producto a * s modulo x^n + 1 (sin reducir los coeficientes modulo q).

    Un polinomio se guarda como la lista de sus coeficientes, empezando por x^0:
    [3, 0, 2] es 3 + 2x^2.

    Se multiplica como siempre (cada termino de a por cada termino de s), pero como
    trabajamos modulo x^n + 1, se cumple x^n = -1.

    Ejemplo con n = 4:
      x^3 * x^2 = x^5 = x^4 * x = -x            [0,0,0,1] * [0,0,1,0] = [0,-1,0,0]
      (1 + x) * (1 + x) = 1 + 2x + x^2          [1,1,0,0] * [1,1,0,0] = [1,2,1,0]
    """
    n = len(a)
    resultado = [0] * n
    for i in range(n):
        for j in range(n):
            # a_i x^i * s_j x^j = a_i s_j x^(i+j)
            if i + j < n:
                resultado[i + j] += a[i] * s[j]
            else:
                resultado[i + j - n] -= a[i] * s[j]    # x^(i+j) = -x^(i+j-n)
    return resultado


def matriz_de_polinomio(a: list[int]) -> list[list[int]]:
    """Matriz M que hace lo mismo que multiplicar por a: M * s = a * s.

    La columna j de M es a * x^j. Por que: el polinomio x^j es el vector (0, ..., 1, ..., 0)
    con el 1 en la posicion j, y M por ese vector da justo la columna j de M.
    En la practica, a * x^j son los coeficientes de a desplazados j posiciones; lo que se
    sale por abajo vuelve por arriba con el signo cambiado, porque x^n = -1.

    Ejemplo con n = 4 y a = 1 + 2x + 3x^2 + 4x^3:
        [[1, -4, -3, -2],
         [2,  1, -4, -3],
         [3,  2,  1, -4],
         [4,  3,  2,  1]]
    """
    n = len(a)
    columnas = []
    for j in range(n):
        x_j = [0] * n
        x_j[j] = 1                                   # el polinomio x^j
        columnas.append(producto_polinomios(a, x_j))
    return transpuesta(columnas)                     # cada lista era una columna: la pasamos a filas


def romper_clave_ring(tarea: TareaRingLWE) -> list[int]:
    """Recupera el secreto s de la clave publica b = a*s + e (con s y e pequenos).

    Ataque propio, que funciona por como estan hechas las tareas: a tiene coeficientes
    de 0 a 15, y s y e son pequenos, asi que los coeficientes de a*s + e nunca llegan a q/2.
    Por eso b (centrado) es EXACTAMENTE a*s + e con enteros normales, sin modulo q, y
    b = a*s + e es un sistema lineal normal: M s = b - e, con M = matriz_de_polinomio(a).

    Pasos:
      1. Centrar b: los coeficientes pasan a estar entre -q/2 y q/2 (con q = 1399, 1330 es -69).
      2. Resolver M s = b con fracciones exactas, como si no hubiera error.
      3. El error solo mueve un poco la solucion (Tier3_T01: 0,07 / 1,94 / 1,06 ...), asi que
         redondeando sale s (0 / 2 / 1 ...).
    Devuelve s con sus coeficientes pequenos (por ejemplo -1, no q - 1).
    """
    b = centrado_vector(tarea.b, tarea.q)
    M = matriz_de_polinomio(tarea.a)
    s_aproximado = matriz_por_vector(inversa(M), b)
    return redondeo_vector(s_aproximado)


def descifrar_ring(tarea: TareaRingLWE, s: list[int]) -> list[int]:
    """Palabra de bits del criptograma (c1, c2), conocido el secreto s (esquema del Tema 11).

    Cifrado: c1 = a*r + e1 y c2 = b*r + e2 + m*(q/2), con r, e1, e2 pequenos y m la palabra
    de bits (un bit en cada coeficiente). Al calcular d = c2 - s*c1 se cancela a*r*s:
        d = e*r + e2 - s*e1 + m*(q/2)
    Lo que no es m*(q/2) son productos de cosas pequenas, asi que cada coeficiente de d
    (centrado) queda cerca de 0 si el bit es 0, o cerca de q/2 (o -q/2) si el bit es 1.
    Es la misma regla que en descifrar_bit, coeficiente a coeficiente: |d| < q/4 -> 0; si no, 1.

    Ejemplo (Tier3_T01, q = 1399, q/4 = 349,75): d empieza por -2, -697, 8 -> bits 0, 1, 0.
    """
    d = centrado_vector(resta_vectores(tarea.c2, producto_polinomios(s, tarea.c1)), tarea.q)
    bits = []
    for x in d:
        if abs(x) < tarea.q / 4:
            bits.append(0)
        else:
            bits.append(1)
    return bits
