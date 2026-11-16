"""Regenerar las mediciones, soluciones y trazas de la propuesta de memoria.

  python3 reportproposal/generar_datos.py --repeticiones 21

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
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from pqc.celosias import babai_plano_cercano, babai_redondeo, gso, lll  # noqa: E402
from pqc.celosias.enumeracion import EstadisticasEnumeracion, enumeracion  # noqa: E402
from pqc.lector_tareas import leer_todas  # noqa: E402
from pqc.matrices import es_entera, inversa, norma2, resta_vectores, vector_por_matriz  # noqa: E402

SELECCION = ["Tier01T05_Latt", "Tier02T01_Latt", "Tier02T02_Latt", "Tier02T04_Latt",
             "Tier02T05_Latt", "Tier03T03_Latt", "Tier03T04_Latt"]


def escribir_csv(ruta, filas):
    with ruta.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


def etiqueta(nombre):
    tier, numero = nombre[len("Tier"):].split("T")
    return f"{int(tier)}.{int(numero.split('_')[0]):02d}"


def vector_tex(p):
    return "(" + ",".join(str(int(v)) for v in p) + ")"


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
    resultados, curvas, puntos, trazas = [], [], {}, {}
    for tarea in tareas.values():
        t = tarea.objetivo if tarea.objetivo is not None else [0] * tarea.dim
        enumeracion(lll(tarea.base), tarea.objetivo)   # calentamiento, fuera de las medidas
        medidas_lll, medidas_enum, medidas_total, medidas_babai = [], [], [], []
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
            if tarea.objetivo is not None:
                ini_babai = perf_counter()
                aproximado = babai_plano_cercano(R, t)
                fin_babai = perf_counter()
                medidas_babai.append(1000 * ((medio - ini) + fin_babai - ini_babai))

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
        if tarea.objetivo is not None:
            curvas.append({"tarea": tarea.nombre, "dimension": tarea.dim,
                           "ms_babai": statistics.median(medidas_babai), "ms_exacto": fila["ms_total"]})
        if tarea.nombre in ("Tier01T05_Latt", "Tier02T03_Latt"):
            mu, normas, _ = gso(R)
            traza = {"base_original": tarea.base, "base_reducida": R, "objetivo": tarea.objetivo,
                     "mu": [[str(v) for v in row] for row in mu], "normas2_gso": [str(v) for v in normas],
                     "optimo": punto, "coef_optimos": [int(v) for v in vector_por_matriz(punto, inversa(R))],
                     "estadisticas": {k: str(v) for k, v in asdict(datos).items()}}
            if tarea.objetivo is not None:
                traza.update({"babai": aproximado,
                              "coef_babai": [int(v) for v in vector_por_matriz(aproximado, inversa(R))],
                              "d2_babai": int(norma2(resta_vectores(aproximado, t))),
                              "d2_redondeo": int(norma2(resta_vectores(babai_redondeo(R, t), t)))})
            trazas[tarea.nombre] = traza

    escribir_csv(carpeta / "resultados.csv", resultados)
    escribir_csv(carpeta / "comparacion_cvp.csv", curvas)
    (carpeta / "trazas.json").write_text(json.dumps(trazas, indent=2, ensure_ascii=False) + "\n")
    por_nombre = {f["tarea"]: f for f in resultados}
    filas_tex, soluciones_tex = [], []
    for nombre in SELECCION:
        f = por_nombre[nombre]
        tiempo = f"{f['ms_total']:.2f}".replace(".", "{,}")
        filas_tex.append(f"{f['etiqueta']} & {f['tipo']} & {f['dimension']} & {f['radio2_inicial']} & {f['d2']} & {f['nodos']} & {tiempo} \\\\")
        p = puntos[nombre]
        indice = f"v_{{\\text{{{f['etiqueta']}}}}}"
        if len(p) > 7:
            soluciones_tex.append(f"{indice}={{}}&({','.join(map(str,p[:8]))},\\\\\n &\\phantom{{(}}{','.join(map(str,p[8:]))}) \\\\")
        else:
            soluciones_tex.append(f"{indice}={{}}&{vector_tex(p)} \\\\")
    cabecera = ("\\begin{tabular}{@{}lcrrrrr@{}}\n\\toprule\n"
                "Tarea & Tipo & $n$ & $R_0^2$ & $d^2$ óptima & Nodos & Tiempo (ms)\\\\\n\\midrule\n")
    (carpeta / "tabla_seleccion.tex").write_text(cabecera + "\n".join(filas_tex) + "\n\\bottomrule\n\\end{tabular}\n")
    (carpeta / "soluciones.tex").write_text("\\begin{align*}\n" + "\n".join(soluciones_tex) + "\n\\end{align*}\n")
    datos_plot = []
    for nombre_columna, macro in [("ms_babai", "PuntosBabai"), ("ms_exacto", "PuntosExactos")]:
        coords = " ".join(f"({f['dimension']},{f[nombre_columna]:.6f})" for f in curvas)
        datos_plot.append(f"\\newcommand{{\\{macro}}}{{{coords}}}")
    datos_plot.append(f"\\newcommand{{\\Repeticiones}}{{{args.repeticiones}}}")
    (carpeta / "mediciones.tex").write_text("\n".join(datos_plot) + "\n")
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = "no disponible"
    fuentes = [ROOT / "src/pqc/celosias" / n for n in ("gso.py", "lll.py", "babai.py", "enumeracion.py")]
    entorno = {"fecha_documento": "2026-11-15", "python": sys.version, "sistema": platform.platform(),
               "arquitectura": platform.machine(), "repeticiones": args.repeticiones, "calentamiento": 1,
               "estadistico": "mediana", "unidad_tiempos": "ms", "commit": commit,
               "hashes_fuentes": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in fuentes}}
    (carpeta / "entorno.json").write_text(json.dumps(entorno, indent=2, ensure_ascii=False) + "\n")
    print(f"Regeneradas {len(resultados)} tareas, {len(curvas)} CVP comparados y {len(SELECCION)} seleccionadas.")
    print(f"Medianas de {args.repeticiones} repeticiones; Python {platform.python_version()}, {platform.machine()}.")


if __name__ == "__main__":
    main()
