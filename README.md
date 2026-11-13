# Trabajo de criptografía post-cuántica

Criptoanálisis de GGH (SVP/CVP en celosías), LWE y Ring-LWE.
Asignatura: Criptología y Seguridad de los Datos (MUCC, ETSInf-UPV).
Grupo: Óscar García García y Valentín Valero Jiménez. Entrega: 16/11/2026.

## Documentación

| Fichero | Contenido |
|---|---|
| `docs/enunciado.pdf` | Enunciado del trabajo y criterios de evaluación |
| `docs/MUCC - Criptologia MUCC Tema-11-1.pdf` | Temario (Tema 11): GGH, LWE y Ring-LWE con ejemplos |
| `docs/algoritmos.md` | Qué hace cada algoritmo, por qué funciona y por qué lo usamos (para la memoria y la defensa) |
| `docs/defensa_ggh.md` | Justificación de la estrategia GGH, alternativas, garantías y comparaciones pendientes |
| `docs/dificultades_encontradas.md` | Progreso del trabajo, dificultades encontradas y decisiones tomadas |

## Uso (Windows y macOS)

Requisitos: Python 3.9 o superior (desarrollado con 3.13) y, para la memoria, LaTeX con `latexmk`
(MiKTeX en Windows; MacTeX o BasicTeX en macOS). En macOS usar `python3` / `pip3`.

```
pip install -r requirements.txt
python run.py list                  # lista las tareas y sus parámetros
python run.py solve Tier0T01_Latt   # resuelve una tarea
python run.py all                   # resuelve todas -> results/results.md
python -m pytest                    # tests
python report/build.py              # memoria -> report/memoria.pdf
```

## Estructura

```
data/ggh, data/lwe         ficheros de tareas (45: 22 GGH + 20 LWE + 3 Ring-LWE)
run.py                     ejecutar las tareas desde la terminal
src/pqc/
  lector_tareas.py         lee los ficheros de tareas -> TareaGGH / TareaLWE / TareaRingLWE   HECHO
  matrices.py              operaciones con vectores y matrices (exactas y modulo q)            HECHO
  celosias/                algoritmos comunes a GGH y LWE
    gso.py  lll.py  babai.py                                                                   HECHO
    enumeracion.py          SVP/CVP exactos, cotas racionales y orden Schnorr-Euchner          HECHO
  ggh/                     GGH
    resolver.py  reduccion_babai.py                                                            HECHO
    fuerza_bruta.py  celosia_modular.py                                                        TODO
    juguete.py             GGH de juguete (generar claves, cifrar, descifrar)                  HECHO
  lwe/                     LWE y Ring-LWE                                                       TODO
    resolver.py  fuerza_bruta.py  ataque_celosia.py  descifrado.py  ring.py
scripts/resultados_ggh.py  regenerar resultados y tiempos de los 19 GGH sin módulo               HECHO
scripts/bench.py           tiempo frente a talla                                                TODO
tests/                     tests (pytest)
report/memoria.tex         memoria en LaTeX (máx. 5 páginas; pesos 15/30/40/15)
  estilo.tex               diseño (sobrio, sin color): algoritmos, trazas, tabla de tareas
  secciones/               una sección por fichero (contenido)
  figuras/                 diagramas TikZ y gráfica de tiempos
  datos/                   CSV de tiempos para la gráfica (los genera scripts/bench.py)
```

### Estado de GGH

`run.py solve` usa **LLL + enumeración exacta** para las tareas sin módulo. Babai da
el candidato inicial de CVP y un vector corto de la base reducida da el de SVP.
La búsqueda usa fracciones exactas y solo descarta ramas que no pueden mejorar ese
candidato. En SVP se excluye el cero; en empates se devuelve cualquier óptimo.

Se han ejecutado las **19 tareas sin módulo**, incluidas las dos de dimensión 15.
En `Tier02T03_Latt`, la enumeración mejora la distancia² de Babai de 186 a **155**.
Los resultados se regeneran con `python3 scripts/resultados_ggh.py` y se guardan en
`results/ggh_exactos.csv` (ignorado por Git). Separan el coste de LLL del de la
enumeración e incluyen el número de nodos visitados.
Esta medición puntual no sustituye el estudio comparativo de `scripts/bench.py`.
El ataque aproximado sigue disponible en `ggh/reduccion_babai.py` para contrastarlo.
Las tres tareas modulares siguen pendientes de aclaración e implementación.

## Convenios

- **Matrices:** listas de filas de `int` o `Fraction` (aritmética exacta, sin decimales). En una base de
  celosía cada fila es un vector, y los vectores se multiplican como filas (`x B`).
- **LWE:** `b = A s + e (mod q)`, así que el error es `e = b - A s`. **Ring-LWE:** `b = a s + e (mod q, x^n + 1)`.
  Fuente: Tema 11 y Ejemplo 4 del enunciado (ver `tests/test_convenios.py`). La ecuación (1) del enunciado
  escribe "A x = b + e", pero su propio Ejemplo 4 sigue `b = A s + e` (ver `docs/algoritmos.md`, 3.3).
- **Ring-LWE (Tema 11):** cifrado `c1 = a r + e1`, `c2 = b r + e2 + m`; descifrado `d = c2 - s c1`, y cada
  coeficiente se asigna al polo más cercano (0 → bit 0, q/2 → bit 1).
- **Redondeo:** `redondeo()` de `matrices.py` (los empates x,5 hacia arriba), nunca `round()` de Python.
- Los algoritmos (LLL, Babai, enumeración...) se implementan nosotros: el enunciado valora las soluciones
  propias y pide justificar cada algoritmo con una traza.

## Las tareas (ver `python run.py list`)

| Tier | GGH | LWE | Valor |
|---|---|---|---|
| 0 | bases ortogonales, 2D (traen solución) | n=3-5, ruido bajo (traen solución) | 0 |
| 1 | dim 2-6; SVP y CVP | n=3-4; rotura y criptoanálisis | 0,3 (máx 1,4) |
| 2 | dim 4-7 | n=4-10 | 0,5 (máx 1,8) |
| 3 | dim 15 y celosías **modulares** | n=7-10, q=1223; **Ring-LWE** n=16/32/64 | 1 (sin tope) |

La nota de tareas tiene un tope de 4 puntos.

## Erratas y puntos abiertos

- `Tier3T01_LWE` y `Tier3T03_LWE`: faltan llaves `{`/`}` (no importa: de cada bloque solo se leen los números).
- `Tier0T04_LWE` y `Tier0T05_LWE`: dicen `criptograma` en vez de `criptoanalisis` (se leen como criptoanálisis).
- `Tier1T05`, `Tier2T02`, `Tier2T04` y `Tier2T05` (LWE): algún coeficiente vale exactamente `q` (equivale a 0):
  reducir mod q antes de operar (`mod_matriz`).
- Tema 11, ejemplo de Ring-LWE con q = 463: el error de la diapositiva no coincide con `b - a s`, y en c2 aparece
  un coeficiente mayor que q (erratas del temario).
- **Pendiente de confirmar con el profesor:** GGH con "reducción módulo n" (Tier03T01/T02/T05). En las tres,
  det(B) es invertible mod n, así que la celosía L + nZ^d es todo Z^d y el problema sería trivial.
- **Sin especificar:** el signo del vector solución del SVP (v y -v son igual de cortos).
