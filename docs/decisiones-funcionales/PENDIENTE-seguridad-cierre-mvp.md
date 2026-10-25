# Seguridad y cierre del MVP — decisiones SEG y pendientes materiales

- **Origen:** [issue #24 y sus comentarios](https://github.com/mundoinformaticacanaria/whereis/issues/24), fuente viva y prevalente sobre este documento.
- **Actualización:** 25/10/2026, conciliación de SEG-01–04, opción B confirmada en D-09/SEG-02 el 23/10/2026 y restricciones locales/coste cero confirmadas el 25/10/2026 en [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41).
- **Clasificación:** MATERIAL; **estado mixto** por subdecisión (no todo PENDIENTE).
- **Integración:** documentación funcional para revisión TECH LEAD; **baseline MVP global, programación, infraestructura y proveedores NO AUTORIZADOS**.

## Estado inequívoco por subdecisión

| Subdecisión | Estado confirmado por el PROPIETARIO | Pendientes reales |
|---|---|---|
| **SEG-01 — Fallo seguro** | **CONFIRMADO 19/10/2026**. No entregar una nueva ubicación si no puede verificarse autorización direccional vigente; solo posición previa legítima, fechada/anterior si D-09/D-10 permiten mostrarla | Mecanismo y momento de validación, concurrencia/revocación sin conexión; no prometer revocación instantánea |
| **SEG-02 — Identidad y opción B** | **CONFIRMADO 19/10/2026:** ID/QR no autentica; instalación y relación requieren prueba auténtica, protección contra suplantación, replay, enumeración y abuso. **CONFIRMADO 23/10/2026:** opción **B**; no revelar existencia del ID ante actor no autenticado o sin derecho a conocerla, con resultado indistinguible entre inexistente y existente no divulgable/verificable | Arquitectura y controles medibles de antiabuso, viabilidad de descubrimiento remoto/local, prueba de no filtración por texto/códigos/metadatos/latencia, derechos de conocimiento, costes y revisión QA; SEG-02 **no cerrado técnicamente** |
| **SEG-03 — Modo para menores** | **CONFIRMADO 19/10/2026**: por ahora **no** se incluye un modo familiar diferenciado; mismos flujos ordinarios sin privilegios parentales automáticos | **PENDIENTE** revisión jurídica y técnica sobre menores, legitimación/representación, información, controles, derechos, minimización, conservación y borrado; no habilita acceso oculto |
| **SEG-04 — Reinstalación y backup** | **CONFIRMADO 19/10/2026**: la nueva instalación empieza con nuevo ID, sin recuperar ubicaciones ni permisos desde backup; el consultante no reinstalado puede conservar su última posición legítima de emisor desinstalado (D-10) | Estrategia Android/backup, datos externos, retención legal, borrado verificable y seguridad del almacenamiento |
| **SEG-05 — Android y avisos** | **PENDIENTE** de viabilidad y, si altera comportamiento, aprobación material adicional | Permisos/versiones y ejecución no visible, notificaciones por solicitante/24 h, reinicio de límites, batería |
| **SEG-06 — Acuses/conectividad** | **PENDIENTE técnico** con reglas funcionales de D-09/D-12 ya confirmadas | «Recibida» en app versus notificación, idempotencia, estado remoto realmente verificable, garantías offline y sincronización |
| **SEG-07 — Mapas/direcciones/proveedores** | **PENDIENTE** selección y viabilidad. **CONFIRMADA en #41** la restricción de persistencia exclusivamente en teléfonos participantes y coste de funcionamiento 0 €, sin contratación ni nube autorizada | Licencias, atribuciones, cartografía/teselas/geocodificación local u otra alternativa sin dependencia no autorizada, viabilidad y privacidad de cualquier tercero; ningún servicio seleccionado |

**Precedencia:** SEG-01 y SEG-02 se aplican a **todas** las consultas de ubicación nueva, incluso si la interfaz o caché declara un interruptor activado. Ante autorización o identidad no verificable, no hay nueva ubicación. Conservar una ubicación anterior **no** equivale a recuperar autorizaciones ni a historiar. La modificación **concreta** de D-09 sobre revelación de existencia está autorizada mediante opción B; **ninguna otra regla** de D-09 cambia sin nueva decisión MATERIAL.

## Decisión material D-09 / SEG-02 — opción B CONFIRMADA (23/10/2026)

El [PROPIETARIO aprobó expresamente la opción B en #24](https://github.com/mundoinformaticacanaria/whereis/issues/24#issuecomment-6371711122); **A descartada** para la verificación por actores sin derecho a conocer existencia. Se **SUPERSEDE parcialmente** el mensaje antiguo «ID no encontrado» de D-09: frente a actor **no autenticado o sin derecho verificado de divulgación**, la respuesta sobre ID inexistente debe ser **indistinguible en cuanto a existencia** de la correspondiente a ID existente pero no divulgable/verificable. La regla afecta a la verificación de ID previa a alta y bloqueo, sin convertir ID/QR en credencial ni conceder permisos.

**Texto UX propuesto por FUNCIONAL, basado en orientación del PROPIETARIO:** «No se pudo verificar el identificador. Comprueba los datos e inténtalo de nuevo». El literal no fue fijado irrevocablemente por el PROPIETARIO y debe validarse como microcopy; la **indistinguibilidad** sí es requisito confirmado. Un aviso general por ausencia de red puede mostrarse si esa condición está acreditada, sin revelar existencia de un ID. Si la verificación falla, no se añade dispositivo, no se encola bloqueo preventivo ni se confiere autorización; reintento manual permitido. Los resultados para sujetos con **derecho demostrado** a conocer existencia, los criterios para demostrar ese derecho y el detalle de UX siguen **PENDIENTES** de diseño/validación; no reintroducir un oráculo.

**Invariantes intactas:** QR/ID puede usarse en vinculaciones legítimas; aceptar una solicitud solo crea conocido y la ubicación exige activar permiso individual y verificar instalación/relación; solicitudes expiran tras 24 h desde envío; rechazo/caducidad permiten nuevo intento salvo bloqueo, sin duplicar solicitudes, y un acuse requiere disponibilidad real en la app. No se autoaprueban límites nuevos ni cambios de notificación/bloqueo. La defensa contra enumeración incluye también pruebas de contenido, códigos, tamaño, tiempos, metadatos, descubrimiento IP/puertos/handshake y estado online/offline, **sin prometer igualdad exacta ni soluciones ya demostradas**. SEG-02 permanece **PENDIENTE de pruebas y arquitectura**.

**Restricción material posterior #41 (25/10/2026):** uso familiar personal en España; almacenamiento de datos de la app **solo en instalaciones participantes**, no en nube ni backend externo contratado, **funcionamiento obligatorio sin coste adicional (0 €)**. No autoriza seleccionar servicios de terceros aunque se anuncien gratuitos. La viabilidad de transporte entre teléfonos remotos, descubrimiento, mapa/geocodificación y compatibilidad de anti-enumeración debe comprobarse; la [PR #45](https://github.com/mundoinformaticacanaria/whereis/pull/45) es un **estudio PROPUESTA**, no baseline. Si los requisitos no pueden satisfacerse simultáneamente, TECH LEAD eleva alternativas al PROPIETARIO sin cambiarlos por iniciativa propia.

## Criterios funcionales mínimos y verificación posterior

1. Solo el ID/QR copiado no permite consultar ubicación ajena; intento de suplantación/replay o permiso no verificable no entrega nueva posición (**SEG-01/02**). Para un actor sin derecho a conocer existencia, ID inexistente frente a existente no divulgable/verificable no produce respuestas distinguibles por existencia, incluyendo canales laterales medibles (criterio opción B, pruebas **NO EJECUTADAS**).
2. Revocación y consultas concurrentes, con red intermitente, se someten a comprobación de autorización vigente en un punto efectivo de control; no fingir eficacia remota instantánea.
3. Solicitud aceptada desde desconocido da de alta como conocido **sin** permiso; bloqueo impide consultas/solicitudes y desbloqueo no reautoriza (D-09).
4. Reinstalación con backup no recupera ID, permisos ni última posición en el dispositivo reinstalado; el consultante no reinstalado puede conservar el último dato legítimo anterior (SEG-04/D-10).
5. El tratamiento de datos de menores y la retención efectiva requieren revisión legal antes del baseline global; preferir seguridad del menor no implica renunciar a garantías aplicables.
6. Validar con TECH LEAD/ARQUITECTO límites Android, latencia, conectividad, privacidad y **viabilidad local-only / 0 €** de #41; QA independiente y controles de CI/gates siguen exigibles antes de código real. Contrastar especialmente anti-enumeración en redes directas, acuse autenticado y revocación sin autoridad remota común; no suponer transporte autorizado.

## Handoff y límites

- **PROPIETARIO:** **ya decidió opción B** para D-09/SEG-02; conserva autoridad sobre cualquier nueva incompatibilidad, revisión jurídica SEG-03/04 y alcance local-only/0 € de #41.
- **TECH LEAD / ARQUITECTO:** evaluación de autenticidad, anti-enumeración real, transporte y pruebas negativas, sin autoaprobar gastos ni requisitos; cotejar #24, #41 y los estudios pendientes.
- **FUNCIONAL:** aplicar exclusivamente la modificación D-09 aprobada, proponer textos/estados y elevar nuevas incompatibilidades sin alterar reintentos, consentimiento ni permisos.
- **QA:** independiente si llega a haber implementación autorizada.
- **Estado global:** #24 abierta, baseline funcional y arquitectónico PENDIENTES, gates #28 PENDIENTES, **NO ASIGNAR PROGRAMADOR ni activar timer**.
