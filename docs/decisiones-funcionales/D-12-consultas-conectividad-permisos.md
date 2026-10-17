# D-12 — Consultas, conectividad y permisos

- **Fecha:** 17/10/2026 (acuerdos del 16–17/10/2026)
- **Estado:** `CONFIRMADO` para las elecciones expresas del PROPIETARIO, `PENDIENTE` para los límites identificados.
- **Clasificación:** `MATERIAL`.
- **Fuente viva:** [issue #22](https://github.com/mundoinformaticacanaria/whereis/issues/22). Su cuerpo y comentarios prevalecen ante cambios posteriores.
- **Integración:** revisión por TECH LEAD, no constituye baseline MVP ni habilita implementación.

## Clasificación y estado
**MATERIAL — estados operativos, permisos Android y seguridad de consulta.**
**CONFIRMADO por PROPIETARIO** mediante respuestas del 17/10/2026, pendiente validación técnica; formalización expresamente solicitada.

## Contrato aprobado
1. Consulta **individual** autorizada: mostrar «Actualizando…» en la lista y progreso en mapa; permite iniciar otras consultas individuales mientras la primera sigue pendiente; impide duplicar la consulta del mismo dispositivo hasta terminar. Sin cancelación manual: respuesta o timeout, cuyo umbral/ejecución decide TECH LEAD.
2. **Actualizar todos** inicia consultas faltantes de dispositivos autorizados, conserva las que ya están en curso y no duplica destinos; resultados individualizados «Actualizando/Actualizado/Error» y resumen final («N actualizados, M con error»). Si no hay elegibles, botón visible **deshabilitado** con explicación.
3. Éxito individual: el mapa se centra en posición nueva; actualización de varios/todos: mantener encuadre; fallo individual: conservar encuadre y error, «Whereis» permite ir a última posición existente.
4. Dispositivo consultante **sin Internet**: aviso persistente «Sin conexión a Internet» mientras dure; deshabilitar refrescos hasta recuperar conexión, no encolarlos ni ejecutar al volver; posición anterior sigue visible.
5. Dispositivo emisor **sin conexión**: intento falla y no queda pendiente para ejecución al reconectar. Si el estado «sin conexión» puede verificarse, mostrar «Dispositivo sin conexión»; si no, mensaje genérico «No se ha podido actualizar la ubicación». Timeout muestra mensaje genérico, no detalle técnico; reintento solo manual.
6. Si emisor tiene la **ubicación Android desactivada** se mantiene autorización Whereis, sin nueva posición; Android no permite activarla silenciosamente desde Whereis. Al abrir la app, pedir activación guiada. Consultante ve fallo genérico, nunca ese motivo preciso. Tras activar en emisor, consultante debe solicitar **otra vez** (no reanudar automáticamente).
7. Emisor podrá recibir notificación cuando una consulta autorizada no pueda obtener ubicación porque tiene el servicio Android desactivado, si Android lo permite. **Una notificación por ID/alias solicitante** (B y C pueden generar dos); **máximo una por solicitante cada 24h** mientras permanezca desactivado; al activarse el servicio se reinicia el límite si luego vuelve a desactivarse. Incluye alias/ID solicitante y acceso a Whereis. No confundir con avisos por consultas exitosas: estos NO se envían.
8. Permisos Android: si faltan, Whereis informa y guía a solicitarlos de nuevo **solo cuando Android permita hacerlo** o a Ajustes, advirtiendo funciones degradadas; la app sigue utilizable con operaciones dependientes del permiso deshabilitadas. Para ubicación propia no habilitada, no inventa marcador. Ubicación aproximada permitida con claridad. No garantizar respuesta en segundo plano donde Android lo impida.
9. No avisar por consultas autorizadas ordinarias; no historial de consultas visible para emisor. No enviar notificaciones push por cambios de permiso; consulta de estado disponible en la app.

## Criterios de aceptación
- D12-CA01: A en curso, B se consulta aparte; segunda A no duplica; «Actualizar todos» no duplica A.
- D12-CA02: «Actualizar todos» resumen+resultados independientes, sin iniciar automáticamente al abrir mapa.
- D12-CA03: sin red local, controles inactivos y aviso persistente; al volver red no hay consulta automática.
- D12-CA04: timeout genérico y última ubicación anterior con hora, sin éxito simulado.
- D12-CA05: servicio de ubicación apagado no implica revocar permiso; ningún encendido silencioso; aviso a emisor por solicitante con límite 24h y reinicio tras habilitar/deshabilitar.
- D12-CA06: denegación permisos degrada operaciones dependientes sin cerrar app; reintentar diálogo o abrir Ajustes conforme al sistema.
- D12-CA07: las consultas/remociones ordinarias de autorización no envían notificaciones.

## PENDIENTE / técnico
No prometer precisión, recepción de notificaciones, verificación exacta de estado remoto ni revocación instantánea offline; permisos/versiones Android, timeout, concurrencia, colas, batería, recuperación de red, accesibilidad y pruebas de error a cargo de TECH LEAD. Considerar salvaguardas y consentimiento en contexto de menores. Relacionadas #2, #6, #10, #12, #16. No se aprueba infraestructura ni implementación.
