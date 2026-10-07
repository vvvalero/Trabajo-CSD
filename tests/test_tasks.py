from pathlib import Path

from pqc.tasks import load_all

DATA = Path(__file__).parent.parent / "data"


def test_all_files_parse():
    t = load_all(DATA)
    assert len(t["ggh"]) == 22 and len(t["lwe"]) == 23


def test_lwe_shapes():
    for t in load_all(DATA)["lwe"]:
        if t.kind != "ringlwe":
            assert len(t.A) == len(t.b) and all(len(r) == t.dim for r in t.A), t.name


def test_ggh_shapes():
    for t in load_all(DATA)["ggh"]:
        assert len(t.basis) == t.dim and (t.kind == "SVP") == (t.target is None), t.name


# TODO: tests de cada algoritmo. Las tareas Tier0 traen solucion (task.expected):
#   - GGH Tier0T01..T05: ggh.solve(t) == t.expected
#   - LWE Tier0T01..T05: lwe.break_key / decrypt_bit == t.expected
# TODO: ejemplos del PDF (GGH Ej.1-3: c=<43,176>; LWE Ej.4-6) como tests de validacion.
