# D-05 — Activar y desactivar permiso de consulta de ubicación

- **Aprobación del Propietario:** 16/10/2026.
- **Estado:** `CONFIRMADO` respecto del control y de la última ubicación; aplicación remota sin conexión `PENDIENTE` de definición y validación técnica.
- **Clasificación:** `MATERIAL`.
- **Issue:** [#10](https://github.com/mundoinformaticacanaria/whereis/issues/10).
- **Vínculos:** [D-03 #6](https://github.com/mundoinformaticacanaria/whereis/issues/6), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-01 #1](https://github.com/mundoinformaticacanaria/whereis/issues/1) y [D-02 #2](https://github.com/mundoinformaticacanaria/whereis/issues/2).
- **Baseline funcional global:** `PENDIENTE`; la decisión no autoriza implementar.
- **Decisiones previas sustituidas:** el enfoque planteado inicialmente para D-05 que exigía una nueva petición tras revocar queda `SUPERSEDED` como propuesta y queda reemplazado por reactivación mediante interruptor; se mantiene D-04 sobre reinstalación.

## Necesidad y actores

Permitir al dispositivo que comparte su ubicación controlar fácilmente, de modo individual y reversible, qué dispositivos conocidos pueden consultar posiciones puntuales, sin inundar bandejas con solicitudes. Mantener la última ubicación conocida en el consultante tras retirar el permiso, con indicación fiable de antigüedad.

- **A:** dispositivo que comparte su ubicación y gestiona el permiso.
- **B:** dispositivo que desea consultar A; previamente conocido por QR o ID y con primera solicitud realizada según D-03.
- **C:** otro dispositivo autorizado por A que no debe verse afectado por la decisión sobre B.

## Confirmación del PROPIETARIO — 16/10/2026

1. **Autorización controlada por botón/interruptor:** en el listado de dispositivos conocidos de A se indica, por separado para cada uno, si está **activado o desactivado** el permiso que deja consultar la ubicación de A.
2. **Desactivación:** A apaga el permiso a favor de B. Una vez aplicado el cambio, B **no puede realizar nuevas consultas eficaces ni obtener nuevas posiciones** de A. No se borra a B de la lista de conocidos por este hecho.
3. **Última posición conservada (opción B):** B **mantiene visible la última ubicación previamente obtenida**, **acompañada de su fecha y hora reales**, identificada explícitamente como **última posición conocida/anterior** y nunca como ubicación recién consultada.
4. **Reactivación:** A vuelve a encender el interruptor de B y restaura la posibilidad de nuevas consultas puntuales **sin necesidad de que B vuelva a solicitar permiso**. No se genera una nueva notificación de solicitud por este cambio.
5. **Individualidad y dirección:** desactivar B no cambia la autorización de C. La autorización A→B no concede B→A por sí sola.
6. **La primera habilitación se verifica:** cuando se habilita por primera vez el permiso de consulta en A, Whereis debe **comprobar los servicios y permisos de ubicación Android exigidos por la modalidad prevista**, guiando a la persona a concederlos/activarlos si faltan; no se conceden automáticamente ni se presupone que solo exista un permiso.
7. **Solo consultas puntuales:** mientras un permiso está activo, B solo accede a posiciones solicitadas expresamente con las restricciones de D-01/D-02; el interruptor no inicia rastreo continuo ni una captura en vivo.
8. **Sin peticiones repetidas:** el flujo de primera solicitud de D-03 se utiliza para pedir el acceso inicial; la posterior suspensión/reanudación del permiso no crea solicitudes nuevas. La interfaz debe evitar solicitudes iniciales duplicadas de un mismo par.

## Tabla de estados funcionales

| Conocido | Permiso de A para B | Puede obtener nueva ubicación A | Qué muestra B |
|---|---|---|---|
| No | No concedido | No | Sin posición facilitada |
| Sí, solicitud inicial pendiente | Desactivado | No | Sin nueva ubicación |
| Sí | Activado y efectivo | Puede consultar puntualmente si Android y conexión lo permiten | Resultado nuevo, cuando exista; identificado por fecha y hora |
| Sí | Desactivado y aplicado | **No** | **Última ubicación obtenida, fecha y hora, claramente marcada como anterior** |
| Nueva instalación por reinstalación | Sin vinculaciones heredadas (D-04) | No, hasta nueva vinculación | No se restauran autorizaciones anteriores |

La tabla es ilustrativa de **estados funcionales**, no define una arquitectura de sincronización ni promete que todas las operaciones sean instantáneas.

## Criterios de aceptación

- **D05-CA01:** A ve al menos el ID de cada dispositivo conocido y su autorización individual activada/desactivada.
- **D05-CA02:** A desactiva solo B. Tras aplicarse la desactivación, B no obtiene una nueva ubicación de A; C sigue conservando su permiso anterior.
- **D05-CA03:** si B había obtenido una posición antes de la desactivación, la sigue viendo con **fecha/hora de esa posición** y rótulo que evite confundirla con una ubicación actual.
- **D05-CA04:** B no dispone de una consulta eficaz/actualización de posición nueva mientras el permiso esté desactivado y efectivo; no se muestran datos antiguos como respuesta fresca.
- **D05-CA05:** A puede reactivar la autorización de B conocido sin volver a solicitar desde B, sin nuevas notificaciones de solicitud y sin cambiar el ID.
- **D05-CA06:** el estado de A→B no habilita automáticamente B→A.
- **D05-CA07:** al activar por primera vez, se comprueban los requisitos Android de ubicación y se orienta para corregir cualquier carencia; nunca se aprueban permisos Android silenciosamente.
- **D05-CA08:** la activación de B no genera seguimiento continuo; las consultas mantienen comportamiento puntual.
- **D05-CA09:** desinstalar/reinstalar A o B **no** se comporta como apagar/encender el interruptor: el nuevo ID e inexistencia de vínculos de D-04 exigen nuevos procesos de reconocimiento y aceptación.

## Reglas de seguridad y privacidad

- Conocer el ID Whereis, estar registrado como «conocido» o haber recibido una notificación **no equivale a consentimiento**.
- Para una consulta se requieren autorización activa y válida del emisor, autenticidad técnica y los permisos Android aplicables; el mecanismo concreto no está elegido.
- Conservar la última ubicación anterior **no** obliga a conservar historial de posiciones, ni autoriza retención indefinida de un historial no definido.
- Se conserva la última posición **dentro de Whereis**; capturas o copias realizadas por un tercero fuera de la app no pueden retirarse desde el interruptor.
- No se promete eliminación o conservación de esa posición al **desinstalar**, porque D-04 fija la eliminación de relaciones, no la política de posiciones ya entregadas.
- Cuando B intenta «Actualizar ubicación» tras una desactivación efectiva, Whereis debe impedir obtener nuevas coordenadas. El estado y mensaje preciso de UI siguen pendientes.

## Incidencias y situaciones pendientes

1. **Sin conexión o sincronización incompleta:** cuando A pulsa desactivar/activar sin conexión o mientras existen peticiones concurrentes, **qué significa «efectivo»**, qué se muestra en cada dispositivo, reintentos y medidas de seguridad exigen definición. No se presupone revocación remota inmediata ni que una interfaz local sea prueba de propagación.
2. **Permisos Android:** tratamiento exacto ante denegación de ubicación, permisos de segundo plano y restricciones por versión de Android; los permisos de notificaciones y lectura de QR se someten a contraste técnico.
3. **Última ubicación:** retención global de posiciones, escenarios sin posición previa, error por falta de fecha y sincronización del reloj siguen pendientes.
4. **Peticiones antiguas y abuso:** protección ante repetición de solicitudes iniciales, bloqueo de consultas pendientes en carrera con una desactivación, autenticidad y validación anti-suplantación.
5. **Desinstalación:** efectos en dispositivos remotos y posiciones previas según D-04; detección instantánea no garantizada.
6. **Tecnología, proveedor, almacenamiento y costes:** no aprobados.

## Trazabilidad y handoff

- El paso «registrar por QR/ID → solicitud inicial con notificación → interruptor» queda documentado en [D-03 / issue #6](https://github.com/mundoinformaticacanaria/whereis/issues/6).
- La vigencia sin caducidad, nuevo ID al reinstalar y no restaurar permisos se mantienen en [D-04 / issue #8](https://github.com/mundoinformaticacanaria/whereis/issues/8).
- **Siguiente acción:** TECH LEAD revisa y propone integración del documento, contrasta viabilidad Android y seguridad con G-01 V3. QA mantiene revisión independiente de futuras implementaciones. No hay autorización de desarrollo.
