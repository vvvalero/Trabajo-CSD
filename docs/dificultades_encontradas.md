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

### Dificultades y decisiones

**LLL demasiado lento en su primera versión.** La primera versión llamaba a `gso` con la base entera antes de
cada resta, y tardaba 17,6 s solo con las 22 tareas GGH. Dos cambios, sin cambiar el algoritmo ni el
resultado:
- Calcular `gso(b[:k + 1])`: para decidir sobre b_k solo intervienen b_0, ..., b_k.
- Recalcular `gso` solo cuando b_k cambia (cuando r ≠ 0), no en cada vuelta del bucle.

Con eso, la tarea GGH más grande (dimensión 15) pasa a tardar 0,5 s, y los 26 tests de LLL ~1 s.
Pendiente: medir con las celosías del ataque a LWE (dimensión hasta 31).
