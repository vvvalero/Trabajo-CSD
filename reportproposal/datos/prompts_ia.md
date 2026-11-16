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

1. ¿Qué cambia al buscar el punto más cercano cuando los vectores de la base no son
   ortogonales?
2. ¿Cómo plantear en Python el sistema que calcula los multiplicadores de la base
   antes de redondearlos?
3. ¿Cómo elegir el radio de búsqueda para no dejar fuera un punto mejor?
4. ¿Por qué LLL y Babai pueden dar un candidato válido sin ser óptimo y cómo completar
   el resolutor con una enumeración exacta?
5. ¿Qué errores o casos límite debería revisar en esta implementación?

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
