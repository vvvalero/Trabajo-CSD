# Propuesta de memoria: GGH

Versión redactada a partir de la organización y el diseño de `../report/`.
El original se conserva como referencia. La propuesta se centra en los GGH sin
módulo que resuelve el código actual: LLL, candidato inicial y enumeración exacta.

## Compilar

Desde la raíz del repositorio, con `latexmk` instalado:

```bash
python3 reportproposal/build.py
```

El resultado es `reportproposal/memoria.pdf`. La propuesta incluye cinco páginas,
contando referencias, con texto, tablas y leyendas a tamaño normal de 12 pt y
márgenes de 2,2 cm. `secciones/` conserva la división de trabajo del original.

## Regenerar resultados y mediciones

```bash
python3 reportproposal/generar_datos.py --repeticiones 21
python3 reportproposal/build.py
```

También se puede ejecutar `python3 reportproposal/build.py --datos`.
Los tiempos son mediciones locales y cambiarán entre ejecuciones y equipos.
Los datos ya generados permiten compilar sin repetir las medidas.

`datos/` contiene las 19 soluciones y sus estadísticas, los once CVP comparados,
las dos trazas reales utilizadas, el entorno y hashes de los algoritmos, y el
resumen de consultas y uso de IA. Los siete ejercicios seleccionados para la
exposición suman 4,1 puntos antes del tope general de 4.
La tabla compara la cota inicial de cada candidato con la distancia óptima final.
El PDF incorpora las consultas resumidas y el uso de las respuestas; el registro en
Markdown aporta contexto adicional, sin ser necesario para leer la memoria.

La validación inicial del 15/11/2026 pasó 222 pruebas. Tras incorporar los métodos
LWE y Ring-LWE al repositorio, la revisión del 16/11/2026 pasa las 250 pruebas de
la batería actual; `datos/validacion.json` registra el comando y el resultado.
Las mediciones publicadas siguen siendo las del 15/11/2026, y sus hashes permiten
comprobar que los algoritmos GGH usados no han cambiado. Los centros de la traza CVP
se muestran como decimales redondeados; el cálculo y los datos JSON conservan las
fracciones exactas.

## Revisión de los autores

El texto está redactado como propuesta completa para revisar entre los dos autores.
Se deben confirmar los nombres, la selección final de tareas y las referencias antes
de entregar, y comprender las trazas y la prueba de optimalidad para la defensa.
No se presenta LWE, Ring-LWE ni los tres casos modulares como trabajo resuelto.
