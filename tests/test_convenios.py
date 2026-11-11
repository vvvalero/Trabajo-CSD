"""Convenios fijados a partir de la asignatura (ver README y docs/algoritmos.md, 3.3).

LWE:      b = A s + e (mod q)  ->  e = b - A s        (Tema 11; Ejemplo 4 del enunciado)
Ring-LWE: b = a s + e (mod q, x^n + 1)                (Tema 11)
"""
from pqc.matrices import centrado_vector, matriz_por_vector, mod_vector, resta_vectores


def test_lwe_ejemplo4_enunciado_b_igual_As_mas_e():
    q = 71
    S = [4, 70, 0, 3]
    E = [-3, 3, -2, 0, 2]
    A = [[70, 6, 25, 15], [19, 51, 27, 32], [53, 55, 51, 6], [59, 46, 26, 51], [23, 5, 36, 45]]
    b = [32, 53, 31, 59, 11]
    As = matriz_por_vector(A, S)
    assert centrado_vector(resta_vectores(b, As), q) == E      # e = b - A s
    assert centrado_vector(resta_vectores(As, b), q) != E      # el otro signo NO


def test_lwe_ejemplo6_enunciado_descifrado():
    # C S mod 71 para los criptogramas del Ejemplo 6 (S del Ejemplo 4)
    q, S = 71, [4, 70, 0, 3]
    C = [[0, 41, 32, 53], [40, 36, 31, 1], [5, 60, 16, 51], [41, 62, 17, 21]]
    assert mod_vector(matriz_por_vector(C, S), q) == [47, 56, 42, 23]


def test_ring_lwe_ejemplo_tema11_estructura():
    # b - a s en Z_463[x]/(x^8 + 1) debe ser un error pequeno. La diapositiva da otro e (errata),
    # pero la estructura b = a s + e con e pequeno se cumple.
    q, n = 463, 8
    a = [1, 14, 3, 3, 2, 11, 5, 1]
    s = [2, 2, 1, 2, 1, 2, 1, 2]
    b = [396, 458, 461, 1, 14, 40, 70, 52]
    producto = [0] * n
    for i in range(n):
        for j in range(n):
            if i + j < n:
                producto[i + j] += a[i] * s[j]
            else:
                producto[i + j - n] -= a[i] * s[j]                  # x^n = -1
    e = centrado_vector(resta_vectores(b, producto), q)
    assert e == [-1, 0, 0, -1, 1, 0, 0, 0]
