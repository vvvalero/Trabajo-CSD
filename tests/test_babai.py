from fractions import Fraction
from pathlib import Path

import pytest

from pqc.celosias import babai_plano_cercano, babai_redondeo, gso, lll
from pqc.lector_tareas import leer_todas
from pqc.matrices import es_entera, inversa, norma2, producto_escalar, resta_vectores, vector_por_matriz

DATA = Path(__file__).parent.parent / "data"
BABAI = [babai_redondeo, babai_plano_cercano]
CVP = [t for t in leer_todas(DATA)["ggh"] if t.problema == "CVP" and not t.modulo]   # sin las modulares

# Ejemplos 1-3 del enunciado
PRIVADA = [[3, 1], [-1, 4]]
PUBLICA = [[5, 19], [3, 14]]
C = [43, 176]
MENSAJE = [44, 175]              # = (7, 3) * PUBLICA


@pytest.mark.parametrize("babai", BABAI)
def test_enunciado_base_privada_acierta(babai):
    assert babai(PRIVADA, C) == MENSAJE


@pytest.mark.parametrize("babai", BABAI)
def test_enunciado_base_publica_falla(babai):
    assert babai(PUBLICA, C) == [45, 184]


@pytest.mark.parametrize("babai", BABAI)
def test_enunciado_base_publica_reducida_acierta(babai):
    assert babai(lll(PUBLICA), C) == MENSAJE


@pytest.mark.parametrize("babai", BABAI)
def test_punto_de_la_celosia_se_queda_igual(babai):
    assert babai(PUBLICA, MENSAJE) == MENSAJE


@pytest.mark.parametrize("babai", BABAI)
@pytest.mark.parametrize("tarea", [t for t in leer_todas(DATA)["ggh"] if t.solucion and t.problema == "CVP"],
                         ids=lambda t: t.nombre)
def test_tareas_tier0(babai, tarea):
    # Las tareas Tier0 traen la solucion: LLL + Babai la encuentra
    assert babai(lll(tarea.base), tarea.objetivo) == tarea.solucion


@pytest.mark.parametrize("tarea", CVP, ids=lambda t: t.nombre)
def test_resultado_es_punto_de_la_celosia(tarea):
    R = lll(tarea.base)
    for babai in BABAI:
        p = babai(R, tarea.objetivo)
        assert es_entera(vector_por_matriz(p, inversa(tarea.base)))      # coordenadas enteras


@pytest.mark.parametrize("tarea", CVP, ids=lambda t: t.nombre)
def test_plano_cercano_propiedad(tarea):
    # Lo que define al plano mas cercano: lo que sobra (t - p) proyectado sobre cada b*_i
    # es como mucho media vez b*_i.
    R = lll(tarea.base)
    sobra = resta_vectores(tarea.objetivo, babai_plano_cercano(R, tarea.objetivo))
    _, normas2, Bstar = gso(R)
    assert all(abs(producto_escalar(sobra, b) / n) <= Fraction(1, 2) for b, n in zip(Bstar, normas2))


def test_plano_cercano_mejora_al_redondeo_en_tier02t03():
    t = {x.nombre: x for x in leer_todas(DATA)["ggh"]}["Tier02T03_Latt"]
    R = lll(t.base)
    assert norma2(resta_vectores(t.objetivo, babai_redondeo(R, t.objetivo))) == 187
    assert norma2(resta_vectores(t.objetivo, babai_plano_cercano(R, t.objetivo))) == 186
