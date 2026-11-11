"""Lectura de los ficheros de tareas (carpeta data/).

Como son los ficheros:
  - Las lineas que empiezan por # son comentarios que explican que dato viene despues.
  - Entre un comentario y el siguiente hay un BLOQUE de datos (una o varias lineas).
  - Cada bloque es un dato, y los bloques vienen siempre en el mismo orden:

    GGH       (6 bloques): tipo | punto objetivo | dimension | base (un vector por linea) |
                           modulo | solucion
    LWE       (7 bloques): tipo | criptograma | n | q | coeficientes (una ecuacion por linea) |
                           terminos independientes | solucion
    Ring-LWE  (7 bloques): tipo | criptograma (c1 y c2, una linea cada uno) | n | q |
                           polinomio a | polinomio b | solucion

Asi que leer un fichero es: separarlo en bloques y coger cada bloque por su posicion.
De cada bloque sacamos los numeros enteros que aparecen, sin mirar llaves ni comas
(algunos ficheros tienen llaves de menos, y asi no importa).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


# ============================================================================ TIPOS DE TAREA

@dataclass
class TareaGGH:
    nombre: str                     # nombre del fichero, p. ej. "Tier0T01_Latt"
    problema: str                   # "SVP" o "CVP"
    dim: int                        # dimension de la celosia
    base: list[list[int]]           # un vector de la base por fila
    objetivo: list[int] | None      # punto objetivo del CVP (None en SVP)
    modulo: int | None              # "reduccion modulo n" (None si el fichero dice N/A)
    solucion: list[int] | None      # solucion que trae el fichero (None si dice N/D)


@dataclass
class TareaLWE:
    nombre: str
    problema: str                   # "rotura" (sacar s) o "criptoanalisis" (descifrar un bit)
    n: int                          # numero de incognitas (longitud del secreto s)
    q: int                          # modulo
    A: list[list[int]]              # coeficientes: una ecuacion por fila
    b: list[int]                    # terminos independientes (b = A s + e)
    criptograma: tuple[list[int], int] | None   # (coeficientes, termino independiente); None en rotura
    solucion: list[int] | int | None            # secreto s (rotura), bit (criptoanalisis) o None


@dataclass
class TareaRingLWE:
    nombre: str
    n: int                          # grado: trabajamos con polinomios modulo x^n + 1
    q: int                          # modulo de los coeficientes
    a: list[int]                    # clave publica (a, b); el coeficiente i es el de x^i
    b: list[int]
    c1: list[int]                   # criptograma (c1, c2)
    c2: list[int]
    solucion: list[int] | None      # palabra de bits (None si dice N/D)


# ============================================================================ LECTURA BASICA

def leer_bloques(ruta: str | Path) -> list[list[str]]:
    """Devuelve los bloques de datos del fichero (cada bloque es una lista de lineas)."""
    datos = Path(ruta).read_bytes()
    try:
        texto = datos.decode("utf-8-sig")   # "-sig": ignora la marca BOM que pone a veces el Bloc de notas
    except UnicodeDecodeError:
        texto = datos.decode("cp1252")   # los ficheros originales del Poliformat vienen asi

    bloques: list[list[str]] = []
    actual: list[str] = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if linea == "" or linea.startswith("#"):
            # Comentario o linea vacia: si estabamos leyendo un bloque, se ha terminado.
            if actual:
                bloques.append(actual)
                actual = []
        else:
            actual.append(linea)
    if actual:
        bloques.append(actual)
    return bloques


def numeros(texto: str) -> list[int]:
    """Todos los enteros que aparecen en el texto. Ejemplo: "{85, -42, 211}," -> [85, -42, 211]."""
    return [int(x) for x in re.findall(r"-?\d+", texto)]


def _sin_valor(linea: str) -> bool:
    """True si el fichero no da ese dato: pone "N/A" (no aplica) o "N/D" (no disponible).

    Ejemplos: el modulo en una celosia normal es N/A; la solucion de las tareas sin resolver es N/D.
    """
    return linea.strip().upper() in ("N/A", "N/D")


def _comprobar(condicion: bool, ruta: Path, mensaje: str) -> None:
    """Da un error claro, con el nombre del fichero, si algo no cuadra."""
    if not condicion:
        raise ValueError(f"{ruta.name}: {mensaje}")


# ============================================================================ GGH

def leer_ggh(ruta: str | Path) -> TareaGGH:
    ruta = Path(ruta)
    bloques = leer_bloques(ruta)
    _comprobar(len(bloques) == 6, ruta, f"se esperaban 6 bloques y hay {len(bloques)}")
    tipo, objetivo, dimension, base, modulo, solucion = bloques

    problema = tipo[0].upper()                      # "SVP" o "CVP"
    dim = int(dimension[0])
    tarea = TareaGGH(
        nombre=ruta.stem,
        problema=problema,
        dim=dim,
        base=[numeros(linea) for linea in base],   # un vector por linea
        objetivo=None if problema == "SVP" else numeros(objetivo[0]),   # en SVP pone "0 0"
        modulo=None if _sin_valor(modulo[0]) else int(modulo[0]),
        solucion=None if _sin_valor(solucion[0]) else numeros(solucion[0]),
    )

    _comprobar(problema in ("SVP", "CVP"), ruta, f"problema desconocido: {tipo[0]}")
    _comprobar(len(tarea.base) == dim and all(len(v) == dim for v in tarea.base),
               ruta, "la base no es de tamano dim x dim")
    _comprobar(tarea.objetivo is None or len(tarea.objetivo) == dim, ruta, "objetivo de tamano incorrecto")
    _comprobar(tarea.solucion is None or len(tarea.solucion) == dim, ruta, "solucion de tamano incorrecto")
    return tarea


# ============================================================================ LWE y Ring-LWE

def leer_lwe(ruta: str | Path) -> TareaLWE | TareaRingLWE:
    ruta = Path(ruta)
    bloques = leer_bloques(ruta)
    _comprobar(len(bloques) == 7, ruta, f"se esperaban 7 bloques y hay {len(bloques)}")
    tipo = bloques[0][0].lower()
    if "ring" in tipo:
        return _leer_ring_lwe(ruta, bloques)

    _, criptograma, n, q, coeficientes, terminos, solucion = bloques
    # Errata: algunos ficheros (Tier0T04, Tier0T05) dicen "criptograma" en vez de "criptoanalisis".
    problema = "rotura" if tipo.startswith("rotura") else "criptoanalisis"
    n, q = int(n[0]), int(q[0])

    # Criptograma: "{coeficientes}, termino independiente" -> el ultimo numero es el termino.
    cripto = None
    if not _sin_valor(criptograma[0]):
        valores = numeros(criptograma[0])
        cripto = (valores[:-1], valores[-1])

    # Solucion: el secreto (rotura) o un unico bit (criptoanalisis).
    sol = None
    if not _sin_valor(solucion[0]):
        valores = numeros(solucion[0])
        sol = valores if problema == "rotura" else valores[0]

    tarea = TareaLWE(
        nombre=ruta.stem,
        problema=problema,
        n=n,
        q=q,
        A=[numeros(linea) for linea in coeficientes],     # una ecuacion por linea
        b=numeros(" ".join(terminos)),
        criptograma=cripto,
        solucion=sol,
    )

    _comprobar(all(len(fila) == n for fila in tarea.A), ruta, "alguna ecuacion no tiene n coeficientes")
    _comprobar(len(tarea.b) == len(tarea.A), ruta,
               "distinto numero de ecuaciones y de terminos independientes")
    _comprobar(cripto is None or len(cripto[0]) == n, ruta, "criptograma de tamano incorrecto")
    # La rotura no trae criptograma y el criptoanalisis si: asi detectamos un tipo mal escrito.
    _comprobar((problema == "rotura") == (cripto is None), ruta,
               f"el tipo '{bloques[0][0]}' no cuadra con el criptograma")
    if problema == "rotura":
        _comprobar(sol is None or len(sol) == n, ruta, "el secreto de la solucion no tiene n valores")
    else:
        _comprobar(sol in (None, 0, 1), ruta, "la solucion de un criptoanalisis debe ser un bit")
    return tarea


def _leer_ring_lwe(ruta: Path, bloques: list[list[str]]) -> TareaRingLWE:
    _, criptograma, n, q, a, b, solucion = bloques
    _comprobar(len(criptograma) == 2, ruta, "el criptograma debe tener dos lineas (c1 y c2)")
    n, q = int(n[0]), int(q[0])
    tarea = TareaRingLWE(
        nombre=ruta.stem,
        n=n,
        q=q,
        a=numeros(a[0]),
        b=numeros(b[0]),
        c1=numeros(criptograma[0]),
        c2=numeros(criptograma[1]),
        # La palabra de bits se lee digito a digito ("0110 1100" -> [0, 1, 1, 0, 1, 1, 0, 0]).
        solucion=None if _sin_valor(solucion[0]) else [int(c) for c in solucion[0] if c in "01"],
    )
    for nombre_pol in ("a", "b", "c1", "c2"):
        _comprobar(len(getattr(tarea, nombre_pol)) == n, ruta,
                   f"el polinomio {nombre_pol} no tiene n coeficientes")
    _comprobar(tarea.solucion is None or len(tarea.solucion) == n, ruta, "la palabra de bits no tiene n bits")
    return tarea


# ============================================================================ TODAS LAS TAREAS

def leer_todas(carpeta_data: str | Path) -> dict[str, list]:
    """Lee todas las tareas. Devuelve {"ggh": [...], "lwe": [...], "ringlwe": [...]}."""
    carpeta = Path(carpeta_data)
    lwe_y_ring = [leer_lwe(ruta) for ruta in sorted((carpeta / "lwe").glob("*.txt"))]
    return {
        "ggh": [leer_ggh(ruta) for ruta in sorted((carpeta / "ggh").glob("*.txt"))],
        "lwe": [t for t in lwe_y_ring if isinstance(t, TareaLWE)],
        "ringlwe": [t for t in lwe_y_ring if isinstance(t, TareaRingLWE)],
    }
