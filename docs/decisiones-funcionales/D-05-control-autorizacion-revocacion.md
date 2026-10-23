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
- **B:** dispositivo que desea consultar A; puede iniciar una primera solicitud incluso si A todavía no conoce a B (**D-09 / #19**). Aceptar esa solicitud incorpora B a conocidos, **sin autorizar ubicación**; solo la activación expresa del interruptor individual permite una consulta posterior, sujeta a SEG-01/SEG-02.
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
| Sí | Activado, con identidad de instalación y permiso direccional vigentes **verificados** | Puede consultar puntualmente si Android y conexión lo permiten | Resultado nuevo, cuando exista; identificado por fecha y hora |
| Sí | Desactivado y aplicado | **No** | **Última ubicación obtenida, fecha y hora, claramente marcada como anterior** |
| Nueva instalación por reinstalación | Sin vinculaciones heredadas (D-04/SEG-04) | No, hasta nueva vinculación | **En la nueva instalación no se restauran ni ubicación anterior, ni ID ni autorizaciones desde backup** |

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
- **D-10 / #20 CONFIRMADO:** dentro de Whereis se conserva **solo la última ubicación legítima**, no un historial; no hay caducidad funcional automática hasta eliminación del dispositivo. Los límites legales de conservación, el almacenamiento y borrado efectivo de copias externas siguen **PENDIENTES** de estudio (#24).
- Se conserva la última posición **dentro de Whereis**; capturas o copias realizadas por un tercero fuera de la app no pueden retirarse desde el interruptor.
- **D-10 / #20 y SEG-04 / #24 CONFIRMADOS:** si A se desinstala pero B sigue instalado, B puede conservar la última ubicación legítima anterior fechada hasta eliminación según D-10. Si **B se reinstala**, su nueva instalación **no recupera** posiciones, ID ni permisos de su instalación anterior, incluso desde backup. No se promete detección remota inmediata ni borrado físico universal de copias externas.
- Cuando B intenta «Actualizar ubicación» tras una desactivación efectiva, Whereis debe impedir obtener nuevas coordenadas. El estado y mensaje preciso de UI siguen pendientes.


## Conciliación cronológica — decisiones posteriores CONFIRMADAS (17–19/10/2026)

Esta ampliación no reescribe la aprobación de D-05 del 16/10/2026; aplica reglas posteriores del mismo PROPIETARIO:

- **D-09 / [#19](https://github.com/mundoinformaticacanaria/whereis/issues/19):** una solicitud puede llegar desde B desconocido; aceptarla **solo** lo añade a conocidos. El bloqueo (con confirmación) revoca la autorización, cancela solicitudes pendientes e impide solicitudes y consultas nuevas; **desbloquear no reactiva** permiso, a diferencia de volver a encender el interruptor de un conocido no bloqueado. Mientras A mantiene B bloqueado, no aparece el marcador antiguo de B en el mapa de A; el dispositivo B informado de su propio bloqueo oculta el marcador anterior de A conforme a la respuesta recibida. No equiparar bloqueo con simple desactivación.
- **SEG-01 y SEG-02 / [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24):** aunque el interruptor figure «activado» localmente, **sin prueba verificable de identidad de instalación y autorización direccional activa/vigente no se entrega ubicación nueva** (fail-closed). Esto incluye estados de desconexión, desinstalación, revocación y solicitudes concurrentes. La prueba técnica, el orden de aplicación y la autenticidad remota permanecen **PENDIENTES** de ARCHITECTO/TECH LEAD; ningún cambio visual local acredita revocación instantánea.
- **D-10 / [#20](https://github.com/mundoinformaticacanaria/whereis/issues/20) y SEG-04 / #24:** una sola posición previa legítima, siempre fechada como anterior después de revocar; eliminación del conocido borra esa posición y su personalización en el consultante, con confirmación. La nueva instalación no recupera ubicaciones ni permisos desde backup; el consultante que **no** se reinstaló puede conservar la última posición del emisor desinstalado. Retención legal y borrado universal **PENDIENTES**.

**Aceptación adicional:** (a) B desconocido aceptado no accede a ubicación antes de activar interruptor; (b) B bloqueado no accede y, tras desbloqueo, sigue sin permiso; (c) interruptor activo pero identidad/autorización no verificable no produce posición nueva; (d) reinstalar B no restaura ningún dato y desinstalar A no borra por sí solo la última posición legítima de B no reinstalado.

## Incidencias y situaciones pendientes

1. **Sin conexión o sincronización incompleta:** cuando A pulsa desactivar/activar sin conexión o mientras existen peticiones concurrentes, **qué significa «efectivo»**, qué se muestra en cada dispositivo, reintentos y medidas de seguridad exigen definición. No se presupone revocación remota inmediata ni que una interfaz local sea prueba de propagación.
2. **Permisos Android:** tratamiento exacto ante denegación de ubicación, permisos de segundo plano y restricciones por versión de Android; los permisos de notificaciones y lectura de QR se someten a contraste técnico.
3. **Última ubicación:** la regla funcional está CONFIRMADA por D-10 (solo una última ubicación, sin caducidad funcional automática); **PENDIENTES** de validación la limitación legal del plazo, ubicación/cifrado del dato, copias externas, borrado efectivo y tratamiento técnico de relojes/fechas. Sin posición legítima previa: «Ubicación no disponible» (D-06).
4. **Peticiones antiguas y abuso:** protección ante repetición de solicitudes iniciales, bloqueo de consultas pendientes en carrera con una desactivación, autenticidad y validación anti-suplantación.
5. **Desinstalación:** distinción funcional CONFIRMADA por D-10/SEG-04 entre A desinstalado y B consultante reinstalado; mecanismos de detección remota y recuperación/borrado real aún PENDIENTES. No afirmar sincronización instantánea.
6. **Tecnología, proveedor, almacenamiento y costes:** no aprobados.

## Trazabilidad y handoff

- El paso «registrar por QR/ID → solicitud inicial con notificación → interruptor» queda documentado en [D-03 / issue #6](https://github.com/mundoinformaticacanaria/whereis/issues/6).
- La vigencia sin caducidad, nuevo ID al reinstalar y no restaurar permisos se mantienen en [D-04 / issue #8](https://github.com/mundoinformaticacanaria/whereis/issues/8).
- **Siguiente acción:** TECH LEAD revisa e integra documentalmente bajo **G-02 vigente**, coordinando con **ARQUITECTO (Codex) ya activo** validación de Android, identidad, revocación y menores sin aprobación material implícita. QA mantiene independencia. Baseline funcional global y desarrollo siguen **PENDIENTES**; **NO ASIGNAR PROGRAMADOR**.
