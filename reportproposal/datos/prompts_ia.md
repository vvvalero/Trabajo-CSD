# Consultas y uso de IA en la propuesta GGH

Herramientas declaradas para el trabajo:

- **OpenAI Codex**, de OpenAI: <https://openai.com/codex/>.
- **Claude Code**, de Anthropic: <https://code.claude.com/docs/en/overview>.

Asistencia de programación, explicación, revisión y redacción. Periodo: noviembre de
2026. Se recoge el uso conjunto de las herramientas; no se registran identificadores
precisos de las versiones de los modelos.

## Consultas resumidas

Los puntos siguientes son consultas representativas reformuladas a partir de dudas
planteadas en la conversación. Conservan su propósito y se presentan como paráfrasis,
sin transcribir los mensajes de conversación.
La memoria incluye la misma declaración resumida y la referencia a la herramienta.

1. Si la base no es ortogonal, ¿cómo buscamos el punto más cercano?
2. ¿Cómo hago el sistema en Python para sacar los multiplicadores?
3. ¿Para qué necesitamos Gram-Schmidt en estos algoritmos?
4. ¿Por qué al cambiar la base con LLL seguimos teniendo la misma celosía?
5. ¿Qué diferencia hay entre los dos métodos de Babai?
6. ¿Qué tengo que tener en cuenta para elegir el radio de búsqueda?
7. Si LLL y Babai no siempre dan el óptimo, ¿qué nos falta para asegurarlo?
8. ¿Puedes revisar el código por si se nos ha pasado algún caso?

## Uso y comprobación de las respuestas

El repositorio ya disponía de Gram-Schmidt, LLL y las dos variantes de Babai. Las
consultas abarcaron la comprensión y revisión de estos algoritmos, además del diseño
y la implementación de la enumeración exacta. Las respuestas se incorporaron como
propuestas de código, pruebas, explicaciones y texto del borrador. La organización y
el diseño de la memoria parten de `report/`.

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
