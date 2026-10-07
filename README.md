# Trabajo de criptografia post-cuantica

GGH (SVP/CVP en celosias) y LWE / Ring-LWE. Enunciado: `enunciado.pdf`.

## Lenguaje: Python 3.13 + numpy
- Aritmetica entera de precision arbitraria (modulos, determinantes, HNF) y numpy para el GSO.
- Implementar LLL, enumeracion y Babai uno mismo encaja con lo que se evalua (justificar el algoritmo, traza, soluciones propias).
- Plan B si algun tier grande es lento en Python: pasar el bucle caliente a C (hay `gcc`) o usar fpylll desde WSL (hay Ubuntu).

## Uso
```
pip install -r requirements.txt
python run.py list          # tareas y parametros
python run.py solve Tier0T01_Latt
python run.py all           # -> results/results.md
pytest
```

## Estructura
```
data/ggh, data/lwe   ficheros de tareas
src/pqc/tasks.py     parser (HECHO, tolerante a erratas)
src/pqc/lattice/     un fichero por algoritmo, compartido por GGH y LWE <- TODO
                     gso.py  lll.py  babai.py  enumeration.py  bkz.py
src/pqc/ggh.py       solver GGH + juguete cifrar/descifrar <- TODO
src/pqc/lwe.py       LWE / Ring-LWE                    <- TODO
scripts/bench.py     tiempo vs talla                   <- TODO
tests/               parser OK; tests de algoritmos    <- TODO
report/memoria.tex    memoria en LaTeX (5 pag., pesos 15/30/40/15); compilar: report/build.ps1 -> report/memoria.pdf
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
- Ring-LWE: el PDF no define el cifrado; el fichero habla de c1, c2. Hay que decidir/justificar el esquema.
- GGH con "reduccion modulo n" (Tier3T01/T02/T05): el PDF solo lo menciona. Si det(B) es invertible mod n, la
  celosia L + nZ^d es todo Z^d y el problema seria trivial: **comprobarlo** y preguntar al profesor cual es la
  interpretacion esperada.
- Formato de la solucion de SVP (signo del vector): no esta especificado.
