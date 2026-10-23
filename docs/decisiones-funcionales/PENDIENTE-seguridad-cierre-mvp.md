# Seguridad y cierre del MVP — decisiones SEG y pendientes materiales

- **Origen:** [issue #24 y sus comentarios](https://github.com/mundoinformaticacanaria/whereis/issues/24), fuente viva y prevalente sobre este documento.
- **Actualización:** 23/10/2026, conciliación de decisiones aprobadas el 19/10/2026 y conflicto elevado al PROPIETARIO el 23/10/2026.
- **Clasificación:** MATERIAL; **estado mixto** por subdecisión (no todo PENDIENTE).
- **Integración:** documentación funcional para revisión TECH LEAD; **baseline MVP global, programación, infraestructura y proveedores NO AUTORIZADOS**.

## Estado inequívoco por subdecisión

| Subdecisión | Estado confirmado por el PROPIETARIO | Pendientes reales |
|---|---|---|
| **SEG-01 — Fallo seguro** | **CONFIRMADO 19/10/2026**. No entregar una nueva ubicación si no puede verificarse autorización direccional vigente; solo posición previa legítima, fechada/anterior si D-09/D-10 permiten mostrarla | Mecanismo y momento de validación, concurrencia/revocación sin conexión; no prometer revocación instantánea |
| **SEG-02 — Identidad de instalación** | **CONFIRMADO 19/10/2026**. ID/QR no autentica; cada instalación y relación autorizada necesitan prueba auténtica y medidas contra suplantación, replay, enumeración y abuso | Arquitectura/criptografía, límites verificables, costes, pruebas negativas; **conflicto D-09 «ID no encontrado» aún sin decisión** |
| **SEG-03 — Modo para menores** | **CONFIRMADO 19/10/2026**: por ahora **no** se incluye un modo familiar diferenciado; mismos flujos ordinarios sin privilegios parentales automáticos | **PENDIENTE** revisión jurídica y técnica sobre menores, legitimación/representación, información, controles, derechos, minimización, conservación y borrado; no habilita acceso oculto |
| **SEG-04 — Reinstalación y backup** | **CONFIRMADO 19/10/2026**: la nueva instalación empieza con nuevo ID, sin recuperar ubicaciones ni permisos desde backup; el consultante no reinstalado puede conservar su última posición legítima de emisor desinstalado (D-10) | Estrategia Android/backup, datos externos, retención legal, borrado verificable y seguridad del almacenamiento |
| **SEG-05 — Android y avisos** | **PENDIENTE** de viabilidad y, si altera comportamiento, aprobación material adicional | Permisos/versiones y ejecución no visible, notificaciones por solicitante/24 h, reinicio de límites, batería |
| **SEG-06 — Acuses/conectividad** | **PENDIENTE técnico** con reglas funcionales de D-09/D-12 ya confirmadas | «Recibida» en app versus notificación, idempotencia, estado remoto realmente verificable, garantías offline y sincronización |
| **SEG-07 — Mapas/direcciones/proveedores** | **PENDIENTE** | Licencias, atribuciones, servicios de teselas/geocodificación, coste, disponibilidad, proveedor/infrastructura y autorización humana |

**Precedencia:** SEG-01 y SEG-02 se aplican a **todas** las consultas de ubicación nueva, incluso si la interfaz o caché declara un interruptor activado. Ante autorización o identidad no verificable, no hay nueva ubicación. Conservar una ubicación anterior **no** equivale a recuperar autorizaciones ni a historiar. No alterar D-09 sin decisión humana nueva.

## Conflicto material D-09 / SEG-02 — siguiente acción PROPIETARIO

El [comentario TECH LEAD del 23/10/2026 en #24](https://github.com/mundoinformaticacanaria/whereis/issues/24) contrasta el texto «ID no encontrado» aprobado en D-09 con la protección frente a enumeración exigida por SEG-02. **No hay opción A/B aprobada aún.**

- **A propuesta:** conservar el mensaje D-09 y exigir defensas antiabuso demostrables; persistiría riesgo residual de revelar existencia.
- **B propuesta:** mensaje indistinguible para identificadores inexistentes/no verificables en consulta no autenticada, modificando la UX D-09 por decisión expresa del PROPIETARIO.
- **No se elige ninguna opción en esta PR.** Continúan vigentes tanto el mensaje de D-09 como la obligación SEG-02; cualquier incompatibilidad para implementación bloquea resolverla por intuición. Mantener issue #24 etiquetada **PROPIETARIO** hasta su decisión.

## Criterios funcionales mínimos y verificación posterior

1. Solo el ID/QR copiado no permite consultar ubicación ajena; intento de suplantación/replay o permiso no verificable no entrega nueva posición (**SEG-01/02**).
2. Revocación y consultas concurrentes, con red intermitente, se someten a comprobación de autorización vigente en un punto efectivo de control; no fingir eficacia remota instantánea.
3. Solicitud aceptada desde desconocido da de alta como conocido **sin** permiso; bloqueo impide consultas/solicitudes y desbloqueo no reautoriza (D-09).
4. Reinstalación con backup no recupera ID, permisos ni última posición en el dispositivo reinstalado; el consultante no reinstalado puede conservar el último dato legítimo anterior (SEG-04/D-10).
5. El tratamiento de datos de menores y la retención efectiva requieren revisión legal antes del baseline global; preferir seguridad del menor no implica renunciar a garantías aplicables.
6. Validar con TECH LEAD/ARQUITECTO límites Android, latencia, conectividad, privacidad y costes; QA independiente y controles de CI/gates siguen exigibles antes de código real.

## Handoff y límites

- **PROPIETARIO:** decisión A/B sobre D-09/SEG-02 y demás autorizaciones materiales reservadas.
- **TECH LEAD / ARQUITECTO (activo por G-02):** evaluación, trazabilidad, alternativas técnicas y seguridad, sin autoaprobar gastos ni requisitos.
- **FUNCIONAL:** conciliación de contratos y criterios, sin cambiar el mensaje D-09 por intuición.
- **QA:** independiente si llega a haber implementación autorizada.
- **Estado global:** #24 abierta, baseline funcional y arquitectónico PENDIENTES, gates #28 PENDIENTES, **NO ASIGNAR PROGRAMADOR ni activar timer**.
