# ADR-PROP-22 — Consultas puntuales cuando la app emisora no está visible

- **Estado:** `PROPUESTA / NO APROBADA`.
- **Clasificación:** `MATERIAL` — permisos Android, privacidad, comunicación, concurrencia y seguridad.
- **Issue:** [#22 — D-12](https://github.com/mundoinformaticacanaria/whereis/issues/22).
- **Contrato relacionado: [#2 — D-02](https://github.com/mundoinformaticacanaria/whereis/issues/2), [#8 — D-04](https://github.com/mundoinformaticacanaria/whereis/issues/8), [#19 — D-09](https://github.com/mundoinformaticacanaria/whereis/issues/19), [#20 — D-10](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#24 — SEG-01/02/03/05/06/07](https://github.com/mundoinformaticacanaria/whereis/issues/24) y [PR #49](https://github.com/mundoinformaticacanaria/whereis/pull/49) (D-09–D-13/SEG integrada documentalmente).
- **Alcance:** estudio y alternativas; **no** selecciona proveedor, SDK, backend, push, mapas, infraestructura o versiones Android objetivo; no hay pruebas de dispositivo ni implementación. **L-02 CONFIRMADA en [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6399627418), ampliada por L-02b/c/d [en #41](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6410130695):** consulta familiar remota esencial; solo se autoriza **estudiar** señalización externa a coste incremental 0 €, con ubicación y relaciones persistentes en teléfonos. No se autoriza adoptar ni usar proveedor, API, servicio, cuenta o infraestructura.
- **Autoridad / transición:** [#37, opción B CONFIRMADA](https://github.com/mundoinformaticacanaria/whereis/issues/37#issuecomment-6395244289) asigna `ARQUITECTO` al chat independiente de ChatGPT y su enmienda G-02 **ya está integrada en `main`** por PR #43. La propuesta sigue pendiente de revisión y QA independiente, sin autoaprobación.

## 1. Comportamiento CONFIRMADO que se debe preservar

1. B puede intentar consultar puntualmente a A autorizado aunque Whereis no sea visible en A, **solo cuando Android lo permita**. No seguimiento continuo ni localizaciones automáticas recurrentes. No prometer disponibilidad/latencia universal (D-02).
2. Una petición individual mantiene estado propio. B no inicia dos consultas de un mismo A simultáneamente; sí puede consultar C a la vez. «Actualizar todos» reutiliza las activas, agrega las faltantes y resume éxitos/errores (D-12).
3. B sin Internet: controles de refresco deshabilitados, aviso persistente y **nada encolado para reconectar**. A sin Internet o sin ubicación/permisos: sin éxito ficticio, reintento solo manual. No divulgar a B la razón sensible de ubicación Android desactivada.
4. Mostrar última posición legítima únicamente como **anterior/no actual**, con fecha real y aviso; sin historial automático (D-06/D-10).
5. SEG-01/02: antes de liberar una posición nueva acreditar identidad auténtica **y** autorización direccional activa y verificable. Un ID/QR, acuse push, caché o permiso previo no basta.
6. La alerta por servicio Android apagado en A, cuando sea posible, no debe superar **una por solicitante y 24h**, con reinicio condicionado al ciclo de activación/desactivación realmente observado. No avisar por consultas ordinarias exitosas (D-12).
7. **Opción B D-09/SEG-02 CONFIRMADA** por PROPIETARIO en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24#issuecomment-6371711122): consulta de existencia de ID por actor no autenticado/sin derecho => respuesta indistinguible para ID inexistente o no divulgable. El resto de UX D-09, incluido plazo/reintentos legítimos, no se altera por esta decisión. SEG-02 técnico permanece PENDIENTE.

## 2. Hechos y restricciones de plataforma (documentales, NO probados en hardware)

| Alcance | Restricción / implicación |
|---|---|
| Android 8+ (API 26) | Restricción a obtención de ubicaciones en segundo plano; no hay captura fresca ni latencia garantizada |
| Android 10+ (API 29) | Distinguir permiso foreground/background; valorar `ACCESS_BACKGROUND_LOCATION` para captura sin actividad visible |
| Android 11+ (API 30) | Concesión de background escalonada mediante Ajustes y UX de transparencia; no conceder silenciosamente |
| Android 12+ (API 31) | Restricción al arranque de foreground service desde background, salvo excepciones legítimas |
| Android 13+ (API 33) | Avisos ordinarios sujetos a `POST_NOTIFICATIONS`, que el usuario puede denegar |
| Android 14+ (API 34) | Tipos de FGS, `FOREGROUND_SERVICE_LOCATION` y límites de permisos «while-in-use»: pueden causar `SecurityException`; push no equivale a excepción universal |
| OEM/Doze/force-stop | El aviso puede llegar tarde, no despertar o no permitir capturar; cierre forzado puede impedir la ejecución hasta intervención del usuario |

**No asumir:** `WorkManager`, FCM de prioridad alta, una notificación o una excepción FGS no dan automáticamente acceso a ubicación ni garantizan ejecución, especialmente con permisos insuficientes, app forzada a detenerse o políticas del fabricante. El uso de prioridad alta silenciosa para capturar ubicación debe contrastarse con las condiciones de distribución y comportamiento del proveedor: no se propone como puerta trasera para eludir Android.

## 3. Opciones de transporte/despertar

| Opción | Ventajas | Limitaciones/coste/privacidad | Evaluación |
|---|---|---|---|
| Canal directo de B a A **cuando ya exista conectividad efectiva**, aceptación en vivo de la misma operación manual | No necesita almacenamiento ni relay de datos WHEREIS; permite prueba de sesión original y evitar cola | LAN/proximidad o Internet directamente alcanzable; descubrimiento, NAT/CGNAT/IPv6, background Android y permisos sin garantías generales | **PROPUESTA condicional bajo #41**, no cobertura remota general |
| Socket persistente / canal P2P mientras la app no es visible | Evita alguna intermediación si es alcanzable | Batería, NAT/CGNAT, suspensión Android, direcciones variables, descubrimiento; sin mecanismo universal de despertar | **NO DEMOSTRADO** a distancia; solo estudio en redes favorables |
| Push, broker/rendezvous, STUN/TURN o relay ajenos | Puede dar señalización/despertar o tránsito | Terceros, términos, IP/metadatos, disponibilidad y eventuales costes; L-02b/c/d **autoriza estudiar**, no usar ni adoptar | **ESTUDIO AUTORIZADO; ADOPCIÓN PENDIENTE** de decisión material |
| Polling periódico/alarma para buscar peticiones | Aparentemente sencillo | Respuesta tardía, batería y ejecución automática recurrente incompatible con el objetivo de consulta puntual | **No recomendado para el MVP** |
| Solo consulta con A visible | Riesgo técnico menor | Dejaría sin cubrir los casos admitidos por D-02 con A no visible | Degradación por impedimento Android, no cambio unilateral de requisito |

El PROPIETARIO **ha autorizado solo el estudio documental**, no el uso ni la adopción, de intermediación externa bajo L-02b/c/d, incluso si se ofrece gratis (FCM, STUN/TURN, broker/relay). Un canal directo ya alcanzable no requiere contratación propia, pero solo es viable en redes favorables y no demuestra recepción con A no visible. Las pruebas de NAT/CGNAT, privacidad, batería y coste real son PENDIENTES. Véanse PR #45/#50/#55.

## 4. Límites y contratos propuestos

### 4.1. Cliente consultante B

- `RequestCoordinator`: por cada destino autorizado A, a lo sumo un `requestId` activo para **esa instalación B**; permite A y C concurrentes. «Actualizar todos» agrega solo destinos elegibles sin duplicar. No crea trabajos al iniciar app o reconectar.
- `LocationRequest`: `requestId` impredecible y único; `requesterInstallationId`, `targetInstallationId`, `createdAt`, `expiresAt`, `authorizationRevision` de referencia y `purpose=manual`. El reloj de expiración debe estar ligado a fuente fiable y revisarse; umbral final = decisión TECH LEAD.
- `TerminalResult`: un resultado definitivo `fresh-success`, `failure` o `timeout` por `requestId`. Las respuestas repetidas/tardías de intentos cerrados se ignoran; no hay reintento automático.
- Si B está offline, no se emite solicitud ni queda esperando una que se dispare sola al recuperar conectividad.
- **Si A está offline en el intento original:** resultado terminal de fallo genérico, **sin solicitud de captura ni wake pendiente** de ejecución. El mero TTL de un mensaje no da este comportamiento: si A vuelve antes del TTL, una push encolada podría despertar y capturar tarde; eso contradiría D-12. El canal propuesto debe garantizar que la captura solo se acepta como continuación de **la misma época de conectividad/aceptación en vivo iniciada durante el intento original**, sin reintento automático. Si no puede acreditar esta semántica, no se afirma cumplimiento y se eleva una incompatibilidad MATERIAL a PROPIETARIO vía TECH LEAD.

### 4.2. Transporte

- `WakeHint`: **hipótesis de alternativa externa autorizada exclusivamente para estudio bajo L-02b/c/d, NO para uso**; sin proveedor push adoptado, solo puede existir un evento de la propia comunicación directa mientras A está disponible. Un aviso/paquete retenido NO equivale a petición viva. No crear cola de capturas en A, transporte ni al reconectar; la llegada posterior nunca desencadena captura basándose solo en `expiresAt`.
- **`LiveAcceptance` (PROPUESTA condicionada):** asociar cada intento a `connectivityEpoch` autenticada de A observada **en el momento de iniciar la consulta manual** y a aceptación explícita de A mientras siga esa misma época. El verificador comprueba época, `requestId`, vigencia y no haber cierre terminal. Si A estaba desconectado, el intento concluye como fallo y no podrá aceptarse en una época creada tras recuperar conexión, aunque todavía queden minutos de TTL. Si no se dispone de prueba fiable de conectividad/época en vivo en plataformas Android objetivo, el mecanismo NO satisface esta parte de D-12 sin degradación aprobada. Los avisos pueden informar/activar un proceso permitido, pero **no** preservar una petición para consumirla tras reconexión.
- **`ExistenceDisclosure` (opción B CONFIRMADA):** las verificaciones de ID sin autorización de existencia no distinguen inexistente/no divulgable por contenido, error HTTP, longitud, cabeceras, tiempo o metadatos de transporte observables; ensayar diferencias estadísticas, con defensas antiabuso. No filtrar existencia por un acuse diferenciado de `LiveAcceptance`. D-09 está integrada documentalmente mediante PR #49; su verificación técnica y SEG-02 siguen PENDIENTES.
- `RequestVerifier`: **autoridad local en A, no backend**: prueba de posesión de identidad de B y verificación actual de relación A→B y su revisión mediante canal directo ya alcanzable. Mensaje duplicado/replay, caducado, identidad anterior o autorización no verificable = denegar. **B no puede consultar estado remoto vivo de A sin canal**, por lo que el fallo seguro es indisponibilidad, no un resultado nuevo.
- `DeliveryGate`: debe concordar con el `AuthorizedLocationRelease` de [ADR-PROP-08 / PR #34](https://github.com/mundoinformaticacanaria/whereis/pull/34). La autoridad de relación serializa revocación/bloqueo/cambio de revisión con la decisión final de **liberar** cada respuesta. Una muestra ya capturada/preparada NO queda autorizada indefinidamente. Revocación aplicada antes de `Release` => no se transmite el dato; retransmisión exige revalidación y misma revisión vigente. No basta un chequeo anterior separado del paso de transmisión. Si falla verificador, fail-closed. Si `Release` ocurre antes de revocación, los bytes ya emitidos pueden llegar tarde por red: no prometer retractarlos. Como defensa en B, revalidar vigencia/época antes de **aceptar o mostrar** respuesta retrasada; si no es verificable, no mostrarla como nueva. La autoridad y atomicidad reales se deben demostrar, no inferir de esta ADR.
- El canal debe usar autenticación, cifrado en tránsito y reglas estrictas de caducidad/borrado de respuestas transitorias. **Si** es imprescindible persistencia en un intermediario, la ubicación, cifrado, plazos y minimización serán decisiones MATERIAL/PROPIETARIO sujetas a SEG-03/04/07, no defaults implícitos.

### 4.3. Emisor A

- `CaptureAttempt`: un intento acotado por solicitud vigente, aceptación en vivo de la **época original** y permisos Android efectivos. Tras desconexión/cambio de época no ejecutar captura al reconectar aunque una push siga dentro de TTL; la solicitud se cierra sin guardar trabajo. Nunca ejecutar geolocalización periódica ni abrir ajuste de ubicación automáticamente.
- Timestamp de `Location` = instante real de la **muestra**, no el de llegada de la notificación o respuesta. Una ubicación cacheada anterior a la petición no se declara actualización; si no se consigue muestra suficientemente fresca, reportar error. Umbral de frescura requiere definición técnica y validación.
- A ejecuta controles de seguridad antes de captura **y** liberación. Si pierde red o se revoca A→B durante operación, no entregar posición nueva sin revalidación.
- `NotificationThrottle` para servicio de ubicación apagado: clave por instalación solicitante, ventana 24h, reset tras transición observable a ubicación activada y luego nuevamente desactivada. La app **no puede acreditar retroactivamente** cambios ocurridos sin observación mientras estaba terminada; registrar limitación y elevar UX si es material. El emisor puede no mostrar notificación por permisos/políticas Android.
- Separar respuesta técnica interna («ubicación desactivada») de error genérico expuesto a B, conforme D-12.

### 4.4. Estado y privacidad

- `LastLegitimateLocation` en B solo cambia después de aceptar éxito nuevo y autorizado. En error se conserva timestamp real anterior sin variar el encuadre donde lo exija D-12.
- Si A está bloqueado, B eliminado o instalación inválida confirmada, las respuestas retrasadas nunca recrean una relación ni hacen reaparecer marcador oculto o datos borrados (D-09/D-10/SEG-04).
- No enviar ubicación/alias en push ni incluir coordenadas, tokens, IDs sensibles o relaciones personales en logs; observabilidad agregada/minimizada y datos ficticios en ensayos.

## 5. Comportamiento degradado y frontera legal

- App visible y permisos adecuados: puede intentar captura actual, sin prometer éxito.
- App no visible con background permission y ejecución permitida: intentar respuesta puntual con límites de Android y TTL.
- App no visible con foreground-only, force-stop, notificaciones deshabilitadas o restricciones OEM: **no** forzar ejecución; fallo tras timeout y posición anterior, si corresponde.
- Servicio de ubicación apagado: no generar ubicación; aviso local en A sujeto a condiciones aprobadas; B no conoce el motivo detallado.
- Normativa de distribución/consentimiento de ubicación de fondo y protección de menores = análisis jurídico/proveedor `PENDIENTE`, especialmente si se pretende distribuir en tienda.

## 6. Matriz de pruebas negativas — NO EJECUTADAS

| Escenario | Resultado esperado |
|---|---|
| A visible/background/proceso eliminado/force-stopped, Doze y batería restringida en varias versiones/OEM | Intentar solo donde sea legítimo; observar latencia/éxito; timeout controlado sin falsas garantías |
| Solo while-in-use vs ubicación «todo el tiempo»; precisa/aproximada/denegada; Android 12–14+ | Ningún bypass de permisos o FGS; `SecurityException` y fallos se manejan sin filtrar coordenadas |
| Cierre forzado o aviso perdido/repetido/tardío | No cola automática; no ejecución fuera de TTL ni replay |
| B consulta A, repite A, consulta C y pulsa «Actualizar todos» | A no duplicada; C independiente; cada resultado individualizado y resumen correcto |
| B offline, luego vuelve red | No consulta diferida; refresco manual explícito |
| A offline al solicitar → vuelve red **antes de expiresAt**; push retenida se entrega | No captura, ningún request pendiente ni nuevo intento automático; una epoch nueva invalida el aviso anterior |
| A pierde red en mitad del intento, vuelve antes del TTL | Tras interrupción no reiniciar captura/respuesta; terminar con fallo y exigir nueva consulta manual |
| Reintentos de vinculación D-09 frente a consulta D-12 | Permitir solo reintento idempotente de solicitudes de vínculo en su política de 24 h; no aplicar ese mecanismo a nuevas capturas de ubicación |
| Revocación tras captura y antes de liberar, reintentos y red lenta | Gate deniega liberar si revocación ya aplicada; respuesta emitida antes de revocación tiene límite físico de retiro y B revalida antes de mostrar |
| ID inexistente frente a ID no divulgable para actor no autorizado | Sin oráculo de existencia por cuerpo/código/cabeceras/tiempo/acuse de canal; prueba negativa estadística |
| Revocar A→B y bloquear B mientras solicitud en vuelo | Fallo cerrado en gate; ningún dato nuevo tras revisión revocada |
| Copiar ID/QR/credencial vieja, reinstalar A o B | Denegar suplantación y solicitudes de instalación previa; sin resultados antiguos |
| Ubicación sistema apagada y aviso permitido/denegado | Error genérico en B; límite de notificación a A de una/solicitante/24h donde verificable |
| Resultado GPS cacheado anterior al intento | No etiquetar como posición nueva; conservar última legítima fechada |
| B elimina dispositivo durante respuesta en vuelo | No resucitar marcador, alias ni ubicación |

Medir `targetSdk`, permisos efectivos, error Android real, estado de proceso, éxito/fallo, latencia, consumo de batería y verificación/tiempo de revocación con datos ficticios; no afirmar CI/QA o tasas de éxito antes de ensayos autorizados.

## 7. L-02 y P-52a/b/c/d: estado material vigente (31/10/2026)

**CONFIRMADO por PROPIETARIO:** L-02 conserva consultas familiares **a distancia como esenciales**; L-02c acepta fallos veraces sin SLA, sin convertir ubicación anterior en actual ni reducir el producto a LAN. El estudio documental de señalización externa está permitido, pero **no** se autoriza usar FCM, ntfy, ICE/STUN, TURN, broker ni emisor. Persistencia de ubicaciones y relaciones funcionales únicamente en los teléfonos, coste incremental de funcionamiento 0 € exigido pero **no demostrado** para ninguna combinación.

**Decisiones P-52a/b/c/d ya CONFIRMADAS exclusivamente para estudio**, según [#52, decisión PROPIETARIO del 29/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/52#issuecomment-6508017348):

- **P-52a:** permitido *analizar* Firebase Installation IDs/tokens técnicos persistentes en terceros, diferenciados del ID funcional WHEREIS y de los metadatos efímeros. **NO** autorizada su transmisión/retención real, aceptación jurídica ni adopción de FCM. Su posible retención externa hasta borrado y 180 días posteriores permanece un **riesgo de compatibilidad/privacidad** a evaluar en #41.
- **P-52b:** permitido comparar documentalmente FCM + posible emisor confiable sin secretos privilegiados en APK frente a broker ntfy. Ningún servicio, proveedor, cuenta, SDK o API seleccionado.
- **P-52c:** se **mantiene obligatorio** autenticación de B, antiabuso/anti-enumeración y permiso direccional A→B **vigente y validado en A al liberar**. Una capacidad antigua puede despertar A tras revocación, pero no autoriza entregar ubicación. Es necesaria mitigación contra spam sin directorio externo de relaciones.
- **P-52d:** pruebas reales de Android, notificaciones, entrega, servicios, retención o coste requieren **nueva autorización previa** del PROPIETARIO; ninguna se ha ejecutado.

**Viabilidad técnica PENDIENTE:** en red directa remota, NAT/CGNAT/IPv6 y Android en segundo plano/Doze/force-stop impiden prometer acceso universal. Si se utiliza canal externo en un estudio futuro, su ACK sólo prueba aceptación de transporte, **no** inbox A/acuse D-09 ni autorización. En D-12, incluso un aviso con TTL no agotado debe **descartarse sin capturar** si A estaba offline y reconecta: una nueva época de red nunca reanuda la solicitud de ubicación antigua. `LiveAcceptance`/`connectivityEpoch` siguen como propuestas sin verificación en dispositivo. D-09 permite reintentos de *vinculación* según su contrato, no reapertura automática de una **consulta**. La notificación por ubicación Android apagada nace sólo al procesar A la consulta autorizada y queda sujeta a permisos del SO.

**Seguridad pendiente:** A es autoridad final local de relación/revisión/revocación; la liberación está condicionada a revalidar justo antes de emitir. B sólo puede mostrar la última ubicación legítima anterior con timestamp real ante fallo; no inferir revocación remota instantánea ni retirada de paquetes ya emitidos. La opción B anti-enumeración está confirmada como requisito, **no verificada** en canales laterales de IP, endpoint o tiempos. Conectar A a terceros, cambiar alcance o aceptar retención real exige decisión humana nueva.

## 8. Handoff y responsables actualizados (31/10/2026)

- **ARQUITECTO — [#22](https://github.com/mundoinformaticacanaria/whereis/issues/22):** corrige en esta ADR los DEFECTOS documentales de [QA #57 sobre HEAD `e275162c023d0e9184962f4a8058c29803975716`](https://github.com/mundoinformaticacanaria/whereis/pull/35#issuecomment-6536186491). **Nuevo HEAD requiere nuevo dictamen QA independiente**; la issue hija #57 terminó con DEFECTOS, no APTO.
- **TECH LEAD — #22 tras handoff:** verificar HEAD nuevo, coordinar QA independiente y reconciliar PR #35 con [PR #55](https://github.com/mundoinformaticacanaria/whereis/pull/55), [PR #50](https://github.com/mundoinformaticacanaria/whereis/pull/50), PR #34/#45 y gates de #24/#28. Definir umbrales técnicos, APIs/targets, timeout y ensayos futuros **solo tras autorizaciones**.
- **TECH LEAD — [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41):** análisis jurídico documental SEG-03/04 tras [decisión del PROPIETARIO de no contratar asesoría externa](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6508016590); no equivale a validación jurídica. Revisiones hijas: [#60 FUNCIONAL](https://github.com/mundoinformaticacanaria/whereis/issues/60) para transparencia/borrado y [#61 ARQUITECTO](https://github.com/mundoinformaticacanaria/whereis/issues/61) para superficies/backups/supresión.
- **ARQUITECTO — [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52), temporalmente para corrección QA:** PR #55 conserva P-52a/b/c/d como decisiones **confirmadas solo para estudio** y sigue sin proveedor, coste integral acreditado ni pruebas Android. TECH LEAD retomará coordinación tras nuevo HEAD.
- **TECH LEAD — [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24) y [#19](https://github.com/mundoinformaticacanaria/whereis/issues/19):** SEG-01/02/05–07 y riesgos técnicos D-09–D-13; PR #49 integrada documentalmente, sin declarar SEG-01/02 implementados. G-02 en `main` designa al chat independiente como ARQUITECTO desde #37.
- **PROPIETARIO:** toda adopción de proveedor/servicio, envío real de tokens, nueva política de retención, coste, cambio de UX/alcance o prueba real requiere aprobación expresa posterior; no confundir estas decisiones con P-52a/b/c/d.

**Estado:** `PROPUESTA / NO APROBADA`, PR #35 DRAFT, sin tests Android, QA APTO del nuevo HEAD, CI verde ni autorización de PROGRAMADOR, servidor, CRM o timers. No realizar merge.

## 9. Fuentes técnicas externas

- [Android Background location limits](https://developer.android.com/develop/sensors-and-location/location/background)
- [Android Background location permissions](https://developer.android.com/develop/sensors-and-location/location/permissions/background)
- [FGS background restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start)
- [Android 14 FGS types](https://developer.android.com/about/versions/14/changes/fgs-types-required)
- [Android notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
- [FCM delivery priorities: constraints, NOT selection](https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-priority)

**Estado de esta ADR: `PROPUESTA`, no arquitectura confirmada.**
