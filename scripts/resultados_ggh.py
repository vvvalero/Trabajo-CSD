"""Regenerar resultados y tiempos de los GGH sin modulo.

Desde la raiz del proyecto:
    python3 scripts/resultados_ggh.py
    python3 scripts/resultados_ggh.py --salida /tmp/ggh_exactos.csv

Sigue la ruta del resolutor: LLL + enumeracion exacta. Separa ambos tiempos y
registra las estadisticas de busqueda. Es una medicion puntual, no un estudio
comparativo ni una prueba independiente de optimalidad. El CSV se genera en
results/, carpeta ignorada por Git; no es necesario versionarlo.
"""
from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict
from pathlib import Path
from time import perf_counter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from pqc.celosias import lll  # noqa: E402
from pqc.celosias.enumeracion import EstadisticasEnumeracion, enumeracion  # noqa: E402
from pqc.lector_tareas import leer_todas  # noqa: E402
from pqc.matrices import es_entera, inversa, norma2, resta_vectores, vector_por_matriz  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--salida", type=Path, default=ROOT / "results" / "ggh_exactos.csv")
    args = parser.parse_args()
    filas = []
    modulares = 0
    for tarea in leer_todas(ROOT / "data")["ggh"]:
        if tarea.modulo:
            modulares += 1
            continue

        inicio = perf_counter()
        base = lll(tarea.base)
        despues_lll = perf_counter()
        datos = EstadisticasEnumeracion()
        punto = enumeracion(base, tarea.objetivo, estadisticas=datos)
        fin = perf_counter()

        # La validacion se hace despues de medir el tiempo de los algoritmos.
        objetivo = tarea.objetivo if tarea.objetivo is not None else [0] * tarea.dim
        distancia = norma2(resta_vectores(punto, objetivo))
        if not es_entera(vector_por_matriz(punto, inversa(tarea.base))):
            raise RuntimeError(f"{tarea.nombre}: el resultado no pertenece a la celosia")
        if tarea.problema == "SVP" and not any(punto):
            raise RuntimeError(f"{tarea.nombre}: SVP no admite el cero")
        if datos.radio2_final != distancia:
            raise RuntimeError(f"{tarea.nombre}: distancia incoherente con las estadisticas")
        if tarea.solucion is not None and distancia != norma2(resta_vectores(tarea.solucion, objetivo)):
            raise RuntimeError(f"{tarea.nombre}: no coincide la distancia de referencia")

        filas.append({
            "tarea": tarea.nombre, "problema": tarea.problema, "dimension": tarea.dim,
            **asdict(datos),
            "segundos_lll": f"{despues_lll - inicio:.9f}",
            "segundos_enumeracion": f"{fin - despues_lll:.9f}",
            "segundos_total": f"{fin - inicio:.9f}", "punto": str(punto),
        })
        print(f"{tarea.nombre}: distancia2 {datos.radio2_inicial} -> {distancia}; {datos.nodos} nodos")

    if not filas:
        raise RuntimeError("No se han encontrado tareas GGH sin modulo")
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    with args.salida.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        escritor.writeheader()
        escritor.writerows(filas)
    print(f"Guardadas {len(filas)} tareas en {args.salida}; {modulares} modulares pendientes excluidas.")


if __name__ == "__main__":
    main()
