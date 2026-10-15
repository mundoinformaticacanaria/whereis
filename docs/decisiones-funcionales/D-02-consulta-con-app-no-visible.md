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
- **Ubicación anterior:** su posible presentación diferenciada, caducidad y retención permanecen `PENDIENTE`; no se aprueban aquí.

## PENDIENTE de contraste técnico y definición posterior

- Versiones de Android y alcance real de ejecución con app no visible, cerrada o forzosamente detenida.
- Permisos, requisitos de plataforma y de distribución de la aplicación.
- Mecanismo técnico de solicitud/respuesta y requisitos de conexión, sin proveedor seleccionado.
- Tiempo de espera, reintentos, precisión, último dato conocido, política de retención y mensajes.
- Evaluación del efecto sobre batería, privacidad, seguridad y costes.
- **D-03 a D-05:** asociación de dispositivos, autorización individual, vigencia y revocación.

## Impacto y límites

- **Alcance:** localización remota puntual, no navegación en tiempo real.
- **Privacidad:** solo peticiones autorizadas.
- **Arquitectura/operación:** evaluación `PENDIENTE` por `ARQUITECTO` y `TECH LEAD`.
- Ningún stack, proveedor, infraestructura o estrategia de persistencia resulta aprobado por este documento.

## Handoff

`TECH LEAD` y, por implicar ciclo de vida Android, permisos y comunicación remota, `ARQUITECTO` deberán validar la viabilidad técnica antes de planificar la implementación. Esta decisión no constituye por sí sola autorización para programar.
