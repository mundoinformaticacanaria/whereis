# #115 — matriz de conciliación D-08/D-12 (propuesta, no baseline)

**Estado:** propuesta TECH LEAD para revisión FUNCIONAL/ARQUITECTO y QA independiente. No implementada, no adoptada. Fuentes: [#115](https://github.com/mundoinformaticacanaria/whereis/issues/115), [#114/B](https://github.com/mundoinformaticacanaria/whereis/issues/114), [#120/B](https://github.com/mundoinformaticacanaria/whereis/issues/120), [#132/A](https://github.com/mundoinformaticacanaria/whereis/issues/132), [PR #112](https://github.com/mundoinformaticacanaria/whereis/pull/112) y [PR #122](https://github.com/mundoinformaticacanaria/whereis/pull/122).

## Contratos confirmados y separación G/Q

- G es una operación grupal con progreso **finalizados/total**, control **Cancelar** separado y timeout obligatorio. Terminar/cancelar no lanza automáticamente otra actualización: requiere nuevo gesto manual (#115).
- Cancelar G congela su resumen y no implica interrumpir por la fuerza solicitudes individuales Q remotas. Las respuestas tardías de G no reabren G ni recentran automáticamente el mapa (#115, #132/A).
- Q individual autónoma **preexistente** y reutilizada por G conserva la posibilidad de actualizar P0 al llegar legítimamente antes de su propio timeout, con identidad y permisos válidos. Una Q nacida exclusivamente para G **no** adquiere esa autonomía al cancelar G (#132/A).
- La política de botón durante G (#120/B) **no** se extrapola a una Q individual aislada. La precedencia de encuadre grupal corresponde a #114/B, no a una regla genérica de llegada tardía.

## Matriz de escenarios para pruebas UX115

| Caso | Disparador | Resultado contractual / comprobación requerida |
| --- | --- | --- |
| UX115-N01 | Cancelar G con Q autónoma preexistente en vuelo | G terminal y resumen congelado; Q puede actualizar P0 solo si llega legítimamente antes de su timeout y mantiene permisos/identidad; sin recentrado automático por G |
| UX115-N02 | Cancelar G con Q creada solo por G en vuelo | G terminal; Q no obtiene autonomía por cancelación; ninguna respuesta tardía revive G |
| UX115-N03 | Vence timeout de G con respuestas pendientes | G termina por timeout; progreso y resumen final consistentes; rechazar actualización tardía atribuida a G; no reintentar automáticamente |
| UX115-N04 | Revocación o cambio de identidad mientras Q está en vuelo | No aceptar respuesta bajo identidad o permiso caducado; evitar revelar ubicación retirada |
| UX115-N05 | Nueva pulsación manual tras G terminal | Solo el gesto explícito puede iniciar nueva operación, sujeto a elegibilidad y no duplicación; no reutilizar resumen terminal como operación activa |
| UX115-N06 | Segunda pulsación mientras G activa | Aplicar exclusivamente la decisión #120/B, sin extenderla a Q individual aislada |
| UX115-N07 | Respuesta de Q reutilizada tras cancelar G | Separar efecto individual P0 permitido de cualquier efecto de G terminal; verificar precedencia #114/B |
| UX115-N08 | Todos los destinos inelegibles / sin conectividad | No presentar éxito ficticio ni progreso imposible; confirmar microcopy con FUNCIONAL |

## Aspectos no resueltos por esta matriz

1. **Duración numérica del deadline:** no aprobada; 60 segundos es referencia histórica, no contrato.
2. **Mecanismo de cancelación y carreras G/Q:** requiere dictamen técnico [#170](https://github.com/mundoinformaticacanaria/whereis/issues/170) antes de prometer garantía de despacho completo o timeout efectivo.
3. **Texto exacto y estados accesibles:** corresponde a FUNCIONAL; no se aprueba microcopy por esta propuesta.
4. **Integración:** comparar los HEAD vigentes de PR #112 y #122, resolver contradicciones documentales y solicitar QA independiente del HEAD resultante. No reutilizar QA de un SHA anterior.

**Gates:** sin Android, ejecución de pruebas reales, integración, secretos, servidores, CRM, proveedores, costes ni timers. CI/enforcement #42 y autorización individual de merge siguen pendientes.
