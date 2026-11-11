"""Operaciones con vectores y matrices que usan GGH, LWE y los algoritmos de celosias.

Como guardamos las matrices:
  - Una matriz es una lista de filas. Ejemplo: [[3, 1], [-1, 4]] tiene dos filas, (3, 1) y (-1, 4).
  - Los numeros son enteros (int) o fracciones exactas (Fraction). No usamos decimales para no
    tener errores de redondeo.
  - En una base de celosia, cada FILA es un vector de la base.
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import List, Tuple, Union

# Nombres para los tipos, para que las funciones se lean mejor.
# (Se escriben con Union/List para que funcione tambien en Python 3.9.)
Numero = Union[int, Fraction]
Vector = List[Numero]
Matriz = List[List[Numero]]


# ============================================================================ VECTORES

def _misma_longitud(u: Vector, v: Vector) -> None:
    """Da error si los dos vectores no tienen el mismo numero de componentes."""
    if len(u) != len(v):
        raise ValueError(f"Longitudes distintas: {len(u)} y {len(v)}")


def suma_vectores(u: Vector, v: Vector) -> Vector:
    """Suma componente a componente. Ejemplo: (1, 2) + (3, 4) = (4, 6)."""
    _misma_longitud(u, v)
    return [a + b for a, b in zip(u, v)]


def resta_vectores(u: Vector, v: Vector) -> Vector:
    """Resta componente a componente. Ejemplo: (1, 2) - (3, 4) = (-2, -2)."""
    _misma_longitud(u, v)
    return [a - b for a, b in zip(u, v)]


def escalar_por_vector(k: Numero, v: Vector) -> Vector:
    """Multiplica cada componente por k. Ejemplo: 2 * (1, 2) = (2, 4)."""
    return [k * a for a in v]


def producto_escalar(u: Vector, v: Vector) -> Numero:
    """Multiplica componente a componente y suma. Ejemplo: (1, 2) . (3, 4) = 1*3 + 2*4 = 11."""
    _misma_longitud(u, v)
    return sum(a * b for a, b in zip(u, v))


def norma2(v: Vector) -> Numero:
    """Longitud del vector AL CUADRADO. Ejemplo: (3, 4) -> 9 + 16 = 25.

    Usamos el cuadrado para no calcular raices: si a^2 < b^2 entonces a < b, asi que sirve
    igual para comparar que vector es mas corto, y el resultado sigue siendo exacto.
    """
    return producto_escalar(v, v)


# ============================================================================ MATRICES

def dimensiones(A: Matriz) -> Tuple[int, int]:
    """Devuelve (numero de filas, numero de columnas). Da error si hay filas de distinta longitud."""
    if not A:
        return 0, 0
    columnas = len(A[0])
    if any(len(fila) != columnas for fila in A):
        raise ValueError("Filas de longitudes distintas")
    return len(A), columnas


def _cuadrada(A: Matriz) -> int:
    """Devuelve el tamano n de una matriz n x n. Da error si no es cuadrada."""
    filas, columnas = dimensiones(A)
    if filas != columnas:
        raise ValueError(f"La matriz debe ser cuadrada y es {filas}x{columnas}")
    return filas


def identidad(n: int) -> Matriz:
    """Matriz n x n con unos en la diagonal y ceros fuera. Ejemplo: n=2 -> [[1, 0], [0, 1]]."""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def transpuesta(A: Matriz) -> Matriz:
    """Cambia filas por columnas. Ejemplo: [[1, 2, 3], [4, 5, 6]] -> [[1, 4], [2, 5], [3, 6]]."""
    dimensiones(A)
    return [list(columna) for columna in zip(*A)]


def producto_matrices(X: Matriz, Y: Matriz) -> Matriz:
    """Producto X * Y. Cada casilla es el producto escalar de una fila de X por una columna de Y."""
    if dimensiones(X)[1] != dimensiones(Y)[0]:
        raise ValueError(f"No se pueden multiplicar {dimensiones(X)} por {dimensiones(Y)}")
    return [[producto_escalar(fila, columna) for columna in zip(*Y)] for fila in X]


def vector_por_matriz(x: Vector, B: Matriz) -> Vector:
    """Calcula x * B: suma las filas de B, cada una multiplicada por su coeficiente de x.

    Es la operacion de GGH: el criptograma es c = x * B' + e.
    Ejemplo: (7, 3) * [[5, 19], [3, 14]] = 7*(5, 19) + 3*(3, 14) = (44, 175).
    """
    return producto_matrices([x], B)[0]


def matriz_por_vector(A: Matriz, s: Vector) -> Vector:
    """Calcula A * s: el producto escalar de cada fila de A por s.

    Es la operacion de LWE: cada fila de A es una ecuacion y b = A * s + e.
    """
    return [producto_escalar(fila, s) for fila in A]


def es_entera(A: Union[Matriz, Vector]) -> bool:
    """True si todos los numeros (de una matriz o de un vector) son enteros.

    Sirve, por ejemplo, para comprobar si un punto pertenece a la celosia (sus coeficientes
    en la base son enteros) o si dos bases generan la misma celosia.
    """
    filas = A if A and isinstance(A[0], list) else [A]
    return all(Fraction(x).denominator == 1 for fila in filas for x in fila)


# ============================================================================ INVERSA Y DETERMINANTE

def inverse(A: Matriz) -> Matriz:
    """Matriz inversa exacta (con fracciones), por el metodo de Gauss-Jordan.

    Idea: escribimos A y la identidad I una al lado de la otra. Hacemos operaciones de filas
    hasta que A se convierte en I; esas mismas operaciones convierten I en la inversa de A.
    """
    n = _cuadrada(A)
    A = [[Fraction(a) for a in fila] for fila in A]  # copia, para no modificar la original
    I = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for i in range(n):
        # Si en la diagonal hay un 0, intercambiamos con una fila de abajo que no lo tenga.
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    I[i], I[j] = I[j], I[i]
                    break
            else:
                raise ValueError("Matriz singular (no tiene inversa)")
        # Dividimos la fila i para que en la diagonal quede un 1.
        pivote = A[i][i]
        A[i] = [a / pivote for a in A[i]]
        I[i] = [a / pivote for a in I[i]]
        # Restamos la fila i a las demas para dejar ceros en el resto de la columna i.
        for j in range(n):
            if j != i:
                factor = A[j][i]
                A[j] = [a - factor * b for a, b in zip(A[j], A[i])]
                I[j] = [a - factor * b for a, b in zip(I[j], I[i])]
    return I


def det(A: Matriz) -> Fraction:
    """Determinante exacto, por eliminacion gaussiana.

    Idea: dejamos la matriz con ceros debajo de la diagonal. Entonces el determinante es el
    producto de la diagonal. Cada intercambio de filas cambia el signo.
    """
    n = _cuadrada(A)
    M = [[Fraction(a) for a in fila] for fila in A]
    d = Fraction(1)
    for i in range(n):
        # Buscamos una fila (desde la i hacia abajo) sin 0 en la columna i.
        p = next((j for j in range(i, n) if M[j][i] != 0), None)
        if p is None:
            return Fraction(0)  # columna de ceros: el determinante es 0
        if p != i:
            M[i], M[p] = M[p], M[i]
            d = -d
        d *= M[i][i]
        # Ponemos ceros debajo de la diagonal en la columna i.
        for j in range(i + 1, n):
            factor = M[j][i] / M[i][i]
            M[j] = [a - factor * b for a, b in zip(M[j], M[i])]
    return d


# ============================================================================ REDONDEO

def redondeo(x: Numero) -> int:
    """Entero mas cercano. Si esta justo en medio (2,5) redondea hacia arriba (3).

    No usamos round() de Python porque en esos casos redondea al numero par
    (round(2.5) = 2 pero round(3.5) = 4), y con fracciones esos empates ocurren de verdad.
    """
    return math.floor(Fraction(x) + Fraction(1, 2))


def redondeo_vector(v: Vector) -> List[int]:
    """Redondea cada componente. Es lo que hace el redondeo de Babai: round(c * B^-1)."""
    return [redondeo(x) for x in v]


# ============================================================================ MODULO q

def _entero(x: Numero) -> int:
    """Convierte a int, pero da error si x tiene decimales (int() los quitaria sin avisar: 7/2 -> 3)."""
    if Fraction(x).denominator != 1:
        raise ValueError(f"Se esperaba un entero y llego {x}")
    return int(x)


def mod_vector(v: Vector, q: int) -> List[int]:
    """Cada componente pasa a estar entre 0 y q-1. Ejemplo (q = 71): (-1, 71, 72) -> (70, 0, 1)."""
    return [_entero(x) % q for x in v]


def mod_matriz(A: Matriz, q: int) -> Matriz:
    """Igual que mod_vector, para cada fila. Arregla, por ejemplo, coeficientes que valen justo q."""
    return [mod_vector(fila, q) for fila in A]


def centrado(x: int, q: int) -> int:
    """Pasa x mod q al rango centrado en 0 (para q = 71: de -35 a 35).

    Sirve para ver si un numero modulo q es "pequeno": por ejemplo, 70 mod 71 es en realidad -1.
    Lo usamos para medir errores (e = b - A s en LWE) y distancias al descifrar.
    """
    return ((_entero(x) + q // 2) % q) - q // 2


def centrado_vector(v: Vector, q: int) -> List[int]:
    """Aplica centrado() a cada componente."""
    return [centrado(x, q) for x in v]


def inversa_mod(A: Matriz, q: int) -> Matriz:
    """Matriz inversa trabajando modulo q (resultado con numeros entre 0 y q-1).

    Es el mismo Gauss-Jordan que inverse(), pero en vez de dividir multiplicamos por el
    inverso modular. Por ejemplo, modulo 7 el inverso de 3 es 5, porque 3 * 5 = 15 = 1 (mod 7).
    Funciona cuando q es primo (todos los modulos de las tareas lo son).
    """
    n = _cuadrada(A)
    M = mod_matriz(A, q)
    I = identidad(n)
    for i in range(n):
        # Buscamos una fila cuyo valor en la columna i tenga inverso modulo q.
        p = next((j for j in range(i, n) if math.gcd(M[j][i], q) == 1), None)
        if p is None:
            raise ValueError(f"La matriz no tiene inversa modulo {q}")
        M[i], M[p] = M[p], M[i]
        I[i], I[p] = I[p], I[i]
        # Multiplicamos la fila i por el inverso del pivote para que quede un 1 en la diagonal.
        inv = pow(M[i][i], -1, q)
        M[i] = [a * inv % q for a in M[i]]
        I[i] = [a * inv % q for a in I[i]]
        # Dejamos ceros en el resto de la columna i.
        for j in range(n):
            if j != i and M[j][i] != 0:
                factor = M[j][i]
                M[j] = [(a - factor * b) % q for a, b in zip(M[j], M[i])]
                I[j] = [(a - factor * b) % q for a, b in zip(I[j], I[i])]
    return I
