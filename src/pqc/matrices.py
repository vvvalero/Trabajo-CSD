"""Algebra lineal exacta sobre listas de filas (int o Fraction), compartida por ggh, celosias y lwe.

Convenio: una matriz es una lista de filas; los vectores se tratan como filas (x B, no B x).
"""
from __future__ import annotations

from fractions import Fraction


def producto_matrices(X, Y):
    """Producto de matrices (listas de filas) con int o Fraction, exacto."""
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*Y)] for fila in X]


def inverse(A):
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


def det(A):
    """Determinante exacto (Fraction) por eliminacion gaussiana."""
    n = len(A)
    assert all(len(fila) == n for fila in A), "A debe ser cuadrada"
    M = [[Fraction(a) for a in fila] for fila in A]
    d = Fraction(1)
    for i in range(n):
        p = next((j for j in range(i, n) if M[j][i] != 0), None)
        if p is None:
            return Fraction(0)
        if p != i:
            M[i], M[p] = M[p], M[i]
            d = -d
        d *= M[i][i]
        for j in range(i + 1, n):
            f = M[j][i] / M[i][i]
            M[j] = [a - f * b for a, b in zip(M[j], M[i])]
    return d
