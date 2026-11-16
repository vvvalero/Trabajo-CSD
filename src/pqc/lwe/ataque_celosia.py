"""Ataque a LWE con celosias: recuperar s resolviendo un CVP (mismas herramientas que en GGH).

Idea:
  - Los vectores A s (mod q), para todos los s posibles, forman una celosia de Z^m (la celosia
    "q-aria" de A): sumar dos de ellos o sumar q a una coordenada da otro del mismo tipo.
  - La clave publica es b = A s + e con e pequeno, asi que b esta muy cerca del punto A s de esa
    celosia. Encontrar s es encontrar el punto de la celosia mas cercano a b: un CVP.
  - Lo resolvemos igual que en GGH: LLL para conseguir una base buena y enumeracion exacta.

Base de la celosia (vectores por filas, m = numero de ecuaciones, n = incognitas):
  si A1 son las n primeras ecuaciones (invertible modulo q) y A2 el resto, un punto y = A s
  cumple y2 = (A2 A1^-1) y1 (mod q). Una base es
        [ I_n | C^T     ]      con C = A2 A1^-1 mod q   (n filas)
        [ 0   | q I_m-n ]                                (m - n filas)
  Ejemplo con n = 1, m = 2, q = 7, A = (2, 3): C = 3 * 2^-1 = 3 * 4 = 12 = 5 (mod 7),
  base = [[1, 5], [0, 7]], y por ejemplo s = 1 da A s = (2, 3) = 2*(1, 5) - 1*(0, 7).

Del punto encontrado y se saca s = A1^-1 y1 (mod q).
"""
from __future__ import annotations

from ..celosias import enumeracion, lll
from ..lector_tareas import TareaLWE
from ..matrices import inversa_mod, matriz_por_vector, mod_matriz, mod_vector


def sistema_a_celosia(tarea: TareaLWE):
    """Devuelve (base de la celosia q-aria de A, objetivo b, inversa de A1 modulo q)."""
    q, n, m = tarea.q, tarea.n, len(tarea.A)
    A = mod_matriz(tarea.A, q)                # algunos ficheros traen coeficientes que valen justo q
    inversa_A1 = inversa_mod(A[:n], q)
    # C = A2 * A1^-1 (mod q): fila i = ecuacion n + i escrita en funcion de las n primeras
    C = [[sum(A[n + i][k] * inversa_A1[k][j] for k in range(n)) % q for j in range(n)]
         for i in range(m - n)]
    base = []
    for j in range(n):                        # [ I_n | C^T ]
        base.append([1 if k == j else 0 for k in range(n)] + [C[i][j] for i in range(m - n)])
    for i in range(m - n):                    # [ 0 | q I ]
        base.append([0] * n + [q if k == i else 0 for k in range(m - n)])
    return base, list(tarea.b), inversa_A1


def ataque(tarea: TareaLWE) -> list[int]:
    """Encuentra el punto de la celosia mas cercano a b (CVP exacto) y devuelve s (entre 0 y q-1)."""
    base, objetivo, inversa_A1 = sistema_a_celosia(tarea)
    punto = enumeracion(lll(base), objetivo)  # el punto A s (mod q) mas cercano a b
    y1 = mod_vector(punto[:tarea.n], tarea.q)
    return mod_vector(matriz_por_vector(inversa_A1, y1), tarea.q)
