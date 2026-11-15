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

## 13/11/2026

### Hecho
- `lwe/fuerza_bruta.py`: se prueban todos los errores posibles de las n primeras ecuaciones, se despeja s
  con la inversa módulo q y se comprueba que el error de **todas** las ecuaciones es pequeño.
- `lwe/descifrado.py`: R = C·s mod q y d = B − R centrado; bit 0 si |d| < q/4, bit 1 si no.
- `lwe/resolver.py`: fuerza bruta con error_max = 0, 1, 2… hasta 10⁵ intentos. Con error_max = 0 es
  simplemente resolver el sistema (Tier0T01/T02 no tienen error).
- Resultado: las 5 Tier0 coinciden con la solución del fichero; salen las 5 Tier1 y Tier2T01/T02.
  Quedan para el ataque de celosía Tier2T03–T05 y las 5 Tier3 (n grande o error grande).

| Tarea | n | Error máximo | Tiempo |
|---|---|---|---|
| Tier0T01/T02 | 3–4 | 0 | 0,00 s |
| Tier0T03–T05 | 4–5 | ±1 | 0,00 s |
| Tier1T01/T03 | 3 | ±1 | 0,00 s |
| Tier1T02/T04 | 3 | ±4 | 0,01 s |
| Tier1T05 | 4 | ±4 | 0,09 s |
| Tier2T01 | 4 | ±4 | 0,10 s |
| Tier2T02 | 5 | ±4 | 1,4 s |

### Dificultades y decisiones

**Con pocas ecuaciones de sobra la fuerza bruta da un secreto falso.** En el Ejemplo 4 del enunciado
(4 incógnitas, 5 ecuaciones, errores hasta ±3) solo sobra una ecuación para comprobar, y el primer
candidato que pasa el filtro es (11, 25, 5, 51), no el secreto (4, 70, 0, 3). En las tareas no pasa:
traen unas 3 veces más ecuaciones que incógnitas, y la probabilidad de que un s falso deje todas las
ecuaciones sobrantes con error pequeño es despreciable (Tier1T02: 9³ candidatos, 9 ecuaciones de sobra,
cada una pasa con probabilidad 9/379 → 729·(9/379)⁹ ≈ 10⁻¹²).
Comprobado además recorriendo **todos** los s posibles (q³, unos 54 millones con q = 379) en las 5 tareas
con n = 3: en cada una solo hay un s con los errores tan pequeños, y es el que da la fuerza bruta.

**El descifrado no queda en duda.** En las 6 tareas de criptoanálisis Tier0/Tier1, d = B − R está muy
lejos del umbral q/4:
- bit 0: d = 0, −1 o −3 (cerca de 0);
- bit 1: d = 114 con q = 229 y d = −183 con q = 379 (cerca de ±q/2).

**Ring-LWE se rompe sin celosías (observación propia sobre los datos).** El ataque de resolver un sistema
real y redondear no está en ningún libro: funciona por cómo están generadas estas tareas. En un Ring-LWE
de verdad, `a` tiene coeficientes aleatorios entre 0 y q − 1, y a·s "da la vuelta" módulo q muchas veces.
Aquí `a` va de 0 a 15 y `s` y `e` son pequeños, así que a·s nunca llega a q/2: `b` centrado es
**exactamente** a·s + e con enteros normales, y b = a·s + e es un sistema lineal normal (la matriz es la de
"multiplicar por `a`"). Se resuelve con fracciones exactas como si no hubiera error y se redondea.
Comprobado en las 3 tareas:

| Tarea | n | q | max \|a·s\| | q/2 | `s` | `e = b − a·s` | Desvío máximo antes de redondear | Tiempo |
|---|---|---|---|---|---|---|---|---|
| Tier3_T01 | 16 | 1399 | 97 | 699 | 0 … 2 | −1 … 1 | 0,07 | 0,01 s |
| Tier3_T02 | 32 | 3119 | 293 | 1559 | 0 … 2 | −1 … 1 | 0,12 | 0,09 s |
| Tier3_T03 | 64 | 5903 | 271 | 2951 | −2 … 2 | −1 … 1 | 0,20 | 0,8 s |

El redondeo solo fallaría con un desvío de 0,5 o más; el peor es 0,20. Con el ejemplo del Tema 11
(q = 463, n = 8) el mismo método recupera el secreto conocido (2, 2, 1, 2, 1, 2, 1, 2).

**Ring-LWE: el descifrado no queda en duda.** Con el `s` recuperado, d = c₂ − s·c₁ = e·r + e₂ − s·e₁ + m·q/2.
Los coeficientes de d (centrados) quedan muy cerca de su polo, lejísimos del umbral q/4:

| Tarea | q/4 | Bit 0: \|d\| máximo | Bit 1: distancia máxima a q/2 | Palabra |
|---|---|---|---|---|
| Tier3_T01 | 349,75 | 8 | 7 | 0100111001010000 |
| Tier3_T02 | 779,75 | 18 | 16 | 10100011110000010010000000101100 |
| Tier3_T03 | 1475,75 | 33 | 26 | 0011111100001011111011010001010000010001001001100101000100100111 |

El ejemplo del Tema 11 no trae un criptograma válido (errata), así que para probar el descifrado ciframos
nosotros un mensaje con su clave pública y comprobamos que se recupera.

### Enumeración exacta de GGH

- Implementada la enumeración SVP/CVP por distancias con orden Schnorr-Euchner en
  `celosias/enumeracion.py`. Gram-Schmidt descompone la distancia en sumandos no negativos:
  se descarta una rama cuando no puede mejorar el candidato actual. El cero se excluye en SVP.
- Las cotas se calculan sin decimales ni raíces aproximadas: si el centro es p/q, se
  acota el entero `q*x-p` mediante `isqrt`. Así no se pierde una solución por redondeos
  de coma flotante, incluso con multiplicadores grandes.
- `ggh/resolver.py` conecta LLL con la enumeración. El método aproximado LLL + Babai
  permanece separado en `reduccion_babai.py` para compararlo.
- Las 19 tareas sin módulo terminan, incluidas las dos de dimensión 15. En Tier02T03
  la distancia² baja de 186 (Babai) al óptimo 155. Las 5 Tier0 siguen coincidiendo con
  la referencia. La mención anterior a «resolver 19 tareas» describía candidatos;
  ahora la ruta por defecto completa la búsqueda exacta.
- 63 pruebas nuevas: contraste con fuerza bruta sobre puntos del espacio en casos
  pequeños, ceros y empates, racionales, coordenadas grandes, regresión de Tier02T03
  e integración de las 19 tareas. Total: **221 tests pasan**.
- `results/ggh_exactos.csv` guarda resultados, nodos y tiempos de una ejecución local.
  Sigue pendiente el estudio comparativo de tiempos. Las 3 tareas modulares y LWE
  no se han implementado en este paso.

### Revisión de la enumeración

- Revisión de las cotas exactas, el orden que justifica detener una rama y los
  cambios de radio: 1500 contrastes directos de cotas y orden y 510 casos aleatorios
  SVP/CVP en dimensiones 2 a 4, comparados con un oráculo independiente sobre puntos
  enteros. No se encontraron discrepancias.
- Añadida una regresión con objetivo racional y varias mejoras sucesivas del radio.
  Total de la batería permanente: **222 tests pasan**.
- El CSV estaba ignorado por Git y faltaba un comando para reproducirlo. Se añade
  `scripts/resultados_ggh.py`, que regenera los 19 resultados y sus estadísticas,
  comprueba pertenencia y referencias y separa los tiempos de LLL y enumeración.
