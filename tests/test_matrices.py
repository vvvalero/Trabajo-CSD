from fractions import Fraction

import pytest

from pqc.matrices import det, inverse, producto_matrices


def test_producto_matrices():
    assert producto_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert producto_matrices([[7, 3]], [[5, 19], [3, 14]]) == [[44, 175]]  # Ejemplo 2 del PDF sin ruido


def test_det():
    assert det([[3, 1], [-1, 4]]) == 13
    assert det([[3, 4], [2, 3]]) == 1
    assert det([[1, 2], [2, 4]]) == 0
    assert det([[0, 1], [1, 0]]) == -1  # el intercambio de filas cambia el signo


def test_inverse_por_matriz_identidad():
    A = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    assert producto_matrices(A, inverse(A)) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def test_inverse_con_pivote_cero():
    assert inverse([[0, 1], [1, 0]]) == [[0, 1], [1, 0]]


def test_inverse_exacta_y_singular():
    assert inverse([[3, 1], [-1, 4]]) == [[Fraction(4, 13), Fraction(-1, 13)], [Fraction(1, 13), Fraction(3, 13)]]
    with pytest.raises(ValueError):
        inverse([[1, 2], [2, 4]])
