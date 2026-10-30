# D-06 — Consulta fallida: última ubicación conocida con fecha y hora

- **Fecha de aprobación del Propietario:** 16/10/2026.
- **Clasificación:** `MATERIAL` — definición funcional.
- **Estado de decisión:** `CONFIRMADO` por aprobación expresa; documento integrado en `main` mediante [PR #13](https://github.com/mundoinformaticacanaria/whereis/pull/13) el 23/10/2026. El baseline funcional global sigue `PENDIENTE`.
- **Issue:** [#12 — D-06](https://github.com/mundoinformaticacanaria/whereis/issues/12).
- **Decisiones relacionadas:** [D-01 #1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02 #2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-05 #10](https://github.com/mundoinformaticacanaria/whereis/issues/10).
- **Baseline funcional completo del MVP:** `PENDIENTE`; esta decisión no lo aprueba.
- **Decisiones históricas sustituidas:** ninguna. Se concreta un aspecto que permanecía `PENDIENTE` en D-02.

## Necesidad

Cuando no se puede obtener una nueva ubicación en una consulta puntual autorizada, la aplicación debe dejar clara la falta de respuesta actual y, cuando exista, ofrecer la última ubicación previamente obtenida sin inducir a error sobre su antigüedad.

## Actores y precondiciones

- **A:** dispositivo cuya ubicación se consulta.
- **B:** dispositivo consultante que está autorizado conforme a D-03/D-05 para solicitar una nueva ubicación.
- Se refiere a **fallos en una consulta que B podía realizar**, por ejemplo debido a falta de conectividad, indisponibilidad del dispositivo A, permisos Android o limitaciones de ejecución.
- **No** se interpreta como autorización para solicitar nuevas ubicaciones cuando A ha desactivado el permiso: en ese caso se aplica **D-05**.

## Decisión del Propietario — CONFIRMADO

1. **Aviso de fallo:** si una consulta puntual autorizada no puede obtener una nueva ubicación de A, Whereis informa explícitamente de que no se pudo actualizar la posición.
2. **Fallback informativo:** si B ya obtuvo con autorización una ubicación anterior de A, conserva y muestra **la última ubicación conocida**, acompañada de su **fecha y hora**, y una advertencia visible de que **no es actual**.
3. **Separación temporal:** la fecha y hora que acompañan esa ubicación representan la obtención previa; **no se sustituyen por la hora de la consulta fallida** ni se da a entender que la posición antigua es una posición reciente.
4. **Sin posición previa:** si B **nunca obtuvo una ubicación válida** de A, Whereis muestra «**Ubicación no disponible**» en lugar de coordenadas o ubicaciones ficticias.
5. **Sin consulta continua:** el fallo no provoca un modo de seguimiento continuo, ni actualizaciones periódicas automáticas. Las consultas siguen siendo iniciadas manualmente según D-01.

## Ejemplo de comportamiento

Se utiliza un ejemplo ficticio, no datos de una persona real:
- B obtuvo la ubicación de A el 16/10/2026 a las 14:00.
- A las 19:00, B solicita actualizar, pero la consulta falla por una condición de conectividad.
- Whereis muestra un aviso equivalente a «No se pudo actualizar la ubicación», conserva la posición previa y la identifica «Última ubicación conocida: 16/10/2026 14:00 — no es actual».
- Si nunca existió ubicación anterior, se muestra «Ubicación no disponible».

El texto exacto de las pantallas puede ajustarse durante el diseño UX sin alterar la obligación de informar del fallo y de la antigüedad.

## Reglas funcionales

- **D06-RN01:** un error en una consulta **no es** una ubicación nueva ni permite marcar el resultado anterior como ubicación actual.
- **D06-RN02:** solo se puede mostrar como último dato una ubicación **realmente obtenida en una consulta anterior autorizada**; no se infieren ni inventan coordenadas.
- **D06-RN03:** no se actualiza la fecha y hora asociada a la última posición al fallar la nueva consulta.
- **D06-RN04:** si la ubicación previa no existe o ya no puede mostrarse legítimamente, el resultado será «Ubicación no disponible». **D-10 / #20 CONFIRMADO**: se conserva solo la última posición legítima, sin caducidad funcional automática hasta eliminación del dispositivo; plazos de retención **legales**, almacenamiento y borrado físico efectivo siguen `PENDIENTES` de revisión.
- **D06-RN05:** la revocación de D-05 impide nuevas ubicaciones; **no** se debe usar D-06 para intentar consultas sin permiso. La opción B aprobada de D-05 permite conservar visible la última ubicación fechada cuando el permiso ha sido desactivado.
- **D06-RN06:** la desinstalación/reinstalación mantiene las reglas de D-04/SEG-04: el consultante **reinstalado** no recupera permisos, ID ni posiciones antiguas desde backup. Si solo se desinstala el emisor, el consultante que no se reinstaló puede conservar su última posición legítima anterior conforme D-10.

## Criterios de aceptación

- **D06-CA01:** B realiza una consulta autorizada que falla y ya dispone de última ubicación válida: Whereis comunica el fallo, presenta la última ubicación previa con fecha y hora.
- **D06-CA02:** dicha posición se identifica de forma inequívoca como «última conocida», «anterior» o equivalente, y no como ubicación actual.
- **D06-CA03:** el intento fallido **no cambia** la fecha/hora de la ubicación previa.
- **D06-CA04:** B realiza una consulta autorizada que falla sin historial de ubicación válida: se muestra «Ubicación no disponible», sin coordenadas inventadas.
- **D06-CA05:** el error no inicia reintentos periódicos automáticos ni un seguimiento continuo.
- **D06-CA06:** al desactivarse el permiso de B conforme a D-05, una nueva petición de B no obtiene una nueva posición por la vía de D-06.
- **D06-CA07 (SEG-01/02):** si la identidad de instalación o la autorización no es verificable, no se obtiene posición nueva; el último dato solo aparece donde D-09/D-10 permitan su visualización.
- **D06-CA08 (D-13):** mostrar siempre `DD/MM/AAAA HH:mm:ss` local del consultante referido a la posición previa, no a la consulta fallida.
- **D06-CA09 (SEG-04):** reinstalar B no restaura última posición ni permisos; desinstalar A no elimina por sí solo la última posición legítima en B que no se reinstala.

## Validaciones, errores y asuntos PENDIENTES

- **CONFIRMADO en D-10 / #20:** una sola última ubicación sin caducidad funcional automática; eliminar el dispositivo borra posición y personalización en ese consultante. Bloquear puede ocultar el marcador sin borrar el último dato; desbloquear no reactiva permiso. **PENDIENTE:** revisión jurídica de los plazos de retención y del borrado real de copias externas (#24).
- **D-12 / #22 CONFIRMADO:** mensaje genérico «No se ha podido actualizar la ubicación» cuando no hay causa remota verificable, no se encola ni reintenta automáticamente, y la repetición es manual. Sin conexión del consultante, aviso persistente y acción de refrescar deshabilitada. **PENDIENTE técnico:** umbrales concretos de timeout y capacidad de identificar/verificar causas remotas.
- **D-13 / #23 CONFIRMADO:** mostrar precisión en metros cuando exista y «Precisión no disponible» cuando falte; ubicación aproximada diferenciada. **PENDIENTE técnico:** exactitud disponible por versión/permisos de Android.
- **D-13 / #23 CONFIRMADO:** representar la **fecha/hora de obtención de la ubicación** como `DD/MM/AAAA HH:mm:ss` en zona horaria local del consultante, nunca en expresiones relativas. La hora de intento fallido **no** sustituye la de la posición previa. **PENDIENTE técnico:** precisión/sincronización fiable del reloj y zona horaria; no fingir exactitud no obtenida.
- **SEG-04 / #24 CONFIRMADO:** una instalación nueva tras desinstalación/reinstalación **no** recupera ID, última ubicación ni autorizaciones desde backup. Si solo A se desinstala, la ubicación legítima previa conservada por B (que no se reinstaló) puede seguir mostrándose conforme D-10. **PENDIENTE:** almacenamiento/cifrado, copia externa, plazos legales y borrado verificable; no prometer eliminación universal.
- **SEG-01/SEG-02 / #24 CONFIRMADOS:** si no se puede verificar identidad de la instalación y autorización direccional activa/vigente, ninguna petición obtiene ubicación nueva (fail-closed); solo última ubicación legítima previamente recibida cuando su visualización esté permitida por D-09/D-10. **PENDIENTE técnico:** autenticidad de la verificación, concurrencia y propagación de revocaciones/desconexión.
- Requisitos de accesibilidad/UX precisos para señalización de fallo y antigüedad.
- No se aprueba guardar un **historial** de trayectos ni nuevas categorías de datos; solo el uso funcional de la última ubicación ya obtenida.

## Riesgos e impacto

- **Privacidad:** conservar una posición antigua revela un dato personal aun si está etiquetado como anterior; requiere normas de acceso y retención.
- **Seguridad:** la consulta fallida no debe sortear el consentimiento; distinguir permiso activo de dato obtenido históricamente.
- **Alcance:** consulta puntual (D-01), ejecución condicionada por Android (D-02) y conservación de última ubicación tras revocar (D-05).
- **Arquitectura / costes:** `PENDIENTE`; TECH LEAD evaluará mecanismo mínimo que cumpla el contrato sin introducir proveedores o infraestructura sin autorización.


## Conciliación cronológica — D-09/D-10/D-12/D-13 y SEG (posteriores)

Las reglas originales D-06 siguen CONFIRMADAS para consultas puntuales **legítimas**. En su aplicación prevalecen los acuerdos posteriores: **D-09/#19** (bloqueo puede ocultar marcador previo, eliminar y desbloquear no concede autorización), **D-10/#20** (solo última ubicación, nunca historial, sin caducidad funcional automática), **D-12/#22** (fallos y no reintentos automáticos), **D-13/#23** (fecha/hora exacta local y precisión) y **SEG-01/02/04 en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24)** (denegar nuevas ubicaciones sin verificación real; sin recuperación tras reinstalar). El dato previo nunca se transforma en permiso ni en posición actual.

**Pendientes reales:** seguridad/menores, retención legal, medios de verificación, concurrencia, Android y proveedores. Sigue el **baseline funcional global PENDIENTE**. Bajo **G-02 vigente**, TECH LEAD revisa e integra con asesoramiento de ARQUITECTO activo; QA independiente en futuras implementaciones. **NO ASIGNAR PROGRAMADOR** por esta actualización documental.

## Enmienda funcional CONFIRMADA — descarte de respuestas posteriores al timeout (29/10/2026)

**Autoridad:** decisión MATERIAL expresa del PROPIETARIO, opción A, en [#12 (comentario de aprobación)](https://github.com/mundoinformaticacanaria/whereis/issues/12#issuecomment-6508029995), tras [propuesta FUNCIONAL A/B](https://github.com/mundoinformaticacanaria/whereis/issues/12#issuecomment-6507979579). Esta enmienda precisa D-06; no aprueba el baseline global ni una implementación.

- **D06-RN07:** una vez que B declara timeout/error de la consulta puntual **Q1**, se **descarta toda respuesta de ubicación Q1 recibida después**, incluso si A inició la captura legítimamente antes del timeout. Q1 permanece en `Error`; no se convierte en `Actualizado`, ni modifica posición conservada, instante de captura, marcador, mapa, ficha, lista o resumen de «Actualizar todos».
- **D06-RN08:** si existe una última posición legítima **P0**, se mantiene con su fecha/hora real y aviso de antigüedad; si no existe o no es visible legítimamente, se muestra «Ubicación no disponible». Ni timeout ni recepción tardía actualizan la fecha de P0.
- **D06-RN09:** solo una nueva consulta **Q2 manual**, con identidad y autorización vigentes verificables, puede obtener una nueva posición. Una respuesta tardía Q1 se descarta **antes, durante o después de Q2**, tanto si Q2 tiene éxito como si falla; no modifica sus resultados ni sobrescribe datos aceptados. Reconectar A no ejecuta capturas Q1 diferidas (D-12).
- **D06-RN10:** revocación, bloqueo, eliminación o reinstalación no se revierten por una respuesta tardía. Prevalecen D-04/D-05/D-09/D-10 y SEG-01/02; ninguna posición borrada/ocultada ni autorización se restituye.

**Criterios de aceptación aprobados para diseño y QA futura (NO ejecutados):**

- **D06-T01:** Q1 expira sin P0; fallo + «Ubicación no disponible»; una Q1 tardía no crea marcador ni cambia estado.
- **D06-T02:** Q1 expira con P0; fallo + P0 anterior fechada; una Q1 tardía no cambia posición ni timestamp.
- **D06-T03:** Q1 tardía llega antes/durante/después de Q2, con Q2 exitosa o fallida; Q1 no afecta Q2, mapa, última posición aceptada ni «Actualizar todos».
- **D06-T04:** A estaba offline y reconecta; no se captura Q1 diferida; solo una Q2 manual puede iniciar captura.
- **D06-T05:** revocación, bloqueo, eliminación o reinstalación con Q1 tardía; no reaparecen posiciones borradas/ocultas ni permisos.
- **D06-T06:** fecha/hora de ubicación realmente aceptada según D-13 (zona local de B, `DD/MM/AAAA HH:mm:ss`); timeout y recepción no se usan como hora de captura.

**PENDIENTE técnico:** umbral/mecanismo de timeout, IDs y versionado de Q1/Q2, orden/idempotencia, reloj y autenticidad de captura, transporte, condiciones Android y pruebas negativas reproducibles; conciliar con D-12/#22, SEG/#24 y [PR #35](https://github.com/mundoinformaticacanaria/whereis/pull/35) aún DRAFT. **No** se autoriza código, pruebas reales, proveedor, servicios, servidor/CRM, PROGRAMADOR ni timers Linux.

## Trazabilidad y siguiente acción

[Issue #12](https://github.com/mundoinformaticacanaria/whereis/issues/12). La regla de D-02 «no presentar una ubicación antigua como actual» sigue `CONFIRMADA` y queda especificada con este comportamiento de último dato conocido, no sustituida.

**TECH LEAD** revisará el documento y la PR asociada sobre su head SHA correspondiente. No se habilita desarrollo, proveedor, gasto, almacenamiento o baseline funcional general.
