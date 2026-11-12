# Dificultades encontradas

Progreso y dificultades encontradas, en orden. Sirve para la memoria (conclusiones, decisiones
justificadas) y para preparar la defensa.

## 11/11/2026

### Hecho
- Análisis del enunciado, del temario (Tema 11) y de las 45 tareas. Plan de trabajo hasta la entrega (16/11).
- Convenios fijados: matrices como listas de filas con `Fraction` (exactas) y signo de LWE `b = A s + e`.
- `matrices.py`: operaciones con vectores y matrices, exactas y módulo q.
- `lector_tareas.py`: lectura de los ficheros por bloques, con validaciones.
- `celosias/gso.py`: Gram-Schmidt exacto.
- `celosias/lll.py`: LLL.
- `celosias/babai.py`: Babai por redondeo y por plano más cercano. Con LLL + Babai salen las 5 tareas Tier0 de GGH.
- `ggh/reduccion_babai.py` y `ggh/resolver.py`: ataque LLL + Babai (plano más cercano) conectado a `run.py`.
  Resuelve las 19 tareas GGH sin módulo (la más lenta, dimensión 15, en 0,44 s). Faltan las 3 modulares.

### Dificultades y decisiones

**LLL demasiado lento en su primera versión.** La primera versión llamaba a `gso` con la base entera antes de
cada resta, y tardaba 17,6 s solo con las 22 tareas GGH. Dos cambios, sin cambiar el algoritmo ni el
resultado:
- Calcular `gso(b[:k + 1])`: para decidir sobre b_k solo intervienen b_0, ..., b_k.
- Recalcular `gso` solo cuando b_k cambia (cuando r ≠ 0), no en cada vuelta del bucle.

Con eso, la tarea GGH más grande (dimensión 15) pasa a tardar 0,5 s, y los 26 tests de LLL ~1 s.

**LLL sigue siendo lento con las celosías del ataque a LWE.** Medido con la celosía del ataque primal
(dimensión = número de ecuaciones + 1). El resultado es correcto en todos los casos (encuentra el error),
pero el tiempo crece muy deprisa con la dimensión:

| Tarea | Dimensión | Tiempo | Error encontrado |
|---|---|---|---|
| Tier2T01_LWE | 13 | 1,1 s | ±4 |
| Tier1T05_LWE | 17 | 4,9 s | ±4 |
| Tier3T02_LWE | 17 | 8,4 s | ±15 |
| Tier3T01_LWE | 19 | 14,0 s | ±13 |
| Tier2T05_LWE | 31 | 329,7 s (5,5 min) | ±6 |

Causa: cada llamada a `gso` recalcula todo con fracciones de muchas cifras, y en dimensión 19 hay unas
4500 llamadas. Posible solución (pendiente de decidir antes de LWE): al hacer b_k ← b_k − r·b_j, actualizar
μ directamente (`mu[k][j] -= r` y `mu[k][i] -= r * mu[j][i]` para i < j) en vez de recalcular `gso`.

**Solución (12/11): `gso` una sola vez y luego actualizar μ y ||b*||².** Ver la entrada del 12/11.

**LLL + Babai no siempre da el punto más cercano.** Comprobado en las tareas GGH de dimensión ≤ 7
probando todas las combinaciones x·R con x en [-2, 2]^d (R la base reducida por LLL):
- SVP: en las 6 tareas ningún x·R ≠ 0 es más corto que el que da LLL.
- CVP: sumando x·R al punto de Babai, en 9 de 10 no sale ninguno más cercano. En **Tier02T03** Babai (plano más cercano) da
  distancia² 186 (el redondeo, 187) y existe un punto a distancia² **155**.

Es la razón para tener también la enumeración: LLL + Babai es rápido pero aproximado.

## 12/11/2026

### Hecho
- `celosias/lll.py` acelerado: se llama a `gso` una sola vez al principio y después solo se actualizan
  los valores de μ y ||b*||² que cambian. Mismo resultado: las 22 tareas GGH dan exactamente la misma base
  que con la versión anterior, y pasan los 158 tests.
- Memoria preparada (sin redactar), con estilo sobrio y las 4 secciones del enunciado: diseño en
  `report/estilo.tex`, una sección por fichero en `report/secciones/`, esquema del trabajo, figura de base
  mala/buena, un apartado por algoritmo (idea, por qué funciona, coste), tabla de estado de tareas con la
  puntuación calculada sola, trazas y gráfica de tiempos que se activa con los CSV de `report/datos/`.

### Dificultades y decisiones

**Cómo se evitó recalcular `gso`.** Hay dos momentos en los que la base cambia:
- Al restar r·b_j a b_k, los b* no cambian; solo la fila k de μ: `mu[k][j] -= r` y
  `mu[k][i] -= r * mu[j][i]` para i < j.
- Al intercambiar b_(k-1) y b_k solo cambian b*_(k-1) y b*_k. Con m = μ_(k,k-1): la nueva
  ||b*_(k-1)||² = ||b*_k||² + m²·||b*_(k-1)||², y el producto de las dos normas se conserva. Además se
  intercambian las filas k-1 y k de μ, y se corrigen las columnas k-1 y k de las filas posteriores.

Probamos primero solo el primer punto (`gso` una vez por vuelta): era solo el doble de rápido. Con los
dos puntos se ganan dos órdenes de magnitud:

| Celosía | Dimensión | Antes | Solo restas | Restas + intercambio |
|---|---|---|---|---|
| Tier2T01_LWE (primal) | 13 | 1,13 s | 0,55 s | 0,02 s |
| Tier1T05_LWE (primal) | 17 | 4,91 s | 2,30 s | 0,05 s |
| Tier3T01_LWE (primal) | 19 | 13,84 s | 5,90 s | 0,12 s |
| Tier2T05_LWE (primal) | 31 | 329,7 s | — | 0,69 s |
| 22 tareas GGH (total) | ≤ 15 | 0,95 s | — | 0,03 s |

Con esto, las 15 celosías primales de LWE Tier1 a Tier3 se reducen en menos de 1 s cada una (la mayor,
Tier3T05, de dimensión 31, en 0,83 s). En todas, LLL deja en la base una fila acabada en ±1 que
contiene el error (con valores hasta ±15 en Tier3).
