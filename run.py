"""Resolver las tareas desde la terminal.

  python run.py list              lista las tareas y sus parametros
  python run.py solve <nombre>    resuelve una tarea (p. ej. python run.py solve Tier0T01_Latt)
  python run.py all               resuelve todas y guarda la tabla en results/results.md
"""
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).parent
sys.path.insert(0, str(RAIZ / "src"))   # para poder importar el paquete pqc

from pqc import ggh, lwe  # noqa: E402
from pqc.lector_tareas import TareaGGH, TareaRingLWE, leer_todas  # noqa: E402


def describir(tarea) -> str:
    """Una linea con los datos principales de la tarea (para 'list')."""
    if isinstance(tarea, TareaGGH):
        modulo = f" mod={tarea.modulo}" if tarea.modulo else ""
        return f"GGH {tarea.problema} dim={tarea.dim}{modulo}"
    if isinstance(tarea, TareaRingLWE):
        return f"Ring-LWE n={tarea.n} q={tarea.q}"
    return f"LWE {tarea.problema} n={tarea.n} q={tarea.q} ecuaciones={len(tarea.A)}"


def resolver(tarea):
    """Llama al metodo que corresponde segun el tipo de tarea."""
    if isinstance(tarea, TareaGGH):
        return ggh.solve(tarea)
    if isinstance(tarea, TareaRingLWE):
        s = lwe.romper_clave_ring(tarea)
        return lwe.descifrar_ring(tarea, s)
    s = lwe.romper_clave(tarea)
    if tarea.problema == "rotura":
        return s
    return lwe.descifrar_bit(tarea, s)


def resolver_y_medir(tarea):
    """Resuelve la tarea, la imprime y devuelve (nombre, resultado, esperado, segundos)."""
    inicio = time.perf_counter()
    try:
        resultado = resolver(tarea)
    except NotImplementedError:
        resultado = "sin implementar"
    segundos = time.perf_counter() - inicio
    print(f"{tarea.nombre:20s} {resultado}  (esperado: {tarea.solucion})  {segundos:.3f} s")
    return tarea.nombre, resultado, tarea.solucion, segundos


def guardar_tabla(filas) -> None:
    """Guarda los resultados como tabla Markdown en results/results.md."""
    lineas = ["| tarea | resultado | esperado | segundos |", "|---|---|---|---|"]
    lineas += [f"| {nombre} | {res} | {esp} | {seg:.3f} |" for nombre, res, esp, seg in filas]
    carpeta = RAIZ / "results"
    carpeta.mkdir(exist_ok=True)
    (carpeta / "results.md").write_text("\n".join(lineas), encoding="utf-8")
    print(f"Tabla guardada en {carpeta / 'results.md'}")


def main(argumentos) -> None:
    tareas = {t.nombre: t for lista in leer_todas(RAIZ / "data").values() for t in lista}
    orden = argumentos[1] if len(argumentos) > 1 else "list"

    if orden == "list":
        for tarea in tareas.values():
            print(f"{tarea.nombre:20s} {describir(tarea)}")

    elif orden == "solve" and len(argumentos) == 3:
        nombre = argumentos[2]
        if nombre not in tareas:
            print(f"No existe la tarea '{nombre}'. Usa 'python run.py list' para ver los nombres.")
            return
        resolver_y_medir(tareas[nombre])

    elif orden == "all":
        guardar_tabla([resolver_y_medir(tarea) for tarea in tareas.values()])

    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
