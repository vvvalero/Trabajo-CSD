"""Datos de LWE y Ring-LWE para la memoria: tabla de resultados y tiempos.

  python reportproposal/generar_datos_lwe.py --repeticiones 5

Escribe en reportproposal/datos/:
  tabla_lwe.tex       una fila por tarea LWE resuelta (Tier1 y Tier2) y por tarea Ring-LWE
  mediciones_lwe.tex  coordenadas (dimension, ms) para la grafica de tiempo frente a talla
  resultados_lwe.csv  lo mismo en CSV, con el secreto y el error completos

Cada tiempo es la mediana de las repeticiones (perf_counter), tras una ejecucion de calentamiento.
"""
from __future__ import annotations

import argparse
import csv
import math
import statistics
import sys
from pathlib import Path
from time import perf_counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "src"))

from pqc.lector_tareas import leer_todas  # noqa: E402
from pqc.lwe.ataque_celosia import ataque  # noqa: E402
from pqc.lwe.descifrado import descifrar_bit  # noqa: E402
from pqc.lwe.resolver import romper_clave  # noqa: E402
from pqc.lwe.ring import descifrar_ring, producto_polinomios, romper_clave_ring  # noqa: E402
from pqc.matrices import centrado_vector, matriz_por_vector, mod_matriz, resta_vectores  # noqa: E402

# Tareas LWE que resuelve la fuerza bruta (las de Tier0 no puntuan y no se muestran).
LWE = ["Tier1T01_LWE", "Tier1T02_LWE", "Tier1T03_LWE", "Tier1T04_LWE", "Tier1T05_LWE",
       "Tier2T01_LWE", "Tier2T02_LWE", "Tier2T03_LWE"]
# Tareas LWE que resolvemos como CVP en la celosia q-aria (demasiado grandes para la fuerza bruta).
LWE_CELOSIA = ["Tier2T04_LWE", "Tier2T05_LWE", "Tier3T01_LWE", "Tier3T02_LWE", "Tier3T03_LWE",
               "Tier3T04_LWE", "Tier3T05_LWE"]


def mediana_ms(funcion, repeticiones):
    """Ejecuta funcion() una vez para calentar y devuelve la mediana de los tiempos en ms."""
    funcion()
    tiempos = []
    for _ in range(repeticiones):
        ini = perf_counter()
        funcion()
        tiempos.append(1000 * (perf_counter() - ini))
    return statistics.median(tiempos)


def tiempo_legible(ms):
    """0.104 -> '0,1 ms';  92.3 -> '92 ms';  1404 -> '1,4 s'."""
    if ms < 1:
        return f"{ms:.1f} ms".replace(".", ",")
    if ms < 1000:
        return f"{round(ms)} ms"
    return f"{ms / 1000:.1f} s".replace(".", ",")


def coordenadas_con_etiqueta(puntos):
    """[(3, 6.7), (4, 92)] -> '(3,6.7) [7 ms] (4,92) [92 ms]' (pgfplots escribe la etiqueta junto al punto)."""
    return " ".join(f"({x},{ms:.6f}) [{tiempo_legible(ms)}]" for x, ms in puntos)


def factores(puntos, x_medio):
    """Un texto 'xK' entre cada par de puntos seguidos, K = cuanto se multiplica el tiempo.
    x_medio dice donde cae la mitad en el eje X (media normal si el eje es lineal, geometrica si es logaritmico).
    """
    nodos = []
    for (x1, t1), (x2, t2) in zip(puntos, puntos[1:]):
        nodos.append(f"\\node[factor] at (axis cs:{x_medio(x1, x2):.4f},{math.sqrt(t1 * t2):.6f}) "
                     f"{{$\\times{round(t2 / t1)}$}};")
    return " ".join(nodos)


def ms_tex(ms):
    """3.14159 -> '3{,}14' (coma decimal en LaTeX)."""
    return f"{ms:.2f}".replace(".", "{,}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeticiones", type=int, default=5)
    args = parser.parse_args()
    todas = leer_todas(ROOT / "data")
    lwe = {t.nombre: t for t in todas["lwe"]}
    filas_csv, filas_tex, puntos_lwe, puntos_ring = [], [], [], []

    # ------------------------------------------------------------------ LWE: fuerza bruta
    for nombre in LWE:
        t = lwe[nombre]
        s = romper_clave(t)
        # Error de todas las ecuaciones con el secreto encontrado: e = b - A s (centrado).
        e = centrado_vector(resta_vectores(t.b, matriz_por_vector(mod_matriz(t.A, t.q), s)), t.q)
        c = max(abs(x) for x in e)            # cota del error que ha necesitado la busqueda
        if t.problema == "rotura":
            resultado = "$s=(" + ",".join(map(str, s)) + ")$"
            ms = mediana_ms(lambda: romper_clave(t), args.repeticiones)
        else:
            resultado = f"bit {descifrar_bit(t, s)}"
            ms = mediana_ms(lambda: descifrar_bit(t, romper_clave(t)), args.repeticiones)
        # Prefijo L para no confundirlas con las GGH: Tier1T05_LWE -> L1.05 (la GGH 1.05 es otra tarea)
        etiqueta = "L" + nombre.replace("Tier", "").replace("_LWE", "").replace("T0", ".0")
        filas_tex.append(f"{etiqueta} & {t.n} & {len(t.A)} & {t.q} & {c} & "
                         f"${2 * c + 1}^{{{t.n}}}$ & {resultado} & {ms_tex(ms)} \\\\")
        filas_csv.append({"tarea": nombre, "n": t.n, "m": len(t.A), "q": t.q, "cota_error": c,
                          "resultado": resultado, "secreto": s, "error": e, "ms": ms})
        puntos_lwe.append((t.n, ms, c))      # c: cota del error, para separar las series en la grafica

    # ------------------------------------------------------------------ LWE: CVP en la celosia q-aria
    # Las que la fuerza bruta no alcanza. Se llama directamente a ataque() para medir solo este metodo.
    filas_tex.append("\\midrule")
    t203 = lwe["Tier2T03_LWE"]
    if ataque(t203) != romper_clave(t203):          # los dos metodos deben dar el mismo secreto
        raise RuntimeError("L2.03: la fuerza bruta y el CVP no coinciden")
    ms_l203_cvp = mediana_ms(lambda: descifrar_bit(t203, ataque(t203)), args.repeticiones)
    for nombre in LWE_CELOSIA:
        t = lwe[nombre]
        s = ataque(t)
        e = centrado_vector(resta_vectores(t.b, matriz_por_vector(mod_matriz(t.A, t.q), s)), t.q)
        c = max(abs(x) for x in e)
        if t.problema == "rotura":
            resultado = "$s=(" + ",".join(map(str, s)) + ")$"
            ms = mediana_ms(lambda: ataque(t), args.repeticiones)
        else:
            resultado = f"bit {descifrar_bit(t, s)}"
            ms = mediana_ms(lambda: descifrar_bit(t, ataque(t)), args.repeticiones)
        etiqueta = "L" + nombre.replace("Tier", "").replace("_LWE", "").replace("T0", ".0")
        filas_tex.append(f"{etiqueta} & {t.n} & {len(t.A)} & {t.q} & {c} & -- & {resultado} & {ms_tex(ms)} \\\\")
        filas_csv.append({"tarea": nombre, "n": t.n, "m": len(t.A), "q": t.q, "cota_error": c,
                          "resultado": resultado, "secreto": s, "error": e, "ms": ms})

    # ------------------------------------------------------------------ Ring-LWE: sistema lineal
    filas_tex.append("\\midrule")
    for t in todas["ringlwe"]:
        s = romper_clave_ring(t)
        e = resta_vectores(centrado_vector(t.b, t.q), producto_polinomios(t.a, s))
        if max(abs(x) for x in e) > 1:
            raise RuntimeError(f"Error inesperado en {t.nombre}: el secreto no es valido")
        bits = "".join(map(str, descifrar_ring(t, s)))
        ms = mediana_ms(lambda: descifrar_ring(t, romper_clave_ring(t)), args.repeticiones)
        etiqueta = "R" + t.nombre.replace("Tier3_T0", "3.0").replace("_LWE", "")
        resultado = f"palabra de {len(bits)} bits"
        filas_tex.append(f"{etiqueta} & {t.n} & {t.n} & {t.q} & 1 & -- & {resultado} & {ms_tex(ms)} \\\\")
        filas_csv.append({"tarea": t.nombre, "n": t.n, "m": t.n, "q": t.q, "cota_error": 1,
                          "resultado": bits, "secreto": s, "error": e, "ms": ms})
        puntos_ring.append((t.n, ms))

    carpeta = HERE / "datos"
    cabecera = ("\\begin{tabular}{@{}lrrrcclr@{}}\n\\toprule\n"
                "Tarea & $n$ & $m$ & $q$ & $c$ & Casos & Resultado & Tiempo (ms)\\\\\n\\midrule\n")
    (carpeta / "tabla_lwe.tex").write_text(cabecera + "\n".join(filas_tex) + "\n\\bottomrule\n\\end{tabular}\n",
                                           encoding="utf-8")
    # Curvas para la grafica de tiempos. Para que se lean sin interpretar el eje:
    #   - cada punto lleva escrito su tiempo ("7 ms", "1,4 s"),
    #   - entre dos puntos seguidos se escribe por cuanto se multiplica el tiempo ("x14").
    # LWE: solo las tareas con c = 4 (asi solo cambia n); si hay dos con el mismo n, su media geometrica.
    con_c4 = {}
    for n, ms, c in puntos_lwe:
        if c == 4:
            con_c4.setdefault(n, []).append(ms)
    curva_lwe = [(n, math.exp(statistics.mean(math.log(t) for t in ts))) for n, ts in sorted(con_c4.items())]
    curva_ring = sorted(puntos_ring)

    def factores_texto(puntos):
        """Los mismos factores que en la grafica, para citarlos en el texto: '12 y 15'."""
        k = [str(round(t2 / t1)) for (_, t1), (_, t2) in zip(puntos, puntos[1:])]
        if len(set(k)) == 1:
            return f"{k[0]} cada vez"               # '14 cada vez' en lugar de '14 y 14'
        return ", ".join(k[:-1]) + " y " + k[-1]

    (carpeta / "mediciones_lwe.tex").write_text(
        f"\\newcommand{{\\CurvaLWE}}{{{coordenadas_con_etiqueta(curva_lwe)}}}\n"
        f"\\newcommand{{\\FactoresLWE}}{{{factores(curva_lwe, lambda a, b: (a + b) / 2)}}}\n"
        f"\\newcommand{{\\TextoFactoresLWE}}{{{factores_texto(curva_lwe)}}}\n"
        f"\\newcommand{{\\CurvaRing}}{{{coordenadas_con_etiqueta(curva_ring)}}}\n"
        f"\\newcommand{{\\FactoresRing}}{{{factores(curva_ring, lambda a, b: (a + b) / 2)}}}\n"
        f"\\newcommand{{\\TextoFactoresRing}}{{{factores_texto(curva_ring)}}}\n"
        # L2.03 tambien como CVP, para compararla con la fuerza bruta en el texto
        f"\\newcommand{{\\TiempoCVPLdosTres}}{{{tiempo_legible(ms_l203_cvp)}}}\n",
        encoding="utf-8")
    with (carpeta / "resultados_lwe.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(filas_csv[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(filas_csv)
    print(f"LWE: {len(LWE)} tareas; Ring-LWE: {len(puntos_ring)} tareas. Medianas de {args.repeticiones}.")


if __name__ == "__main__":
    main()
