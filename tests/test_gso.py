from fractions import Fraction

import pytest

from pqc.celosias import gso
from pqc.matrices import det, producto_escalar, producto_matrices

B = [[3, 1], [-1, 4]]   # base privada de los ejemplos del enunciado


def test_ejemplo_a_mano():
    mu, normas2, Bstar = gso(B)
    assert Bstar == [[3, 1], [Fraction(-13, 10), Fraction(39, 10)]]
    assert mu[1][0] == Fraction(1, 10)
    assert normas2 == [10, Fraction(169, 10)]


@pytest.mark.parametrize("base", [
    B,
    [[5, 19], [3, 14]],                                   # base publica del enunciado
    [[18, -2, -1], [0, 18, -2], [1, 0, 16]],              # base privada del Tema 11
    [[1997, 334, -478], [-3816, -634, 908], [-10610, -1762, 2523]],   # base publica del Tema 11
])
def test_propiedades(base):
    mu, normas2, Bstar = gso(base)
    n = len(base)
    # 1) Los b*_i son perpendiculares entre si
    for i in range(n):
        for j in range(i):
            assert producto_escalar(Bstar[i], Bstar[j]) == 0
    # 2) La base se recupera: B = mu * B*
    assert producto_matrices(mu, Bstar) == base
    # 3) El producto de las ||b*_i||^2 es det(B)^2
    producto = 1
    for x in normas2:
        producto *= x
    assert producto == det(base) ** 2


def test_no_modifica_la_base():
    copia = [fila[:] for fila in B]
    gso(B)
    assert B == copia


def test_vectores_dependientes():
    with pytest.raises(ValueError):
        gso([[1, 2], [2, 4]])
