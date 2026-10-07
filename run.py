"""CLI del proyecto.

  python run.py list              lista las tareas y sus parametros
  python run.py solve <nombre>    ejecuta el solver de una tarea (p.ej. Tier0T01_Latt)
  python run.py all               ejecuta todas y escribe results/results.md
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))

from pqc import ggh, lwe  # noqa: E402
from pqc.tasks import GGHTask, load_all  # noqa: E402


def solve_task(t):
    if isinstance(t, GGHTask):
        return ggh.solve(t)
    if t.kind == "ringlwe":
        s = lwe.break_ring_key(t)
        return lwe.decrypt_ring(t, s)
    s = lwe.break_key(t)
    return s if t.kind == "rotura" else lwe.decrypt_bit(t, s)


def main(argv):
    tasks = load_all(ROOT / "data")
    allt = {t.name: t for ts in tasks.values() for t in ts}
    cmd = argv[1] if len(argv) > 1 else "list"
    if cmd == "list":
        for t in allt.values():
            extra = f"{t.kind} dim={t.dim}" + (f" mod={t.modulus}" if isinstance(t, GGHTask) and t.modulus else "")
            if not isinstance(t, GGHTask):
                extra += f" q={t.q}" + (f" m={len(t.A)}" if t.A else "")
            print(f"{t.name:20s} {extra}")
    elif cmd in ("solve", "all"):
        names = [argv[2]] if cmd == "solve" else list(allt)
        rows = []
        for n in names:
            t0 = time.perf_counter()
            try:
                res = solve_task(allt[n])
            except NotImplementedError:
                res = "TODO"
            rows.append((n, res, allt[n].expected, time.perf_counter() - t0))
            print(f"{n:20s} {res} (esperado: {allt[n].expected}) {rows[-1][3]:.3f}s")
        if cmd == "all":
            out = ["| tarea | resultado | esperado | s |", "|---|---|---|---|"]
            out += [f"| {n} | {r} | {e} | {s:.3f} |" for n, r, e, s in rows]
            (ROOT / "results").mkdir(exist_ok=True)
            (ROOT / "results" / "results.md").write_text("\n".join(out), encoding="utf-8")
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
