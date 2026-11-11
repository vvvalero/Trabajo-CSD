from pathlib import Path

import pytest

from pqc import ggh
from pqc.ggh.reduccion_babai import ataque
from pqc.lector_tareas import leer_todas
from pqc.matrices import es_entera, inversa, vector_por_matriz

DATA = Path(__file__).parent.parent / "data"
TAREAS = [t for t in leer_todas(DATA)["ggh"] if not t.modulo]      # sin las modulares (Tier3)


def test_enunciado_ejemplos_1_a_3():
    # Con la base publica sola Babai falla (45, 184); con LLL delante recupera el mensaje.
    assert ataque([[5, 19], [3, 14]], [43, 176]) == [44, 175]


def test_svp_vector_corto():
    # Base mala de Z^2 (determinante 1): el vector mas corto tiene longitud 1.
    v = ataque([[5, 19], [1, 4]], None)
    assert sorted(map(abs, v)) == [0, 1]


@pytest.mark.parametrize("tarea", [t for t in TAREAS if t.solucion], ids=lambda t: t.nombre)
def test_tareas_con_solucion(tarea):
    assert ggh.solve(tarea) == tarea.solucion


@pytest.mark.parametrize("tarea", TAREAS, ids=lambda t: t.nombre)
def test_resultado_es_punto_de_la_celosia(tarea):
    p = ggh.solve(tarea)
    assert es_entera(vector_por_matriz(p, inversa(tarea.base)))     # coordenadas enteras
    if tarea.problema == "SVP":
        assert any(p)                                               # no vale el vector 0
