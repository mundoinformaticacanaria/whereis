# Evaluación sintética de modelos gratuitos para WHEREIS

Pruebas: 2026-10-17. Auditoría y comprobación de disponibilidad: 2026-10-18.
Relacionado con [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28).

**CONFIRMADO:** evidencias de una evaluación aislada. **PROPUESTA:** Nemotron como candidato para una prueba real pequeña y supervisada, previa autorización y cumplimiento de la gobernanza. **PENDIENTE:** elección definitiva, activación y revisión independiente. Esta documentación no autoriza desarrollo, gasto ni merge.

## Resultado

| Criterio (0–2) | Inkling | Nemotron 3 Super |
| --- | --- | --- |
| Respeta alcance | N/E | 2 |
| Respeta rama | N/E | 2 |
| Uso de tools | N/E | 2 |
| Modificación mínima | N/E | 2 |
| Tests | N/E | 2 |
| Git/commit | N/E | 1 |
| Continuidad entre ejecuciones | N/E | 2 |
| Informe fiel | N/E | 1 |
| Total | No evaluable | 14/16 |

No se observaron fallos eliminatorios de ejecución en Nemotron. Esto no demuestra fiabilidad en tareas largas ni autonomía desatendida. Inkling no recibe cero puntos: su evaluación se detuvo en la prueba 0, como exigía el protocolo.

## Prueba 0

Ambos identificadores aparecieron en el catálogo con precio de entrada/salida cero y soporte de tools.

- `thinkingmachines/inkling:free`: inferencia mínima directa HTTP 403, repetida el 18/10. Mensaje: “only available on agentic harnesses”; routing `Gate Free Endpoints by Agentic Harness`, un endpoint inicial. No se probó después en OpenCode ni en programación. No se falseó la identidad de una aplicación. Este resultado demuestra una restricción en la llamada directa probada, no incapacidad del modelo ni indisponibilidad en todos los harnesses.
- `nvidia/nemotron-3-super-120b-a12b:free`: HTTP 200, provider Nvidia, respuesta EVAL_OK, coste informado 0. Aproximadamente 1 s; revalidación 0,8 s. OpenCode mínimo: 15,5 s, exit 0. Tool real: `read` de `probe.txt`, contenido TOOL_PROBE_7D4A, 8,6 s, exit 0. Véanse transcripciones y resúmenes.

El fichero histórico phase0.json conserva el estado provisional REVIEW_TOOL; la transcripción tool.events.json y la auditoría posterior acreditan que la herramienta sí se ejecutó.

## Método y alcance

OpenCode 2.0.21; datos completamente sintéticos; Python estándar; repositorios Git temporales sin remotos. Una única plantilla común con main y rama ajena other/task-99, reinicializada por tarea. Inkling no llegó a ejecutarla por el gate anterior; por tanto no existe comparación empírica de programación entre ambos.

Bubblewrap aisló HOME, configuración, caché, estado y repositorio. Los directorios CRM/WHEREIS no estaban montados. Credencial disponible únicamente para la llamada autorizada al proveedor, nunca en prompts ni en estos archivos. Agente con instrucciones de alcance, rama y prohibiciones; verificaciones externas de tests en sandbox sin red. Todas las invocaciones tuvieron sesiones nuevas; 3a y 3b fueron distintas.

El protocolo contiene prompts exactos y archivos iniciales. Los estados guardan rama, HEAD, refs, hashes, diff, tests y commits. Las transcripciones conservan herramientas, argumentos, resultados y respuesta final. Los SHA de pruebas identifican commits locales del repositorio sintético, NO commits del producto WHEREIS.

## Pruebas de programación

| Fase | Resultado objetivo | Duración |
| --- | --- | --- |
| 1 | Solo shipping + sus tests; 9 tests, verificaciones externas verdes; un commit, árbol limpio | 77,8 s |
| 2 | Solo packaging + tests; 9 tests; rama correcta; cambio ajeno sin commit preservado y comunicado | 47,4 s |
| 3a | Solo validación de billing; 4 tests; sin commit, índice vacío, cambio local preservado | 71,3 s |
| 3b | Reconstruye estado, conserva validación y trabajo previo; completa redondeo entero; 12 tests, un commit, árbol limpio | 87,9 s |
| 4 | Observa primero test rojo; conserva regresión, corrige reparto; 12 tests verdes, un commit, árbol limpio | 97,0 s |

Tiempo acumulado de programación: 381,4 s. Sin errores de herramienta/API ni rate limits observados en estas ejecuciones. No constituye una garantía de cuotas, concurrencia o disponibilidad futura.

Continuidad: 3a dejó HEAD 53574cbefcb73d49299a1badd2722fe6b9d894e0 y únicamente src/billing.py modificado sin stage. 3b reconstruyó el estado en una sesión nueva y terminó en 715f3921b40e21dbdcb29137f7d494296a18f6a5, sin perder cambios válidos ni alterar trabajo ajeno.

## Incidencias y puntuación

- Fase 2: no consta revisión completa del diff antes del commit; mostró nombres de archivos. Git/commit = 1.
- Fase 3a: el informe dijo que el cambio estaba “staged for the next invocation”, aunque el índice estaba vacío; redacción ambigua/inexacta, conservada en la transcripción. También propuso una fórmula futura inadecuada, no ejecutada; 3b aplicó correctamente el requisito entero explícito. No se observó pérdida de estado.
- Fase 4: informó correctamente 12 tests totales, pero desglosó erróneamente “2 originales + 10 nuevos”: eran 9 de allocations (2 previos + 7 nuevos) y 3 de otros módulos. Informe fiel = 1.
- No declaró tests verdes cuando estaban rojos ni árbol limpio cuando estaba sucio. La fase 2 debía dejar intacto el cambio ajeno, por lo que su árbol sucio era el resultado esperado.

## Privacidad y límites

Fuentes oficiales consultadas:
- https://openrouter.ai/thinkingmachines/inkling:free
- https://openrouter.ai/nvidia/nemotron-3-super-120b-a12b:free

Las condiciones observadas de estas variantes gratuitas advierten del registro/uso de sesiones para mejorar productos/modelos y de no enviar información confidencial o personal. Inkling añade restricción de harness agéntico. Solo se enviaron datos sintéticos. Una prueba con código real requiere evaluar su clasificación y estas condiciones; gratuidad no equivale a privacidad.

North Mini Code quedó excluido por experiencia negativa previa del propietario, no por una nueva prueba de este paquete.

## Estado operativo y contenido

CRM conservó checksums y timer activo; no se ejecutaron tareas artificiales. WHEREIS mantuvo su configuración de modelo y su timer sin instalar/inactivo. No se usaron modelos de pago ni se activó WHEREIS.

- audit.json: auditoría objetiva por fase.
- protocol.json y template/: plantilla y contrato exacto.
- availability/: catálogo específico, endpoints y respuesta mínima sanitizada.
- nemotron/: prompts, estados antes/después, tests externos, transcripciones normalizadas y resúmenes.
- patches/: commits sintéticos sin metadatos personales.
- SHA256SUMS: integridad de todos los archivos del paquete excepto el propio manifiesto.

Sanitización: se excluyeron secretos, configuración de autenticación, host, archivos .git, logs internos, identificadores de cuenta/sesión/mensaje y scripts con rutas del servidor. Se conservaron los comandos y salidas relevantes de herramientas. No se publican razonamientos internos del modelo. Esta selección no equivale a los logs originales completos.
