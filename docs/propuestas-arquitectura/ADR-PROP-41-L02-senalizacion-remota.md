# ADR-PROP-41-L02 — Canales externos de señalización para consulta familiar remota

- **Estado:** PROPUESTA / COMPARACIÓN ANALÍTICA, NO APROBADA. Ningún proveedor, SDK, API, cuenta, infraestructura ni servicio se ha adoptado o probado.
- **Clasificación:** MATERIAL — arquitectura, comunicaciones, datos de menores, disponibilidad, terceros y coste.
- **Decisión fuente:** [#41, L-02 CONFIRMADA por PROPIETARIO, 25/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6399627418).
- **Handoff:** [#41, TECH LEAD a ARQUITECTO, 25/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6399767087).
- **Documentos relacionados:** [PR #45, estudio local-only](https://github.com/mundoinformaticacanaria/whereis/pull/45), [PR #34, identidad/revocación](https://github.com/mundoinformaticacanaria/whereis/pull/34), [PR #35, Android/D-12](https://github.com/mundoinformaticacanaria/whereis/pull/35), [#24 SEG-01–07](https://github.com/mundoinformaticacanaria/whereis/issues/24), [#19 D-09](https://github.com/mundoinformaticacanaria/whereis/issues/19), [#20 D-10](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#28 gates](https://github.com/mundoinformaticacanaria/whereis/issues/28).
- **Fuente de verdad:** instrucciones y decisiones en el repositorio GitHub. Las fuentes públicas siguientes solo acreditan comportamientos publicados de terceros a fecha 25/10/2026; condiciones sujetas a cambio.

## 1. Invariantes CONFIRMADOS de producto

1. Consulta de ubicación **remota familiar a distancia esencial**: L-01 (limitar la app a LAN/proximidad) **NO aprobada**. No prometer que toda red, estado Android o teléfono desconectado responda.
2. Identidad, relaciones, autorizaciones, alias y datos de ubicación **persistentes exclusivamente dentro de instalaciones de teléfonos participantes**. Solo última ubicación legítimamente obtenida por dispositivo conocido en B; sin historial de posiciones en terceros (D-10), nueva instalación sin restore de identidad/ubicación/autorización (D-04).
3. Coste incremental de operación **0 €**, ningún gasto ni contratación exigida; la posible modalidad gratuita de un servicio NO autoriza usarlo. No existe proveedor elegido.
4. L-02 permite **únicamente estudiar** intermediarios/canales externos de señalización, avisos, NAT traversal y entrega; **NO** dar de alta cuenta, SDK ni usar endpoint, credencial, infraestructura, servicio de pago o gratuito. Antes de cada alternativa concreta, decisión MATERIAL posterior del PROPIETARIO.
5. SEG-01/02: instalación solicitante auténtica y permiso unidireccional actual verificado en la autoridad de A; sin verificador disponible, **ninguna ubicación nueva**. Opción B anti-enumeración: ID inexistente y no divulgable no distinguibles para actor sin derecho. No confundir ID o QR con credencial.
6. D-09: solicitud de vinculación `recibida` **solo con acuse verificable de que está disponible en la app A**, en su bandeja local, sin duplicados; caducidad 24 h; aceptar no equivale a activar el interruptor. Los reintentos de **vinculación** son distintos de las consultas de ubicación.
7. D-12: consultas de ubicación manuales, no seguimiento continuo, sin cola que capture automáticamente cuando A reconecta; la última posición en B solo se indica **anterior** con timestamp. Las notificaciones de localización desactivada en A tienen condiciones específicas (una por solicitante/24 h), no hay notificación ordinaria por consulta exitosa. Android podría impedir captura o avisos.

## 2. Cuatro mecanismos para estudiar: prestaciones y límites

| Opción, solo **candidata de estudio** | ¿Cómo ayuda a familias distantes / A no visible? | Identidad, entrega D-09, D-12 y revocación | Coste publicado / terceros y retención | Evaluación |
|---|---|---|---|---|
| **A. Firebase Cloud Messaging (FCM), push de datos** | Aviso al token del Android A pese a NAT/CGNAT; puede activar un procesamiento **limitado** bajo reglas Android; no es conexión A↔B ni transporte de posición de extremo a extremo | Envío mediante HTTP v1 exige OAuth/credenciales de entorno confiable; **no** poner service-account en APK. Sin emisor confiable no hay propuesta completa compatible con restricciones. ACK FCM = aceptado por FCM, **no** inbox disponible en A. Mensaje de actualización con `ttl=0` puede descartarse si no es entregable de inmediato, pero **NO** acredita por sí solo que Android no lo procese retrasado; validación de petición/época en A obligatoria. Prioridad alta **silenciosa** puede degradarse; no inventar notificación de consulta exitosa para sortear la política | FCM figura **sin coste** en la tabla oficial de Firebase; NO incluye demostrar coste 0 del emisor/infraestructura. Tercero Google ve tokens/identificadores Firebase, información de entrega y mensajes; su política documenta retención de IDs de instalación hasta petición de borrado y eliminación en sistemas dentro de hasta 180 días tras solicitud. No enviar coordenadas ni ID WHEREIS en claro; condiciones y transferencia pendientes | **CONDICIONAL; no implementable como sistema completo con solo dos teléfonos bajo requisitos actuales sin explicar emisor seguro/operación** |
| **B. Broker de avisos externo con mensajes efímeros: ntfy.sh, ejemplo concreto** | Publicación HTTP en tópico y recepción por suscripción; puede esquivar entrada directa IPv4/CGNAT; **no** garantiza despertar app en Android, según método cliente usado; ntfy.sh puede usar FCM para notificaciones Android | Tópicos públicos no prueban identidad ni autorización. Elegir nombres aleatorios opacos y **cifrado de extremo a extremo de payload** sería requisito de diseño, no protección demostrada; antiabuso y anti-enumeración. `Cache: no` documenta entrega solo a conectados, sin almacenar en cache de mensajes; ello reduce entrega diferida pero también disponibilidad. ACK HTTP de broker **no** equivale a inbox A. A debe deduplicar, validar firma/edad/época y confirmar inbox, sin capturar tras reconexión | Documentación pública permite uso anónimo gratuito sujeto a términos/rate limits (250 mensajes/día en ntfy.sh según docs actuales), **sin SLA**. Por defecto cachea mensajes **12 h**, a menos que se solicite no guardar; su privacidad indica IP/tópicos y registros técnicos. No se ha verificado política de retención de todos los componentes FCM/cliente en combinación; `Cache: no` no demuestra cero metadatos externos | **CANDIDATO solo documental**, mayor riesgo de tópicos, metadatos y dependencia; no autorizado y sin compatibilidad Android confirmada |
| **C. Señalización efímera + ICE/STUN/WebRTC P2P** | Canal externo intercambia candidatos/direcciones y establece si es posible un enlace cifrado directo entre A y B. Supera **algunos**, no todos, escenarios NAT; A/B deben tener conectividad y app receptiva. STUN no es relay ni sistema de push | Señalización requiere **otro canal** previo, no nace espontáneamente de STUN; prueba de identidad y autorizaciones permanece en A. ACK de signaling no es acuse D-09. Sesión/época corta, solicitudes no encoladas para reconexión. Puede fallar tras CGNAT/NAT simétrico/firewall | WebRTC es tecnología, **no oferta gratuita** de un servicio STUN/rendezvous. Operar/usarlo necesita endpoint administrado por alguien, con política de IP/puertos/candidatos, costes y licencias; ninguno elegido o autorizado. Compartir IP públicas/privadas y patrones de conectividad puede ser sensible | **CONDICIONAL** en topologías favorables; no satisface por sí sola objetivo remoto familiar ni wakeup A dormido |
| **D. TURN/relay externo + señalización y opcional push** | Retransmite paquetes cuando P2P falla, ayudando en NAT/CGNAT; enlace A↔relay↔B requiere ambos participantes conectados y A capaz de ejecutar. TURN **no despierta** por sí solo un Android suspendido | Autoridad y `Release` siguen en A; cifra extremo a extremo los datos, no confiar en relay ni almacenar coordenadas en él. Un relay puede ver IP/timing/volumen y un broker la señalización; ACK de relay tampoco acredita bandeja D-09. TTL/eventos de consulta sujetos a epoch original | El software TURN puede ser libre, pero operación/transferencia/banda ancha del relay **no se ha demostrado gratis, estable ni sin contratación**. Exigir datos completos de cuotas, política de retención, región, SLA, autenticación, seguridad y términos; sin proveedor seleccionado | **CONDICIONAL, no elegible todavía**; coste 0 permanente no acreditado, requiere tercero e infraestructura y no cubre push/background |

**Fuentes de hechos concretos**: precio y envío FCM [1–4]; prioridades/TTL [3–5]; Firebase y datos [6]; ntfy público, cache, límites, privacidad y términos [7–11]; ICE/WebRTC/STUN/TURN [12–13]; permisos Android [14–15]. Referencias URL completas al final.

### Por qué 0 € anunciado no acredita 0 € funcional

- FCM = precio de **mensajería**, no de una arquitectura completa; el endpoint HTTP v1 con privilegios de envío no debería exponerse a teléfonos no confiables. Faltan solución segura de **quién envía y autoriza** y condiciones de cualquier componente externo.
- ntfy público = operación no contratada posible en condiciones publicadas, pero no necesariamente estabilidad de términos, fiabilidad, privacidad ni servicios complementarios. En especial un tópico público no se convierte en autenticación por conocer su URL.
- ICE/STUN = establecimiento condicionado por la topología; TURN paga o consume recursos de un tercero; ni el hecho de que existan servidores públicos ni software libre acredita gratuidad contractual estable.
- Una conexión móvil/Wi-Fi del usuario ya disponible es un **supuesto**, no prueba de inexistencia de cargos por datos ni de cobertura de operadores.
- Almacenar la ubicación solo en A/B **no significa que terceros no traten identificadores, tokens, IP, latencia, mensajes o metadatos**; requiere evaluación en #41 y autorización humana antes de adoptar.

## 3. Arquitectura de seguridad propuesta, neutral a proveedor

```text
Teléfono B (consulta manual)  -- [canal externo de AVISO / señalización, opcional y NO AUTORIZADO] -->  Teléfono A
   B mantiene última posición       sin coordenadas; requestId opaco                              A conserva permiso A→B local
   B crea petición efímera            no decide consentimiento                                     A recibe y valida identidad B
   B espera ACK auténtico de A        no inventar ACK "recibida"                                    A valida permiso vigente
   B acepta una sola respuesta        no re-ejecutar tras reconnect                                 A captura una vez (Android permite)
   B muestra timestamp real          canal cifrado A→B (directo o relay candidato)                 A revalida antes de liberar
```

- **Identidad inicial:** vinculación auténtica de clave pública de cada instalación mediante procedimiento aún PENDIENTE (QR/ID copiado solo presenta información pública). Las credenciales privadas permanecen en cada teléfono, no recuperables en reinstalación; no incrustar secreto de envío de un proyecto externo en APK distribuido.
- **Aviso efímero, no localización:** como máximo `requestId` opaco aleatorio, destinatario/pseudónimo mínimo, nonce, deadline y metadatos indispensables. Sin coordenadas, alias de menores, listas de familias, estado de permisos ni tokens secretos en payload legible del tercero. No suponer que un `requestId` opaco impide inferir relaciones o patrones de tráfico.
- **Autoridad local A:** `Grant`/ `Revoke`/ `Block` serializados con `Release` final de cada resultado; si no puede verificarse instalación auténtica y permiso efectivo, denegar. `Release` realizado antes de revocar puede ser entregado físicamente después; documentar límite de redes distribuidas y control adicional en B.
- **D-09 / acuses:** una solicitud de vinculación enviada por broker/push se considera `recibida` solo después de almacenarse en la bandeja local de A y generarse acuse auténtico de A. Sin acuse, `entrega no confirmada`, no `rechazada`. Repetir con el mismo ID, sin reabrir 24 h ni activar permisos.
- **D-12 / no diferir:** consulta de ubicación de B no se transforma en job durable ni se ejecuta tras reconexión de A. No basta `expiresAt`, TTL0 ni la ausencia de cache en un broker: verificar `requestId` y **aceptación en la misma época viva original**, cerrar intento tras pérdida real de conectividad y exigir acción manual nueva. La demostración de epoch bajo Doze, reconexiones invisibles o notificaciones retrasadas **NO EXISTE**; si no se puede demostrar, elevar incompatibilidad y no prometer éxito.
- **Android background:** permisos `ACCESS_BACKGROUND_LOCATION`, restricciones FGS y `POST_NOTIFICATIONS` según API/target; ni FCM de prioridad alta ni socket/relay constituyen bypass de Android. No usar alta prioridad silenciosa repetitiva para seguimiento encubierto. El móvil A puede no estar operativo para capturar.
- **No enumeración:** todo punto de verificación de ID frente a tercero o aplicación debe resistir diferencias observables (cuerpo, código, tiempo, destinatario, canal, topic). Sin directorio seguro y sin autenticación previa, podría requerirse ajustar el flujo D-09 mediante decisión de FUNCIONAL/PROPIETARIO. No degradar opción B para facilitar el canal.
- **Minimización/supresión:** A almacena localmente autorización y solicitudes; B almacena localmente solo última ubicación legítima. Los terceros pueden conservar IDs técnicos/metadatos aun si no ven coordenadas; la política de borrado del proveedor requiere valoración específica, especial protección de menores y decisión #41.

## 4. Matriz de fallos y verificaciones — PRUEBAS PROPUESTAS, NO EJECUTADAS

| Escenario adversarial | Criterio verificable de aceptación/rechazo | Mecanismos afectados |
|---|---|---|
| A desconectado; aviso se publica; A reconecta **antes del TTL** | Ninguna captura diferida del intento B original; solo nueva solicitud manual | Todos; FCM TTL0 / ntfy Cache:no son defensas parciales, no prueba suficiente |
| FCM responde éxito de `messages:send`, Android no recibe | B NO declara `recibida` ni ubicación; no inferir conexión de A | A |
| FCM high priority silenciosa degradada/delegada por Play Services | No activar modo de seguimiento ni elevar privilegios; timeout sin datos nuevos | A |
| ntfy topic adivinada/suscrita por atacante o paquete duplicado | Sin coordenadas ni autorización sin clave; no filtrar IDs por respuesta o topic, deduplicación | B |
| P2P ICE falla por CGNAT/firewall y no hay TURN aprobado | Falla cerrado; no suponer camino directo ni geolocalización | C |
| Relay TURN recibe tráfico cifrado pero registra IP/timing | Identificar y minimizar metadatos; aprobación de protección de datos antes de adopción | D |
| A acepta D-09 pero no habilita interruptor A→B | Conocido sin permiso; cualquier petición de ubicación denegada | Todos |
| Revocar permiso en A después de capturar y **antes** de liberar | Sin entrega de nueva ubicación; descartar resultado preparado y reintentos | Todos |
| Copiar QR/ID, instalar C, restaurar backup de B | Sin autenticación ni herencia de permiso; nueva instalación sin ID anterior | Todos |
| A con ubicación Android denegada, API 34+, Doze o force-stop | No bypass ni captura garantizada; error genérico, última legítima anterior fechada | Todos |
| Mensaje de D-09 duplicado, ACK retrasado, reloj alterado | Una pendiente, 24 h originales; «recibida» solo tras inbox A/acuse válido | Todos |
| Servicio pasa de gratuito a pago, supera límite o se cae | No coste automático ni pérdida de seguridad; fail-closed, evaluar retirada | A–D |

**Evidencia NO obtenida:** prueba Android u OEM, envío de mensajes FCM, suscripción ntfy, test de ICE/TURN, tarifas contractuales aplicables al despliegue, acceso/permiso de cuentas, latencias, volumen de datos, SLA, borrado real, tratamiento transfronterizo, evaluación jurídica. Nada en esta ADR acredita tecnología lista para producción o autorización de uso.

## 5. Decisiones específicas reservadas al PROPIETARIO

- **L-02a: canal de señalización prioritario para investigación posterior.** TECH LEAD podrá proponer uno o combinar dos **solo tras** contrastar seguridad, necesidad de emisor privilegiado, dependencia externa, Android no visible, retención de IDs/IP, coste incremental 0 € verificable y términos. Esta ADR **no elige** A–D ni aprueba cuentas/API/servicios.
- **L-02b: metadatos y tratamiento externo aceptable.** Sin guardar ubicaciones fuera de teléfonos, ¿puede un proveedor procesar/retener temporalmente tokens, IP, mensajes cifrados o metadatos de solicitud? ¿Cuánto, en qué región, con qué mecanismos de supresión? Requiere decisión expresa y revisión jurídica contextual (uso familiar de menores en España).
- **L-02c: requisitos de disponibilidad.** Si un proveedor gratis no tiene SLA y Android limita recepciones, ¿qué degradación/frecuencia de fallo es aceptable sin modificar la consulta remota esencial? No se presupone un SLA.
- **L-02d: gestión segura de claves/cuentas.** Si el canal exige credenciales privilegiadas de envío, ¿se permite estudiar/componer un servicio de autorización/salida que no almacene ubicaciones? Sería **nueva** autorización de infraestructura/coste/proveedor; no debe incrustarse en el APK como atajo.

**Handoff técnico recomendado:** TECH LEAD revisar matriz y HEAD, delimitar una alternativa con riesgos documentados y **elevar propuesta concreta al PROPIETARIO** antes de cualquier cuenta, proveedor, SDK, acceso API o prueba real. Si no puede demostrarse solución de coste 0 que preserve requisitos, devolver alternativas de alcance/garantías al PROPIETARIO; no reducir por decisión técnica autónoma.

## 6. Fuentes oficiales públicas, solo para hechos externos

1. Firebase — precios públicos, FCM como producto sin coste listado: https://firebase.google.com/pricing
2. Firebase — FCM HTTP v1, OAuth y emisor de confianza: https://firebase.google.com/docs/cloud-messaging/send/v1-api
3. Firebase — prioridad Android, degradación/abuso de high-priority: https://firebase.google.com/docs/cloud-messaging/android-message-priority
4. Firebase — entrega, cola, TTL y TTL=0: https://firebase.google.com/docs/cloud-messaging/customize-messages/setting-message-lifespan
5. Firebase — recepción Android con app en background: https://firebase.google.com/docs/cloud-messaging/android/receive-messages
6. Firebase — tratamiento IDs técnicos y retención: https://firebase.google.com/support/privacy
7. ntfy — envío, tópico público y límites: https://docs.ntfy.sh/publish/
8. ntfy — cache de mensajes, `Cache: no`: https://docs.ntfy.sh/config/ y https://docs.ntfy.sh/publish/
9. ntfy — servicio de alojamiento y datos/IP/tópicos: https://docs.ntfy.sh/privacy/
10. ntfy — plan sin cuenta y términos: https://docs.ntfy.sh/terms/
11. ntfy — condiciones de disponibilidad y Firebase bajo ntfy.sh: https://docs.ntfy.sh/faq/
12. IETF RFC 8445 — ICE, STUN, TURN y NAT: https://www.rfc-editor.org/rfc/rfc8445.html
13. WebRTC — peer connection, ICE y necesidad de signaling: https://webrtc.org/getting-started/peer-connections
14. Android — restricciones de foreground service/background: https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start
15. Android — permisos location FGS y Android 14: https://developer.android.com/about/versions/14/changes/fgs-types-required

**Conclusión:** autorizar **un estudio** de tercero no concede **uso**. Los cuatro mecanismos son opciones de análisis; ninguno está comprobado como solución completa de WHEREIS a 0 €, segura, fiable, legalmente validada y sin persistencia externa de ubicaciones. La aprobación y cualquier ejecución posterior corresponden al PROPIETARIO y a las gates de TECH LEAD/QA.
