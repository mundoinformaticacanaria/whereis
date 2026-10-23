# ADR-PROP-22 — Consultas puntuales cuando la app emisora no está visible

- **Estado:** `PROPUESTA / NO APROBADA`.
- **Clasificación:** `MATERIAL` — permisos Android, privacidad, comunicación, concurrencia y seguridad.
- **Issue:** [#22 — D-12](https://github.com/mundoinformaticacanaria/whereis/issues/22).
- **Contrato relacionado:** [#2 — D-02](https://github.com/mundoinformaticacanaria/whereis/issues/2), [#8 — D-04](https://github.com/mundoinformaticacanaria/whereis/issues/8), [#19 — D-09](https://github.com/mundoinformaticacanaria/whereis/issues/19), [#20 — D-10](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#24 — SEG-01/02/03/05/06/07](https://github.com/mundoinformaticacanaria/whereis/issues/24) y PR #25.
- **Alcance:** estudio y alternativas; **no** selecciona proveedor, SDK, backend, push, mapas, infraestructura o versiones Android objetivo; no hay pruebas de dispositivo ni implementación.
- **Autoridad:** estudio puntual solicitado por PROPIETARIO en conversación. Conforme G-02 de `main`, ARQUITECTO formal = Codex; se requiere revisión/handoff formal antes de considerar completada la issue por ese rol.

## 1. Comportamiento CONFIRMADO que se debe preservar

1. B puede intentar consultar puntualmente a A autorizado aunque Whereis no sea visible en A, **solo cuando Android lo permita**. No seguimiento continuo ni localizaciones automáticas recurrentes. No prometer disponibilidad/latencia universal (D-02).
2. Una petición individual mantiene estado propio. B no inicia dos consultas de un mismo A simultáneamente; sí puede consultar C a la vez. «Actualizar todos» reutiliza las activas, agrega las faltantes y resume éxitos/errores (D-12).
3. B sin Internet: controles de refresco deshabilitados, aviso persistente y **nada encolado para reconectar**. A sin Internet o sin ubicación/permisos: sin éxito ficticio, reintento solo manual. No divulgar a B la razón sensible de ubicación Android desactivada.
4. Mostrar última posición legítima únicamente como **anterior/no actual**, con fecha real y aviso; sin historial automático (D-06/D-10).
5. SEG-01/02: antes de liberar una posición nueva acreditar identidad auténtica **y** autorización direccional activa y verificable. Un ID/QR, acuse push, caché o permiso previo no basta.
6. La alerta por servicio Android apagado en A, cuando sea posible, no debe superar **una por solicitante y 24h**, con reinicio condicionado al ciclo de activación/desactivación realmente observado. No avisar por consultas ordinarias exitosas (D-12).

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
| Aviso remoto efímero + consulta y respuesta autenticadas con TTL | Buen encaje lógico para solicitud manual sin polling | Requiere canal entregable a A y alguna función lógica de verificación/entrega; no garantiza despertar; coste/proveedor por analizar | **Preferida para validar**, no seleccionar proveedor |
| Socket persistente / canal P2P mientras la app no es visible | Evita alguna intermediación según conectividad | Batería, NAT, restricciones de background, proceso suspendido, disponibilidad del teléfono; no garantiza cobertura | Alternativa solo si pruebas lo justifican |
| Polling periódico/alarma para buscar peticiones | Aparentemente sencillo | Respuesta tardía, batería y ejecución automática recurrente incompatible con el objetivo de consulta puntual | **No recomendado para el MVP** |
| Solo consulta con A visible | Riesgo técnico menor | Dejaría sin cubrir los casos admitidos por D-02 con A no visible | Degradación por impedimento Android, no cambio unilateral de requisito |

Una alternativa comercial concreta de mensajes, incluida FCM, **no** está autorizada. Las pruebas de recepción, políticas de privacidad, costes, cuota, data locality y dependencia comercial son parte de SEG-07 y decisión posterior.

## 4. Límites y contratos propuestos

### 4.1. Cliente consultante B

- `RequestCoordinator`: por cada destino autorizado A, a lo sumo un `requestId` activo para **esa instalación B**; permite A y C concurrentes. «Actualizar todos» agrega solo destinos elegibles sin duplicar. No crea trabajos al iniciar app o reconectar.
- `LocationRequest`: `requestId` impredecible y único; `requesterInstallationId`, `targetInstallationId`, `createdAt`, `expiresAt`, `authorizationRevision` de referencia y `purpose=manual`. El reloj de expiración debe estar ligado a fuente fiable y revisarse; umbral final = decisión TECH LEAD.
- `TerminalResult`: un resultado definitivo `fresh-success`, `failure` o `timeout` por `requestId`. Las respuestas repetidas/tardías de intentos cerrados se ignoran; no hay reintento automático.
- Si B está offline, no se emite solicitud ni queda esperando una que se dispare sola al recuperar conectividad.

### 4.2. Transporte

- `WakeHint`: aviso opaco sin coordenadas, nombre, alias, ubicación o secretos. Despertar no implica permiso ni aceptación; A consulta el estado real y actual del request solo si Android permite procesarlo.
- `RequestVerifier`: prueba de posesión de identidad de B y verificación actual de relación A→B y su revisión. Mensaje duplicado/replay, caducado, identidad anterior o autorización no verificable = denegar.
- `DeliveryGate`: **revalidación de la relación justo antes de liberar la posición nueva** con semántica coherente con revocación concurrente. Ninguna ubicación se publica por error si la relación ya fue revocada al punto de verificación. No se garantiza retirar lo entregado antes de revocación ni conocer una desinstalación remota instantáneamente.
- El canal debe usar autenticación, cifrado en tránsito y reglas estrictas de caducidad/borrado de respuestas transitorias. **Si** es imprescindible persistencia en un intermediario, la ubicación, cifrado, plazos y minimización serán decisiones MATERIAL/PROPIETARIO sujetas a SEG-03/04/07, no defaults implícitos.

### 4.3. Emisor A

- `CaptureAttempt`: un intento acotado por solicitud vigente con permisos Android efectivos. Nunca ejecutar geolocalización periódica ni abrir ajuste de ubicación automáticamente.
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
| A offline, luego vuelve red | No ejecución tardía de request caducado |
| Revocar A→B y bloquear B mientras solicitud en vuelo | Fallo cerrado en gate; ningún dato nuevo tras revisión revocada |
| Copiar ID/QR/credencial vieja, reinstalar A o B | Denegar suplantación y solicitudes de instalación previa; sin resultados antiguos |
| Ubicación sistema apagada y aviso permitido/denegado | Error genérico en B; límite de notificación a A de una/solicitante/24h donde verificable |
| Resultado GPS cacheado anterior al intento | No etiquetar como posición nueva; conservar última legítima fechada |
| B elimina dispositivo durante respuesta en vuelo | No resucitar marcador, alias ni ubicación |

Medir `targetSdk`, permisos efectivos, error Android real, estado de proceso, éxito/fallo, latencia, consumo de batería y verificación/tiempo de revocación con datos ficticios; no afirmar CI/QA o tasas de éxito antes de ensayos autorizados.

## 7. Pendientes, coste y siguientes responsables

- **TECH LEAD**: decidir matriz API/target a validar, presupuesto de complejidad, máximo tiempo de espera y frescura, revisar opciones de transporte y necesidad mínima de componente verificador. No asignar desarrollo hasta #28.
- **PROPIETARIO — #24 ya tiene label `PROPIETARIO`**: conflicto D-09/SEG-02, límites jurídicos de menores, retención/borrado, permisos en background/distribución y autorización material de proveedores/costes. No alterar mensajes D-09 por criterio técnico unilateral.
- **FUNCIONAL — PR #25 devuelta para conciliación:** mantener semántica de fallos/reintentos/avisos confirmada; abrir decisión MATERIAL adicional si restricciones reales hacen imposible algún flujo.
- **ARQUITECTO formal (Codex)**: validar hipótesis de Android y seguridad, coordinar con [ADR-PROP-08](https://github.com/mundoinformaticacanaria/whereis/issues/8) y devolver a TECH LEAD cuando exista una propuesta revisable. Esta PR no constituye cierre formal ni handoff.
- **Prototipo Android**: requiere autorización y issue distinta de esta ADR. No toca código, servidores, tokens, proveedores ni timers.

## 8. Fuentes técnicas externas

- [Android Background location limits](https://developer.android.com/develop/sensors-and-location/location/background)
- [Android Background location permissions](https://developer.android.com/develop/sensors-and-location/location/permissions/background)
- [FGS background restrictions](https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start)
- [Android 14 FGS types](https://developer.android.com/about/versions/14/changes/fgs-types-required)
- [Android notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
- [FCM delivery priorities: constraints, NOT selection](https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-priority)

**Estado de esta ADR: `PROPUESTA`, no arquitectura confirmada.**
