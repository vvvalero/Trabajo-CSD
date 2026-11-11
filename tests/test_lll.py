from fractions import Fraction
from pathlib import Path

import pytest

from pqc.celosias import gso, lll
from pqc.lector_tareas import leer_todas
from pqc.matrices import det, es_entera, inversa, producto_matrices

DATA = Path(__file__).parent.parent / "data"


def misma_celosia(B, R):
    """R genera la misma celosia que B: R = U B con U entera y det(U) = +-1."""
    U = producto_matrices(R, inversa(B))
    return es_entera(U) and abs(det(U)) == 1


def esta_reducida(R, delta=Fraction(99, 100)):
    """R cumple las dos condiciones de LLL."""
    mu, normas2, _ = gso(R)
    n = len(R)
    tamano = all(abs(mu[i][j]) <= Fraction(1, 2) for i in range(n) for j in range(i))
    lovasz = all(normas2[k] >= (delta - mu[k][k - 1] ** 2) * normas2[k - 1] for k in range(1, n))
    return tamano and lovasz


def test_ejemplo1_enunciado():
    # Base publica (5, 19), (3, 14) -> la privada (3, 1), (-1, 4) con el signo cambiado
    assert lll([[5, 19], [3, 14]]) == [[-3, -1], [1, -4]]


def test_ejemplo_tema11_recupera_la_clave_privada():
    privada = [[18, -2, -1], [0, 18, -2], [1, 0, 16]]
    publica = [[1997, 334, -478], [-3816, -634, 908], [-10610, -1762, 2523]]
    sin_signo = lambda v: max(v, [-x for x in v])      # noqa: E731
    assert sorted(map(sin_signo, lll(publica))) == sorted(map(sin_signo, privada))


@pytest.mark.parametrize("tarea", leer_todas(DATA)["ggh"], ids=lambda t: t.nombre)
def test_tareas_ggh(tarea):
    R = lll(tarea.base)
    assert misma_celosia(tarea.base, R)
    assert esta_reducida(R)


def test_no_modifica_la_base():
    B = [[5, 19], [3, 14]]
    lll(B)
    assert B == [[5, 19], [3, 14]]


def test_errores():
    with pytest.raises(ValueError):
        lll([[1, 0], [0, 1]], delta=Fraction(1, 4))     # delta fuera de rango
    with pytest.raises(ValueError):
        lll([[1, 2], [2, 4]])                            # vectores dependientes (lo detecta gso)
