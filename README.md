# Trabajo de criptografia post-cuantica

GGH (SVP/CVP en celosias) y LWE / Ring-LWE. Enunciado: `docs/enunciado.pdf`.

## Lenguaje: Python 3.13
- Convenio: matrices como **listas de filas de `int` / `Fraction`** (aritmetica exacta, ver `src/pqc/matrices.py`);
  una base de celosia tiene un vector por fila. GSO y LLL exactos, sin errores de redondeo en la condicion de Lovasz.
- numpy solo donde no hace falta exactitud (vectorizar la fuerza bruta, bench) y matplotlib para las graficas.
- Convenio LWE: b = A s + e (mod q), luego el error es e = b - A s; Ring-LWE: b = a s + e (mod q, x^n + 1).
  Fuente: Tema 11 y Ejemplo 4 del enunciado (verificado en `tests/test_convenios.py`). La ec. (1) del
  enunciado escribe "A x = b + e", pero su propio Ejemplo 4 sigue b = A s + e (ver `docs/algoritmos.md`, 3.3).
- Implementar LLL, enumeracion y Babai uno mismo encaja con lo que se evalua (justificar el algoritmo, traza, soluciones propias).
- Plan B si algun tier grande es lento en Python: pasar el bucle caliente a C (hay `gcc`) o usar fpylll desde WSL (hay Ubuntu).

## Uso (Windows y macOS)
Requisitos: Python 3.9 o superior (desarrollado con 3.13) y, para la memoria, LaTeX con `latexmk`
(MiKTeX en Windows; MacTeX o BasicTeX en macOS).

En macOS usar `python3` / `pip3` donde abajo pone `python` / `pip`.
```
python -m venv .venv                     # opcional
.venv\Scripts\activate                   # Windows   (macOS: source .venv/bin/activate)
pip install -r requirements.txt
python run.py list                       # tareas y parametros
python run.py solve Tier0T01_Latt
python run.py all                        # -> results/results.md
python -m pytest
python report/build.py                   # memoria -> report/memoria.pdf
```

## Estructura
```
data/ggh, data/lwe   ficheros de tareas
src/pqc/tareas.py     parser (HECHO, tolerante a erratas)
src/pqc/celosias/    un fichero por algoritmo, compartido por GGH y LWE <- TODO
                     gso.py  lll.py  babai.py  enumeracion.py  bkz.py
src/pqc/ggh/         GGH, un fichero por metodo            <- TODO
                     resolver.py  reduccion_babai.py  fuerza_bruta.py  celosia_modular.py  juguete.py
src/pqc/lwe/         LWE / Ring-LWE, un fichero por metodo <- TODO
                     resolver.py  gauss.py  fuerza_bruta.py  ataque_celosia.py  descifrado.py  ring.py
scripts/bench.py     tiempo vs talla                   <- TODO
tests/               parser OK; tests de algoritmos    <- TODO
report/memoria.tex    memoria en LaTeX (5 pag., pesos 15/30/40/15); compilar: python report/build.py -> report/memoria.pdf
```

## Las tareas (45 ficheros: 22 GGH + 23 LWE; ver `run.py list`)
| Tier | GGH | LWE | Valor |
|---|---|---|---|
| 0 | bases ortogonales, 2D (traen solucion) | n=3-5, ruido bajo (traen solucion) | 0 |
| 1 | dim 2-6; SVP y CVP | n=3-4; rotura y criptoanalisis | 0,3 (max 1,4) |
| 2 | dim 4-7 | n=4-10 | 0,5 (max 1,8) |
| 3 | dim 15 y celosias **modulares** | n=7-10, q=1223; **Ring-LWE** n=16/32/64 | 1 (sin tope) |

## Erratas / puntos abiertos en los datos
- `Tier3T01_LWE` y `Tier3T03_LWE`: faltan llaves `{`/`}` (el parser las ignora).
- `Tier0T04_LWE`: dice `criptograma` en vez de `criptoanalisis`.
- `Tier1T05`, `Tier2T02`, `Tier2T04` y `Tier2T05` (LWE): algun coeficiente vale exactamente `q` (equivale a 0 mod q).
  Es valido, pero hay que reducir mod q antes de operar.
- Ring-LWE: el PDF no define el cifrado; el fichero habla de c1, c2. Hay que decidir/justificar el esquema.
- GGH con "reduccion modulo n" (Tier3T01/T02/T05): el PDF solo lo menciona. Si det(B) es invertible mod n, la
  celosia L + nZ^d es todo Z^d y el problema seria trivial: **comprobarlo** y preguntar al profesor cual es la
  interpretacion esperada.
- Formato de la solucion de SVP (signo del vector): no esta especificado.
