"""Lectura de los ficheros de tareas (GGH y LWE / Ring-LWE).

Los ficheros son texto con lineas de comentario (#). Hay erratas en algunos
(llaves que faltan, 'criptograma' en vez de 'criptoanalisis'...), asi que el
parser no se fia de las llaves: aplana todos los enteros del cuerpo y reparte
segun las dimensiones declaradas.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_INT = re.compile(r"-?\d+")


def _body_lines(path: Path) -> list[str]:
    """Lineas no vacias y sin comentarios. UTF-8; los originales del Poliformat vienen en cp1252."""
    raw = Path(path).read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("cp1252", errors="replace")
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]


def _ints(s: str) -> list[int]:
    return [int(t) for t in _INT.findall(s)]


@dataclass
class GGHTask:
    name: str
    kind: str                      # "SVP" | "CVP"
    dim: int
    basis: list[list[int]]         # una fila por vector
    target: list[int] | None       # None en SVP
    modulus: int | None            # None si "N/A"
    expected: list[int] | None     # solucion de referencia si el fichero la trae


@dataclass
class LWETask:
    name: str
    kind: str                      # "rotura" | "criptoanalisis" | "ringlwe"
    dim: int
    q: int
    A: list[list[int]] = field(default_factory=list)   # m x n (LWE)
    b: list[int] = field(default_factory=list)         # m   (LWE)  /  polinomio b (Ring-LWE)
    a_poly: list[int] = field(default_factory=list)    # Ring-LWE
    cipher: tuple[list[int], int] | None = None        # (vector A, termino B)  LWE de 1 bit
    cipher_ring: tuple[list[int], list[int]] | None = None  # (c1, c2) Ring-LWE
    expected: list[int] | int | None = None


def parse_ggh(path: str | Path) -> GGHTask:
    path = Path(path)
    ln = _body_lines(path)
    kind = ln[0].strip().upper()
    dim = int(ln[2])
    target = _ints(ln[1])
    basis = [_ints(ln[3 + i]) for i in range(dim)]
    mod_s, sol_s = ln[3 + dim], ln[4 + dim]
    modulus = None if mod_s.upper().startswith("N/A") else int(mod_s)
    expected = None if sol_s.upper().startswith("N/D") else _ints(sol_s)
    assert all(len(r) == dim for r in basis), f"{path.name}: base no cuadrada"
    return GGHTask(path.stem, kind, dim, basis, None if kind == "SVP" else target[:dim], modulus, expected)


def parse_lwe(path: str | Path) -> LWETask:
    path = Path(path)
    ln = _body_lines(path)
    head = ln[0].lower()
    ring = "ring" in head
    kind = "ringlwe" if ring else ("rotura" if head.startswith("rotura") else "criptoanalisis")

    if ring:
        # ln: tipo, c1, c2, dim, q, a, b, solucion
        c1, c2 = _ints(ln[1]), _ints(ln[2])
        n, q = int(ln[3]), int(ln[4])
        a, b = _ints(ln[5]), _ints(ln[6])
        assert len(c1) == len(c2) == len(a) == len(b) == n, f"{path.name}: tamanos Ring-LWE"
        return LWETask(path.stem, kind, n, q, b=b, a_poly=a, cipher_ring=(c1, c2))

    # LWE: tipo, criptograma, dim, q, <coeficientes y terminos independientes>, solucion
    cipher = None
    if not ln[1].upper().startswith("N/A"):
        v = _ints(ln[1])
        cipher = (v[:-1], v[-1])
    n, q = int(ln[2]), int(ln[3])
    sol_s = ln[-1]
    flat = [x for line in ln[4:-1] for x in _ints(line)]
    assert len(flat) % (n + 1) == 0, f"{path.name}: {len(flat)} enteros no divisible por n+1={n+1}"
    m = len(flat) // (n + 1)
    A = [flat[i * n:(i + 1) * n] for i in range(m)]
    b = flat[m * n:]
    expected = None
    if not sol_s.upper().startswith("N/D"):
        v = _ints(sol_s)
        expected = v[0] if kind == "criptoanalisis" else v
    return LWETask(path.stem, kind, n, q, A=A, b=b, cipher=cipher, expected=expected)


def load_all(data_dir: str | Path) -> dict[str, list]:
    d = Path(data_dir)
    return {
        "ggh": [parse_ggh(p) for p in sorted((d / "ggh").glob("*.txt"))],
        "lwe": [parse_lwe(p) for p in sorted((d / "lwe").glob("*.txt"))],
    }
