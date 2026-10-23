# D-09 — Solicitudes y lista negra

- **Fecha:** 17/10/2026 (acuerdos del 16–17/10/2026)
- **Estado:** `CONFIRMADO` para las elecciones expresas del PROPIETARIO, `PENDIENTE` para los límites identificados.
- **Clasificación:** `MATERIAL`.
- **Fuente viva:** [issue #19](https://github.com/mundoinformaticacanaria/whereis/issues/19). Su cuerpo y comentarios prevalecen ante cambios posteriores.
- **Integración:** revisión por TECH LEAD, no constituye baseline MVP ni habilita implementación.

## Clasificación y autorización
**MATERIAL — requisitos de consentimiento/seguridad y revisión de D-03/D-05.**
**CONFIRMADO por PROPIETARIO en conversación del 17/10/2026**, con mandato expreso de formalizar en GitHub. Este registro recoge únicamente opciones elegidas; no aprueba baseline global ni desarrollo.

## Contrato aprobado
1. Sección «Solicitudes», con **Enviadas** (pendientes y estado) y **Recibidas** (aceptar/rechazar/bloquear). El emisor no cancela una solicitud; el destinatario la acepta, rechaza o bloquea. Sin historial de rechazadas ni caducadas; no se expone motivo de rechazo.
2. Las solicitudes **caducan 24 horas desde su envío**. Una recibida se entiende **disponible en Whereis del destinatario aunque no se haya leído**; el acuse de recepción debe ser real, no confundirse con entrega de una notificación. Si está recibida, no se reenvía mientras siga pendiente; al rechazo o caducidad puede solicitarse de nuevo inmediatamente salvo bloqueo. Si no está confirmada la recepción, se permite reintento **sin solicitudes duplicadas** (D-03).
3. A puede recibir solicitud de un dispositivo B aún no conocido: al llegar queda en «Recibidas», NO en conocidos. **Aceptar** incorpora B a conocidos, pero **NO concede ubicación**; A debe activar expresamente el interruptor individual. B ve «Dispositivo conocido, sin autorización». Rechazo no lo añade.
4. **SUPERSEDED parcialmente D-03 #6:** la precondición antigua «B ya debe estar en conocidos de A» no se exige para recibir la primera solicitud. Se mantienen: ID por instalación, conocimiento ≠ permiso, control individual direccional y autorización expresa. TECH LEAD debe revisar consistencia con PR #7.
5. No se envían notificaciones por activación o revocación ordinaria de permisos; B consulta el estado en la app. No se notifica cada consulta autorizada ni se muestra al usuario un historial de quién consultó y cuándo. No hay botón de revocar «todos»: interruptores individuales, sin confirmación al desactivar o reactivar, respetando comprobación Android.
6. **Bloqueo:** A puede bloquear con confirmación tanto a B conocido como un ID válido introducido preventivamente. Revoca el permiso existente tras aplicación efectiva; impide nuevas solicitudes; cancela pendientes, sin notificar a A ni conservar historial de intentos. Solo se puede quitar mediante **desbloquear**, sin confirmación; no se recupera autorización, requiere nueva concesión expresa. Dispositivo bloqueado se muestra solo en la **lista negra local** de A, no en su lista habitual/mapa. No se elimina directamente de lista negra.
7. Si B es rechazado por bloqueo, no recibe notificación específica, pero al intentar solicitar y recibir respuesta de bloqueo muestra **alias/ID en rojo** y oculta del mapa la posición anterior, sin borrar necesariamente el último dato. Si A desbloquea, B no recibe aviso; al volver a solicitar y obtener respuesta no bloqueada desaparece el rojo, sin reactivar autorización. Diferenciar vista del bloqueador A y vista del bloqueado B.
8. Bloqueo preventivo requiere **verificar ID existente**. ID inexistente: «ID no encontrado», sin alta; sin conexión/no verificable: «No se pudo verificar el ID», reintento manual, sin bloqueo pendiente.
9. Incorporación por QR/ID sin Internet: no se añade provisionalmente; permitir reintento manual cuando pueda verificarse.

## Criterios de aceptación
- D09-CA01: solicitud recibida accesible sin leerla; caduca exactamente a 24h desde envío; no deja historial visible.
- D09-CA02: un reintento de entrega no produce dos solicitudes pendientes para el mismo par.
- D09-CA03: aceptar una solicitud de desconocido crea conocido, pero no autoriza posición; solo activar interruptor habilita consulta.
- D09-CA04: bloquear B impide nuevas solicitudes/posiciones, cancela pendientes y no afecta a C; desbloquear no restituye autorización.
- D09-CA05: lista negra separada; bloqueo remoto en B causa texto rojo y oculta marcador tras respuesta válida.
- D09-CA06: sin Internet o ID inexistente no se crea bloqueo ni alta provisional.
- D09-CA07: no hay notificaciones por consulta ordinaria/activación/revocación, ni historial de consultas visible.

## Actualización SEG y decisión material aún abierta (19–23/10/2026)

**SEG-01/SEG-02 CONFIRMADOS en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24):** el conocimiento de ID/QR no acredita identidad; ninguna ubicación nueva se entrega sin prueba válida de **instalación auténtica y autorización direccional vigente**, incluidas solicitudes concurrentes, desconexión o revocación. Se requiere proteger el flujo frente a suplantación, enumeración y abuso; la tecnología y mecanismos concretos siguen PENDIENTES. No equiparar acuse de solicitud con autorización.

**CONFLICTO PENDIENTE de PROPIETARIO:** el texto **«ID no encontrado»**, confirmado por D-09, podría revelar existencia de IDs ante consultas no autenticadas; el TECH LEAD ha elevado alternativas **A (conservar mensaje y aceptar riesgo residual mitigado)** / **B (respuesta indistinguible y modificar D-09)** en #24. **Esta documentación no elige A/B, no altera el mensaje ni aprueba excepciones a SEG-02.** Eliminar o cambiar esa regla requiere decisión material expresa.

## PENDIENTE / Riesgos
Identificación auténtica del emisor, protección frente a enumeración de IDs, abuso de solicitudes y respuestas a IDs, garantías de acuse; conciliación de estados offline/concurrencia; posible diferencia entre rechazo y desbloqueo. No se garantiza revocación instantánea sin conectividad. Legislación/seguridad de menores no se excluye por priorizar su protección.

## Handoff / trazabilidad
Relacionado con #6 (D-03), #8 (D-04), #10 (D-05), #16 (D-08). **TECH LEAD**: revisar coherencia, seguridad y viabilidad, integrar documentación por PR; **PROPIETARIO**: resolver solo cuestiones materiales residuales. Sin implementación autorizada.
