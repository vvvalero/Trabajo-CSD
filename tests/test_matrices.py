from fractions import Fraction

import pytest

from pqc.matrices import (
    centrado,
    centrado_vector,
    det,
    dimensiones,
    es_entera,
    escalar_por_vector,
    identidad,
    inversa,
    inversa_mod,
    matriz_por_vector,
    mod_matriz,
    mod_vector,
    norma2,
    producto_escalar,
    producto_matrices,
    redondeo,
    redondeo_vector,
    resta_vectores,
    suma_vectores,
    transpuesta,
    vector_por_matriz,
)

# Ejemplos 1-3 del enunciado (GGH)
B_PRIV = [[3, 1], [-1, 4]]
U = [[3, 4], [2, 3]]
B_PUB = [[5, 19], [3, 14]]


# ----------------------------------------------------------------------------- vectores

def test_operaciones_vectores():
    assert suma_vectores([1, 2, 3], [4, -5, 6]) == [5, -3, 9]
    assert resta_vectores([1, 2, 3], [4, -5, 6]) == [-3, 7, -3]
    assert escalar_por_vector(Fraction(1, 2), [2, 3]) == [1, Fraction(3, 2)]
    assert producto_escalar([1, 2, 3], [4, -5, 6]) == 12
    assert norma2([3, 4]) == 25


def test_vectores_longitudes_distintas():
    with pytest.raises(ValueError):
        suma_vectores([1, 2], [1, 2, 3])
    with pytest.raises(ValueError):
        producto_escalar([1], [1, 2])


# ----------------------------------------------------------------------------- matrices

def test_dimensiones_identidad_transpuesta():
    assert dimensiones([[1, 2, 3], [4, 5, 6]]) == (2, 3)
    assert identidad(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert transpuesta([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    with pytest.raises(ValueError):
        dimensiones([[1, 2], [3]])


def test_producto_matrices():
    assert producto_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]]
    assert producto_matrices([[7, 3]], [[5, 19], [3, 14]]) == [[44, 175]]  # Ejemplo 2 del PDF sin ruido
    assert producto_matrices(U, B_PRIV) == B_PUB                           # Ejemplo 1: B' = U B
    with pytest.raises(ValueError):
        producto_matrices([[1, 2, 3]], [[1, 2]])


def test_vector_por_matriz_es_el_cifrado_ggh():
    # Ejemplo 2: c = x B' + e = (7, 3) B' + (-1, 1) = (43, 176)
    assert suma_vectores(vector_por_matriz([7, 3], B_PUB), [-1, 1]) == [43, 176]


def test_matriz_por_vector_es_lwe():
    # Ejemplo 4: A S mod 71 (b = A S + E)
    A = [[70, 6, 25, 15], [19, 51, 27, 32], [53, 55, 51, 6], [59, 46, 26, 51], [23, 5, 36, 45]]
    assert mod_vector(matriz_por_vector(A, [4, 70, 0, 3]), 71) == [35, 50, 33, 59, 9]


def test_es_entera():
    assert es_entera([[1, 2], [Fraction(4, 2), 0]])
    assert not es_entera([[1, Fraction(1, 2)]])
    assert es_entera([3, -1])
    assert es_entera(producto_matrices(B_PUB, inversa(B_PRIV)))  # B' B^-1 = U entera


# ----------------------------------------------------------------------------- exactas

def test_det():
    assert det([[3, 1], [-1, 4]]) == 13
    assert det([[3, 4], [2, 3]]) == 1
    assert det([[1, 2], [2, 4]]) == 0
    assert det([[0, 1], [1, 0]]) == -1  # el intercambio de filas cambia el signo
    assert det(B_PUB) == det(U) * det(B_PRIV)


def test_inversa_por_matriz_identidad():
    A = [[2, 1, 0], [1, 3, 1], [0, 1, 4]]
    assert producto_matrices(A, inversa(A)) == identidad(3)


def test_inversa_con_pivote_cero():
    assert inversa([[0, 1], [1, 0]]) == [[0, 1], [1, 0]]


def test_inversa_exacta_y_singular():
    esperada = [[Fraction(4, 13), Fraction(-1, 13)], [Fraction(1, 13), Fraction(3, 13)]]
    assert inversa([[3, 1], [-1, 4]]) == esperada
    with pytest.raises(ValueError):
        inversa([[1, 2], [2, 4]])
    with pytest.raises(ValueError):
        inversa([[1, 2, 3], [4, 5, 6]])  # no cuadrada


# ----------------------------------------------------------------------------- redondeo

def test_redondeo_empates_hacia_arriba():
    assert [redondeo(Fraction(k, 2)) for k in (-3, -1, 1, 3, 5)] == [-1, 0, 1, 2, 3]
    assert redondeo(7) == 7


def test_redondeo_de_babai_ejemplo3():
    # Ejemplo 3: c B^-1 = (26.769, 37.308) -> y = (27, 37) -> x = y U^-1 = (7, 3)
    y = redondeo_vector(vector_por_matriz([43, 176], inversa(B_PRIV)))
    assert y == [27, 37]
    assert vector_por_matriz(y, inversa(U)) == [7, 3]


# ----------------------------------------------------------------------------- modulares

def test_mod_y_centrado():
    assert mod_vector([-1, 71, 72, 35], 71) == [70, 0, 1, 35]
    assert mod_matriz([[379, -1]], 379) == [[0, 378]]           # coeficientes que valen exactamente q
    assert centrado_vector([0, 35, 36, 70, -36], 71) == [0, 35, -35, -1, 35]
    assert centrado(43 - 63, 71) == -20
    assert mod_vector([Fraction(142, 2)], 71) == [0]                  # fraccion entera: se acepta


def test_mod_y_centrado_rechazan_no_enteros():
    with pytest.raises(ValueError):
        mod_vector([Fraction(7, 2)], 5)
    with pytest.raises(ValueError):
        centrado(Fraction(7, 2), 5)


def test_inversa_mod():
    q = 71
    A = [[70, 6, 25, 15], [19, 51, 27, 32], [53, 55, 51, 6], [59, 46, 26, 51]]
    Ai = inversa_mod(A, q)
    assert mod_matriz(producto_matrices(A, Ai), q) == identidad(4)
    assert all(0 <= x < q for fila in Ai for x in fila)


def test_inversa_mod_resuelve_lwe_sin_error():
    # Si b = A s (sin error), s = A^-1 b mod q
    q, s = 229, [81, 55, 152]
    A = [[85, 42, 211], [167, 161, 95], [140, 110, 159]]
    b = mod_vector(matriz_por_vector(A, s), q)
    assert mod_vector(matriz_por_vector(inversa_mod(A, q), b), q) == s


def test_inversa_mod_singular():
    with pytest.raises(ValueError):
        inversa_mod([[1, 2], [2, 4]], 7)
    with pytest.raises(ValueError):
        inversa_mod([[1, 0], [0, 7]], 7)   # det = 7 = 0 mod 7
