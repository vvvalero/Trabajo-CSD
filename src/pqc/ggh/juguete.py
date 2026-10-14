"""GGH de juguete (seccion 2.1 del PDF) para probar los ataques con ejemplos propios."""
from __future__ import annotations

import random
from fractions import Fraction


def _matmul(X, Y):
    """Producto de matrices (listas de filas) con int o Fraction, exacto."""
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*Y)] for fila in X]


def _random_unimodular(n: int, rng: random.Random, pasos: int, k_max: int):
    """Matriz unimodular: identidad + operaciones elementales (sumar k*fila_j a fila_i, o permutar).

    Cada operacion conserva det = +-1, asi que el resultado es unimodular por construccion.
    """
    U = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(pasos):
        i, j = rng.sample(range(n), 2)
        if rng.random() < 0.1:
            U[i], U[j] = U[j], U[i]
        else:
            k = rng.choice([c for c in range(-k_max, k_max + 1) if c != 0])
            U[i] = [a + k * b for a, b in zip(U[i], U[j])]
    return U


def _inverse(A):
    """Inversa exacta (Fraction) de una matriz cuadrada, usando Gauss-Jordan."""
    n = len(A)
    assert all(len(fila) == n for fila in A), "A debe ser cuadrada"
    A = [[Fraction(a) for a in fila] for fila in A]  # copia en racionales
    I = [[Fraction(int(i == j)) for j in range(n)] for i in range(n)]
    for i in range(n):
        # pivoteo parcial
        if A[i][i] == 0:
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    I[i], I[j] = I[j], I[i]
                    break
            else:
                raise ValueError("Matriz singular")
        # hacer 1 el pivote y eliminar columna
        pivot = A[i][i]
        A[i] = [a / pivot for a in A[i]]
        I[i] = [a / pivot for a in I[i]]
        for j in range(n):
            if j != i:
                factor = A[j][i]
                A[j] = [a - factor * b for a, b in zip(A[j], A[i])]
                I[j] = [a - factor * b for a, b in zip(I[j], I[i])]
    return I


def keygen(n: int, seed: int | None = None, diag: int = 50, off: int = 3, pasos: int | None = None):
    """B, U unimodular, B' = U B. Clave privada <B, U>, publica <B'>.

    B: base buena, casi ortogonal (diagonal grande en [diag, 2*diag], resto en [-off, off]).
       Con diag > n*off es diagonalmente dominante, luego det(B) != 0.
    U: unimodular con entradas grandes, para que B' = U B sea una base mala.
    Devuelve (B, U, B_pub).
    """
    assert n >= 2 and diag > n * off, "diag debe ser > n*off para garantizar det(B) != 0"
    rng = random.Random(seed)
    B = [[rng.randint(diag, 2 * diag) if i == j else rng.randint(-off, off) for j in range(n)] for i in range(n)]
    U = _random_unimodular(n, rng, pasos if pasos is not None else 4 * n * n, k_max=2)
    return B, U, _matmul(U, B)


def encrypt(x, B_pub, e):
    """c = x B' + e"""
    assert len(x) == len(e) == len(B_pub)
    c = _matmul([x], B_pub)[0]
    return [ci + ei for ci, ei in zip(c, e)]
    

def decrypt(c, B_priv, U):
    """y = round(c B^-1);  x = y U^-1"""
    y = [round(v) for v in _matmul([c], _inverse(B_priv))[0]]
    x = _matmul([y], _inverse(U))[0]
    assert all(v.denominator == 1 for v in x), "x no entero: ruido excesivo o claves incoherentes"
    return [int(v) for v in x]
