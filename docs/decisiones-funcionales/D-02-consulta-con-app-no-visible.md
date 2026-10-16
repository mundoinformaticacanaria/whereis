# D-02 — Consulta puntual con Whereis no visible en el dispositivo emisor

- **Fecha de aprobación del Propietario:** 15/10/2026.
- **Estado de la decisión funcional:** `CONFIRMADO` por aprobación expresa del Propietario; incorporación a `main` pendiente de revisión/merge.
- **Clasificación:** `MATERIAL`.
- **Fuente de trazabilidad:** [Issue #2](https://github.com/mundoinformaticacanaria/whereis/issues/2), relacionada con [D-01 / Issue #1](https://github.com/mundoinformaticacanaria/whereis/issues/1).
- **Origen:** aprobación explícita del Propietario en la conversación del 15/10/2026.
- **Baseline funcional del proyecto:** `PENDIENTE`; esta decisión no aprueba el MVP completo.
- **Decisiones sustituidas (`SUPERSEDED`):** ninguna registrada.

## Necesidad

Permitir a B consultar la posición puntual del dispositivo A autorizado incluso si A no tiene Whereis visible en pantalla, evitando que la solución realice seguimiento continuo.

## Actores

- **A:** dispositivo Android que autoriza compartir su ubicación.
- **B:** dispositivo Android previamente autorizado que solicita la consulta.

## Comportamiento CONFIRMADO

1. B puede intentar solicitar una **ubicación puntual de A aunque Whereis no esté visible en la pantalla de A**.
2. No es necesario exigir a la persona que maneja A que abra manualmente Whereis ni que acepte cada consulta si la autorización sigue vigente.
3. Cada nueva consulta o pulsación manual de «Actualizar ubicación» intenta obtener una **nueva posición en el momento de la solicitud**.
4. No habrá seguimiento continuo ni actualizaciones automáticas periódicas.
5. El funcionamiento depende de **permisos concedidos, conectividad y restricciones del sistema Android**. No se promete respuesta inmediata ni disponibilidad garantizada.
6. Si no se consigue una nueva posición, el resultado debe informar de la imposibilidad y **nunca presentar una posición anterior como actual**.

## Reglas funcionales

- La ejecución en segundo plano **no elimina** la necesidad de una autorización funcional previa entre A y B.
- Permiso de Android y autorización de Whereis son conceptos separados; ambos deben permitir la operación.
- No debe generarse ubicación de manera periódica por el solo hecho de que la autorización esté activa.
- La ausencia de respuesta no constituye prueba de ubicación actual.

## Criterios de aceptación propuestos para desarrollo posterior

- **D02-CA01:** con B autorizado, si A tiene la app no visible y Android permite la operación, una consulta de B intenta obtener una nueva posición.
- **D02-CA02:** las consultas de B no exigen aceptación interactiva adicional en A mientras siga vigente su autorización.
- **D02-CA03:** tras una consulta puntual no continúa una actualización periódica automática.
- **D02-CA04:** si A está apagado, sin conectividad, carece de permisos válidos o el sistema impide capturar/responder, B no recibe una nueva ubicación inventada ni una antigua etiquetada como actual.
- **D02-CA05:** el botón «Actualizar ubicación» inicia un intento nuevo, no un modo de seguimiento.

## Validaciones, errores y excepciones

- **Ubicación y permisos desactivados:** no puede prometerse una posición recién capturada.
- **Dispositivo apagado o desconectado:** no es posible recibir una ubicación nueva remota mientras dure esa condición.
- **Restricciones Android, aplicación detenida forzosamente o ejecución limitada:** pueden impedir o retrasar las consultas; el tratamiento exacto queda sujeto a validación técnica.
- **Ubicación anterior:** **D-06 / issue #12, CONFIRMADA posteriormente**, concreta que al fallar una consulta autorizada se muestra el aviso de fallo y, si existe, la última posición conocida con su fecha/hora y advertencia visible de que **no es actual**. Si nunca hubo posición válida, se muestra «Ubicación no disponible». **Caducidad y retención general** continúan `PENDIENTES`. Esta precisión mantiene la prohibición de presentar datos antiguos como actuales.

## PENDIENTE de contraste técnico y definición posterior

- Versiones de Android y alcance real de ejecución con app no visible, cerrada o forzosamente detenida.
- Permisos, requisitos de plataforma y de distribución de la aplicación.
- Mecanismo técnico de solicitud/respuesta y requisitos de conexión, sin proveedor seleccionado.
- Tiempo de espera, reintentos, precisión y mensajes de error detallados; tratamiento de **último dato conocido** ya fijado funcionalmente por **D-06**, mientras que política general de **retención** y almacenamiento siguen `PENDIENTE`.
- Evaluación del efecto sobre batería, privacidad, seguridad y costes.
- **D-03 a D-05:** las decisiones funcionales ya constan como **CONFIRMADAS** en [D-03 #6](https://github.com/mundoinformaticacanaria/whereis/issues/6), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8) y [D-05 #10](https://github.com/mundoinformaticacanaria/whereis/issues/10); sincronización y viabilidad técnicas permanecen `PENDIENTE`.

## Impacto y límites

- **Alcance:** localización remota puntual, no navegación en tiempo real.
- **Privacidad:** solo peticiones autorizadas.
- **Arquitectura/operación:** evaluación `PENDIENTE` por `ARQUITECTO` y `TECH LEAD`.
- Ningún stack, proveedor, infraestructura o estrategia de persistencia resulta aprobado por este documento.

## Handoff

**TECH LEAD**, rol técnico activo según G-01 V3, debe validar la viabilidad técnica (incluidos ciclo de vida Android, permisos y comunicaciones) antes de la planificación; una especialidad adicional requerirá autorización específica. Esta decisión no constituye por sí sola autorización para programar.

La descripción funcional del fallo de consulta queda trazada en [D-06 / issue #12](https://github.com/mundoinformaticacanaria/whereis/issues/12) y [PR #13](https://github.com/mundoinformaticacanaria/whereis/pull/13).
