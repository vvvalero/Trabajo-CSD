"""SVP/CVP exactos: enumeracion por distancias y orden de Schnorr-Euchner.

La base tiene un vector entero por fila. Conviene reducirla con LLL antes:
eso acelera la busqueda sin cambiar sus puntos ni su resultado optimo.
Todas las cotas y comparaciones usan Fraction; no hay podas heuristicas.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import ceil, floor, isqrt

from ..matrices import (
    Matriz,
    Vector,
    dimensiones,
    es_entera,
    norma2,
    producto_escalar,
    resta_vectores,
    vector_por_matriz,
)
from .babai import babai_plano_cercano
from .gso import gso


@dataclass
class EstadisticasEnumeracion:
    """Datos de la ultima llamada; tiempo y coste de LLL se miden por separado.

    Nodos cuenta estados visitados (incluidas las hojas); hojas, combinaciones
    completas visitadas, incluido el cero rechazado en SVP. El candidato inicial
    y las ramas descartadas antes de visitarlas no se incluyen en estos contadores.
    """

    nodos: int = 0
    hojas: int = 0
    mejoras: int = 0
    radio2_inicial: Fraction = Fraction(0)
    radio2_final: Fraction = Fraction(0)


def _limites(centro: Fraction, margen2: Fraction) -> tuple[int, int]:
    """Enteros x con (x-centro)^2 <= margen2, sin aproximar raices.

    Si centro = p/q, la desigualdad equivale a
        (q*x - p)^2 <= margen2*q^2.
    El lado izquierdo es un cuadrado entero: isqrt(floor(lado derecho))
    proporciona la cota exacta para |q*x-p|, incluso con coordenadas grandes.
    """
    p, q = centro.numerator, centro.denominator
    cota = isqrt((margen2.numerator * q * q) // margen2.denominator)
    return ceil(Fraction(p - cota, q)), floor(Fraction(p + cota, q))


def _orden_cercano(centro: Fraction, inferior: int, superior: int):
    """Recorre el intervalo por distancia creciente al centro, sin ordenarlo entero."""
    izquierda = min(floor(centro), superior)
    derecha = max(floor(centro) + 1, inferior)
    while izquierda >= inferior or derecha <= superior:
        if izquierda < inferior:
            yield derecha
            derecha += 1
        elif derecha > superior or centro - izquierda <= derecha - centro:
            yield izquierda
            izquierda -= 1
        else:
            yield derecha
            derecha += 1


def enumeracion(
    B: Matriz,
    objetivo: Vector | None = None,
    *,
    estadisticas: EstadisticasEnumeracion | None = None,
) -> list[int]:
    """Devuelve un punto optimo; SVP si objetivo es None y CVP si no.

    Solo requiere una base entera, cuadrada e independiente, no necesariamente
    reducida. En empates se conserva cualquier optimo. No modifica las entradas.

    Gram-Schmidt expresa la distancia al cuadrado como una suma no negativa:
        sum_i ||b*_i||^2 * (x_i + sum_{j>i} mu[j][i]*x_j - c_i)^2,
    donde c_i = <objetivo, b*_i> / ||b*_i||^2 (c_i = 0 en SVP).

    Elegimos coeficientes desde el ultimo al primero. Cada contribucion parcial
    acota todos sus descendientes: si alcanza la mejor distancia conocida,
    descartamos la rama. Una mejora reduce el radio. Al completar el recorrido
    no queda ningun punto mejor sin comprobar. En SVP se excluye el cero.
    """
    n, columnas = dimensiones(B)
    if n == 0 or columnas != n:
        raise ValueError("La enumeracion requiere una base cuadrada no vacia")
    if not es_entera(B):
        raise ValueError("La base de la enumeracion debe contener enteros")
    if objetivo is not None and len(objetivo) != n:
        raise ValueError("El objetivo y la base deben tener la misma dimension")

    base = [[int(v) for v in fila] for fila in B]
    t = [Fraction(v) for v in objetivo] if objetivo is not None else [Fraction(0)] * n
    mu, normas2, Bstar = gso(base)          # tambien comprueba la independencia

    # Un candidato valido garantiza un radio que contiene cualquier mejora.
    if objetivo is None:
        mejor = list(min(base, key=norma2))
    else:
        mejor = babai_plano_cercano(base, t)
    mejor_distancia = Fraction(norma2(resta_vectores(mejor, t)))

    datos = estadisticas if estadisticas is not None else EstadisticasEnumeracion()
    datos.nodos = datos.hojas = datos.mejoras = 0
    datos.radio2_inicial = datos.radio2_final = mejor_distancia
    if mejor_distancia == 0:               # CVP: ya no hay nada que mejorar
        return mejor

    centros = [producto_escalar(t, v) / norma for v, norma in zip(Bstar, normas2)]
    coeficientes = [0] * n

    def visitar(i: int, parcial: Fraction) -> None:
        nonlocal mejor, mejor_distancia
        datos.nodos += 1
        if i < 0:
            datos.hojas += 1
            if objetivo is None and not any(coeficientes):
                return                    # el origen no es una solucion SVP
            mejor = vector_por_matriz(coeficientes, base)
            mejor_distancia = parcial
            datos.mejoras += 1
            return

        restante = mejor_distancia - parcial
        if restante <= 0:
            return
        centro = centros[i] - sum(mu[j][i] * coeficientes[j] for j in range(i + 1, n))
        inferior, superior = _limites(centro, restante / normas2[i])
        for x in _orden_cercano(centro, inferior, superior):
            distancia = parcial + normas2[i] * (x - centro) ** 2
            if distancia >= mejor_distancia:
                # El orden es creciente: tampoco mejoraran los siguientes x.
                # No necesitamos visitar empates: ya tenemos un candidato valido.
                break
            coeficientes[i] = x
            visitar(i - 1, distancia)

    visitar(n - 1, Fraction(0))
    datos.radio2_final = mejor_distancia
    return mejor
