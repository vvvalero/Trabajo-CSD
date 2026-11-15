from pathlib import Path

import pytest

from pqc.lector_tareas import TareaRingLWE, leer_todas
from pqc.lwe.ring import descifrar_ring, matriz_de_polinomio, producto_polinomios, romper_clave_ring
from pqc.matrices import centrado_vector, matriz_por_vector, mod_vector, resta_vectores, suma_vectores

DATA = Path(__file__).parent.parent / "data"
RING = leer_todas(DATA)["ringlwe"]

# Clave publica del ejemplo de Ring-LWE del Tema 11 (q = 463, n = 8). Aqui conocemos el secreto.
TEMA11 = TareaRingLWE(
    nombre="Tema11", n=8, q=463,
    a=[1, 14, 3, 3, 2, 11, 5, 1], b=[396, 458, 461, 1, 14, 40, 70, 52],
    c1=[], c2=[], solucion=None,
)
S_TEMA11 = [2, 2, 1, 2, 1, 2, 1, 2]


# ---------------------------------------------------------------- producto de polinomios

def test_producto_sin_pasar_de_grado_n():
    # (1 + x) * (1 + x) = 1 + 2x + x^2
    assert producto_polinomios([1, 1, 0, 0], [1, 1, 0, 0]) == [1, 2, 1, 0]


def test_producto_x_n_es_menos_uno():
    # x^3 * x^2 = x^5 = -x   (porque x^4 = -1)
    assert producto_polinomios([0, 0, 0, 1], [0, 0, 1, 0]) == [0, -1, 0, 0]
    # x^3 * x = x^4 = -1
    assert producto_polinomios([0, 0, 0, 1], [0, 1, 0, 0]) == [-1, 0, 0, 0]


def test_ejemplo_tema11():
    # b - a*s tiene que ser un error pequeno.
    e = centrado_vector(resta_vectores(TEMA11.b, producto_polinomios(TEMA11.a, S_TEMA11)), TEMA11.q)
    assert e == [-1, 0, 0, -1, 1, 0, 0, 0]


# ---------------------------------------------------------------- matriz del polinomio

def test_matriz_de_polinomio_n4():
    assert matriz_de_polinomio([1, 2, 3, 4]) == [
        [1, -4, -3, -2],
        [2, 1, -4, -3],
        [3, 2, 1, -4],
        [4, 3, 2, 1],
    ]


def test_matriz_por_s_es_lo_mismo_que_a_por_s():
    a, s = TEMA11.a, S_TEMA11
    assert matriz_por_vector(matriz_de_polinomio(a), s) == producto_polinomios(a, s)


# ---------------------------------------------------------------- rotura de la clave

def test_rotura_ejemplo_tema11():
    assert romper_clave_ring(TEMA11) == S_TEMA11


@pytest.mark.parametrize("tarea", RING, ids=lambda t: t.nombre)
def test_rotura_tareas_s_y_e_pequenos(tarea):
    # No traen el secreto: comprobamos que s es pequeno y que b - a*s tambien lo es.
    s = romper_clave_ring(tarea)
    e = centrado_vector(resta_vectores(tarea.b, producto_polinomios(tarea.a, s)), tarea.q)
    assert max(abs(x) for x in s) <= 2
    assert max(abs(x) for x in e) <= 1


# ---------------------------------------------------------------- descifrado

def test_cifrar_y_descifrar_con_la_clave_del_tema11():
    # El ejemplo del Tema 11 no trae un criptograma correcto (errata), asi que ciframos
    # nosotros con su clave publica y comprobamos que se recupera el mensaje.
    q, a, b = TEMA11.q, TEMA11.a, TEMA11.b
    r = [1, 0, 1, 1, 0, 0, 1, 0]                 # pequenos, elegidos a mano
    e1 = [1, 0, -1, 0, 0, 1, 0, 0]
    e2 = [0, 1, 0, 0, -1, 0, 0, 1]
    m = [1, 0, 1, 1, 0, 0, 1, 0]                 # palabra de bits
    m_por_mitad = [bit * (q // 2) for bit in m]  # cada bit 1 pasa a valer q/2
    c1 = mod_vector(suma_vectores(producto_polinomios(a, r), e1), q)                              # a*r + e1
    c2 = mod_vector(suma_vectores(suma_vectores(producto_polinomios(b, r), e2), m_por_mitad), q)  # b*r + e2 + m*q/2
    tarea = TareaRingLWE(nombre="Tema11", n=8, q=q, a=a, b=b, c1=c1, c2=c2, solucion=None)
    assert descifrar_ring(tarea, S_TEMA11) == m


@pytest.mark.parametrize("tarea", RING, ids=lambda t: t.nombre)
def test_descifrado_tareas_sin_dudas(tarea):
    # Cada coeficiente de d = c2 - s*c1 tiene que estar claramente cerca de 0 o de q/2:
    # por debajo de q/8 o por encima de 3q/8 (lejos del umbral q/4).
    s = romper_clave_ring(tarea)
    d = centrado_vector(resta_vectores(tarea.c2, producto_polinomios(s, tarea.c1)), tarea.q)
    assert all(abs(x) < tarea.q / 8 or abs(x) > 3 * tarea.q / 8 for x in d)
    assert len(descifrar_ring(tarea, s)) == tarea.n
