# Guion vídeo — Function calling (`hora_actual`)

1. Intro (30 s): de S11 (estado) a S12 (tools). Aún no es un agente.
2. Frase clave: el LLM pide; Python ejecuta (a mano o con AFC).
3. Mostrar `def hora_actual` y la declaración con AFC **desactivado**.
4. Ciclo manual: `function_call` → resultado ISO → respuesta en texto.
5. Contraste AFC: una sola `generate_content` con `tools=[hora_actual]`.
6. Cerrar: misma idea; cambia quién orquesta el loop, no quién corre Python.
