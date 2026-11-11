from pathlib import Path

import pytest

from pqc.lector_tareas import leer_bloques, leer_ggh, leer_lwe, leer_todas, numeros

DATA = Path(__file__).parent.parent / "data"


def test_se_leen_todos_los_ficheros():
    t = leer_todas(DATA)
    assert len(t["ggh"]) == 22 and len(t["lwe"]) == 20 and len(t["ringlwe"]) == 3


def test_numeros_ignora_llaves_y_comas():
    assert numeros("{85, -42, 211},") == [85, -42, 211]
    assert numeros("1161, 1060, 508}") == [1161, 1060, 508]      # llave que falta (Tier3T01_LWE)


def test_bloques_ggh():
    # tipo | objetivo | dimension | base (2 lineas) | modulo | solucion
    assert leer_bloques(DATA / "ggh" / "Tier0T01_Latt.txt") == [
        ["CVP"], ["81 76"], ["2"], ["3 0", "0 2"], ["N/A"], ["81 76"],
    ]


# ----------------------------------------------------------------------------- GGH

def test_ggh_cvp_con_solucion():
    t = leer_ggh(DATA / "ggh" / "Tier0T01_Latt.txt")
    assert (t.problema, t.dim, t.base, t.objetivo, t.modulo, t.solucion) == (
        "CVP", 2, [[3, 0], [0, 2]], [81, 76], None, [81, 76])


def test_ggh_svp_sin_objetivo_y_con_modulo():
    t = leer_ggh(DATA / "ggh" / "Tier03T05_Latt.txt")
    assert t.problema == "SVP" and t.objetivo is None and t.modulo == 541 and t.solucion is None
    assert t.base[1] == [482, 2, 2, 5, 14]


def test_ggh_formas():
    for t in leer_todas(DATA)["ggh"]:
        assert len(t.base) == t.dim and all(len(v) == t.dim for v in t.base), t.nombre
        assert (t.problema == "SVP") == (t.objetivo is None), t.nombre


# ----------------------------------------------------------------------------- LWE

def test_lwe_rotura():
    t = leer_lwe(DATA / "lwe" / "Tier0T01_LWE.txt")
    assert (t.problema, t.n, t.q, len(t.A)) == ("rotura", 3, 229, 10)
    assert t.A[0] == [85, 42, 211] and t.b[0] == 47
    assert t.criptograma is None and t.solucion == [81, 55, 152]


def test_lwe_criptoanalisis():
    t = leer_lwe(DATA / "lwe" / "Tier0T03_LWE.txt")
    assert t.problema == "criptoanalisis"
    assert t.criptograma == ([186, 202, 73, 192], 174)
    assert t.solucion == 1


@pytest.mark.parametrize("nombre", ["Tier0T04_LWE", "Tier0T05_LWE"])
def test_lwe_errata_criptograma(nombre):
    # Errata: el fichero dice "criptograma" en lugar de "criptoanalisis"
    assert leer_lwe(DATA / "lwe" / f"{nombre}.txt").problema == "criptoanalisis"


def test_lwe_errata_llaves_que_faltan():
    t = leer_lwe(DATA / "lwe" / "Tier3T01_LWE.txt")
    assert len(t.A) == len(t.b) == 18 and t.b[0] == 1161


def test_lwe_formas():
    for t in leer_todas(DATA)["lwe"]:
        assert len(t.A) == len(t.b) and all(len(fila) == t.n for fila in t.A), t.nombre


# ----------------------------------------------------------------------------- Ring-LWE

def test_ring_lwe():
    t = leer_lwe(DATA / "lwe" / "Tier3_T01_LWE.txt")
    assert (t.n, t.q) == (16, 1399)
    assert t.a[:3] == [3, 14, 13] and t.b[0] == 1330
    assert t.c1[0] == 10 and t.c2[0] == 89
    assert t.solucion is None


def test_ring_lwe_formas():
    for t in leer_todas(DATA)["ringlwe"]:
        assert len(t.a) == len(t.b) == len(t.c1) == len(t.c2) == t.n, t.nombre


# ----------------------------------------------------------------------------- ficheros raros o mal formados

GGH_MINIMO = "#\nCVP\n#\n1 2\n#\n2\n#\n3 0\n0 2\n#\nN/A\n#\nN/D\n"


def test_fichero_con_bom(tmp_path):
    ruta = tmp_path / "con_bom.txt"
    ruta.write_bytes(b"\xef\xbb\xbf" + GGH_MINIMO.encode())
    assert leer_ggh(ruta).base == [[3, 0], [0, 2]]


def test_fichero_cp1252(tmp_path):
    ruta = tmp_path / "cp1252.txt"
    ruta.write_bytes(("# Dimensión de la celosía\n" + GGH_MINIMO).encode("cp1252"))
    assert leer_ggh(ruta).dim == 2


def test_error_claro_si_falta_un_vector(tmp_path):
    ruta = tmp_path / "mal.txt"
    ruta.write_text(GGH_MINIMO.replace("0 2\n", ""), encoding="utf-8")
    with pytest.raises(ValueError, match="mal.txt: la base"):
        leer_ggh(ruta)


def test_error_si_rotura_trae_criptograma(tmp_path):
    # Cambiamos la linea de datos "N/A" (no la del comentario, que tambien contiene "N/A")
    texto = (DATA / "lwe" / "Tier0T01_LWE.txt").read_text(encoding="utf-8")
    texto = texto.replace("\nN/A\n", "\n{1, 2, 3}, 4\n", 1)
    ruta = tmp_path / "rotura_mal.txt"
    ruta.write_text(texto, encoding="utf-8")
    with pytest.raises(ValueError, match="no cuadra con el criptograma"):
        leer_lwe(ruta)


# TODO: tests de cada algoritmo. Las tareas Tier0 traen solucion (tarea.solucion):
#   - GGH Tier0T01..T05: ggh.solve(t) == t.solucion
#   - LWE Tier0T01..T05: lwe.romper_clave / lwe.descifrar_bit == t.solucion
