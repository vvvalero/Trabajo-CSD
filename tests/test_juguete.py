import random
from fractions import Fraction

import pytest

from pqc.ggh.juguete import _inverse, _matmul, decrypt, encrypt, keygen

# Ejemplos 1-3 del PDF
B = [[3, 1], [-1, 4]]
U = [[3, 4], [2, 3]]
B_PUB = [[5, 19], [3, 14]]


def _det(M):
    """Determinante exacto por eliminacion con Fraction (independiente de _inverse)."""
    M = [[Fraction(a) for a in fila] for fila in M]
    n, det = len(M), Fraction(1)
    for i in range(n):
        p = next((j for j in range(i, n) if M[j][i] != 0), None)
        if p is None:
            return Fraction(0)
        if p != i:
            M[i], M[p] = M[p], M[i]
            det = -det
        det *= M[i][i]
        for j in range(i + 1, n):
            f = M[j][i] / M[i][i]
            M[j] = [a - f * b for a, b in zip(M[j], M[i])]
    return det


def test_ejemplo1_clave_publica():
    assert _matmul(U, B) == B_PUB


def test_ejemplo2_cifrado():
    assert encrypt([7, 3], B_PUB, [-1, 1]) == [43, 176]


def test_ejemplo3_descifrado():
    assert decrypt([43, 176], B, U) == [7, 3]


def test_ejemplo3_error_excesivo_no_descifra():
    # e' = (-2, 2) -> c = (42, 177): el redondeo de Babai cae en otro punto
    c = encrypt([7, 3], B_PUB, [-2, 2])
    assert c == [42, 177]
    assert decrypt(c, B, U) != [7, 3]


def test_inverse_exacta():
    assert _inverse(B) == [[Fraction(4, 13), Fraction(-1, 13)], [Fraction(1, 13), Fraction(3, 13)]]
    assert _inverse(U) == [[3, -4], [-2, 3]]


def test_inverse_singular():
    with pytest.raises(ValueError):
        _inverse([[1, 2], [2, 4]])


@pytest.mark.parametrize("n", range(2, 8))
def test_keygen_unimodular_y_publica(n):
    B_, U_, P = keygen(n, seed=n)
    assert abs(_det(U_)) == 1
    assert _det(B_) != 0
    assert P == _matmul(U_, B_)
    assert _det(P) == _det(U_) * _det(B_)


def test_keygen_reproducible():
    assert keygen(4, seed=7) == keygen(4, seed=7)
    assert keygen(4, seed=7) != keygen(4, seed=8)


def test_keygen_base_publica_peor_que_privada():
    B_, _, P = keygen(5, seed=1)
    assert max(abs(v) for f in P for v in f) > max(abs(v) for f in B_ for v in f)


@pytest.mark.parametrize("n", range(2, 8))
def test_ida_y_vuelta_aleatoria(n):
    rng = random.Random(n)
    for seed in range(30):
        B_, U_, P = keygen(n, seed=seed)
        x = [rng.randint(-100, 100) for _ in range(n)]
        e = [rng.randint(-1, 1) for _ in range(n)]
        assert decrypt(encrypt(x, P, e), B_, U_) == x


def test_encrypt_dimensiones_incoherentes():
    with pytest.raises(AssertionError):
        encrypt([1, 2, 3], B_PUB, [0, 0])
