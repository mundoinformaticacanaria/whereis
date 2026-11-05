# WHEREIS — contrato funcional confirmado R-60a/b/c (#60)

**Estado:** CONFIRMADO exclusivamente en su alcance funcional por decisiones expresas del PROPIETARIO en #41, 04/11/2026. **No es aprobación jurídica, baseline global, arquitectura ni autorización de implementación.**

## Fuentes de autoridad y trazabilidad

- R-60a: https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6643785646
- R-60b: https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6643816206
- R-60c: https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6644123381
- Propuesta anterior (no elevarla íntegramente a confirmada): PR #77, HEAD `7eb8dded24e194af8e9ebf307f4f3a3a76c75d74`, QA #79 APTO DOCUMENTAL **solo para ese SHA**.
- Contrastar D-06, D-09, D-10, SEG-01/02, #24, #41 y propuesta arquitectónica #61/PR #66. En caso de contradicción material no resuelta, escalar a TECH LEAD/PROPIETARIO; no inferir derogaciones.

## R-60a — última ubicación local en B (CONFIRMADO funcional)

Para cada instalación conocida de A, B conserva **como máximo una última ubicación recibida legítimamente**, sin historial y **sin caducidad funcional automática** por tiempo transcurrido, hasta que B elimine manualmente el dispositivo/relación mediante confirmación. Mostrar el instante **real de captura**, precisión real y antigüedad; nunca convertir una posición antigua en actual ni sustituir la marca temporal por un intento fallido. La revocación efectiva en A impide entregas futuras, pero **no borra unilateralmente** la posición ya recibida en B; preservar las reglas de bloqueo, incluida la posible ocultación de marcador. La eliminación confirmada desde B borra localmente vínculo, última ubicación y personalización conforme a D-10. Reinstalar A no restaura su identidad anterior ni autoriza nuevas entregas al ID antiguo; tampoco elimina automáticamente la posición legítima en un B no reinstalado.

## R-60b — supresión remota A→B (CONFIRMADO alcance MVP)

**No existe en el MVP** botón, solicitud interna, cola, protocolo, acuse ni estado de borrado remoto de A hacia B. B puede borrar sus datos locales mediante eliminación confirmada del dispositivo. Explicar que revocar/bloquear en A no elimina datos previamente recibidos legítimamente en B; tampoco se promete borrado de backups, capturas, otros dispositivos o terceros. Esta exclusión de una función interna **no niega** posibles derechos legales de supresión ni solicitudes por canales externos cuando correspondan; aplicabilidad y procedimiento legal permanecen PENDIENTES.

## R-60c — menores y transparencia (CONFIRMADO por ahora)

Mantener autorización **por instalación y relación direccional** para todos los casos, incluidos menores, **sin modo parental especial** ni privilegios por parentesco. Información comprensible sobre qué instalación comparte, quién puede consultar con autorización expresa, última posición conservada, antigüedad y límites de revocación/borrado. Conocer un ID/QR o aceptar un conocido **no equivale** a autorización para obtener ubicación. Mantener controles de identidad, permiso vigente, anti-enumeración y fail-closed de SEG-01/02. No presumir consentimiento válido, representación legal ni acceso por parentesco. Reconsiderar controles específicos de menores si se identifica obligación o riesgo, mediante nueva decisión material.

## Criterios de aceptación funcional propuestos para verificación futura (NO EJECUTADOS)

1. Dos posiciones legítimas consecutivas de A en B: B conserva únicamente la segunda; no se crea historial.
2. Sin actualización durante un periodo largo: la última posición permanece, con instante de captura original y antigüedad visible, nunca etiquetada como actual.
3. Intento fallido, A offline o sin permiso: no sustituye coordenadas, precisión ni instante de la última captura válida.
4. Revocación efectiva en A: nuevas consultas no obtienen nuevas posiciones; los datos previos de B no se declaran borrados.
5. Bloqueo: se respetan las reglas de visibilidad y autorización de D-09/SEG sin deducir borrado remoto.
6. B cancela la confirmación de eliminación: se conserva relación y datos; B confirma: se eliminan localmente relación, última posición y personalización según D-10.
7. A se reinstala: su ID antiguo no puede volver a entregar nuevas posiciones a B por la relación anterior; no se presupone eliminación de datos previos en B.
8. Interfaz de A: no aparece una función MVP de solicitud de borrado remoto a B ni mensajes de acuse o borrado remoto completado.
9. Información de revocación/borrado: distingue bloqueo de futuras entregas, eliminación local y posibles derechos legales externos; no promete eliminación en backups/terceros.
10. Conocido añadido por ID/QR sin autorización direccional vigente: no puede consultar ubicación; se aplica fail-closed.
11. Instalación usada por menor: no obtiene permisos especiales por parentesco ni activa modo parental implícito.
12. Información comprensible en A/B: identifica actor que comparte/consulta, posición y antigüedad, y límites de la revocación; textos finales sujetos a revisión funcional y legal aplicable.

## PENDIENTE / NO DEMOSTRADO

**PENDIENTE:** base jurídica y derechos de interesados, representación de menores, legalidad de conservación sin caducidad, obligaciones de información y supresión, compatibilidad con SEG-03/04, #24/#41 y gates #42. **NO DEMOSTRADO:** exclusión y no-resurrección de datos en backups cloud/D2D/OEM, borrado de capturas/terceros, pruebas Android/red, CI y protección de main. ADR-61/PR #66 continúa siendo propuesta técnica, no arquitectura aprobada.

**Handoff:** FUNCIONAL entrega formalización documental a TECH LEAD para revisión de consistencia y QA independiente sobre el HEAD exacto de esta nueva PR. No modificar PR #77 ya revisada; no merge, PROGRAMADOR, proveedor, gasto, servidores ni timers.
