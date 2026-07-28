# Preguntas de evaluación — Sprint 10

`preguntas_eval.json` se usa en los Workouts 2 y 3 para evaluar **respuestas generadas** (y comparar con el retrieval de S9).

| Campo | Uso |
|-------|-----|
| `id` | Identificador |
| `texto` | Pregunta |
| `fuente_esperada` | Fuente orientativa del corpus |
| `respuesta_esperada` | Criterio manual de acierto (no corrección automática) |
| `deberia_abstenerse` | `true` si no hay evidencia suficiente en el corpus |
| `notas` | Caso pedagógico (alucinación, top-k, etc.) |
