"""Contrastar la busqueda en coeficientes con fuerza bruta en puntos del espacio."""
from copy import deepcopy
from fractions import Fraction
from itertools import product
from math import ceil, floor, isqrt
from pathlib import Path
import random

import pytest

from pqc.celosias import babai_plano_cercano, enumeracion, lll
from pqc.celosias.enumeracion import EstadisticasEnumeracion
from pqc.ggh import solve
from pqc.lector_tareas import leer_ggh, leer_todas
from pqc.matrices import (
    det,
    es_entera,
    inversa,
    norma2,
    resta_vectores,
    suma_vectores,
    vector_por_matriz,
)

DATA = Path(__file__).parent.parent / "data"
TAREAS = [t for t in leer_todas(DATA)["ggh"] if not t.modulo]


def distancia2(p, t):
    return sum((x - y) ** 2 for x, y in zip(p, t))


def optimo_en_puntos(B, objetivo):
    """Oraculo independiente: recorre puntos enteros, no coeficientes de la base.

    Usa como radio la longitud de una fila (SVP) o la distancia al cero (CVP).
    El cubo que encierra esa bola incluye todo punto que pueda mejorar la cota.
    La inversa solo se usa para comprobar la pertenencia a la celosia.
    """
    t = [0] * len(B) if objetivo is None else objetivo
    radio2 = min(norma2(v) for v in B) if objetivo is None else distancia2([0] * len(B), t)
    radio = isqrt(ceil(radio2))
    if radio * radio < radio2:
        radio += 1
    intervalos = [range(ceil(x - radio), floor(x + radio) + 1) for x in t]
    inv = inversa(B)
    return min(
        distancia2(p, t)
        for p in product(*intervalos)
        if (objetivo is not None or any(p))
        and distancia2(p, t) <= radio2
        and es_entera(vector_por_matriz(list(p), inv))
    )


def casos_pequenos():
    yield [[3]], [Fraction(3, 2)]                  # empate exacto en la frontera
    yield [[3]], None
    yield [[3, 1], [1, 3]], None                 # el mas corto no es una fila
    yield [[2, 1], [-1, 2]], [Fraction(1, 3), Fraction(-7, 4)]
    yield [[2, 1], [-1, 2]], [0, 0]
    yield [[1, 1, 0], [0, 2, 1], [1, 0, 2]], None
    yield [[1, 1, 0], [0, 2, 1], [1, 0, 2]], [1, -1, 2]
    rng = random.Random(2026)
    for _ in range(12):
        while True:
            B = [[rng.randint(-3, 3) for _ in range(2)] for _ in range(2)]
            if det(B) != 0:
                break
        yield B, None
        yield B, [rng.randint(-3, 3), rng.randint(-3, 3)]


@pytest.mark.parametrize("base,objetivo", list(casos_pequenos()))
def test_coincide_con_busqueda_exhaustiva_independiente(base, objetivo):
    p = enumeracion(base, objetivo)
    t = [0] * len(base) if objetivo is None else objetivo
    assert distancia2(p, t) == optimo_en_puntos(base, objetivo)
    assert es_entera(vector_por_matriz(p, inversa(base)))
    if objetivo is None:
        assert any(p)


def test_cvp_mejora_babai_y_el_radio_ingenuo_no_basta():
    base, t = [[1, 101], [0, 10]], [0, 5]
    assert distancia2(babai_plano_cercano(base, t), t) == 25
    p = enumeracion(base, t)
    # Dentro del radio inicial 5, la pertenencia equivale a (y-101*x) % 10 == 0.
    optimo = min(
        x * x + (y - 5) ** 2
        for x in range(-5, 6) for y in range(0, 11)
        if (y - 101 * x) % 10 == 0
    )
    assert distancia2(p, t) == optimo == 13


def test_traslacion_enorme_no_pierde_precision_en_las_cotas():
    base = [[1, 101], [0, 10]]
    desplazamiento = vector_por_matriz([2**60 + 1, -(3 * 2**60) + 7], base)
    t = suma_vectores(desplazamiento, [0, 5])
    p = enumeracion(base, t)
    assert distancia2(p, t) == 13
    assert es_entera(vector_por_matriz(p, inversa(base)))


def test_cvp_con_mejoras_sucesivas_del_radio():
    # En esta base sin reducir se encuentran varias mejoras antes del optimo.
    # Contrasta el resultado final con un recorrido independiente sobre puntos.
    base = [[-3, 3, 1], [3, 2, 0], [0, -1, 0]]
    t = [Fraction(-2, 3), Fraction(1), Fraction(-1, 3)]
    p = enumeracion(base, t)
    assert distancia2(p, t) == optimo_en_puntos(base, t) == Fraction(5, 9)


def test_no_modifica_entradas():
    base, t = [[2, 1], [-1, 2]], [1, 3]
    copia_base, copia_t = deepcopy(base), t[:]
    enumeracion(base, t)
    assert base == copia_base and t == copia_t


def test_estadisticas_y_cvp_ya_en_la_celosia():
    datos = EstadisticasEnumeracion()
    enumeracion([[3, 1], [1, 3]], estadisticas=datos)
    assert datos.radio2_inicial == 10 and datos.radio2_final == 8
    assert datos.nodos > 0 and datos.hojas > 0 and datos.mejoras > 0
    assert enumeracion([[2, 0], [0, 3]], [4, 9], estadisticas=datos) == [4, 9]
    assert datos.radio2_inicial == datos.radio2_final == 0
    assert datos.nodos == datos.hojas == datos.mejoras == 0


@pytest.mark.parametrize("base", [[], [[1, 0, 0], [0, 1, 0]], [[1, 2], [2, 4]], [[Fraction(1, 2)]]])
def test_rechaza_bases_invalidas(base):
    with pytest.raises(ValueError):
        enumeracion(base)


def test_rechaza_objetivo_de_dimension_incorrecta():
    with pytest.raises(ValueError):
        enumeracion([[1, 0], [0, 1]], [0])


def test_regresion_tier02t03_encuentra_el_optimo():
    tarea = leer_ggh(DATA / "ggh" / "Tier02T03_Latt.txt")
    R = lll(tarea.base)
    assert norma2(resta_vectores(babai_plano_cercano(R, tarea.objetivo), tarea.objetivo)) == 186
    p = solve(tarea)
    assert norma2(resta_vectores(p, tarea.objetivo)) == 155


@pytest.mark.parametrize("nombre,radio2", [("Tier03T03_Latt", 8), ("Tier03T04_Latt", 250)])
def test_tier3_sin_modulo_dimension15(nombre, radio2):
    tarea = leer_ggh(DATA / "ggh" / f"{nombre}.txt")
    p = solve(tarea)
    t = tarea.objetivo if tarea.objetivo is not None else [0] * tarea.dim
    assert distancia2(p, t) == radio2
    assert es_entera(vector_por_matriz(p, inversa(tarea.base)))
    if tarea.problema == "SVP":
        assert any(p)


@pytest.mark.parametrize("tarea", TAREAS, ids=lambda t: t.nombre)
def test_todas_las_tareas_sin_modulo_mejoran_o_igualan_el_candidato(tarea):
    R = lll(tarea.base)
    t = tarea.objetivo if tarea.objetivo is not None else [0] * tarea.dim
    candidato = min(R, key=norma2) if tarea.objetivo is None else babai_plano_cercano(R, t)
    p = solve(tarea)
    assert distancia2(p, t) <= distancia2(candidato, t)
    assert es_entera(vector_por_matriz(p, inversa(tarea.base)))


def test_modulares_siguen_pendientes():
    with pytest.raises(NotImplementedError):
        solve(leer_ggh(DATA / "ggh" / "Tier03T01_Latt.txt"))
