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
- **Ubicación anterior:** **D-06 / issue #12, CONFIRMADA posteriormente**, concreta que al fallar una consulta autorizada se muestra el aviso de fallo y, si existe, la última posición legítima con su fecha/hora y advertencia visible de que **no es actual**; si nunca hubo una válida, «Ubicación no disponible». **D-10 / #20** confirma conservar solo la última posición, sin historial ni caducidad funcional automática hasta la eliminación del dispositivo; **plazos legales, borrado efectivo y ubicación del almacenamiento siguen PENDIENTES**. Nunca presentar dato antiguo como actual.
- **Autorización no verificable:** **SEG-01 / #24 CONFIRMADO**: no se devuelve una ubicación nueva mientras no se pueda verificar autorización vigente; la posición anterior solo puede mostrarse según las reglas de bloqueo, eliminación y permisos ya aprobadas. **SEG-02 / #24 CONFIRMADO** exige verificar identidad auténtica de instalación y relación, no solo ID/QR.

## PENDIENTE de contraste técnico y definición posterior

- Versiones de Android y alcance real de ejecución con app no visible, cerrada o forzosamente detenida.
- Permisos, requisitos de plataforma y de distribución de la aplicación.
- Mecanismo técnico de solicitud/respuesta y requisitos de conexión, sin proveedor seleccionado.
- Umbrales técnicos de espera/timeout y ejecución de reintentos según Android siguen `PENDIENTE`. **D-12 / #22 CONFIRMADO** fija error genérico, reintentos manuales y ausencia de cola automática tras fallos; **D-13 / #23 CONFIRMADO** fija presentación de precisión disponible o su ausencia. Validar viabilidad y rendimiento sin prometer precisión o latencia garantizada.
- Evaluación del efecto sobre batería, privacidad, seguridad, protección de menores, retención legal/borrado efectivo y costes: `PENDIENTE` (#24).
- **D-03 a D-05 y D-09:** autorización individual y revocación **CONFIRMADAS** en [D-03 #6](https://github.com/mundoinformaticacanaria/whereis/issues/6), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-05 #10](https://github.com/mundoinformaticacanaria/whereis/issues/10) y ampliación [D-09 #19](https://github.com/mundoinformaticacanaria/whereis/issues/19); conocer o aceptar un dispositivo no equivale a permiso activo, y las solicitudes desde desconocidos se rigen por D-09. Autenticación, propagación, concurrencia y garantías Android continúan `PENDIENTE` de validación técnica.
- **SEG-04 / #24 CONFIRMADO:** tras reinstalación, no restaurar ID/ubicaciones/autorizaciones en la nueva instalación; las posiciones previas conservadas legítimamente en otro consultante no reinstalado pueden mantenerse conforme a [D-10 #20](https://github.com/mundoinformaticacanaria/whereis/issues/20).

## Impacto y límites

- **Alcance:** localización remota puntual, no navegación en tiempo real.
- **Privacidad:** solo peticiones autorizadas.
- **Arquitectura/operación:** evaluación `PENDIENTE` por `ARQUITECTO` y `TECH LEAD`.
- Ningún stack, proveedor, infraestructura o estrategia de persistencia resulta aprobado por este documento.

## Handoff

**TECH LEAD**, conforme a **G-02 vigente**, revisa la documentación e integración y coordina la validación técnica de ciclo de vida Android, permisos y comunicaciones con **ARQUITECTO (Codex), ya activo**. Ambos deben elevar al **PROPIETARIO** nuevas decisiones materiales o conflictos de seguridad y menores (#24); ninguno puede autoaprobar requisitos, proveedores ni desarrollo. Esta decisión no constituye por sí sola autorización para programar y el baseline MVP sigue `PENDIENTE`.

La descripción funcional del fallo de consulta queda trazada en [D-06 / issue #12](https://github.com/mundoinformaticacanaria/whereis/issues/12) y [PR #13](https://github.com/mundoinformaticacanaria/whereis/pull/13).
