# Memoria: criptoanálisis de GGH, LWE y Ring-LWE

Es la memoria que se entrega (`memoria.pdf`). Parte de la organización y el diseño de `../report/`,
que se conserva solo como esqueleto. El límite es de 5 páginas en total, incluidas las referencias,
con texto a 12 pt y márgenes de 2,2 cm. `\finmemoria` (en `estilo.tex`) da error si el documento
completo pasa de 5 páginas.

Contenido:

- GGH: las 14 tareas puntuables sin módulo con LLL + enumeración exacta (Tabla 1, trazas de 2.03 y
  3.03). Las 3 con reducción módulo n no se resuelven.
- LWE: Tier1 T01–T05 y Tier2 T01–T03 por fuerza bruta sobre el error; Tier2 T04–T05 y Tier3 T01–T05
  como CVP en la celosía q-aria (`src/pqc/lwe/ataque_celosia.py`). Tabla 2, trazas de L1.05 y L3.01.
- Ring-LWE: las 3 tareas Tier3 como sistema lineal sin reducción mod q (traza de R3.01).
- Figura de tiempo frente a talla para los tres métodos.

## Compilar

Desde la raíz del repositorio, con `latexmk` instalado:

```bash
python reportproposal/build.py            # solo compila
python reportproposal/build.py --datos    # regenera los datos y compila
```

## Regenerar los datos

```bash
python reportproposal/generar_datos.py --repeticiones 21    # GGH
python reportproposal/generar_datos_lwe.py --repeticiones 5 # LWE y Ring-LWE
```

Las mediciones actuales son del 16/11/2026 (Windows, Python 3.13) y cambian entre equipos.
`datos/` guarda las tablas LaTeX generadas (`tabla_ggh.tex`, `tabla_lwe.tex`), las coordenadas de
la figura (`mediciones*.tex`), los resultados completos en CSV, las trazas GGH (`trazas.json`), el
entorno de medida y el registro de uso de IA (`prompts_ia.md`).

## Antes de entregar

- Revisar entre los dos autores el texto y las trazas.
- Revisar que la declaración de IA de `secciones/5_referencias.tex` refleja el uso real.
