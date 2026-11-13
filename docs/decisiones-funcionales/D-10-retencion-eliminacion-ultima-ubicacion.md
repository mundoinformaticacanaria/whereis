# D-10 — Retención y eliminación

- **Fecha:** 17/10/2026 (acuerdos del 16–17/10/2026)
- **Estado:** `CONFIRMADO` para las elecciones expresas del PROPIETARIO, `PENDIENTE` para los límites identificados.
- **Clasificación:** `MATERIAL`.
- **Fuente viva:** [issue #20](https://github.com/mundoinformaticacanaria/whereis/issues/20). Su cuerpo y comentarios prevalecen ante cambios posteriores.
- **Integración:** revisión por TECH LEAD, no constituye baseline MVP ni habilita implementación.

## Clasificación y estado
**MATERIAL — retención, eliminación y privacidad.**
**CONFIRMADO por PROPIETARIO** durante decisiones del 16–17/10/2026, cuya formalización en GitHub ordena expresamente. Complementa D-04/D-05/D-06 sin constituir un baseline global.

## Contrato aprobado
1. Whereis conserva **solo la última ubicación obtenida legítimamente por dispositivo**, con instante real (sin historial de desplazamientos ni expiración temporal automática).
2. Permanece disponible como ubicación **anterior y fechada**, después de consulta fallida, desactivación de autorización y cuando el emisor desinstala la app y se confirma instalación inválida. No concede nuevas consultas. La retención hasta eliminación del dispositivo la gobierna el usuario consultante, sujeto a definiciones legales pendientes.
3. Tras bloqueo, la ubicación anterior se conserva, pero el marcador queda **oculto** mientras esté bloqueado. Al desbloquear, puede reaparecer como antigua, sin restaurar autorización. Distinguir baja de instalación de baja manual de relación.
4. **Eliminar un dispositivo** de la lista exige confirmación explicando consecuencias; cancela la relación y revoca permisos asociados, elimina su última ubicación **de Whereis en ese dispositivo consultante** y también alias, foto y color. Para volver a compartir/consultar hace falta nueva incorporación, solicitud y autorización expresa.
5. Dispositivo de instalación anterior **confirmada** permanece listado hasta eliminación manual, con texto **tachado** y «Instalación anterior», sin nuevas consultas. No asumir detección instantánea de desinstalación remota.
6. Se conserva una sola ubicación por dispositivo: una nueva ubicación legítima sustituye la anterior; un error no altera su fecha/hora. No se recuperan datos/identidad de instalación anterior por copia de seguridad (D-04).

## Criterios de aceptación
- D10-CA01: solo existe la última posición visible del dispositivo, no una serie cronológica; no expira automáticamente.
- D10-CA02: desactivación, fallo o desinstalación del emisor no convierte ubicación previa en actual ni habilita nuevas consultas.
- D10-CA03: bloqueo oculta el marcador conservando última posición; desbloqueo puede recuperarla con estado anterior, sin nuevo permiso.
- D10-CA04: eliminación confirmada borra última ubicación y personalización del consultante; cancelación no borra.
- D10-CA05: instalación anterior confirmada aparece tachada y no puede recibir consultas.

## Precisiones posteriores de seguridad y reinstalación (CONFIRMADAS)

- **SEG-01/SEG-02 / [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24):** la existencia de una última posición conservada no permite nuevas consultas sin comprobar identidad auténtica de la instalación y autorización direccional vigente; si la verificación falla, solo se muestra esa última posición legítima donde D-09 permita visualizarla.
- **SEG-04 / #24:** desinstalar/reinstalar el **consultante** genera nuevo ID y no recupera posiciones anteriores ni permisos desde backup. Desinstalar únicamente el **emisor** no elimina automáticamente la posición previamente obtenida y legítimamente conservada en un consultante no reinstalado.
- **SEG-03 / #24:** sin modo familiar especial de momento, pero tratamiento y plazo de retención de datos de menores y borrado verificable **PENDIENTES** de validación jurídica; no afirmar borrado físico universal.

## PENDIENTE / riesgos
Ubicación real del almacenamiento, borrado en otras copias/dispositivos, periodos máximos exigibles, ejercicio de derechos, recuperación y sincronización offline. La regla de retención no legitima almacenar indefinidamente datos personales contra obligaciones aplicables; se requiere revisión de privacidad y diseño de eliminación verificable. No autoriza historiado ni almacenamiento en servidores concretos.

## Trazabilidad
D-04 #8, D-05 #10, D-06 #12, D-07 #14. Siguiente acción **TECH LEAD** (viabilidad, controles, PR). Sin desarrollo ni baseline global.
