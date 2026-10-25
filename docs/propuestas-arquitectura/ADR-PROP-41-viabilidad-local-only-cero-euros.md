# ADR-PROP-41 — Viabilidad de WHEREIS sin nube, con datos locales y coste adicional 0 €

- **Estado:** \`PROPUESTA / PENDIENTE DE DECISIÓN MATERIAL\`. **No** es baseline ni garantía de viabilidad.
- **Clasificación:** MATERIAL — arquitectura, seguridad, permisos Android, privacidad y servicios.
- **Encargo:** [issue #41, handoff de TECH LEAD del 25/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6396002383).
- **Trazabilidad:** [#8 / PR #34](https://github.com/mundoinformaticacanaria/whereis/pull/34), [#22 / PR #35](https://github.com/mundoinformaticacanaria/whereis/pull/35), [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24), [#19 (D-09)](https://github.com/mundoinformaticacanaria/whereis/issues/19), [#20 (D-10)](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37).
- **Evidencia:** análisis documental de contratos de GitHub y fuentes Android/IETF/OSMF/AEPD citadas al final; **ningún experimento ejecutado**, sin mediciones reales de compatibilidad, coste ni latencia.
- **Autoridad:** decisión del PROPIETARIO en #41 CONFIRMADA; estudio de ARQUITECTO. La enmienda G-02 sobre ejecutor ChatGPT está aprobada por PROPIETARIO en #37, pero su integración documental en \`main\` sigue pendiente en PR #43/QA. No confundir aprobación humana de la función con integración de gobernanza.

## 1. Contratos materiales CONFIRMADOS

1. **Uso personal/familiar en España**, sin objetivo comercial, y sin crear por defecto un modo parental distinto. Los controles parentales Android, por sí solos, no constituyen pronunciamiento legal sobre menores [#41].
2. **Almacenamiento persistente exclusivamente dentro de cada instalación participante**: identificador/credenciales y relaciones/autorizaciones propios; en B únicamente la **última ubicación legítimamente obtenida por cada A**, sin historial [D-10]. La nueva instalación no restaura identificadores, autorizaciones ni ubicaciones antiguas [D-04/SEG-04].
3. **Sin backend, hosting o almacenamiento en nube y sin contratar servicios para que WHEREIS funcione**. Que un proveedor ofrezca modalidad gratuita **no implica autorización** de usarlo. No se ha autorizado ningún proveedor de push, STUN/TURN, tiles, geocodificación ni intermediación.
4. **Coste adicional de funcionamiento obligatorio: 0 €**, sin cuotas, suscripciones, proveedores de pago, contratación ni servicios propios sobre un servidor compartido. La conexión de datos o Wi-Fi ya disponible en cada teléfono es un **supuesto condicionado**: no se ha confirmado que el consumo de datos móviles esté incluido sin cargos y no debe confundirse «sin contratar nuevos servicios» con red universal gratuita.
5. Continúan **SEG-01/02**: identidad auténtica de instalación, permiso direccional vigente, revocación fail-closed, anti-enumeración opción B, no acceso con mero ID/QR. Requisitos de menores, retención y borrado no se descartan por uso doméstico.
6. **D-02/D-12:** consulta nueva puntual iniciada manualmente, incluso con A no visible **cuando Android lo permita**; no polling continuo; si A o B pierden conexión no ejecutar automáticamente al volver; respuesta fallida conserva únicamente dato anterior fechado cuando procede.
7. **D-09:** bandejas de solicitudes, recepción/acuse real acreditable, 24 h desde el envío y reintentos idempotentes de solicitudes de vinculación (distintos de reintentos de consulta de ubicación). Aceptar solicitud no activa autorización.

## 2. Hallazgo estructural: almacenamiento local ≠ conectividad remota

Para consultar un teléfono A lejos de B hacen falta, como mínimo, **un camino de red entre ambos, una forma de conocer un destino alcanzable, recepción/ejecución del evento en A y verificación de identidad y permiso**. Que ambos guarden sus datos únicamente en local no proporciona por sí solo descubrimiento, rendezvous, NAT traversal, canal de avisos ni disponibilidad en segundo plano.

La comunicación directa sobre Internet **es posible en topologías favorables**, no imposible por principio: por ejemplo, IPv6 global verdaderamente accesible y permitido, o IPv4 con entrada y puertos configurados. Pero los dos teléfonos pueden quedar tras NAT/CGNAT/firewalls de operador, con direcciones variables, redes móviles suspendidas y sin posibilidad de aceptar conexiones entrantes. El RFC 8445 sobre ICE depende de un **mecanismo de señalización previo** y describe STUN/TURN, cuyo uso implicaría infraestructura de terceros hoy no autorizada; STUN no garantiza superar todos los NAT y TURN es relay. Compartir un QR con una clave o ID **no crea** un camino a través de CGNAT.

**Conclusión documental:** bajo el conjunto estricto de restricciones **NO SE HA DEMOSTRADO** una arquitectura que garantice consultas remotas generales con A no visible, 0 € y sin ninguna infraestructura de intermediación. Un alcance de cercanía/LAN sí tiene vías técnicas conocidas, sujeto a seguridad/permisos. No convertir una hipótesis favorable (IPv6 libre, NAT abierto, dispositivo despierto) en garantía de producto.

## 3. Matriz de alternativas de transporte

| Alternativa | Alcance/estado de conexión | Descubrimiento/recepción | Dependencia externa, coste y licencia | Seguridad/UX; veredicto |
|---|---|---|---|---|
| **LAN local**, sockets o NSD | Dispositivos en misma red; simultáneamente accesibles | Descubrimiento local NSD o emparejamiento, proceso A receptivo | Sin backend de WHEREIS; usa router/red ya disponibles. Coste incremental contractual **condicionado**, no acreditado universalmente | **CONDICIONAL** para dispositivos cercanos. Puede fallar con aislamiento Wi-Fi, app suspendida y permisos |
| **Wi-Fi Direct**, quizá BLE para emparejamiento | Proximidad física, no familiares en otras ciudades | Descubrimiento y negociación de pares Android, permisos de dispositivos cercanos | API Android; no requiere Internet, pero requiere radios compatibles y permisos; evaluar energía | **CONDICIONAL** cercano, **NO CUMPLE** consulta remota a distancia |
| **Internet P2P directo IPv6 / IPv4 con entrada** | Distancia arbitraria **solo si** redes son alcanzables y A responde | Dirección/puerto conocido y vigente, intercambiado por canal previo de confianza; cambios IP y movilidad difíciles sin rendezvous | No hosting WHEREIS; tráfico por operadores existentes, posibles cargos. Sin garantía de DNS/descubrimiento, NAT, firewall o proceso vivo | **CONDICIONAL / SIN COBERTURA GENERAL**. Necesita pruebas por operadores, IPv6, CGNAT, batería, Android |
| **ICE / STUN sin TURN**, con señalización previa | Puede ayudar a atravesar algunos NAT si ambos están en red y colaboran | **Requiere señalización inicial externa o canal alternativo**; STUN requiere servicio | Servicios/STUN ajenos **NO AUTORIZADOS**; servicio gratuito no equivale a permitido; STUN no resuelve todo | **NO ADOPTABLE AHORA**; incluso autorizado seguiría sin garantía general |
| **TURN/relay, rendezvous, push (ej. FCM) o backend** | Proporciona intermediación o aviso remoto útil, con límites Android | Infraestructura/terceros aportan señalización, mensajes o relay | **EXCLUIDO por decisión vigente** hasta nueva autorización material, también si gratis; revisar datos enviados y condiciones | Alternativa de estudio, **NO AUTORIZADA** ni prueba de éxito universal |
| **Servidor «propio» o doméstico/compartido** | Puede intermediar si está disponible y accesible | DNS/puertos/red pública, seguridad y mantenimiento | Cambia infraestructura/operación; **NO AUTORIZADO** para WHEREIS, especialmente servidor multiproyecto | **EXCLUIDO**; no inferir coste 0 € por tener un ordenador |
| **Reducir objetivo a presencia cercana/LAN** | Sólo dentro de alcance local, bajo demanda | Emparejamiento cercano y canal directo | Posible sin nube ni coste añadido de proveedor; Android/permisos pendientes | **VIABLE EN PRINCIPIO**, pero **cambio MATERIAL** del uso remoto familiar previsto: requiere PROPIETARIO |

La ausencia de servicios cloud **no prohíbe la red IP en sí**; cualquier alternativa requiere definir qué dispositivos y operadores aportan conectividad, qué metadatos se exponen a terceros y si el usuario acepta esa dependencia. No se ha seleccionado ninguna opción.

## 4. Contratos de identidad, solicitudes y ubicación SIN autoridad central

### 4.1. Autoridad localizada en el teléfono A

**PROPUESTA CONDICIONAL** para un canal directo *ya existente*:

- **A es autoridad de las autorizaciones A→B**: registra en almacenamiento propio una revisión monótona por relación/instalación, estado del interruptor, bloqueos y decisiones. B registra solo su lista conocida/recibida y su última ubicación legítima. No hay directorio global de IDs ni copia de permisos/ubicaciones en nube.
- Instancias con un **ID público** y credencial de prueba de posesión **local no restaurable** (Android Keystore como candidato a verificar). Emparejamiento QR/manual no autentica por sí solo la identidad, ni revela datos sin concesión; desafío fresco y enlace a clave pública por una ceremonia de vinculación confiable siguen PENDIENTES de diseño. La reinstalación elimina posibilidad de operar como instalación antigua, **sin garantizar que B conozca al instante una desinstalación remota**.
- En una consulta puntual, **B firma/autentica la solicitud**, A verifica solicitud, identidad B, ventana de validez y permiso local en A. El **gate de liberación** es decisión final en A, ordenada de forma verificable respecto a un bloqueo/revocación local. Si A no está alcanzable, **no se puede afirmar** permiso vigente ni entregar posición nueva: SEG-01 se satisface mediante fallo cerrado, no mediante caché remota.
- Si B recibe un resultado antiguo después de una revocación **ya aplicada en A** pero paquete emitido previamente, B puede desconocer aún la revisión sin conectividad: no prometer retiro de paquetes ya transmitidos. Vincular respuesta a requestID/revisión y descartar lo caducado, reintentado, bloqueado localmente o no verificable. **No afirmar garantía distribuida absoluta** con redes arbitrarias.
- Sin servidor no hay detector remoto universal de la existencia de una instalación por ID. La **opción B** exige no revelar existencia a solicitantes sin derecho mediante códigos, cuerpo, tiempo o metadatos. La respuesta externa uniforme, minimización y controles antiabuso son diseño propuesto; una conexión directa a un endpoint identificado puede constituir un **canal lateral de existencia**. Si el contrato exige un verificador público de ID accesible desde cualquier red, será necesario otro alcance/protocolo o una decisión de PROPIETARIO.

### 4.2. D-09: bandeja, caducidad y acuse

- **Envío:** B crea solicitud local con \`requestId\` y hora de envío fijada de forma fiable; la regla de 24 h no se renueva en reintentos. Sin backend, los relojes pueden diferir: hora confiable/anti-retroceso y sincronización son PENDIENTES.
- **Recepción:** sólo mostrar «recibida» cuando A ha guardado durablemente la solicitud en **su almacenamiento local** y devuelve un **acuse autenticado** ligado a \`requestId\`, identidades y revisión. Éxito de socket, notificación o devolución de API no equivale a acuse. **Si A está offline, ninguna «recibida» demostrable**. Si A apaga la app y Android no recibe/procesa, idem.
- **Reintento de vinculación**: B puede reentregar una solicitud aún vigente cuando el canal sea accesible, conservando el mismo \`requestId\` y caducidad original. A deduplica; sin prueba de entrega, B indica «entrega no confirmada». No inventar posibilidad de distribución automática fiable a un A sin camino de red.
- **Aceptar** añade B a conocidos en A pero deja permiso de ubicación inactivo hasta el interruptor expreso. Rechazo, bloqueo o expiración se aplican por revisión, de manera que respuestas tardías no crean relaciones ni autorizaciones.

### 4.3. D-12: ubicación puntual sin ejecución en reconexión

- **Solicitud de posición ≠ solicitud de vinculación**. La consulta sólo existe como **intento manual acotado y en vivo** de B, sin cola persistente en transportes ni A para capturar al reconectar. B no mantiene operación pendiente tras timeout/fallo.
- Un \`expiresAt\` o un push demorado **NO** bastan: si A estaba desconectado y reaparece antes de TTL, un mensaje retenido podría producir captura prohibida. **PROPUESTA condicional:** un enlace directo autenticado y aceptación por A durante la **sesión original y en la misma época de conectividad**; al perder conexión, cerrar operación e invalidar su identificador. En una nueva sesión, rechazar la solicitud anterior aun no expirada. Esto depende de que la plataforma pueda **observar inequívocamente la sesión**, no está demostrado en Android.
- La captura debe ser nueva y legítima según permisos/ubicación del sistema, con timestamp del sensor (no del envío). A revalida autorización vigente al **liberar**; B acepta sólo respuesta de solicitud vigente, no reinterpretando caché como posición nueva.
- **Si A no puede ejecutar por estar en segundo plano/force-stop**, fallar sin cola. Android API 26+, permisos de ubicación background API 29+ y foreground services API 31+/34+ restringen captura; recepción de un evento no equivale a permiso para ejecutar. Sin sistema push autorizado y sin socket mantenible, tampoco hay mecanismo universal para despertar A.
- **Bloqueo/retención:** tras bloqueo el marcador anterior se oculta, conservando sólo cuando D-10 lo permite; tras eliminación local se borra dato/alias/estado de B y se impide resurrección por mensajes tardíos. Si A no puede recibir el aviso de eliminación, no se afirma revocación remota inmediata.

**Resultado de la prueba conceptual:** las garantías de **seguridad negativa** (no dar ubicación nueva al fallar la verificación) se pueden especificar con autoridad local en A. La **disponibilidad positiva** de consultas remotas a un A no visible y desconectado/no alcanzable, y la prueba global de existencia/acuse de ID, **no** pueden garantizarse con el canal ausente. Es una incompatibilidad de alcance/operación que corresponde elevar, no resolver reduciendo autenticación.

## 5. Diagrama de flujo y residencia de datos (propuesto)

~~~text
Teléfono B (consultante)                    Red ya existente                  Teléfono A (emisor)
────────────────────────                    ─────────────────                  ──────────────────
ID/claves propios (sin backup)                IP/puertos, metadatos              ID/claves propios (sin backup)
Lista de conocidos y solicitudes             visibles a operador               Inbox solicitudes local
Última posición legítima por A               NAT/firewall/CGNAT                 Autoridad LOCAL de A→B
Alias/foto/color locales                     sin relay autorizado               Revisión, bloqueos, revocación
                                             ⇄ canal directo condicional ⇄
B pide consulta manual   ──────────────────  identidad, requestID  ──────────► A comprueba y captura (si permitido)
B recibe posición ◄─────────────────────────  cifra/autoriza/TTL  ◄────────── A hace gate final antes de liberar
B sustituye última posición legítima
B sin respuesta = dato anterior fechado, nunca actualidad
~~~

**Sin infraestructura de WHEREIS:** no hay almacenamiento permanente de posiciones ni permisos de aplicación fuera de esos teléfonos. En cualquier conexión IP, el **operador de red** maneja metadatos técnicos; no asegurar «cero terceros» ni «cero tráfico externo» sin modo completamente offline local. En alternativas descartadas, una pasarela/push/STUN/TURN vería al menos metadatos/IP, y un proveedor de mapas/geocodificación podría recibir zonas/coordenadas: **ninguno está autorizado**.

| Categoría de dato | Quién lo conserva (propuesta local) | Retención técnica / supresión | Cautela pendiente |
|---|---|---|---|
| ID y prueba de instalación | Cada teléfono, material privado fuera de backup | Hasta fin/invalidación de esa instalación; reinstalación => identidad nueva | Keystore/backup D2D/OEM y gestión de pérdidas |
| Solicitud D-09 y acuse | B enviadas, A recibidas; sin servidor | Caduca a 24 h de envío; limpieza local y deduplicación | Reloj fiable, consentimientos, criterio legal |
| Relación/autorización/bloqueo | Autoridad A; representación local B para UX | Revocación local inmediata; propagación remota NO asegurada | Borrado, tombstones, límites legales |
| Ubicación puntual en A | Sólo memoria transitoria necesaria para respuesta | No persistir historial en A por defecto; borrar tras intento | Ficha de ubicación, temporales, logs |
| Última ubicación/alias/foto de A en B | Sólo B instalado, máximo una por A | Sobrescribir con nuevo éxito; eliminación manual borra; reinstalación B no restaura | Duración máxima legal, visibilidad tras bloqueo |
| Claves/errores/telemetría | Cada teléfono, mínima y sin coordenadas en logs | Eliminación acotada pendiente de política | Datos sensibles/menores y copias |
| Teselas/geocodificación local | En el paquete o archivo autorizado de cada teléfono | Datos de cartografía sin coordenadas privadas remotas | Atribución, ODbL, tamaño, actualizaciones |

**Excepción doméstica RGPD:** la AEPD indica que determinadas actividades estrictamente personales/domésticas de particulares quedan excluidas del RGPD, **no** que cualquier operador, proveedor o acceso a terceros quede excluido. Cuando el tratamiento se base en consentimiento, la AEPD describe reglas especiales para menores de 14 años en España. Se requiere revisión jurídica contextual de quién trata los datos, de los representantes y de derechos de los menores; no afirmar dictamen ni exención por el mero hecho de no detectar edad. Fuente AEPD citada al final.

## 6. Cartografía, direcciones y coste contractual 0 €

Separar expresamente **renderizador**, **datos** y **servicios**:

| Elemento | Alternativa local sin proveedor contratado | Límite no resuelto |
|---|---|---|
| Renderizado de mapa | Biblioteca de software libre integrada, **p. ej. MapLibre**, como candidato, no seleccionada | SDK no equivale a fuente de teselas ni permiso de uso de un servidor |
| Datos callejeros | Extractos/datasets con licencias compatibles, empaquetados para uso offline y mostrados con atribución correcta | Tamaño APK/almacenamiento, actualización, preparación lícita, ODbL y política de redistribución; validar coste total y licencias |
| Teselas OSMF públicas | **No adoptar por defecto**. Servicios ajenos no autorizados; la OSMF prohíbe usar sus tiles públicos para descargas masivas o paquetes offline y no garantiza SLA | Usarlos directamente contradiría el propósito de autonomía/offline y requeriría decisión material nueva |
| Geocodificación inversa | Opcional si es técnicamente viable con índice/datos geográficos locales y licencia; si no, mostrar sólo coordenadas/precisión según D-13 y elevar cambio MATERIAL si la UX aprobada se degrada | Dataset local de direcciones, almacenamiento, exactitud, cobertura, licencias; **NO** enviar coordenadas de menores a Nominatim público por defecto |
| Geocodificación pública Nominatim | No autorizada por defecto, aunque parezca gratuita | Política pública de uso (máx. 1 req/s total de aplicación, identificación, caché, privacidad, cambio de proveedor), incompatibilidad con supuestos de uso masivo/offline |

Un mapa puramente offline **es posible en principio** sin abono de proveedor si se obtiene y distribuye un dataset legalmente utilizable. **No hay demostración** de que los datos callejeros completos, direcciones precisas, actualizaciones y necesidades de almacenamiento de WHEREIS se satisfagan sin costes indirectos. No utilizar \`tile.openstreetmap.org\` como origen de precargas.

## 7. Matriz de validación y pruebas negativas — TODAS PENDIENTES

| Prueba, sin datos reales | Evidencia/resultado mínimo | Situación |
|---|---|---|
| A/B a distancia tras CGNAT IPv4 distinto | Registrar conectividad entrante realmente posible, sin relay/STUN/servicios no autorizados; fallo seguro | NO EJECUTADA |
| IPv6 global, reglas firewall distintas, IP cambia en movilidad | Accesibilidad y descubrimiento válidos; documentar redes y variabilidad | NO EJECUTADA |
| LAN con client isolation, Wi-Fi Direct sin permisos y Bluetooth fuera de alcance | No falsas afirmaciones de disponibilidad | NO EJECUTADA |
| A offline; B consulta; A reconecta **antes** del TTL | Ninguna captura/entrega diferida del intento original | NO EJECUTADA |
| A offline, solicitud D-09 por B; reintento al conectar | «recibida» sólo con acuse firmado de almacenamiento local de A; máximo una pendiente, 24 h originales | NO EJECUTADA |
| A en segundo plano, Doze/force-stop/ubicación sólo while-in-use, distintos Android/OEM | Respetar restricciones; sin captura si no permitida, sin despertar garantizado | NO EJECUTADA |
| Copia de ID/QR, repetición, ID inexistente/no divulgable | No consultar sin autenticación/permisos; no canal de enumeración observable | NO EJECUTADA |
| Revocación local A entre captura y liberación; B reinicia/reintenta | No liberar después de revocación aplicada; distinguir paquete ya emitido | NO EJECUTADA |
| Restauración cloud/D2D para A o B, backup parcial | Nueva identidad, sin ubicación/autorizaciones antiguas | NO EJECUTADA |
| B elimina última posición mientras llega respuesta tardía | No reaparece; ocultación correcta tras bloqueo; timestamp antiguo preservado en error | NO EJECUTADA |
| Modo sin Internet externo: mapa offline e índice postal local | Atribución/licencias, tamaño y cobertura medidos en dispositivo | NO EJECUTADA |
| Instrumentación de coste contractual/operativo | Inventario de servicios utilizados, licencias y condiciones sin contratos ni gasto; aclarar tráfico de datos del usuario | NO EJECUTADA |

**No existe todavía código Android de producto aprobado, banco hardware, test ejecutado, CI verificado ni prueba de prestaciones.** No fabricar porcentaje de viabilidad ni coste observado.

## 8. Decisiones concretas a elevar al PROPIETARIO (sin aprobar por el ARQUITECTO)

- **Decisión L-01 — Alcance geográfico y disponibilidad:** ¿mantener las restricciones **local-only/0 €**, aceptando consultas garantizables *sólo cuando exista conectividad directa demostrada* (p. ej., LAN/proximidad/IPv6 alcanzable) y declarando fallos frecuentes a distancia, o conservar como requisito esencial consulta remota familiar general? La primera opción puede reducir materialmente D-02/D-12; **necesita decisión expresa**.
- **Decisión L-02 — Infraestructura de señalización:** si la consulta remota general es imprescindible, ¿autorizar estudio posterior de algún canal ajeno de señalización/push/relay **sin almacenamiento persistente de ubicaciones**, sujeto a privacidad, coste contractual 0 € y permisos? Esto **relajaría la exclusión absoluta de servicios externos**; no se autoriza por proponerlo. Si la respuesta es no, admitir la limitación de alcance.
- **Decisión L-03 — Descubrimiento y verificabilidad de IDs:** ¿se acepta vinculación presencial/QR con intercambio de claves/endpoints cuando no exista directorio global, y qué se espera del alta de un ID manual no conocido? SEG-02 opción B impide devolver oráculos de existencia.
- **Decisión L-04 — Mapa y direcciones offline:** definir nivel mínimo de cobertura geográfica, periodicidad de actualización y si la dirección postal puede no estar disponible sin servicio externo; cualquier reducción respecto a D-13 requiere autoridad del PROPIETARIO con FUNCIONAL.
- **Decisión L-05 — Uso doméstico, menores y retención:** acordar con revisión jurídica futura el alcance de excepción doméstica, tratamiento por terceros (si alguno), límites de conservación y controles de transparencia; no deducir legalidad del uso familiar ni de ajustes Android.

**Propuesta de secuencia:** TECH LEAD contrasta esta ADR con #8/#22 y baselines, solicita al PROPIETARIO sólo las decisiones materiales esenciales de L-01/L-02 y, después de ellas, define qué pruebas/prototipos acotados necesitarían nueva autorización. No hay autorización para resolver por implementación algo que es una incompatibilidad de requisitos.

## 9. Fuentes públicas consultadas para viabilidad y límites (no sustituyen GitHub)

- Android: [Conexión de dispositivos y NSD/P2P](https://developer.android.com/develop/connectivity/wifi) y [Wi-Fi Direct](https://developer.android.com/develop/connectivity/wifi/wifi-direct), proximidad y permisos.
- Android: [Restricciones al iniciar foreground services desde background](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start) y [ubicación en segundo plano](https://developer.android.com/develop/sensors-and-location/location/background).
- IETF [RFC 8445 — ICE/STUN/TURN](https://www.rfc-editor.org/rfc/rfc8445.html): NAT traversal, dependencia de señalización y relays.
- OSM Foundation [política de teselas públicas](https://operations.osmfoundation.org/policies/tiles/) y [política Nominatim](https://operations.osmfoundation.org/policies/nominatim/): sin paquetes offline desde sus servidores públicos y límites de geocodificación.
- AEPD [tratamiento doméstico de particulares](https://www.aepd.es/preguntas-frecuentes/0-conceptos-basicos/FAQ-0012-sobre-datos-personales-tratados-por-un-particular-en-actividades-privadas), [menores](https://www.aepd.es/preguntas-frecuentes/10-menores-y-educacion/FAQ-1002-se-puede-recabar-y-tratar-datos-personales-de-menores), sin dictamen jurídico del proyecto.

## 10. Handoff propuesto — revisión técnica y decisión material

**ARQUITECTO:** entrega la matriz y riesgo demostrable de incompatibilidad. **TECH LEAD:** siguiente responsable de revisar esta PR sobre su head exacto, coordinar reconciliación de PR #34/#35 y elevar decisiones L-01/L-02 al PROPIETARIO. **PROPIETARIO:** único facultado para aceptar cambios de alcance, proveedores/servicios, privacidad o costes. **FUNCIONAL:** ajusta D-02/D-09/D-12/D-13 sólo tras decisión humana si se requieren cambios. **QA:** independiente del autor para entregas que lo requieran. **G-02/#37**: la enmienda documental está en PR #43 y no se presume integrada.

No se elige tecnología/proveedor, ni se modifica \`docs/arquitectura.md\` como baseline. No se abre exposición de red, no se toca servidor/CRM, no se contrata nada, no se ejecuta producto ni se activa timer Linux.
