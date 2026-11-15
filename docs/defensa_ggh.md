# Defensa de la estrategia GGH

## Alcance y estado real

El objetivo es resolver SVP y CVP euclideos en las instancias GGH sin modulo elegidas.
En SVP se excluye el vector cero. Cada fila de la base es un vector y los multiplicadores
deben ser enteros. No es necesario recuperar la clave privada original: basta resolver
el problema geometrico sobre la misma celosia.

Actualmente estan implementados Gram-Schmidt, LLL, las dos variantes de Babai y la
enumeracion exacta. El resolutor usa **LLL + candidato inicial + enumeracion exacta**.
Para CVP el candidato viene de Babai del plano mas cercano; para SVP es el vector mas
corto de la base reducida. La enumeracion se encarga de comprobar las mejoras posibles.
Se han ejecutado las 19 instancias sin modulo, incluidas las dos de dimension 15.
La bateria completa tiene 222 tests, incluidos contrastes con fuerza bruta independiente
en casos pequenos, objetivos racionales y coordenadas grandes.
Las tres instancias modulares se tratan aparte: su interpretacion sigue pendiente
de confirmar con el profesor.

## Por que necesitamos cada pieza

| Pieza | Aportacion | Garantia y limite |
|---|---|---|
| Gram-Schmidt | Permite expresar la distancia como suma de contribuciones perpendiculares. | Sus vectores auxiliares no suelen pertenecer a la celosia: no sustituyen la base de busqueda. |
| LLL | Cambia la descripcion de la celosia por una base reducida y facilita la busqueda posterior. | Conserva la celosia mediante operaciones enteras reversibles. No garantiza el vector mas corto ni la clave privada original. |
| Babai, para CVP | Obtiene un candidato barato con el que fijar una distancia maxima inicial. | El candidato pertenece a la celosia, pero puede no ser el mas cercano. |
| Vector mas corto de la base reducida, para SVP | Proporciona un candidato no nulo y una longitud maxima inicial. | Es el mas corto entre las filas de esa base, no necesariamente entre todos los puntos de la celosia. |
| Enumeracion completa | Busca todas las combinaciones que puedan mejorar el candidato. | Da el optimo si las cotas y descartes son correctos y se completa el recorrido. Su coste es exponencial en el peor caso. |

## Por que la enumeracion demuestra el optimo

1. Tenemos un candidato valido de distancia R al objetivo (al origen en SVP).
2. Cualquier solucion mejor tiene que estar dentro de esa bola.
3. Gram-Schmidt descompone la distancia al cuadrado en sumandos no negativos.
4. Si una eleccion parcial ya alcanza o supera la mejor distancia, ninguna continuacion
   puede mejorarla: es seguro descartar toda esa rama. No necesitamos otras soluciones
   empatadas, pues ya hay un candidato valido con esa distancia.
5. Si encontramos un punto mejor, reducimos el radio a su distancia. No excluimos una
   solucion aun mejor, porque tambien estaria dentro del nuevo radio.
6. Al terminar todos los intervalos justificados, no queda un punto mejor sin explorar.

Esta justificacion requiere incluir los desplazamientos del objetivo en las formulas
de CVP. Para SVP, ademas, hay que excluir el cero. Usar un intervalo arbitrario de
multiplicadores o descartar ramas por una regla heuristica no conserva esta garantia.

## Alternativas y respuestas para la defensa

| Pregunta | Respuesta defendible |
|---|---|
| Por que no resolver el sistema y redondear? | Es un candidato inicial. En una base no ortogonal, redondear separadamente no garantiza minimizar la distancia. |
| Por que no usar solo LLL? | LLL resuelve reduccion de bases con garantias de aproximacion, no SVP/CVP exactos en general. |
| Por que no usar solo Babai? | Existe un contraejemplo en nuestros propios datos: Tier02T03. Necesitamos una fase exacta. |
| Por que enumerar despues de LLL? | El conjunto de puntos no cambia, pero cambian los intervalos y el arbol explorado. Esperamos menos trabajo con una base reducida; lo comprobaremos contando nodos y tiempos. |
| Por que no fuerza bruta con varios bucles? | Puede ser exacta con cotas justificadas. La enumeracion por distancias evita explorar muchas combinaciones que ya no pueden mejorar el candidato. La fuerza bruta sirve como contraste en casos pequenos. |
| Por que no Lagrange-Gauss? | Es una buena alternativa exacta para SVP en 2D. Nuestra busqueda comun debe cubrir tambien dimensiones 3 a 15. Podemos usar Gauss como contraste de los casos 2D. |
| Por que no embedding de Kannan + LLL? | Es una alternativa para obtener candidatos CVP. Introduce una dimension y un parametro adicional; aplicar LLL al embedding tampoco es una garantia general de recuperar el punto mas cercano. |
| Por que no BKZ? | Es una alternativa de reduccion mas elaborada. Primero mediremos si LLL + enumeracion cumple el objetivo con coste razonable; no afirmamos que LLL sea siempre mejor ni que BKZ sea innecesario para otras tallas. |
| Lo hemos implementado nosotros: por eso es mejor? | La implementacion propia permite explicar y trazar las operaciones. No demuestra que sea mas rapida que una biblioteca especializada. |

## Evidencias y experimentos

### Evidencia ya comprobada

En `Tier02T03_Latt`, despues de LLL:

- Babai por redondeo: distancia al cuadrado 187.
- Babai del plano mas cercano: distancia al cuadrado 186.
- El punto [807, 997, 549, 1528, 155] pertenece a la celosia y tiene distancia al cuadrado 155.

La existencia de ese ultimo punto basta para refutar que Babai sea exacto en esta tarea.
La enumeracion completa ya implementada confirma que 155 es la distancia minima global.

### Medicion actual y comparaciones pendientes

`results/ggh_exactos.csv` contiene una ejecucion local de las 19 tareas sin modulo:
distancia inicial y optima, nodos, hojas, mejoras y tiempos separados de LLL y enumeracion.
Se regenera con `python3 scripts/resultados_ggh.py`; el CSV no se versiona.
Es evidencia de viabilidad en estas instancias, no un estudio de rendimiento repetido ni
una comparacion completa con todos los metodos alternativos.

Usar las mismas instancias, maquina y criterio de distancia. Separar el tiempo de LLL
del tiempo de busqueda y presentar tambien su suma. Registrar por tarea:

- problema, dimension y metodo;
- distancia al cuadrado y pertenencia a la celosia;
- tiempo, nodos o combinaciones exploradas y radio inicial;
- si el resultado tiene garantia exacta o es un candidato aproximado.

Comparaciones prioritarias:

1. Babai por redondeo frente a plano mas cercano, ambos sobre la misma base reducida.
2. Babai frente a enumeracion exacta, incluyendo Tier02T03.
3. Enumeracion con y sin LLL en casos pequenos, manteniendo justificada la busqueda.
4. Ejecucion de las dos instancias sin modulo de dimension 15, para comprobar la
   viabilidad de la estrategia final en los ejercicios elegidos.

No atribuir todo el tiempo a la dimension: tambien influyen la geometria de la base,
el tamano de sus entradas y la posicion del objetivo. Un test de pertenencia comprueba
que el resultado es valido; no demuestra que sea optimo.

## Explicacion oral de la estrategia final

Explicacion de la estrategia implementada; al hablar de rendimiento, distinguir la
medicion puntual registrada del estudio comparativo que aun queda por completar:

> Elegimos una estrategia comun para SVP y CVP. Primero usamos LLL para obtener otra
> base de la misma celosia que facilite la busqueda. Para CVP, Babai nos proporciona
> un candidato rapido; para SVP, empezamos por un vector no nulo de la base reducida.
> Como esos candidatos pueden no ser optimos, completamos una enumeracion con cotas
> justificadas. Solo descartamos ramas cuya distancia parcial ya impide mejorar el
> resultado. Esto nos permite garantizar el optimo, y las mediciones muestran el coste
> para las instancias concretas del trabajo. No afirmamos que el problema general sea facil.

## Referencias de apoyo

- S. Galbraith, *Mathematics of Public Key Cryptography*, cap. 17: reduccion, LLL y
  Lagrange-Gauss, especialmente secciones 17.1 y 17.2.
  https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch17.pdf
- S. Galbraith, mismo libro, cap. 18: Babai (18.1 y 18.2), embedding (18.3),
  enumeracion exacta y su adaptacion a CVP (18.4 y 18.4.1).
  https://www.math.auckland.ac.nz/~sgal018/crypto-book/ch18.pdf

Los capitulos enlazados son las versiones ampliadas y corregidas del autor;
la numeracion puede diferir de la edicion impresa. Las referencias respaldan las
garantias teoricas; los resultados de nuestras instancias deben obtenerse del codigo.
