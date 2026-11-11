# Algoritmos del trabajo: qué son, por qué funcionan y por qué los usamos

## 1. Idea de fondo

El Tema 11 lo dice explícitamente: *si la base es ortogonal o casi ortogonal, SVP y CVP son fáciles; si la
base está sesgada, son difíciles*. Toda la estrategia sale de ahí:

1. **Mejorar la base:** reducirla con **LLL**. En tiempo polinómico hace lo que el atacante de GGH necesita:
   convertir la base pública (mala) en una buena.
2. **Resolver de forma barata pero aproximada:** **Babai**, o **embedding + LLL**.
3. **Certificar el óptimo exacto:** las tareas piden *el* vector más corto o *el* más cercano, no uno
   aproximado. Para eso, **enumeración**: búsqueda exhaustiva pero acotada, rápida precisamente porque la
   base ya está reducida.

La **fuerza bruta** y **Lagrange-Gauss** cubren los casos pequeños y sirven de contraste para la gráfica de
tiempo frente a talla que pide el enunciado.

Origen de cada pieza:

- **Redondeo de Babai:** aparece en el propio enunciado (Ejemplo 3, "el llamado Babai round").
- **Ataque a Ring-LWE:** es una **observación propia sobre los datos** (sección 4.3), no un algoritmo
  publicado. Es nuestra "aportación original".
- **El resto:** el conjunto de herramientas clásico de cualquier libro de criptografía con celosías.

## 2. Algoritmos sobre celosías (GGH y base de los ataques a LWE)

### 2.1 LLL (Lenstra, Lenstra y Lovász, 1982)

- **Qué hace:** transforma una base en otra de la misma celosía, casi ortogonal y con vectores cortos, en
  tiempo polinómico.
- **Por qué funciona:** alterna dos operaciones:
  - *Reducción de tamaño:* restar a b_i múltiplos enteros redondeados de b_j (j < i) para que los
    coeficientes de Gram-Schmidt cumplan |μ_ij| ≤ ½.
  - *Intercambio:* intercambiar b_i y b_{i-1} cuando no se cumple la condición de Lovász,
    ‖b*_i‖² ≥ (δ − μ²_{i,i-1}) ‖b*_{i-1}‖², con ¼ < δ < 1 (habitualmente 0,75 o 0,99).
  - Garantía: ‖b_1‖ ≤ 2^((n−1)/2) · λ_1 (con δ = 3/4), es decir, el primer vector está a un factor
    acotado del más corto.
- **Por qué en nuestro caso:** es "la forma de transformar la base pública" que el enunciado deja como
  ejercicio. En dimensiones pequeñas LLL prácticamente **recupera la base privada**: los vectores cortos
  encontrados, como (0, 1, 15, 2) o (−15, 1), son filas de la base privada casi diagonal.

### 2.2 Babai: redondeo (Babai, 1986)

- **Qué hace:** escribe el objetivo en coordenadas de la base (t·B⁻¹), redondea cada coordenada y vuelve a
  multiplicar por B.
- **Por qué funciona:** si t = x·B + e, entonces t·B⁻¹ = x + e·B⁻¹. El redondeo devuelve x **si y solo si
  todas las componentes de e·B⁻¹ están en (−½, ½)**. Es exactamente el argumento del Ejemplo 3 del
  enunciado.
- **Cuándo falla:** con una base mala, B⁻¹ amplifica el error y el redondeo cae en otro punto. Es el caso
  e = (−2, 2) del enunciado.
- **Por qué en nuestro caso:** es el descifrado legítimo de GGH. Aplicado tras LLL a la base pública es
  literalmente el ataque a GGH.

### 2.3 Babai: plano más cercano (Babai, 1986)

- **Qué hace:** lo mismo, pero coordenada a coordenada usando la ortogonalización de Gram-Schmidt. Del
  último vector al primero, en cada nivel elige el hiperplano de la celosía más cercano y resta.
- **Por qué funciona:** con una base reducida con LLL garantiza un punto a distancia como mucho 2^(n/2)
  veces la óptima. Es más robusto que el redondeo.
- **Por qué en nuestro caso:** comparar redondeo y plano más cercano ilustra por qué importa la calidad
  de la base. Además es la pieza sobre la que se construye la enumeración.

### 2.4 Embedding de Kannan (Kannan, 1987)

- **Qué hace:** convierte un CVP en un SVP. Se añade el objetivo t como una fila más, con una constante M:

  ```
  B' = | B  0 |
       | t  M |
  ```

  Si t está cerca de un punto v de la celosía, el vector (t − v, M) es muy corto en la nueva celosía y LLL
  lo encuentra.
- **Por qué en nuestro caso:** **la misma idea resuelve el CVP de GGH y el ataque primal a LWE**, porque en
  LWE b − A·s = e es un vector corto. Un solo concepto sirve para los dos criptosistemas.
- **Limitación observada:** en Tier0T05_Latt, con M = 1, el vector reducido no tenía la última coordenada
  igual a ±M. Hay que elegir bien M o recurrir a Babai o a la enumeración.

### 2.5 Enumeración Fincke–Pohst / Schnorr–Euchner (Fincke y Pohst, 1985; Schnorr y Euchner, 1994)

- **Qué hace:** recorre como un árbol todos los vectores de coeficientes cuyo punto cae dentro de una bola
  de radio R (alrededor del origen para SVP y del objetivo para CVP). Gram-Schmidt da en cada nivel i un
  intervalo finito de valores posibles para el coeficiente x_i, según el radio que queda por gastar:

  |x_i + Σ_{j>i} μ_ji x_j| ≤ sqrt(R² − parcial) / ‖b*_i‖

  Schnorr–Euchner añade dos mejoras: probar los valores en zigzag desde el centro y **reducir R** cada vez
  que encuentra un vector mejor.
- **Por qué funciona:** es exhaustiva dentro de la bola, así que **demuestra** que el resultado es el
  óptimo. Su coste es exponencial en el peor caso, pero con una base reducida con LLL y dimensión ≤ 15
  tarda milisegundos.
- **Por qué la necesitamos:**
  - LLL y Babai son aproximados.
  - En Tier02T03_Latt el embedding dio distancia² = 187, un resultado sospechoso.
  - En Tier03T04_Latt (SVP de dimensión 15), probar todas las combinaciones con coeficientes en
    {−1, 0, 1} tardó 166 s y aun así no prueba que sea el más corto.

### 2.6 Fuerza bruta

- **Por qué:** el enunciado la permite *si se defienden las razones*, y pide mostrar cómo crece el tiempo
  con la talla. La fuerza bruta da la curva exponencial que contrasta con LLL, que es polinómico.
- **Justificación de la cota en GGH:** los coeficientes de la solución x = v·B⁻¹ están acotados por la
  norma de v y la de B⁻¹, así que el espacio de búsqueda [−k, k]ⁿ es finito. Coste: (2k+1)ⁿ.
- **Justificación en LWE:** conviene probar todos los **errores** posibles y no todos los secretos, porque
  (2E+1)ⁿ es mucho menor que qⁿ (por ejemplo, 9³ = 729 frente a 379³ ≈ 5,4·10⁷). Fijados n errores, el
  secreto sale resolviendo un sistema lineal módulo q, y se comprueba que el resto de ecuaciones quedan
  con error |e| ≤ E.

### 2.7 Lagrange-Gauss en 2D (Lagrange, 1773; Gauss, 1801)

- **Qué hace:** resuelve el SVP **de forma exacta** en dimensión 2. Es como el algoritmo de Euclides
  aplicado a vectores: mientras el vector largo se pueda acortar, se le resta el múltiplo redondeado del
  corto y se intercambian.
- **Por qué en nuestro caso:** LLL es su generalización a n dimensiones, así que explicarlo primero hace
  que LLL se entienda. Además resuelve directamente Tier01T05_Latt y Tier01T06_Latt, que son de
  dimensión 2.

### 2.8 Caso modular (Tier03T01, T02 y T05 de GGH)

- **No es un algoritmo, sino una comprobación.** La forma estándar de añadir "reducción módulo q" a una
  celosía es la celosía q-aria Λ_q(B) = {v ∈ Zᵈ : v ≡ x·B (mod q)} = L(B) + qZᵈ (capítulo de Micciancio y
  Regev en Bernstein et al.).
- **Argumento:** si det(B) es invertible módulo q, B es invertible módulo q y cualquier vector módulo q se
  alcanza con la base B. Entonces Λ_q(B) = Zᵈ: el CVP devuelve el propio objetivo y el SVP un vector
  unitario. Con la celosía dual módulo q pasa lo mismo: Λ⊥_q = qZᵈ, también trivial.
- **Por qué el gcd:** comprobar mcd(det B, n) = 1 decide si estamos en ese caso trivial. **En las tres
  tareas modulares lo estamos.** Pendiente de confirmar con el profesor la interpretación esperada.

## 3. Algoritmos específicos de LWE

### 3.1 Eliminación gaussiana módulo q

- Sin error, el sistema A·s ≡ b (mod q) se resuelve directamente: es el "aprendizaje sin errores" del
  Tema 11. Con q primo, Z_q es un cuerpo y existe el inverso de cada pivote.
- Tier0T01_LWE y Tier0T02_LWE tienen error 0. También es la pieza interna de la fuerza bruta sobre los
  errores.

### 3.2 Descifrado de un bit (Regev)

- R = C·s (mod q). Si R está cerca de B (distancia centrada < q/4) el bit es 0; si está cerca de B + q/2
  el bit es 1.
- Comprobar siempre el margen: cuánto se aleja el valor de su polo, frente a q/4.

### 3.3 Ataque primal (Albrecht, Player y Scott, 2015)

- Es el **embedding de Kannan aplicado a LWE**. Se construye una base de la celosía q-aria
  {A·s mod q} ⊂ Zᵐ, se añade la fila (b, 1), y LLL encuentra el vector corto (±e, ±1). A partir de e se
  despeja s resolviendo un sistema módulo q.
- **Convenio de signos:** b = A·s + e, así que el error es e = b − A·s. Equivocarse de signo da
  secretos falsos que parecen plausibles, porque el residuo sale pequeño solo en las ecuaciones usadas
  para despejar.
  - **Fuente del convenio:**
    - Tema 11: "b = A·sᵀ + e mod m"; en Ring-LWE, "b = a·s + e (mod q, xⁿ + 1)".
    - Enunciado, Ejemplo 4, comprobado numéricamente: con S = (4, 70, 0, 3) y q = 71 se obtiene
      A·S mod 71 = (35, 50, 33, 59, 9), y b − A·S = (−3, 3, −2, 0, 2), que es exactamente su E.
- **Verificación:** con el secreto encontrado, *todos* los residuos centrados deben ser pequeños (±15 en
  Tier 3). Que haya una única solución así entre q^n candidatos es una prueba muy sólida.

## 4. Ring-LWE

### 4.1 Producto en el anillo

En Z_q[x]/(xⁿ + 1), multiplicar por a(x) equivale a multiplicar por la matriz **negacíclica** Rot(a)
(Tema 11): cada columna es a·x^j, y los coeficientes que "dan la vuelta" cambian de signo porque
xⁿ ≡ −1.

### 4.2 Esquema (Tema 11)

- Clave: b = a·s + e.
  - Comprobación del ejemplo del Tema 11 (q = 463, n = 8): b − a·s sale (−1, 0, 0, −1, 1, 0, 0, 0), un
    error pequeño. Esto confirma la estructura b = a·s + e en x⁸ + 1, pero no coincide con el e que
    escribe la diapositiva (probable errata del temario). En el mismo ejemplo, el coeficiente "3065x³"
    de c2 es mayor que q, otra errata.
- Cifrado: c1 = a·r + e1, c2 = b·r + e2 + m, donde m codifica cada bit como 0 o ⌊q/2⌉.
- Descifrado: d = c2 − s·c1. Cada coeficiente se asigna al polo más cercano (0 → bit 0, ⌊q/2⌉ → bit 1).

### 4.3 Nuestro ataque (aportación original)

- **Observación:** en las tres tareas, a tiene coeficientes entre 0 y 15, y s y e son pequeños.
- **Hipótesis:** si n · máx|a| · máx|s| < q/2, el producto a·s **no se reduce módulo q**. Entonces
  Rot(a)·s + e = b se cumple también **sobre los enteros**, tomando b con representantes centrados.
- **Ataque:** s = round(Rot(a)⁻¹ · b). Es **un redondeo de Babai** con la base Rot(a) sobre Zⁿ, y acierta
  si ‖Rot(a)⁻¹ · e‖∞ < ½.
- **Validación:** las dos condiciones se comprueban con los datos de cada tarea. Además:
  - el error resultante es como mucho ±1;
  - al descifrar, cada coeficiente queda a 8, 18 y 33 unidades de su polo, frente a márgenes q/4 de 349,
    779 y 1475.
- **Lección para las conclusiones:** Ring-LWE no es inseguro en sí; lo que lo rompe son **parámetros
  mal elegidos**, como coeficientes de a pequeños en vez de uniformes en Z_q.

## 5. Si preguntan "¿y por qué no X?"

- **BKZ:** es LLL combinado con enumeración por bloques de tamaño β. Con estas dimensiones (≤ 31) basta
  LLL. Sería la herramienta para parámetros reales, como n = 256 en ML-KEM (FIPS 203). Buen tema para las
  conclusiones.
- **Ataque dual, BKW, Arora–Ge, cribas (sieving):** existen, pero son más complejos y aquí no hacen falta.
  Nombrarlos demuestra que conocemos la literatura.
- **Ataque de Nguyen a GGH (1999):** aparece en el Tema 11. Aprovecha que en el GGH original el error vale
  exactamente ±σ en cada componente: c + (σ, …, σ) ≡ x·B (mod 2σ), lo que permite despejar x módulo 2σ y
  simplificar el CVP. Mencionarlo como alternativa conocida.

## 6. Referencias (comprobar antes de citar)

- A. K. Lenstra, H. W. Lenstra, L. Lovász. *Factoring polynomials with rational coefficients*.
  Mathematische Annalen 261, 1982.
- L. Babai. *On Lovász' lattice reduction and the nearest lattice point problem*. Combinatorica 6(1), 1986.
- R. Kannan. *Minkowski's convex body theorem and integer programming*. Mathematics of Operations
  Research 12(3), 1987.
- U. Fincke, M. Pohst. *Improved methods for calculating vectors of short length in a lattice, including a
  complexity analysis*. Mathematics of Computation 44(170), 1985.
- C. P. Schnorr, M. Euchner. *Lattice basis reduction: improved practical algorithms and solving subset
  sum problems*. Mathematical Programming 66, 1994.
- O. Goldreich, S. Goldwasser, S. Halevi. *Public-key cryptosystems from lattice reduction problems*.
  CRYPTO '97.
- P. Q. Nguyen. *Cryptanalysis of the Goldreich–Goldwasser–Halevi cryptosystem from Crypto '97*.
  CRYPTO '99, LNCS 1666.
- O. Regev. *On lattices, learning with errors, random linear codes, and cryptography*. Journal of the ACM
  56(6), 2009.
- V. Lyubashevsky, C. Peikert, O. Regev. *On ideal lattices and learning with errors over rings*.
  EUROCRYPT 2010.
- M. R. Albrecht, R. Player, S. Scott. *On the concrete hardness of Learning with Errors*. Journal of
  Mathematical Cryptology 9(3), 2015.
- D. Micciancio, O. Regev. *Lattice-based cryptography*. En D. J. Bernstein, J. Buchmann, E. Dahmen (eds.),
  *Post-Quantum Cryptography*, Springer, 2009. **Está en la bibliografía del Tema 11**: el puente natural
  con la asignatura.
- NIST. *FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard*, 2024.

Para estudiar:

- J. Hoffstein, J. Pipher, J. H. Silverman. *An Introduction to Mathematical Cryptography*. Springer.
  Capítulo de celosías: Gauss, LLL, Babai, GGH y embedding, con ejemplos.
- S. Galbraith. *Mathematics of Public Key Cryptography*. Cambridge University Press, 2012. Capítulos sobre
  reducción de bases y SVP/CVP (disponible gratis en la web del autor).
