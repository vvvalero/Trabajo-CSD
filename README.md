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
python reportproposal/build.py      # memoria -> reportproposal/memoria.pdf (la que se entrega)
```

## Estructura

```
data/ggh, data/lwe         ficheros de tareas (45: 22 GGH + 20 LWE + 3 Ring-LWE)
run.py                     ejecutar las tareas desde la terminal
src/pqc/
  lector_tareas.py         lee los ficheros de tareas -> TareaGGH / TareaLWE / TareaRingLWE
  matrices.py              operaciones con vectores y matrices (exactas y modulo q)
  celosias/                algoritmos comunes a GGH y LWE
    gso.py  lll.py  babai.py
    enumeracion.py         SVP/CVP exactos, cotas racionales y orden Schnorr-Euchner
  ggh/
    resolver.py            LLL + enumeracion exacta (tareas sin modulo)
    reduccion_babai.py     LLL + Babai (aproximado, para comparar)
    celosia_modular.py     tareas con reduccion modulo n: sin resolver
    juguete.py             GGH de juguete (generar claves, cifrar, descifrar)
  lwe/
    resolver.py            fuerza bruta; si pasaria de 10^6 casos, ataque de celosia
    fuerza_bruta.py        probar los errores de n ecuaciones y comprobar el resto
    ataque_celosia.py      CVP en la celosia q-aria de A (LLL + enumeracion)
    descifrado.py          descifrado de un bit
    ring.py                Ring-LWE: sistema lineal sin reduccion mod q y descifrado
scripts/resultados_ggh.py  resultados y tiempos de los 19 GGH sin modulo -> results/
tests/                     tests (pytest)
reportproposal/            memoria que se entrega (ver su README): LaTeX, figuras y datos generados
report/                    esqueleto inicial de la memoria (no se entrega)
```

### Estado

- **GGH:** las 19 tareas sin módulo con LLL + enumeración exacta. En `Tier02T03_Latt` la enumeración
  mejora la distancia² de Babai de 186 a 155. Las tres con reducción módulo n quedan sin resolver
  (ver "Erratas y puntos abiertos").
- **LWE:** las 20 tareas. Fuerza bruta sobre el error hasta Tier2T03; el resto como CVP en la celosía
  q-aria (menos de 1 s cada una).
- **Ring-LWE:** las 3 tareas, como sistema lineal (los coeficientes de `a` son pequeños y el módulo
  q no llega a actuar).

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
