"""Datos GGH de la memoria: tabla de resultados, trazas y tiempos.

  python reportproposal/generar_datos.py --repeticiones 21

No modifica report/ ni el codigo de los algoritmos. Cada tiempo publicado es
la mediana de repeticiones con perf_counter, tras una ejecucion de calentamiento.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import statistics
import subprocess
import sys
from dataclasses import asdict
from datetime import date
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from pqc.celosias import babai_plano_cercano, babai_redondeo, gso, lll  # noqa: E402
from pqc.celosias.enumeracion import EstadisticasEnumeracion, enumeracion  # noqa: E402
from pqc.lector_tareas import leer_todas  # noqa: E402
from pqc.matrices import es_entera, inversa, norma2, resta_vectores, vector_por_matriz  # noqa: E402

def escribir_csv(ruta, filas):
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def etiqueta(nombre):
    tier, numero = nombre[len("Tier"):].split("T")
    return f"{int(tier)}.{int(numero.split('_')[0]):02d}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repeticiones", type=int, default=21)
    args = parser.parse_args()
    if args.repeticiones < 1:
        parser.error("Se necesita al menos una repeticion")
    carpeta = HERE / "datos"
    carpeta.mkdir(exist_ok=True)
    todas = leer_todas(ROOT / "data")["ggh"]
    tareas = {t.nombre: t for t in todas if not t.modulo}
    resultados, puntos, trazas = [], {}, {}
    for tarea in tareas.values():
        t = tarea.objetivo if tarea.objetivo is not None else [0] * tarea.dim
        enumeracion(lll(tarea.base), tarea.objetivo)   # calentamiento, fuera de las medidas
        medidas_lll, medidas_enum, medidas_total = [], [], []
        for _ in range(args.repeticiones):
            ini = perf_counter()
            R = lll(tarea.base)
            medio = perf_counter()
            datos = EstadisticasEnumeracion()
            punto = enumeracion(R, tarea.objetivo, estadisticas=datos)
            fin = perf_counter()
            medidas_lll.append(1000 * (medio - ini))
            medidas_enum.append(1000 * (fin - medio))
            medidas_total.append(1000 * (fin - ini))

        distancia = norma2(resta_vectores(punto, t))
        if not es_entera(vector_por_matriz(punto, inversa(tarea.base))):
            raise RuntimeError(f"Punto ajeno a la celosia en {tarea.nombre}")
        if tarea.objetivo is None and not any(punto):
            raise RuntimeError("El cero no es una solucion de SVP")
        if tarea.solucion is not None and punto != tarea.solucion:
            raise RuntimeError(f"No coincide la referencia de {tarea.nombre}")
        if distancia != datos.radio2_final:
            raise RuntimeError("Estadisticas incoherentes con el punto obtenido")
        fila = {"tarea": tarea.nombre, "etiqueta": etiqueta(tarea.nombre), "tipo": tarea.problema,
                "dimension": tarea.dim, "d2": str(distancia), "nodos": datos.nodos,
                "mejoras": datos.mejoras, "radio2_inicial": str(datos.radio2_inicial),
                "ms_lll": statistics.median(medidas_lll), "ms_enum": statistics.median(medidas_enum),
                "ms_total": statistics.median(medidas_total), "punto": json.dumps(punto)}
        resultados.append(fila)
        puntos[tarea.nombre] = punto
        # Datos de las trazas de la memoria (2.03 y 3.03), con fracciones exactas.
        if tarea.nombre in ("Tier02T03_Latt", "Tier03T03_Latt"):
            mu, normas, _ = gso(R)
            traza = {"base_original": tarea.base, "base_reducida": R, "objetivo": tarea.objetivo,
                     "mu": [[str(v) for v in row] for row in mu], "normas2_gso": [str(v) for v in normas],
                     "optimo": punto, "coef_optimos": [int(v) for v in vector_por_matriz(punto, inversa(R))],
                     "estadisticas": {k: str(v) for k, v in asdict(datos).items()}}
            if tarea.objetivo is not None:
                aproximado = babai_plano_cercano(R, t)
                traza.update({"babai": aproximado,
                              "coef_babai": [int(v) for v in vector_por_matriz(aproximado, inversa(R))],
                              "d2_babai": int(norma2(resta_vectores(aproximado, t))),
                              "d2_redondeo": int(norma2(resta_vectores(babai_redondeo(R, t), t)))})
            trazas[tarea.nombre] = traza

    escribir_csv(carpeta / "resultados.csv", resultados)
    (carpeta / "trazas.json").write_text(json.dumps(trazas, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    por_nombre = {f["tarea"]: f for f in resultados}
    filas_tex = []
    # Todas las tareas GGH puntuables (niveles 1 a 3, sin modulo), ordenadas por etiqueta: 1.01, 1.02...
    # Una fila por tarea con el resultado y el punto obtenido, p. ej.
    #   2.03 & CVP & 5 & 155 & 7 & 1{,}26 & $(807,997,549,1528,155)$ \\
    # (la distancia del punto de partida, R0^2, coincide con d^2 salvo en 2.03, que se comenta en el texto)
    puntuables = sorted((n for n in tareas if not n.startswith("Tier0T")), key=etiqueta)
    for nombre in puntuables:
        f = por_nombre[nombre]
        tiempo = f"{f['ms_total']:.2f}".replace(".", "{,}")
        punto = "$(" + ",".join(str(int(v)) for v in puntos[nombre]) + ")$"
        # (la dimension no va en columna aparte: es el numero de coordenadas del punto)
        # (los nodos de la enumeracion no caben; estan en resultados.csv y se comentan en el texto)
        filas_tex.append(f"{f['etiqueta']} & {f['tipo']} & {f['d2']} & {tiempo} & {punto} \\\\")
    cabecera = ("\\setlength{\\tabcolsep}{5pt}\n\\begin{tabular}{@{}lcrrl@{}}\n\\toprule\n"
                "Tarea & Tipo & $d^2$ & ms & Punto obtenido\\\\\n\\midrule\n")
    (carpeta / "tabla_ggh.tex").write_text(cabecera + "\n".join(filas_tex) + "\n\\bottomrule\n\\end{tabular}\n",
                                           encoding="utf-8")
    datos_plot = []
    # Curva GGH para la grafica: mediana del tiempo de las tareas de cada dimension. Solo se escribe
    # el tiempo junto a la primera, la de dimension 7 y la ultima, para no amontonar etiquetas.
    por_dim = {}
    for f in resultados:
        por_dim.setdefault(f["dimension"], []).append(f["ms_total"])
    dims = sorted(por_dim)
    curva = []
    for d in dims:
        ms = statistics.median(por_dim[d])
        texto = f"{ms:.1f} ms".replace(".", ",") if d in (dims[0], 7, dims[-1]) else ""
        curva.append(f"({d},{ms:.6f}) [{texto}]")
    datos_plot.append(f"\\newcommand{{\\CurvaGGH}}{{{' '.join(curva)}}}")
    datos_plot.append(f"\\newcommand{{\\Repeticiones}}{{{args.repeticiones}}}")
    (carpeta / "mediciones.tex").write_text("\n".join(datos_plot) + "\n", encoding="utf-8")
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "no disponible"
    fuentes = [ROOT / "src/pqc/celosias" / n for n in ("gso.py", "lll.py", "babai.py", "enumeracion.py")]
    entorno = {"fecha_documento": date.today().isoformat(), "python": sys.version, "sistema": platform.platform(),
               "arquitectura": platform.machine(), "repeticiones": args.repeticiones, "calentamiento": 1,
               "estadistico": "mediana", "unidad_tiempos": "ms", "commit": commit,
               "hashes_fuentes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in fuentes}}
    (carpeta / "entorno.json").write_text(json.dumps(entorno, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Regeneradas {len(resultados)} tareas GGH ({len(puntuables)} en la tabla).")
    print(f"Medianas de {args.repeticiones} repeticiones; Python {platform.python_version()}, {platform.machine()}.")


if __name__ == "__main__":
    main()
