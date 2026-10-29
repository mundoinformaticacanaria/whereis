# ADR-PROP-52 — L-02b/c/d: señalización remota, metadatos efímeros y emisor confiable

- **Estado:** `PROPUESTA / PENDIENTE`; **NO** arquitectura aprobada, proveedor elegido ni viabilidad demostrada.
- **Clasificación:** `MATERIAL`, estudio documental autorizado exclusivamente por el PROPIETARIO.
- **Encargo:** [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52), creado por TECH LEAD para las decisiones [L-02b/c/d CONFIRMADAS en #41, 26/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6410130695).
- **Base documental, sin duplicarla:** [PR #50 — cuatro medios de señalización](https://github.com/mundoinformaticacanaria/whereis/pull/50), [PR #45 — local-only / 0 €](https://github.com/mundoinformaticacanaria/whereis/pull/45), [PR #34 — identidad / revocación](https://github.com/mundoinformaticacanaria/whereis/pull/34), [PR #35 — Android / D-12](https://github.com/mundoinformaticacanaria/whereis/pull/35). Esta ADR añade **contratos del emisor, coste agregado, metadatos/retención y gates verificables**; no repite ni sustituye las matrices de esos estudios.
- **Evidencia:** lectura de GitHub y documentación pública oficial al 26/10/2026; **ninguna** cuenta creada, mensaje enviado, API probada, dispositivo ensayado, servicio desplegado, secreto generado ni coste observado.

## 1. Reglas innegociables

**CONFIRMADO** por el PROPIETARIO en #41: (a) consulta familiar **remota** entre teléfonos sigue siendo esencial; no reducir el alcance a LAN; (b) España, uso personal/familiar y coste incremental obligatorio de funcionamiento **0 €**; (c) ubicaciones y relaciones/autorizaciones/identidad funcional persistentes **solo dentro de instalaciones participantes**; prohibido almacenar posiciones persistentemente en terceros; (d) L-02b autoriza **estudiar**, no enviar, IP, tokens de entrega y metadatos técnicos estrictamente necesarios en terceros; (e) L-02c acepta **disponibilidad condicionada sin SLA** ni éxito universal; (f) L-02d permite **estudiar**, no operar, un emisor remoto confiable sin credenciales privilegiadas en APK.

D-09: la petición de vinculación no está `recibida` hasta que **A la haya almacenado en su propia bandeja y emitido acuse autenticado**; un acuse del proveedor no basta; caducidad 24 h y reintentos idempotentes solo para vinculación. D-12: cada consulta de **ubicación** nace de acción manual, no queda en cola para capturar tras reconexión (ni antes de TTL); posición antigua siempre fechada como anterior. SEG-01/02: A valida identidad auténtica de B y permiso A→B **vigente al liberar** la nueva posición; fallo cerrado y opción B anti-enumeración. No notificar consultas ordinarias exitosas al emisor para forzar prioridad push. Menores/retención SEG-03/04, licencias/proveedores SEG-07, #24 y gates #28 **PENDIENTES**.

**Separación fundamental:** `emisor confiable de transporte` = quién posee credenciales globales para solicitar a FCM una entrega. **NO** debe convertirse en `autoridad de autorización de ubicaciones`: únicamente el teléfono A conoce y decide el permiso A→B actual. Una firma o autorización antigua presentada a un relay puede ser válida como identidad criptográfica y a la vez estar **revocada** en A. Proteger el endpoint de spam no equivale a garantizar revocación.

## 2. Tres arquitecturas concretas de ESTUDIO — NO autorizadas para uso

| Variante, sin selección | Emisor / wake y NAT | Datos externos y persistencia técnica | Coste verificable y límites | Resultado arquitectónico |
|---|---|---|---|---|
| **A. B → función serverless gratuita de envío → FCM → A** (ej. Cloudflare Workers Free, solo referencia comercial) | Función externa guarda **secreto privilegiado de FCM fuera del APK**; recibe petición autenticada de B y envía aviso opaco a token de A. FCM puede despertar Android de forma limitada detrás de NAT/CGNAT, NO conceder permiso de ubicación | Cloudflare podría tratar IP de B, hora, destino/token FCM, prueba criptográfica y trazas; Google recibe registro de instalación, token/ruta y payload del aviso. **No** mandar coordenadas, alias, permiso ni secreto privado. La retención de logs/cachés/tokens por ambos terceros debe verificarse | Firebase lista **Cloud Messaging sin coste**. Workers Free publica **100 000 peticiones/día y 10 ms CPU/petición**; superar cuotas puede producir errores. Estas cifras NO prueban que el flujo completo (OAuth, firma, antifraude, FCM, rotación de claves, operación) sea viable gratis y sin método de pago/contrato | **PREFERENCIA SOLO PARA ANÁLISIS DEL PROBLEMA DE EMISOR**; encaja mejor con wake remoto, pero seguridad de emisor, tratamiento de tokens, coste 0 total y Android no demostrados |
| **B. B → broker ntfy.sh con `Cache: no` → A** (y, según configuración de recepción, FCM) | Publicación desde B sin secreto global de FCM en APK; tópico opaco + contenido mínimo autenticado/cifrado, A escucha/recibe. Android sin conexión activa puede depender del **FCM de ntfy**, segundo proveedor, o listener con restricciones de fondo | ntfy trata IP, tópico, timestamps; `Cache: no` suprime **caché del mensaje**, NO acredita borrado de logs o metadatos; el canal Android estándar de ntfy.sh puede retransmitir contenido/metadatos a Google. `Firebase: no` reduce ese tercero pero puede retrasar avisos sin conexión activa; tópico público no es identidad ni secreto confiable | Documentación ntfy indica uso público gratuito sujeto a límites, política mutable y disponibilidad **best effort**; ningún compromiso de 0 € integral/indefinido o tratamiento transfronterizo acreditado. Por defecto ntfy cachea mensajes 12 h **si no** se usa `Cache: no` | **COMPARADOR SIN EMISOR PRIVILEGIADO PROPIO**; superficie de tópicos públicos, spam, metadatos y fiabilidad de ejecución Android sin resolver; no adoptar |
| **C. B → rendezvous/señalización efímera → ICE/STUN → P2P directo A** (TURN solo referencia de descarte) | Intercambio temporal de candidatos, sin emisor FCM; intenta canal A↔B cuando ambas apps están disponibles y NAT/firewall lo permiten. **No** despierta A; CGNAT/NAT restrictivo puede requerir TURN (relay no gratuito acreditado) | Servicio de signaling/STUN trataría IP pública/privada, puertos/candidatos, hora y relación de conectividad; no enviar coordenadas. Si no hay servicio, tampoco discovery remoto confiable. Políticas/retención del operador concretas PENDIENTES | ICE/WebRTC son tecnologías, NO contrato gratuito de señalización, STUN o TURN. Coste 0 del conjunto NO acreditado; relay consume tráfico/infraestructura | **No cubre por sí solo D-02** con A no visible; solo complemento condicional a aviso autorizado, no sustituto de A/B |

**Conclusión de opciones:** A es el candidato de estudio más directamente relacionado con `emisor confiable`; B permite comparar el coste de evitar un emisor privilegiado a cambio de exposición y disponibilidad; C sirve para evaluar qué no resuelve un canal de wake. **No se selecciona proveedor, combinación, cuenta, clave ni infraestructura**. En particular, mencionar Cloudflare Workers NO autoriza crear un Worker ni usar su dominio gratuito.

### 2.1. Emisor de FCM: diseño de frontera y amenaza (variante A, HIPÓTESIS)

Flujo lógico **NO probado**:

1. A genera claves por instalación no restaurables y mantiene local su relación A→B y sus permisos. Durante vinculación confiable, A entrega a B solamente los **datos mínimos de enrutamiento** y prueba pública necesarios; la forma segura de distribuir/rotar token FCM sin directorio externo está `PENDIENTE`. **No** compartir la clave privada de A.
2. B realiza una consulta manual y dirige al emisor una solicitud firmada, acotada al destinatario, con `requestId`, finalidad y expiración breve. El emisor no acepta meros IDs/QR como autenticación. Para limitar abuso, se puede **estudiar** un certificado/capacidad firmada por A durante vinculación y un contador o límite de invocaciones; el riesgo residual es que una capacidad aún válida permita emitir avisos **después de revocación en A**. Revocar sin que el emisor conserve/obtenga estado actual no puede garantizar supresión inmediata de notificaciones. No presentar limitación por IP o challenge estático como defensa completa.
3. Emisor verifica firma, límites y validez observable del request y, con credencial privilegiada **solo en su entorno externo**, solicita a FCM transmitir **únicamente aviso opaco**. Posibles implementaciones de credencial: secreto cifrado en servicio o identidad federada sin clave exportable **cuando el proveedor lo permita realmente**. FCM HTTP v1 requiere OAuth 2.0/servicio de confianza; las credenciales del proyecto **no** van en APK. No se ha acreditado que un plan serverless gratuito admita todas las operaciones criptográficas en 10 ms CPU, ni que la identidad federada concreta exista en el emparejamiento proveedor-Google.
4. Al recibir aviso, A no supone permiso ni entrega garantizada. A autentica petición de B, comprueba frescura/ausencia de reconexión diferida, permisos Android y **autoridad local A→B**. La captura solo procede si Android lo permite; el gate final de liberación se ordena con revocaciones/bloqueos locales (PR #34/#35).
5. `FCM messages:send` confirma aceptación del proveedor, **NO** entrega real a A, lectura en app, nuevo permiso ni ubicación actual. Para D-09, A debe guardar inbox y firmar acuse de `recibida` que B verifique; esto requiere **ruta autenticada de respuesta**, sea directa o segundo aviso al token B, igualmente no diseñada todavía.
6. Un `ttl=0` en FCM implica descartar avisos **no entregables de inmediato**, minimiza cola del proveedor; **no prueba** que un aviso recibido durante la sesión original vaya a procesarse antes de una desconexión/reconexión o que se pueda iniciar ubicación background. La condición D-12 exige **prueba de época/aceptación original** y descarte de intentos tardíos en A, incluso dentro de TTL. Si no puede acreditarse en Android real, **bloqueo de viabilidad**, no excepción técnica tácita.

**Imposibilidad de suponer autoridad global:** con relaciones y permisos persistentes **solo en A**, un emisor sin estado no puede conocer cada revocación al instante; limitarlo a transmisor de avisos reduce el impacto de una credencial equivocada pero no impide spam/wake falsos por sí solo. No añadir directorio externo de relaciones para arreglarlo sin nueva aprobación material.

### 2.2. Brokers efímeros: dos modos Android con amenazas distintas (variante B)

- `Cache: no` de ntfy significa **no persistir el cuerpo en su caché de mensajes** y pérdida posible si A no estaba conectado. **No equivale** a garantizar cero retención de logs/IP/tópicos ni borrado verificable de terceros. Tópicos públicos susceptibles de escucha, publicación maliciosa y correlación: cifrado de payload de extremo a extremo, tópicos aleatorios, firmas y cambio de tópico son **propuestas**, no controles comprobados.
- En ntfy.sh los avisos a la app Android convencional pueden retransmitirse mediante FCM. `Firebase: no` evita ese reenvío pero la propia documentación advierte retraso si no se habilita entrega inmediata; una conexión larga/UnifiedPush alternativa puede consumir batería y estar sometida a suspensión Android. **No** prometer un wake fiable de una APK WHEREIS propia solo por las prestaciones de la app ntfy independiente.
- El broker no es fuente de verdad del permiso ni de la recepción. `HTTP 200` o confirmación ntfy = aceptado por el broker, **no** inbox de A. Rotación tópicos sin provocar pérdida de solicitudes válidas y anti-enumeración de IDs siguen sin diseñar.

## 3. Matriz L-02b: datos del tercero, necesidad y retención NO supuesta

| Flujo / responsable eventual | Metadatos mínimos plausibles visibles externamente | ¿Qué NO enviar? | Retención publicada o riesgo PENDIENTE |
|---|---|---|---|
| **B → emisor serverless (A)** | IP pública B, fecha/hora, URI, pseudónimo/ticket, token objetivo FCM, volumen/contadores de petición, evento de autenticación | Ubicación, precisión, alias o edad de menor, listado familiar, ID WHEREIS legible, estado persistente de autorizaciones, clave privada de instalación | Cloudflare ofrece variables cifradas tipo `Secrets` para credencial FCM; **retención del registro de IP, excepciones, protección contra abuso, logs de Worker y jurisdicción NO ACREDITADAS**. Las `Secrets` del emisor son persistencia externa de **credencial operativa del servicio**, no identidad WHEREIS del dispositivo; requiere aprobación específica. |
| **Emisor → Google/FCM (A)** | Token destino de instancia, ID de proyecto FCM, payload opaco, eventos/tiempos de entrega, IP de emisor | Coordenadas, alias, permisos, lista de vínculos, secretos funcionales | Google declara conservar **Firebase Installation IDs** hasta solicitud de supresión mediante API y retirada de sistemas activos/copias dentro de **hasta 180 días** tras solicitarla. **No son “metadatos efímeros” por defecto**, por lo que debe decidir el PROPIETARIO si esto es compatible con L-02b y almacenamiento local de identidad WHEREIS. Un token técnico externo no debe confundirse con ID WHEREIS, pero permite correlación del dispositivo. |
| **B → ntfy.sh → A (B)** | IP B/A, tópico, hora/longitud/frecuencia, posible servicio FCM secundario y metadatos | Coordenadas y contenido sensible sin cifrado/seudonimización; URL/topic determinista a partir del ID WHEREIS | Con `Cache: no` no se conserva **cuerpo** en caché, pero ntfy admite logs de IP y tópicos; plazo de esos logs, tratamientos auxiliares, FCM/transferencia y supresión efectiva **PENDIENTES**. Sin `Cache:no`, caché de cuerpo por defecto **12 h**. |
| **B/A → rendezvous STUN/ICE (C)** | IP internas/externas, puertos, candidatos ICE, tiempo y patrón de conexiones, posible asociación de extremos | Coordenadas, credenciales de permiso, ubicación persistente en relay | Registro del operador de señalización y de STUN/TURN, trazas, región, coste de ancho de banda y caducidad **NO VERIFICADOS**. TURN puede ver IP/tráfico aun con contenido cifrado. |
| **Teléfono A (autoridad local)** | `A→B` activo/revocado, clave pública, revisiones, ubicación actual generada a petición | No exponer permisos ni ubicación al tercero por el aviso | Persistencia solo en A; política jurídica de retención SEG-03/04 sigue PENDIENTE en #41. |
| **Teléfono B (consulta)** | Última ubicación legítima por A, timestamp real, lista conocida y autorización/ack mostrados | Nunca marcar posición antigua como actual | Persistencia solo en B; reinstalación nueva sin backup; supresión/retención legal PENDIENTE. |

**Distinción esencial L-02b:** “datos de ubicación/relaciones solo en teléfonos” **no** implica “sin metadatos fuera”. Pero tampoco autoriza **perfiles persistentes de instalación en terceros**: para FCM los identificadores de instalación pueden conservarse fuera del teléfono. Si esta excepción material no es aceptable, A no pasa gate sin importar gratuidad. Debe obtenerse la política completa de cada proveedor, tratamiento fuera de España/UE, roles GDPR, base de legitimación, borrado/revocación y condiciones aplicables a menores. La excepción doméstica del titular familiar NO exonera automáticamente a un tercero operador.

## 4. L-02c: veracidad de disponibilidad y estados

| Evento | Qué se puede afirmar a B | Qué no se puede afirmar |
|---|---|---|
| Emisor devuelve éxito de HTTP v1 / broker | Aviso **aceptado por intermediario** si se expone ese estado, no entrega efectiva | “A ha recibido”, “A está conectado”, “permiso activo”, “ubicación actual” |
| Acuse autenticado de A **después de guardar solicitud D-09** | “Solicitud recibida en la bandeja de A”; persistencia **local** y firma verificable | “Ubicación autorizada”; aceptar solicitud no concede permiso |
| A sin red, apagado, Android restringido o force-stop | Fallo genérico comprobable en intento; conservar última legítima fechada y anterior cuando se permita | Estado remoto exacto sin prueba; éxito ficticio o captura tardía tras reconexión |
| B sin red al pulsar | Botón de refresco deshabilitado o error, sin creación de cola | Reintento automático al reconectar |
| Aviso tarde o duplicado con TTL no vencido | Validar requestID, vínculo y época original; si no acreditables, **descartar sin capturar** | Tratar TTL por sí mismo como autorización a capturar |
| Revocación entre captura y liberación | No liberar dato si ya revocado en A; responder fallo sin exponer detalle privado | Retirar un paquete ya transmitido antes de la revocación |
| Servicio sobre cuota gratis, contrato cambia o sufre corte | Fallo seguro de señalización; ninguna compra/upgrade automático | SLA, “siempre gratis” o acceso garantizado |

**No se han definido umbrales numéricos de timeout, disponibilidad o tasa de éxito; no son decisiones delegadas a ARQUITECTO sobre UX**, y no existen pruebas Android u OEM que los justifiquen. L-02c acepta falta de SLA, **no** aprueba seguimiento secreto ni retrasos con captura automática.

## 5. L-02d: requisitos comprobables del emisor y financiación real

Un emisor confiable **de estudio**, no desplegado, debe mostrar:

1. **Aislamiento de secretos:** ninguna credencial de envío FCM/OAuth, service-account o token admin en APK, QR, GitHub o dispositivo B. Gestor de secretos del proveedor o identidad federada verificada, privilegio mínimo, rotación/borrado, auditoría y recuperación sin coste obligatorio; no esconder secretos en un proxy HTTP público sin autenticación.
2. **Admisión autenticada y antiabuso**: firma/challenge por instalación, rate limiting por actor/ventana sin directorio persistente de relaciones (contradicción pendiente), cuotas fail-closed y defensa contra enumeración de IDs/token; no filtrar si existe destinatario cuando el solicitante carece de derecho. Un sender stateless no puede comprobar revocación actual en A; el gate de geolocalización nunca se traslada al sender.
3. **No ubicación en el aviso:** payload `requestId` opaco, destino token donde sea necesario y TTL mínimo; sin coordenadas, permiso o alias en terceros. Cifrado de punta a punta para cualquier contenido no público; FCM **no ofrece E2EE integrada para data payload**, por lo que cifrado propio sería requisito posterior.
4. **Dispositivo A como autoridad final:** inbox D-09 local, acuse firmado, ratificación de relación A→B al liberar; secuencia de revocación observable. Ninguna información de caché externa autoriza ubicación.
5. **Coste del sistema completo a 0 €:** FCM `Cloud Messaging` publicado **sin coste**, Workers Free `100000 solicitudes/día` y `10 ms CPU/petición` en documentación del 12/10/2026; no se ha probado un envío OAuth firmado dentro de esos límites, ni verificado políticas de datos, cargos de red de usuarios, necesidad de tarjeta, caducidad de gratuidad, operaciones de cuenta/proyecto y mantenimiento. Un plan gratuito con cuota **puede fallar por cuota**; si la única salida exige pago, **NO cumple** presupuesto. ntfy declara gratuidad pública best effort sujeta a límites/términos; ICE/TURN no garantiza coste cero integral.
6. **Jurisdicción/retención/menores:** contrato/DPA, roles responsable/encargado, ámbito de tratamiento, transferencias, retención de logs/tokens, supresión y soporte de derechos por cada proveedor, con criterio jurídico contextual a España; **NO CONFIRMADOS** para una combinación concreta.
7. **Continuidad y salida:** rotación tokens, cambio de proveedor sin resucitar vínculos, denegación segura ante outage/cuota/revocación, exportación/borrado de metadatos, no depender de upgrade de pago. La ausencia de SLA se acepta (L-02c), la falsedad de acuses no.

**No asumir que un worker gratis es “sin infraestructura”:** sigue siendo infraestructura externa gestionada por un tercero y **requiere autorización posterior** de cuenta, credenciales, proveedor y operación. Tampoco es lícito reemplazarlo tácitamente por el servidor Linux compartido con CRM: expresamente excluido en #41/#52.

## 6. Pruebas negativas exigibles tras autorización posterior — NINGUNA EJECUTADA

| Prueba futura con identidades/datos ficticios | Observación obligatoria |
|---|---|
| App A force-stopped / Doze / sin permiso de ubicación background; avisos FCM de distintas prioridades | Medir recepción, ejecución real y excepción Android; sin éxito falso ni captura forzada |
| A offline al solicitar; reconecta antes de timeout/TTL, FCM `ttl=0` o ntfy `Cache:no` | **No** capturar ni entregar posición diferida; si época original no verificable, denegar |
| Éxito HTTP del broker/FCM sin app A ejecutada | **No** emitir acuse D-09 “recibida” ni nueva posición |
| Emisor recibe B sin firma, QR copiado, certificado caducado, abuso desde IP compartida | Rechazar abuso sin enumerar ID; medir falsos positivos con familia legítima |
| Revocación en A antes de liberar con sender/aviso retrasado | A descarta consulta o respuesta; un antiguo certificado de envío no reautoriza |
| ntfy tópico público adivinado, 2 atacantes publican, Google FCM habilitado/deshabilitado | Sin exfiltración ni spam no mitigado; broker logs/token/cuerpo tratados según contrato |
| Workers Free excede cuota / CPU 10 ms / FCM token inválido / cambio plan a pago | Fallo cerrado, **no cargo automático**, no acuses ni permisos ficticios |
| Restored backup Android / reinstalación A y B / token FCM renovado | Identidad WHEREIS nueva, sin recuperar acceso; sin usar token técnico obsoleto |
| Firebase Installation ID borrada, registros de IP/tema ntfy y logs Worker | Evidencia de plazo real de supresión, no inferir desde `Cache: no` o `ttl=0` |
| Sin mapa/red externa, datos de menores sintéticos, SDK/servicio no autorizado | No ubicación externa persistente, no datos sensibles en logs; atribución y licencias verificables |

**Todo PENDIENTE:** capturas/red en dispositivos reales, pruebas de servicio gratuito, geolocalización Android, validación de coste, términos y retención jurídica, CI/QA sobre producto, rendimiento, protección de menores y seguridad. No programar para obtener evidencia sin issue y autorización diferenciada.

## 7. Conclusión y decisiones siguientes — TECH LEAD / PROPIETARIO

**Resultado del estudio:** bajo L-02b/c/d hay **dos vías de investigación prioritaria**, ninguna adoptable todavía: **A (emisor serverless gratuito + FCM, para estudiar credenciales, cuotas y metadatos)**; **B (ntfy con caché deshabilitada, para contrastar arquitectura sin credencial FCM propia y sus pérdidas de disponibilidad/privacidad)**. C (ICE/STUN) es complemento eventual, **no** mecanismo de despertar. Esto **NO equivale a elegir FCM, Cloudflare o ntfy** ni a aceptar almacenamiento persistente de Firebase Installation IDs. La solución integral segura a 0 € y con consulta remota esencial sigue **NO DEMOSTRADA**.

**Decisiones materiales concretas que deberá preparar TECH LEAD para PROPIETARIO antes de cualquier uso:**
- **P-52a — Metadatos persistentes de terceros:** ¿pueden aceptarse tokens/identificadores técnicos **no efímeros** de FCM, sabiendo que Google declara retención de Firebase Installation IDs hasta su supresión y limpieza posterior de hasta 180 días? De no aceptarse, el candidato A podría no superar L-02b incluso sin coordenadas almacenadas.
- **P-52b — Emisor y proveedor concreto:** cuenta/proyecto Firebase y un entorno externo confiable (ej. Workers Free) **o** broker ntfy público, con jurisdicción, políticas y ausencia de pago acreditadas por cada proveedor; elegir requiere **nueva aprobación**. No se autoriza con este documento.
- **P-52c — Defensa de abuso sin directorio externo:** aceptar o revisar un protocolo de vinculación y autorización de emisión que evite permitir que un B revocado despierte A o abuse del servicio; determinar si ciertos metadatos técnicos de revocación externos serían admisibles, ya que guardar relaciones fuera de A contradice la regla vigente.
- **P-52d — Evidencia mínima de viabilidad:** autorizar, cuando estén resueltos los gates, ensayo delimitado y controlado de recepción real Android, época de conectividad D-12, acuse D-09 y coste sin datos reales de menores; **NO autorizado ahora**.

**Handoff:** ARQUITECTO deja esta ADR como **PROPUESTA**, relacionada con PR #50/#45/#34/#35 sin alterar esas superficies. **Siguiente responsable: TECH LEAD**, para revisar esta propuesta sobre el HEAD exacto, contrastar documentación de costes/privacidad y elevar decisiones reservadas a PROPIETARIO. El gate jurídico SEG-03/04 permanece en **#41 asignada a PROPIETARIO**; #24/#28 siguen pendientes. Ninguna aprobación de arquitectura, desarrollo, proveedor, servidor/CRM o timer.

## 8. Fuentes primarias de proveedores y sistema (26/10/2026, sin uso de sus APIs)

1. Google Firebase — precios, FCM producto sin coste listado: https://firebase.google.com/pricing
2. Firebase — servidor confiable y tokens que debe proteger: https://firebase.google.com/docs/cloud-messaging/server-environment
3. Firebase — FCM HTTP v1 requiere OAuth 2.0 y cuenta de servicio: https://firebase.google.com/docs/cloud-messaging/send/v1-api
4. Firebase — TTL y `ttl=0` descarta mensajes que no se pueden entregar en el momento: https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan
5. Firebase — mensajes de alta prioridad Android y posible degradación si no hay aviso visible: https://firebase.google.com/docs/cloud-messaging/android-message-priority
6. Firebase — ID instalación, retención y borrado (hasta 180 días tras solicitud): https://firebase.google.com/support/privacy/
7. Firebase — cifrado E2EE sensible no incluido de serie: https://firebase.google.com/docs/cloud-messaging/encryption
8. Cloudflare Workers — plan Free, cuotas y precio: https://developers.cloudflare.com/workers/platform/pricing/
9. Cloudflare Workers — límites Free (100 000 solicitudes/día, 10 ms CPU; 12/10/2026): https://developers.cloudflare.com/workers/platform/limits/
10. Cloudflare Workers — gestión de `Secrets` sin guardarlas en el código: https://developers.cloudflare.com/workers/configuration/secrets/
11. ntfy — `Cache: no`, `Firebase: no`, tópico público y publicación: https://docs.ntfy.sh/publish/
12. ntfy — logs de IP/tópicos, disponibilidad best effort y plan gratuito público: https://docs.ntfy.sh/faq/
13. ntfy — FCM como proveedor adicional de la app estándar: https://docs.ntfy.sh/privacy/
14. IETF — ICE y NAT traversal, sin sustituir señalización ni push: https://www.rfc-editor.org/rfc/rfc8445.html
15. Android — restricciones de ubicación en background: https://developer.android.com/develop/sensors-and-location/location/background
16. Android — restricciones de inicio de servicios foreground desde background: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start

**Todo lo anterior es análisis; no representa autorización de configuración, contratación, uso, despliegue o pruebas de proveedores.**
