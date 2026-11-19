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

## Precedencia de seguridad y copia tras reinstalación

**SEG-01/SEG-02 CONFIRMADOS por [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24):** aun con interruptor aparentemente activo o ubicación anterior en caché, una posición **nueva** exige verificar identidad auténtica de instalación y autorización direccional vigente; ante ausencia/fallo de verificación por caída de red o concurrencia, se **deniega** el dato nuevo y solo queda última posición legítima fechada donde D-09/D-10 permitan verla. No prometer revocación remota instantánea. **SEG-04 CONFIRMADO:** reinstalar consultante no recupera ID, posiciones ni permisos desde backup; consultante no reinstalado puede conservar la última legítima del emisor desinstalado. **SEG-05/06 y SEG-03 jurídico PENDIENTES:** viabilidad Android/avisos, acuse de recepción, sincronización y protección jurídica de menores. No seleccionar mecanismo de autenticación/proveedor.

**Criterios adicionales:** (a) autorización no verificable no devuelve coordenadas nuevas; (b) no se simula ubicación con una caché como respuesta fresca; (c) reinstalar B no recupera última posición aunque exista copia; (d) no se encola solicitud para cuando el emisor recupere conexión.

## PENDIENTE / técnico
No prometer precisión, recepción de notificaciones, verificación exacta de estado remoto ni revocación instantánea offline; permisos/versiones Android, timeout, concurrencia, colas, batería, recuperación de red, accesibilidad y pruebas de error a cargo de TECH LEAD. Considerar salvaguardas y consentimiento en contexto de menores. Relacionadas #2, #6, #10, #12, #16. No se aprueba infraestructura ni implementación.


## Aceptación de precedencia Q1→G — UX114 (casos NO EJECUTADOS)

**Autoridad:** [decisión B del PROPIETARIO #114/6845631908](https://github.com/mundoinformaticacanaria/whereis/issues/114#issuecomment-6845631908). Estas son condiciones observables propuestas para QA futura, no resultados de pruebas Android ni aprobación de implementación.

| Caso | Precondición y acción | Resultado exigido / negativo prohibido |
|---|---|---|
| **UX114-01** | A autorizado, Q1 individual pendiente; pulsar «Actualizar todos» G | G reutiliza Q1, consulta los otros elegibles; ninguna segunda Q a A ni reinicio de plazo |
| **UX114-02** | Q1 reutilizada responde con posición legítima durante G | Posición, estado individual y resumen grupal actualizados **una vez**; el mapa no se recentra por Q1 |
| **UX114-03** | Q1 reutilizada tiene éxito y G termina después | G no aplica centrado diferido por Q1; no duplica captura ni contabiliza dos éxitos |
| **UX114-04** | Solo consulta individual de A, sin colisión G; éxito legítimo | Se centra la nueva posición de A; fallo o timeout no centra |
| **UX114-05** | Existe última posición legítima conservada; pulsar «Whereis» | Centrado explícito sobre esa posición sin consulta nueva, incluso si G no había recentrado |
| **UX114-06** | Q1 reutilizada falla, vence timeout o llega callback posterior al timeout | No se recentra ni se altera ubicación/estado terminal por callback tardío; se conserva aviso/última posición permitida |
| **UX114-07** | Durante G cambian selección/ficha o se revoca, bloquea, borra o reinstala A | Ningún resultado concede permiso, roba foco, resucita datos ni abre una ficha; la selección por lista no consulta ni recentra |

## Opción B CONFIRMADA — segundo toque de «Actualizar todos» (#120)

**Fuente:** [decisión PROPIETARIO #6982580012](https://github.com/mundoinformaticacanaria/whereis/issues/120#issuecomment-6982580012), contrato [CA-120-01..06](https://github.com/mundoinformaticacanaria/whereis/issues/120#issuecomment-6983747096). La mención anterior a #120 como **PENDIENTE** en esta página queda **SUPERSEDED**. Durante G activa, control «Actualizar todos» deshabilitado y no accionable por toque, teclado o asistencia; **no G2, no Q duplicada, no reinicio de deadline**. Progreso accesible finalizados/total y resultados por destino; éxito, fallo y timeout cuentan como finalizados, no todos como éxitos. «Cancelar» es acción separada y accesible durante G, cancela operación grupal de UI conforme a #115 sin prometer cancelación remota de Q. Tras cierre/cancelación terminal, solo se rehabilita con permisos, conectividad y elegibilidad vigentes; nuevo lote requiere gesto manual y revalidación, sin duplicar Q activa. Mantener #114/B (encuadre grupal de Q1 reutilizada), revocación/bloqueo/eliminación/reinstalación fail-closed y callbacks tardíos descartados.

**Aceptación futura, NO EJECUTADA:** CA-120-01 inicio manual único; 02 doble toque y asistencia bloqueados; 03 progreso y resultados terminales; 04 cancelación separada sin promesa remota; 05 rehabilitación condicional sin reintento automático; 06 seguridad y concurrencia, Q1, timeout y callbacks tardíos. Casos negativos: doble toque rápido, cancelación con Q pendiente, timeout+callback, cambio de permiso/red y Q1 concurrente. **PENDIENTES:** diseño UX final, duración de timeout y conciliación técnica #115/#119/PR #112 por TECH LEAD/ARQUITECTO; QA independiente del HEAD final. Sin aprobación de Android, merge, proveedores ni gastos.
