import random

import pytest

from pqc.ggh.juguete import cifrar, descifrar, generar_claves
from pqc.matrices import det, producto_matrices

# Ejemplos 1-3 del enunciado
B = [[3, 1], [-1, 4]]
U = [[3, 4], [2, 3]]
B_PUB = [[5, 19], [3, 14]]


def test_ejemplo1_clave_publica():
    assert producto_matrices(U, B) == B_PUB


def test_ejemplo2_cifrado():
    assert cifrar([7, 3], B_PUB, [-1, 1]) == [43, 176]


def test_ejemplo3_descifrado():
    assert descifrar([43, 176], B, U) == [7, 3]


def test_ejemplo3_error_excesivo_no_descifra():
    # e = (-2, 2) -> c = (42, 177): el redondeo de Babai cae en otro punto
    c = cifrar([7, 3], B_PUB, [-2, 2])
    assert c == [42, 177]
    assert descifrar(c, B, U) != [7, 3]


@pytest.mark.parametrize("n", range(2, 8))
def test_claves_unimodular_y_publica(n):
    B_, U_, P = generar_claves(n, semilla=n)
    assert abs(det(U_)) == 1
    assert det(B_) != 0
    assert P == producto_matrices(U_, B_)
    assert det(P) == det(U_) * det(B_)


def test_claves_reproducibles():
    assert generar_claves(4, semilla=7) == generar_claves(4, semilla=7)
    assert generar_claves(4, semilla=7) != generar_claves(4, semilla=8)


def test_base_publica_peor_que_privada():
    B_, _, P = generar_claves(5, semilla=1)
    assert max(abs(v) for f in P for v in f) > max(abs(v) for f in B_ for v in f)


@pytest.mark.parametrize("n", range(2, 8))
def test_ida_y_vuelta_aleatoria(n):
    rng = random.Random(n)
    for semilla in range(30):
        B_, U_, P = generar_claves(n, semilla=semilla)
        x = [rng.randint(-100, 100) for _ in range(n)]
        e = [rng.randint(-1, 1) for _ in range(n)]
        assert descifrar(cifrar(x, P, e), B_, U_) == x


def test_cifrar_dimensiones_incoherentes():
    with pytest.raises(ValueError):
        cifrar([1, 2, 3], B_PUB, [0, 0])
