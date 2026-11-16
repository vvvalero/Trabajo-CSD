# Consultas y uso de IA en la propuesta GGH

Herramienta: Codex (OpenAI), asistencia de programación, explicación, revisión y
redacción. Periodo: noviembre de 2026. No se registra un identificador preciso de la
versión del modelo.

## Consultas resumidas

Los puntos siguientes son paráfrasis de las consultas realizadas. Conservan su
propósito y se presentan como resúmenes, sin transcribir los mensajes de conversación.
La memoria incluye la misma declaración resumida y la referencia a la herramienta.

1. **Fundamentos:** precisar qué resuelven LLL y Babai y cuándo es necesaria una
   búsqueda exacta para SVP y CVP.
2. **Diseño e implementación:** plantear la enumeración exacta para GGH sin módulo y
   justificar las cotas de búsqueda y los criterios de poda.
3. **Validación:** revisar el código, detectar casos límite y contrastar resultados
   mediante pruebas independientes.
4. **Presentación:** apoyar la preparación del borrador y revisar su estructura,
   la interpretación de resultados, la claridad y el ajuste al enunciado.

## Uso y comprobación de las respuestas

El repositorio ya disponía de Gram-Schmidt, LLL y las dos variantes de Babai. Las
respuestas se incorporaron como propuestas de código para la enumeración exacta,
pruebas, explicaciones y texto del borrador. La organización y el diseño de la memoria
parten de `report/`.

La comprobación incluyó las cinco referencias de tier 0, búsquedas independientes en
casos pequeños y ejecución de las 19 tareas GGH sin módulo. La validación del
15/11/2026 pasó 222 pruebas; la revisión del 16/11/2026 pasa las 250 de la batería
actual, que también incluye LWE y Ring-LWE. El resultado se registra en
`validacion.json`. La justificación del óptimo se basa en la cobertura de la búsqueda
y la poda, además de las comprobaciones experimentales.

Las mediciones publicadas se conservan desde el 15/11/2026. Los resultados, tiempos y
trazas proceden de la ejecución del programa y se guardan en CSV/JSON. En la traza CVP
se muestran centros redondeados para facilitar la lectura; el cálculo usa fracciones
exactas.

La propuesta debe ser revisada y comprendida por ambos autores antes de su entrega.
