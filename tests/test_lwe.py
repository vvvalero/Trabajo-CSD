from pathlib import Path

import pytest

from pqc.lector_tareas import TareaLWE, leer_todas
from pqc.lwe import descifrar_bit, romper_clave
from pqc.lwe.ataque_celosia import ataque, sistema_a_celosia
from pqc.lwe.fuerza_bruta import fuerza_bruta
from pqc.matrices import centrado_vector, matriz_por_vector, resta_vectores

DATA = Path(__file__).parent.parent / "data"
LWE = [t for t in leer_todas(DATA)["lwe"] if isinstance(t, TareaLWE)]
TIER0 = [t for t in LWE if t.nombre.startswith("Tier0")]           # traen la solucion
TIER1 = [t for t in LWE if t.nombre.startswith("Tier1")]

# Ejemplo 4 del enunciado: S = (4, 70, 0, 3), errores (-3, 3, -2, 0, 2), modulo 71
EJEMPLO4 = TareaLWE(
    nombre="Ejemplo4", problema="rotura", n=4, q=71,
    A=[[70, 6, 25, 15], [19, 51, 27, 32], [53, 55, 51, 6], [59, 46, 26, 51], [23, 5, 36, 45]],
    b=[32, 53, 31, 59, 11], criptograma=None, solucion=[4, 70, 0, 3],
)


@pytest.mark.parametrize("tarea", TIER0, ids=lambda t: t.nombre)
def test_tier0_coincide_con_la_solucion_del_fichero(tarea):
    s = romper_clave(tarea)
    resultado = s if tarea.problema == "rotura" else descifrar_bit(tarea, s)
    assert resultado == tarea.solucion


@pytest.mark.parametrize("tarea", TIER1, ids=lambda t: t.nombre)
def test_tier1_errores_pequenos(tarea):
    # No traen solucion: comprobamos que con el s encontrado todos los errores son pequenos.
    s = romper_clave(tarea)
    errores = centrado_vector(resta_vectores(tarea.b, matriz_por_vector(tarea.A, s)), tarea.q)
    assert max(abs(x) for x in errores) <= 4


def test_ejemplo4_pocas_ecuaciones_dan_un_secreto_falso():
    # Con 5 ecuaciones y 4 incognitas solo sobra 1 para comprobar, y con errores de hasta 3
    # pasa el filtro un secreto que no es el bueno (4, 70, 0, 3). Por eso hacen falta bastantes
    # ecuaciones de sobra (las tareas traen unas 3 veces mas ecuaciones que incognitas).
    assert fuerza_bruta(EJEMPLO4, 3) == [11, 25, 5, 51]


@pytest.mark.parametrize("C, B, bit", [
    ([0, 41, 32, 53], 9, 1),       # R = 47: lejos de 9
    ([40, 36, 31, 1], 15, 1),      # R = 56: lejos de 15
    ([5, 60, 16, 51], 42, 0),      # R = 42: igual
    ([41, 62, 17, 21], 25, 0),     # R = 23: cerca de 25
])
def test_descifrado_ejemplo6(C, B, bit):
    # Para descifrar solo hacen falta q y el criptograma (A y b no se usan)
    tarea = TareaLWE(nombre="Ejemplo6", problema="criptoanalisis", n=4, q=71, A=[], b=[],
                     criptograma=(C, B), solucion=None)
    assert descifrar_bit(tarea, [4, 70, 0, 3]) == bit


# ------------------------------------------------------------------ ataque de celosia (CVP)

DIFICILES = [t for t in LWE if t.nombre in (
    "Tier2T04_LWE", "Tier2T05_LWE", "Tier3T01_LWE", "Tier3T02_LWE", "Tier3T03_LWE",
    "Tier3T04_LWE", "Tier3T05_LWE")]


def test_ejemplo4_con_celosia_tambien_da_un_secreto_falso():
    # Con una sola ecuacion de sobra, el punto mas cercano a b no es el del secreto real:
    # (6, 19, 60, 37) deja un error (-1, 0, 1, -1, 0), mas pequeno que el real (-3, 3, -2, 0, 2).
    # Ningun metodo puede distinguirlos: hacen falta ecuaciones de sobra.
    assert ataque(EJEMPLO4) == [6, 19, 60, 37]


def test_base_de_la_celosia_ejemplo_del_docstring():
    tarea = TareaLWE(nombre="mini", problema="rotura", n=1, q=7, A=[[2], [3]], b=[2, 3],
                     criptograma=None, solucion=None)
    base, objetivo, _ = sistema_a_celosia(tarea)
    assert base == [[1, 5], [0, 7]] and objetivo == [2, 3]


@pytest.mark.parametrize("tarea", TIER0 + TIER1, ids=lambda t: t.nombre)
def test_celosia_coincide_con_fuerza_bruta(tarea):
    # Dos metodos distintos deben dar el mismo secreto.
    assert ataque(tarea) == romper_clave(tarea)


@pytest.mark.parametrize("tarea", DIFICILES, ids=lambda t: t.nombre)
def test_celosia_tareas_dificiles_errores_pequenos(tarea):
    s = ataque(tarea)
    errores = centrado_vector(resta_vectores(tarea.b, matriz_por_vector(tarea.A, s)), tarea.q)
    assert max(abs(x) for x in errores) <= 15
