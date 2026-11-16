# Registro del uso de IA en la propuesta GGH

Herramienta: Codex (OpenAI), asistencia de programación, explicación, revisión y
redacción. No se registra aquí un identificador preciso de la versión del modelo.
Propuesta redactada en noviembre de 2026. La bibliografía del PDF declara
la asistencia; este registro conserva las instrucciones del usuario relevantes para
los artefactos presentados. Los mensajes siguientes son literales, incluidas sus erratas.

## Implementación y revisión de la enumeración

Contexto previo: el repositorio ya disponía de Gram-Schmidt, LLL y las dos variantes
de Babai. Se pidió completar la búsqueda exacta para los GGH sin módulo.

> vale pues guiame hacia resolver lo que queda de ggh

> vale, de cara a la defensa del trabajo tenemos que defender el uso de x algoritmo frente a otras opciones y tal quiero que sea defendible.

> pues implementalo supongo?

> revisa los cambios porfa bien por si acaso

Uso del resultado: propuesta del recorrido de enumeración, cotas racionales, orden de
Schnorr-Euchner, integración del resolutor, pruebas y documentación. Se contrastaron
resultados con las referencias de tier 0 y con búsquedas independientes en casos
pequeños. La revisión ejecutó 510 casos aleatorios y 1500 comprobaciones de cotas y
orden; la validación del 15/11/2026 pasó 222 tests. No se usan esos tests como sustituto
de la justificación matemática de cobertura y poda.

## Redacción de esta propuesta

> vale, vamos a revisar el report (memoria)

> como estamos en una rama quizás podemos crear un reportproposal (directorio) basado en report con una versión ya más o menos "final" pudiendo consultar el report original si se quisiese aunque sé q tenemos git y podríamos volver atrás

> ves bien así la memoria propuesta entonces? cumple con las normas del enunciado?

> haz lo q consideres

> a ver quiero que hagas lo que consideres

Uso del resultado: borrador de memoria centrado en GGH, organización y maquetación
basadas en `report/`, generación reproducible de cifras y trazas, explicación de las
garantías y límites y revisión del PDF. Los valores numéricos se ejecutan y guardan
en los CSV/JSON; no se inventan resultados para rellenar tablas.
Los prompts relevantes y el tratamiento de las respuestas también se incluyen en el
propio PDF, que se puede leer sin este registro. La revisión incorpora la cota inicial
por tarea y explica cuándo la enumeración certifica un candidato sin mejorarlo.
La revisión del 16/11/2026 conserva las fórmulas centrales, simplifica los centros
numéricos de la traza CVP y aclara que los métodos LWE y Ring-LWE del repositorio
quedan fuera de la selección de esta memoria. La batería actual pasa 250 tests;
el resultado se registra en `validacion.json`. Las medidas del día 15 se conservan.

Este registro no atribuye a los autores una validación humana que aún no hayan hecho:
la propuesta debe leerse y asumirse críticamente por ambos antes de su entrega.
