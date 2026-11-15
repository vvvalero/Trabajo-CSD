"""Fuerza bruta para LWE: probar los posibles errores de n ecuaciones y comprobar el resto.

Idea (b = A s + e mod q, con n incognitas y m > n ecuaciones):
  - Si conocieramos el error de n ecuaciones, esas n ecuaciones serian un sistema normal
    A_n s = b_n - e_n (mod q), y s se despeja con la inversa modulo q.
  - No lo conocemos, pero es pequeno: probamos todos los e_n con componentes en [-error_max, error_max].
  - Para cada s candidato miramos el error de TODAS las ecuaciones (e = b - A s, centrado).
    Si todos son pequenos, ese es el secreto; si sale alguno grande, el e_n probado era falso.

Ejemplo (Tier0T01_LWE, q = 229): sin error (error_max = 0) solo hay un e_n que probar, (0, 0, 0),
y sale s = (81, 55, 152), que es la solucion del fichero.

Coste: (2*error_max + 1)^n intentos. Con n = 4 y error_max = 2 son 5^4 = 625.
"""
from __future__ import annotations

from itertools import product

from ..lector_tareas import TareaLWE
from ..matrices import centrado_vector, inversa_mod, matriz_por_vector, mod_matriz, mod_vector, resta_vectores


def fuerza_bruta(tarea: TareaLWE, error_max: int) -> list[int] | None:
    """Devuelve s (entre 0 y q-1) si todas las ecuaciones tienen |error| <= error_max, o None."""
    q, n = tarea.q, tarea.n
    A = mod_matriz(tarea.A, q)            # algunos ficheros traen coeficientes que valen justo q
    inversa_n = inversa_mod(A[:n], q)     # inversa de las n primeras ecuaciones (sirve para despejar s)

    # product da todas las combinaciones. Ejemplo con n = 2 y error_max = 1:
    # (-1, -1), (-1, 0), (-1, 1), (0, -1), ..., (1, 1)  ->  3^2 = 9 errores e_n
    valores = range(-error_max, error_max + 1)
    for e_n in product(valores, repeat=n):
        # 1) Suponemos que el error de las n primeras ecuaciones es e_n y despejamos s.
        s = mod_vector(matriz_por_vector(inversa_n, resta_vectores(tarea.b[:n], list(e_n))), q)
        # 2) Comprobamos el error de todas las ecuaciones con ese s.
        errores = centrado_vector(resta_vectores(tarea.b, matriz_por_vector(A, s)), q)
        if max(abs(x) for x in errores) <= error_max:
            return s
    return None
