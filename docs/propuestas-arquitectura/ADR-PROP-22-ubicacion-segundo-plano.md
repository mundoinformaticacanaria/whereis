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

## 7. L-02: consulta remota esencial, estudio externo permitido y coste 0 € (#41/#52)

**ACTUALIZACIÓN L-02 CONFIRMADA:** [PROPIETARIO #41](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6399627418) mantiene la consulta remota familiar como objetivo esencial y **autoriza el estudio**, NO el uso, de señalización externa a coste 0 € y sin almacenamiento persistente externo de posiciones. [PR #50](https://github.com/mundoinformaticacanaria/whereis/pull/50) analiza cuatro mecanismos y sus obstáculos. La tabla de opciones de esta ADR puede estudiarse bajo L-02; **ningún proveedor, FCM, broker, relay ni API está autorizado para adopción**. El aviso externo nunca es prueba de recepción, permiso ni captura; D-12 sigue prohibiendo ejecución diferida tras reconexión incluso con TTL no vencido.

**CONFIRMADO por PROPIETARIO (L-02/L-02b/c/d):** ubicaciones y relaciones persistentes solo en teléfonos; coste incremental 0 € obligatorio; estudio documental de datos técnicos imprescindibles (IP, tokens, metadatos) permitido, **sin** transmisión real ni adopción de terceros. El tratamiento de identificadores técnicos persistentes de FCM está **PENDIENTE de decisión P-52a en #52** y de validación jurídica #41. Esta actualización prevalece sobre restricciones históricas local-only de la ADR.

- **Internet remoto directo:** posible si B conoce una dirección de A **vigente y alcanzable** (IPv6 admitido y sin bloqueo, o IPv4 con configuración) y A está realmente escuchando. Redes móviles con NAT/CGNAT/firewalls, direcciones dinámicas y suspensión del proceso no ofrecen garantías. Intercambiar QR/ID no da automáticamente una dirección alcanzable ni rompe NAT.
- **Wi-Fi Direct/Bluetooth/LAN:** útiles cerca, no resuelven teléfonos familiares separados por ciudades. El transporte entre ciudades sin infraestructura ajena y A no visible **NO SE HA DEMOSTRADO** como funcionalidad general. No improvisar un servidor en el Linux multiproyecto ni usar recursos CRM.
- **Consulta D-12:** la sesión directa sólo puede capturar en la época en vivo original; offline + reconexión (aun antes de TTL) => fallo y **nuevo clic manual**. D-09 sí permite reintentar solicitudes de relación sin duplicados, si se restablece un canal real; no convertir eso en consulta nueva.
- **Ausencia de autoridad externa:** el propio teléfono A es autoridad del permiso direccional y verifica en su gate final. Si A está inaccesible, B falla cerrado y sólo puede mostrar ubicación antigua legítima fechada (salvo ocultación por bloqueo). El acuse «recibida» D-09 debe nacer **después de persistir en el inbox local de A**; una notificación no basta.
- **Notificaciones de permiso Android apagado:** deben generarse localmente en A cuando éste realmente procesa un intento autenticado y observa el estado; permisos Android siguen condicionando si se pueden mostrar. No prometer avisar en un teléfono A desconectado o dormido.
- **Identidad/anti-enumeración:** el endpoint directo puede exponer existencia mediante respuesta/latencia/IP; no declarar opción B SEG-02 satisfecha hasta pruebas negativas. El alta de ID manual con un directorio inexistente puede exigir nueva decisión funcional.
- **Decisión MATERIAL pendiente:** L-02 mantiene la consulta familiar remota como esencial y acepta fallos reales, pero no autoriza ninguna arquitectura. [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52) requiere decisiones P-52a/b/c/d del PROPIETARIO sobre metadatos persistentes, estudio de alternativas, antispam/revocación y ensayos futuros; #41 conserva revisión jurídica SEG-03/04. No degradar unilateralmente a LAN/proximidad ni adoptar terceros.

## 8. Pendientes, coste y siguientes responsables

- **TECH LEAD**: decidir matriz API/target a validar, presupuesto de complejidad, máximo tiempo de espera y frescura, revisar opciones de transporte y necesidad mínima de componente verificador. No asignar desarrollo hasta #28.
- **TECH LEAD — [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24), label `TECH LEAD`:** coordinar SEG-01/02/05–07 y evidencias de canal/acuse; la **opción B D-09/SEG-02 está CONFIRMADA** por PROPIETARIO, por lo que se diseña no divulgación de existencia sin declarar SEG-02 cerrado. Elevar incompatibilidad del protocolo con prohibición de ejecución tras reconexión si no puede probarse.
- **PROPIETARIO — [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41):** revisión jurídica SEG-03/04 de menores, retención, supresión y terceros. **PROPIETARIO — [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52):** decisiones P-52a/b/c/d tras estudio del ARQUITECTO en PR #55 (DRAFT); [#56](https://github.com/mundoinformaticacanaria/whereis/issues/56) conserva QA independiente. PR #50/#45/#34/#35 siguen propuestas, sin baseline, proveedor ni pruebas reales.
- **TECH LEAD — [#19](https://github.com/mundoinformaticacanaria/whereis/issues/19):** D-09–D-13/SEG integradas documentalmente mediante PR #49 tras QA; permanecen riesgos técnicos y funcionales pendientes, sin considerar SEG-01/02 acreditados.
- **ARQUITECTO (chat ChatGPT independiente designado por #37 B)**: el estudio L-02b/c/d ya fue entregado en PR #55 y revisado técnicamente por TECH LEAD; la QA independiente sigue en #56. Las hipótesis Android/seguridad, epoch en A, gate con [ADR-PROP-08](https://github.com/mundoinformaticacanaria/whereis/issues/8) y respuesta tras revocación siguen sin validación experimental. La enmienda G-02 está integrada en `main`; esta ADR continúa como PROPUESTA DRAFT sin aprobación material.
- **Prototipo Android**: requiere autorización y issue distinta de esta ADR. No toca código, servidores, tokens, proveedores ni timers.

## 9. Fuentes técnicas externas

- [Android Background location limits](https://developer.android.com/develop/sensors-and-location/location/background)
- [Android Background location permissions](https://developer.android.com/develop/sensors-and-location/location/permissions/background)
- [FGS background restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start)
- [Android 14 FGS types](https://developer.android.com/about/versions/14/changes/fgs-types-required)
- [Android notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
- [FCM delivery priorities: constraints, NOT selection](https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-priority)

**Estado de esta ADR: `PROPUESTA`, no arquitectura confirmada.**
