# D-04 — Vigencia de autorizaciones, desinstalación y reinstalación

- **Fecha de aprobación:** 16/10/2026 (completada por el PROPIETARIO en la misma fecha).
- **Clasificación:** MATERIAL — FUNCIONAL.
- **Estado:** **CONFIRMADO** por el PROPIETARIO respecto de la vigencia y del comportamiento ante desinstalación/reinstalación. La viabilidad y los mecanismos de aplicación remota siguen **PENDIENTES**.
- **Issue:** [#8 — D-04](https://github.com/mundoinformaticacanaria/whereis/issues/8).
- **PR de documentación:** [#9](https://github.com/mundoinformaticacanaria/whereis/pull/9).
- **Decisiones relacionadas:** [D-01/#1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02/#2](https://github.com/mundoinformaticacanaria/whereis/issues/2) y [D-03/#6](https://github.com/mundoinformaticacanaria/whereis/issues/6).
- **Baseline funcional global y arquitectura:** PENDIENTES; esta decisión no aprueba su totalidad.
- **Decisiones SUPERSEDED:** ninguna registrada. La propuesta de reinstalación del borrador anterior ha sido aceptada, no sustituye una decisión histórica.

## Necesidad y actores

Mantener las autorizaciones individuales de consulta de ubicación durante su vida útil sin renovaciones temporales, evitando que al desinstalar/reinstalar se recuperen vínculos y permisos previos.

- **A:** dispositivo que comparte ubicación.
- **B (o C, ...):** dispositivo consultante, autorizado de manera individual.
- Una autorización permite a B consultar a A según D-01 y D-02; el ID fijo de D-01 es estable **durante la vida de una instalación**. La reinstalación inicia una identidad nueva.

## Decisión CONFIRMADA por el PROPIETARIO

1. **Sin caducidad automática:** las autorizaciones no tienen vencimiento por horas, días o períodos predeterminados.
2. **Finalización:** la autorización termina cuando se revoca expresamente o cuando se desinstala Whereis **en cualquiera de los dos extremos** participantes: dispositivo emisor A o consultante B.
3. **Reinstalación como nueva instalación:** si Whereis se reinstala, incluso en el mismo teléfono físico, se genera un **nuevo ID fijo Whereis** para esa instalación.
4. **Sin reutilización:** una instalación nueva no recupera automáticamente las autorizaciones antiguas, ni las concedidas para que otros consulten su ubicación ni las recibidas para consultar otros dispositivos.
5. **Nueva solicitud y aceptación:** para restablecer una relación anterior tras reinstalar, hay que solicitar y aceptar expresamente una nueva vinculación, de acuerdo con D-03.
6. **Sin seguimiento continuo:** la vigencia de una autorización no habilita consultas automáticas periódicas; permanecen las consultas puntuales establecidas en D-01/D-02.

## Reglas funcionales

- **D04-RN01:** añadir nuevos consultantes no altera el ID de una instalación ya existente.
- **D04-RN02:** una autorización pertenece a la relación entre dos instalaciones identificadas; la nueva instalación no hereda relaciones previas por usar el mismo hardware.
- **D04-RN03:** desinstalar cualquiera de las dos aplicaciones extingue las autorizaciones de esa instalación, incluidas las relaciones con varios dispositivos; no deben recuperarse al reinstalar.
- **D04-RN04:** una restauración de copia de seguridad no debe reactivar ni permitir suplantar la antigua identidad ni sus permisos.
- **D04-RN05:** no se comunica una baja remota como confirmada si todavía no existe constancia de su aplicación. El contrato no presupone que otros dispositivos detecten la desinstalación inmediatamente.

## Flujos principales y casos de aceptación verificables

- **D04-CA01 (vigencia):** tras pasar un período de tiempo arbitrario, B puede seguir intentando consultar A sin reautorización temporal, si ambas instalaciones permanecen válidas y no existe revocación.
- **D04-CA02 (nuevas vinculaciones):** A autoriza a B y a C independientemente; mantiene el ID de esa instalación.
- **D04-CA03 (desinstalación emisor):** al desinstalar Whereis en A, esa instalación no puede responder nuevas consultas; al reinstalar no recupera el ID ni los permisos concedidos anteriormente.
- **D04-CA04 (desinstalación consultante):** al desinstalar Whereis en B, su antigua identidad y autorizaciones de consulta no se trasladan a la siguiente instalación; B deberá volver a solicitar vinculación.
- **D04-CA05 (reinstalación):** reinstalar Whereis en el mismo teléfono genera un nuevo ID y no reutiliza autorizaciones concedidas ni recibidas, tampoco tras restaurar copia de seguridad.
- **D04-CA06 (nueva aceptación):** tras reinstalar A o B, las consultas entre las nuevas instalaciones no son posibles hasta completar otra solicitud y aceptación expresa.
- **D04-CA07 (sin seguimiento):** mantener indefinidamente un vínculo válido no inicia adquisición periódica ni continua de ubicaciones.
- **D04-CA08 (aplicación remota):** cuando el sistema conoce y ha aplicado la invalidez de la instalación antigua, rechaza solicitudes asociadas a ella; no se impone un mecanismo o tiempo de detección imposible de garantizar.

Los criterios anteriores describen el resultado exigido, **no** un mecanismo de detección o persistencia ya elegido.

## Validaciones, errores y riesgos: PENDIENTE de diseño y contraste técnico

- Una desinstalación no garantiza notificación remota inmediata. Puede quedar una relación obsoleta visible o registrada en otros dispositivos mientras se detecta su invalidez: no debe habilitar una nueva identidad ni garantizar nuevas posiciones.
- Android puede restaurar datos de la app mediante backup. TECH LEAD debe definir y validar cómo impedir la restauración de IDs y permisos anteriores sin afirmar que el mecanismo ya existe.
- Pérdida de conexión, reinicio, actualización de Whereis **sin desinstalación**, borrado de datos y restablecimiento de fábrica son situaciones distintas que requerirán definición y pruebas.
- Estado de los vínculos antiguos que sigan mostrándose, eliminación de ubicaciones ya conocidas y retención de datos personales: PENDIENTE de decisiones posteriores.
- La revocación explícita, su alcance temporal, garantías de aplicación y casos sin conexión se detallarán en **D-05**.
- Riesgo de suplantación de instalaciones/IDs antiguos; asegurar autenticidad y control de acceso es responsabilidad de diseño posterior.
- Proveedor, arquitectura, persistencia, comunicaciones, costes, permisos de Android y tiempos de respuesta: **no decididos**.

## Fuera de alcance

No se aprueban cuentas de usuario, recuperación automática, historial geográfico, proveedores, tecnologías o implementación. No se fija aquí la política de eliminación retroactiva de posiciones ya vistas o almacenadas por terceros.

## Handoff

- **PROPIETARIO:** D-04 confirmada.
- **FUNCIONAL:** decisión registrada en [issue #8](https://github.com/mundoinformaticacanaria/whereis/issues/8) y propuesta de documento revisada en PR #9.
- **TECH LEAD:** siguiente acción de revisión documental e integración conforme a G-01 V3, y evaluación posterior de garantías técnicas; no equivale a autorización de programación.
- **QA:** independencia de revisión para entregas de código cuando exista implementación autorizada.
