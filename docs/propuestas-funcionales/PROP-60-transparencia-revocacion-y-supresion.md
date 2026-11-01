# PROP-60 — Transparencia, revocación y supresión en A/B (SEG-03/04)

- **Fecha:** 01/11/2026.
- **Issue ejecutora:** [#60](https://github.com/mundoinformaticacanaria/whereis/issues/60); issue matriz [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41).
- **Clasificación:** **MATERIAL / PROPUESTA FUNCIONAL**, no baseline aprobado.
- **Estado:** inventario de reglas **CONFIRMADAS** y propuestas **PENDIENTES** de revisión TECH LEAD / decisión PROPIETARIO; sin dictamen jurídico.
- **Autoridad:** las decisiones y comentarios de #41, #24 y las decisiones D-04/05/09/10/12 en main prevalecen sobre este análisis.
- **Dependencia paralela:** [#61 / PR #66](https://github.com/mundoinformaticacanaria/whereis/pull/66) inventaría superficies técnicas; QA #69 emitió **DEFECTOS** en el HEAD anterior y ARQUITECTO tiene la corrección pendiente. Este análisis **no** valida aquella PR, sus reglas de backup ni las pruebas Android.
- **Ámbito aprobado:** uso personal/familiar en España; ubicaciones y relaciones persistentes solo en instalaciones participantes; coste de funcionamiento 0 €; ningún proveedor/relay/servicio autorizado. L-02b/c/d permite **solo estudio** de canales externos con metadatos mínimos, no despliegue (#41/#52).

## 1. Actores y lenguaje de interfaz

| Actor | Facultades CONFIRMADAS | Advertencia de transparencia; NO implica derecho nuevo |
|---|---|---|
| **A — dispositivo que comparte** | Gestiona por dispositivo conocido quién puede consultar A, usando interruptor direccional; puede bloquear y desbloquear; controla ubicación y permisos Android | Desactivar impide posiciones nuevas cuando el cambio es efectivo; no elimina automáticamente las ya recibidas por B. No prometer revocación instantánea sin conexión |
| **B — dispositivo consultante** | Puede consultar puntualmente si A lo autorizó y se verifican identidad/permiso. Conserva solo la última posición legítima y puede eliminar localmente el dispositivo conocido con confirmación | Una última ubicación anterior no es una localización actual; B no puede convertirla en dato nuevo. El borrado en B no equivale a borrar copias fuera de su instalación |
| **C — otro consultante** | Autorización individual y direccional, independiente de B | Una decisión sobre B no concede ni retira automáticamente permisos de C |
| **Representante/tutor de un menor, cuando corresponda** | **Ningún privilegio parental adicional CONFIRMADO**: SEG-03 excluye temporalmente modo familiar especial, sin eximir garantías aplicables | Su representación, acceso a información y ejercicio de derechos requieren evaluación jurídica y decisión material; no presumir control automático de A/B ni verificación de edad |

**Distinción obligatoria:** el interruptor y la aceptación de solicitudes son **autorización funcional entre instalaciones**, no prueban por sí solos una base jurídica, representación de menores o consentimiento legalmente suficiente. El conocimiento de ID/QR, aceptación de solicitud y pertenencia a conocidos tampoco autorizan ubicación: SEG-01/02 exigen identidad y permiso vigentes.

## 2. Flujos: estados existentes CONFIRMADOS

### F-01 — Vinculación y primera autorización

1. B conoce un ID/QR, pero **no** recibe posición por conocerlo.
2. Puede llegar a A una solicitud de B desconocido: aparece en «Recibidas». Aceptar crea *conocido*, **no** habilita posición; rechazar no crea conocido. Solicitud expira a las 24 h desde envío, con acuse de disponibilidad real en la app (D-09).
3. A activa expresamente el interruptor individual de B, sujeto a los permisos Android y verificación de identidad/autorización. A no habilita C por activar B.
4. Si no se verifican identidad de instalación y permiso direccional al liberar una posición **no** se entrega posición nueva (SEG-01/02); ni QR ni push son credenciales suficientes.
5. En un actor sin derecho a conocer existencia, la comprobación del ID **no** revela si existe (opción B de SEG-02); tampoco la vista de solicitudes debe revelar datos de terceros indebidamente.

### F-02 — Revocar el permiso de B desde A (NO es borrar)

1. A desactiva el interruptor de B; B sigue siendo conocido.
2. Cuando la revocación se ha aplicado, B deja de obtener posiciones nuevas; otras relaciones (p. ej. C) no cambian. Una verificación no disponible fuerza denegar datos nuevos (SEG-01), sin prometer propagación remota inmediata.
3. B puede seguir viendo **su última posición obtenida legítimamente** de A, con **fecha/hora exacta de captura** y aviso «Ubicación anterior / no actual», conforme D-05/D-06/D-10/D-13; si nunca hubo posición, «Ubicación no disponible».
4. A puede reactivar B conocido sin nueva solicitud; reactivar **no** inicia consulta automática. Las consultas siguen siendo manuales.
5. D-09 prohíbe notificaciones ordinarias por cambios de permiso; no introducir push informativa ni historial de acceso sin nueva decisión.

### F-03 — Bloquear / desbloquear una instalación

1. A confirma bloqueo de B conocido o de ID preventivo **legítimamente verificable**: se revoca el permiso efectivo, se cancelan pendientes y A mueve la relación a la lista negra local; B/C no adquieren posición por ello.
2. En la vista de A, el bloqueado no aparece en lista/mapa habituales. El bloqueo **no es borrado físico remoto** de la última posición que B ya recibió.
3. Tras un intento de B y respuesta de bloqueo válida, su alias/ID aparece rojo y se oculta el marcador antiguo; el dato puede quedar conservado localmente por D-09/D-10. **No** revelar existencia/estado a actores sin derecho; anti-enumeración SEG-02 sigue vigente.
4. Desbloquear A no restaura permisos y no requiere confirmación. B no recibe notificación automática; cambios visibles según D-09 solo tras verificación/reintento legítimo.

### F-04 — Eliminar relación/dispositivo desde B

1. B selecciona «Eliminar dispositivo»: Whereis **confirma las consecuencias** antes de actuar (D-10).
2. Al confirmar, B elimina **en su instalación** la relación local, la última posición y personalización (alias, foto, color) y revoca/cancela los permisos asociados **donde su efecto pueda comprobarse**. Si B cancela, se conservan datos.
3. B no recupera datos eliminados por respuesta tardía, cola automática o restauración de la antigua instalación; criterios a demostrar técnicamente en #61/#24, **NO DEMOSTRADOS**.
4. Volver a relacionarse requiere incorporación/solicitud y autorización expresa nuevas; ninguna eliminación concede permisos.
5. **PENDIENTE:** alcance y estado de revocación en el otro dispositivo cuando no hay conexión. No afirmar «borrado en el teléfono de A/B» si solo se comprobó el borrado local en uno.

### F-05 — Desinstalación/reinstalación

1. Reinstalar **B consultante** da ID nuevo, sin relación, autorizaciones ni ubicaciones anteriores, incluso tras backup (D-04/SEG-04).
2. Si **A emisor** desinstala y B sigue instalado, B puede conservar su última posición legítima de A identificada como anterior y fechada; no recibe posiciones nuevas del ID antiguo. Esta conservación está sujeta a la política legal aún PENDIENTE.
3. Sin detección remota verificada, no mostrar que A «desinstaló» ni que una revocación fue «completada en todos los dispositivos». Las copias cloud/D2D/OEM y datos de terceros requieren pruebas específicas de ARQUITECTO/QA.

### F-06 — Solicitud de supresión de una ubicación ya recibida (NO EXISTE flujo aprobado)

- **CONFIRMADO:** B puede eliminar localmente la ubicación al eliminar la relación; A puede impedir **nuevas** consultas, pero revocar/bloquear no borra automáticamente bytes legítimamente recibidos por B.
- **PROPUESTA, NO ACTIVAR:** ante petición de A o de una persona legitimada para ejercer derechos, exponer un canal o instrucción clara para solicitar supresión al poseedor B y explicar el estado **solicitado / confirmado / no verificable** solo si se define un mecanismo real y no se induce a error.
- **NO DEMOSTRADO:** que Whereis pueda forzar borrado remoto en B apagado/offline, ni borrar capturas de pantalla, exportaciones, portapapeles, backups, copias en terceros, registros del sistema u otros datos fuera de Whereis. No prometerlo como funcionalidad actual.
- **PENDIENTE jurídico/material:** sujeto con legitimación, forma de atención, trazabilidad mínima y límites de retención para cada categoría. No implantar un historial de consultas ni un registro personal persistente por deducción.

## 3. Microcopy de transparencia — alternativas propuestas, NO textos aprobados

| Superficie | Texto informativo PROPUESTO (revisión UX/accesibilidad pendiente) | Qué no debe afirmar |
|---|---|---|
| Activar autorización en A | «Este dispositivo podrá solicitar tu ubicación cuando el permiso esté activo y Android lo permita. No se enviarán posiciones automáticamente.» | Que QR/ID autentica por sí solo o que la consulta siempre funcionará |
| Desactivar en A | «Dejará de recibir ubicaciones nuevas cuando el cambio sea efectivo. Podría conservar la última que ya recibió.» | «Se ha borrado tu ubicación de todos los teléfonos» |
| Pantalla de B tras revocación/fallo | «Última ubicación conocida (no actual): DD/MM/AAAA HH:mm:ss» o «Ubicación no disponible» si nunca hubo válida | «Ubicación actual» o hora del fallo como si fuese la captura |
| Confirmar eliminación local en B | «Se eliminarán de este Whereis la relación, última ubicación guardada, alias, foto y color. No garantiza borrar copias externas o en otros dispositivos.» | «Eliminada en todos los dispositivos» |
| Bloquear en A | «Impedir nuevas solicitudes y consultas una vez aplicado el bloqueo. No elimina automáticamente ubicaciones ya recibidas.» | «Borrado remoto completado» |
| Dispositivo de instalación anterior | «Instalación anterior — última ubicación no actual» (solo si invalidez anterior está verificada) | Afirmar desinstalación confirmada por un silencio de red |
| Información para representantes, cuando corresponda | **Pendiente** de determinar legitimación y actor responsable; explicar qué dispositivo comparte, cuál recibe y qué conserva, sin crear privilegios automáticos | «Se ha validado legalmente el consentimiento parental» |

**Avisos estrictamente informativos:** estos textos no agregan notificaciones, botones de revocar a todos, registro visible de consultas ni una pantalla especial de control parental; todo ello requiere aprobación material si cambiara lo confirmado.

## 4. Alternativas MATERIAL/PENDIENTE para el PROPIETARIO (no seleccionar automáticamente)

**R-60a — Retención temporal de la última posición en B:**
- **Opción 1 — Mantener D-10 actual**: una sola última posición legítima sin caducidad *funcional* automática hasta eliminación manual de relación; requiere **contraste jurídico**, sin declarar lícita la retención indefinida.
- **Opción 2 — Introducir criterio de caducidad/borrado**: plazo máximo o aviso configurable para eliminar/ocultar la última posición; **modifica D-10** y podría reducir disponibilidad de dato útil en emergencias. Sin fijar duración ni prometer cumplimiento por sí solo.
- **Salida pendiente:** TECH LEAD eleva alternativas y análisis de conservación al PROPIETARIO con riesgos de menores/caso doméstico para decisión expresa; no hay plazo aprobado nuevo.

**R-60b — Solicitud de supresión iniciada por A/representante:**
- **Opción 1 — No incorporar flujo remoto nuevo en el MVP**: explicar de forma veraz el límite de revocación y el borrado local de B, facilitando gestión externa cuando sea necesario; queda por determinar si las obligaciones aplicables requieren algo adicional.
- **Opción 2 — Proponer un mecanismo verificable de solicitud a B**: B recibe/gestiona petición, borra localmente y comunica resultado cuando sea posible; exige identidad, autorización para formular/recibir la petición, acuse verdadero, protección antiabuso, desconexión, y revisar datos de registro. **No asegura borrado unilateral remoto ni entrega universal.** Requiere nuevo contrato material/arquitectura y revisión legal.
- **Salida pendiente:** definir titulares de derechos, alcance y posibilidad técnica con #61/PR #66; reservar aprobación PROPIETARIO y gates jurídicos, sin activar botón nuevo.

**R-60c — Transparencia/representación para menores:**
- **Opción 1 — Información comprensible y controles actuales por instalación**, sin modo parental dedicado (alineado con SEG-03). Validar si basta en situaciones reales de representación.
- **Opción 2 — Revisar controles adicionales específicos** (representación/información, no acceso oculto), **solo si análisis jurídico y riesgo concreto muestran necesidad**; nueva decisión material de alcance y UX. No asumir edad, patria potestad ni derecho a localizar automáticamente por estar en una familia.

La decisión del PROPIETARIO de **no contratar asesoría jurídica en esta fase** (#41) no establece una exención legal, no elige R-60a/b/c y no cierra SEG-03/04.

## 5. Matriz de estados, evidencia y responsable

| Aspecto | Estado | Evidencia / siguiente actor |
|---|---|---|
| Permiso A→B por interruptor, direccional; revocación impide nuevos fixes cuando es efectiva | **CONFIRMADO** | D-05/#10; SEG-01/#24; **TECH LEAD/ARQUITECTO** deben validar concurrencia/Android |
| B conserva solo última posición legítima, fechada y no actual, incluso tras revocación; sin historial | **CONFIRMADO funcional, limitación legal PENDIENTE** | D-05/#10, D-06/#12, D-10/#20, D-13/#23; **PROPIETARIO** decide cambios materiales de plazo tras análisis |
| Bloqueo oculta marcador pero puede conservar dato; desbloqueo no reautoriza | **CONFIRMADO** | D-09/#19 y D-10/#20; aplicación offline **NO DEMOSTRADA** |
| Eliminación en B borra relación, última posición y personalización **dentro de su instalación** | **CONFIRMADO funcional** | D-10/#20; respaldo/otras copias, restauración tardía y borrado físico **NO DEMOSTRADOS**, #61 |
| Reinstalación crea identidad nueva sin restaurar posiciones/autorizaciones | **CONFIRMADO como contrato, NO DEMOSTRADO en Android** | D-04/#8, SEG-04/#24; #61/PR #66 en revisión |
| Distinguir autorización técnica de legitimación jurídica y representación de menores | **PENDIENTE jurídico** | SEG-03/#24, #41; no se infiere de uso personal en España |
| Ubicación persistente en teléfonos, coste funcional 0 €, terceros solo estudiables | **CONFIRMADO restricción, viabilidad NO DEMOSTRADA** | #41/#52; PR técnicas propuestas no son selección de servicio |
| Texto de ayuda, advertencias ampliadas, canal de supresión y caducidad adicional | **PROPUESTA** | PROP-60; **TECH LEAD** evalúa; cambios materiales → **PROPIETARIO** |
| Supresión efectiva de ubicaciones en B remoto, cachés/backups/terceros y copias fuera de Whereis | **NO DEMOSTRADO / PENDIENTE técnico-jurídico** | #61/PR #66, #41; QA independiente y pruebas reales faltantes |
| Excepción doméstica, edad/representación, roles responsables, terceros y eventual EIPD | **PENDIENTE jurídico, sin dictamen** | #41 y [matriz preliminar TECH LEAD](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6509996398); el usuario no ha contratado asesoría |

## 6. Pruebas negativas propuestas para revisión futura (NO ejecutadas)

| ID | Escenario | Resultado esperado o gate |
|---|---|---|
| F60-CA01 | A revoca B; C mantiene permiso; B aún tiene P0 | A→B no libera posición nueva; C sin afectación; P0 de B solo anterior/fechada |
| F60-CA02 | Revocar en A sin red, B intenta consultar durante la propagación | No prometer revocación remota instantánea; si permiso vigente no verificable, denegar fix nuevo |
| F60-CA03 | A bloquea B y luego desbloquea | Lista negra/ocultación previstas; desbloquear no devuelve permiso ni revela existencia indebidamente |
| F60-CA04 | B elimina A y cancela diálogo | B conserva datos y relación, sin borrar por cancelación |
| F60-CA05 | B confirma «Eliminar A»; llega respuesta vieja Q1 o se intenta restaurar backup | Datos eliminados no reaparecen por reintento, respuesta tardía o copia; verificación técnica requerida |
| F60-CA06 | A reinstala; B continúa instalado y tiene última ubicación | B solo conserva anterior legítima y no actualiza ID viejo; no asumir borrado de B |
| F60-CA07 | B reinstala con copia cloud/D2D/OEM | ID nuevo, sin permisos ni última posición restaurados; pruebas reales pendientes |
| F60-CA08 | Sin posición legítima anterior en B | «Ubicación no disponible», sin marcador/fecha inventados |
| F60-CA09 | A solicita supresión de una posición ya recibida por B offline | No declarar eliminación completada en B ni crear acuse ficticio; canal y derecho material pendientes |
| F60-CA10 | Captura, portapapeles, exportación, notificación, SDK o terceros hipotéticos | No afirmar eliminación de datos fuera de Whereis; inventario y límites según #61/#41 |
| F60-CA11 | Dispositivo menor con supuesto tutor, sin prueba de representación | No conferir privilegio implícito de consulta ni dar por resuelta legitimación; elevar análisis |
| F60-CA12 | Consulta Q1 vence y respuesta llega tarde | Aplicar opción A del PROPIETARIO [#12](https://github.com/mundoinformaticacanaria/whereis/issues/12#issuecomment-6508029995): descartar Q1 sin resucitar ubicación ni éxito |

## 7. Handoff y límites

1. **FUNCIONAL entrega esta PROPUESTA a TECH LEAD** en #60 para conciliar con #41, #24 y el estudio independiente #61/PR #66 tras corrección y QA; no duplicar decisiones ni suponer que #66 está validada.
2. **TECH LEAD** identifica preguntas MATERIAL que requieren PROPIETARIO: R-60a conservación/caducidad, R-60b posible solicitud de supresión, R-60c transparencia/representación cuando el análisis jurídico determine su necesidad. Revisar coherencia con seguridad, Android, canales externos estudiados y coste 0 €.
3. **PROPIETARIO** conserva aprobación de cambios materiales y aceptación de riesgos dentro del marco aplicable; el estudio gratuito no sustituye dictamen jurídico ni permite obviar derechos o controles exigibles.
4. **PENDIENTES**: revisión legal SEG-03/04, prueba de respaldo/retención/borrado en Android y terceros, revisión QA del documento técnico #61, baselines globales, proveedores y programación. No afirmar que tests de este documento fueron ejecutados.

**No se modifica `main` en esta PR de FUNCIONAL; ningún código, gastos, servicios, claves, cuentas, servidor/CRM, timers Linux o automatización ChatGPT.**
