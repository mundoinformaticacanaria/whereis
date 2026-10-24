# D-08 — Mapa como pantalla inicial, lista de dispositivos y «Actualizar todos»

- **Decisión aprobada por PROPIETARIO:** 16/10/2026.
- **Clasificación:** `MATERIAL — FUNCIONAL`.
- **Estado:** `CONFIRMADO` en el alcance funcional aquí descrito; integración en `main` `PENDIENTE`.
- **Issue de decisión:** [D-08 / #16](https://github.com/mundoinformaticacanaria/whereis/issues/16).
- **Antecedente directo:** [D-07 / #14](https://github.com/mundoinformaticacanaria/whereis/issues/14), mapa conjunto con ubicaciones de varios dispositivos, actualizaciones manuales y preferencia de cartografía libre.
- **Otras relaciones:** [D-01/#1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02/#2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-03/#6](https://github.com/mundoinformaticacanaria/whereis/issues/6), [D-04/#8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-05/#10](https://github.com/mundoinformaticacanaria/whereis/issues/10), [D-06/#12](https://github.com/mundoinformaticacanaria/whereis/issues/12).
- **Baseline funcional global:** `PENDIENTE`; la aprobación de D-08 no autoriza desarrollo.
- **Decisiones `SUPERSEDED`:** ninguna. D-08 precisa la **vista de inicio** de D-07, sin cambiar el mapa confirmado.

## Pregunta funcional y alternativas

¿Qué vista se presenta inicialmente al entrar en el flujo principal de Whereis?

- **Opción A — ELEGIDA / CONFIRMADA:** mostrar **mapa conjunto** como pantalla principal, con acceso a la **lista de dispositivos**.
- **Opción B — NO ELEGIDA:** iniciar en la lista de dispositivos y entrar al mapa desde ella.

El Propietario eligió expresamente el 16/10/2026 la **opción A**, conservando selección individual, actualización manual y autorizaciones D-01 a D-07. En el siguiente mensaje **amplió D-08** con: «**Opción A y además debe haber una opción de actualizar todos**». Esta ampliación está **CONFIRMADA**, no es una hipótesis ni implica seguimiento automático.

## Actores

- **Dispositivo consultante B:** dispone de Whereis e identifica otros dispositivos mediante ID fijo o QR según D-03.
- **Dispositivos A, C, etc.:** conocidos por B; pueden estar autorizados o no para compartir su posición con B. Una posición solo existe en el mapa si B ya la obtuvo legítimamente de la instalación correspondiente.

«Dispositivo conocido» no es sinónimo de «dispositivo con posición disponible» ni de «dispositivo autorizado».

## Contrato funcional CONFIRMADO

1. **Mapa de inicio y distribución (D-11 / #21 CONFIRMADO).** Vista principal **dividida**, mapa conjunto arriba y lista debajo; ambos visibles en la vista normal. Solo el mapa puede maximizarse ocultando la lista; esta no sustituye la vista cartográfica ni requiere pantalla separada.
2. **Lista (D-11).** Lista inferior de conocidos, incluso sin ubicación, ordenada por alias/ID y con búsqueda incremental y filtros Todos/Autorizados/No autorizados/Pendientes. Cuando el mapa está maximizado, restaurar división devuelve la lista.
3. **Representación en mapa.** Las ubicaciones ya obtenidas legítimamente de distintos dispositivos pueden mostrarse en **un mismo mapa**, con **marcadores distinguibles** por dispositivo. Estar en la lista de conocidos, por sí solo, no genera un marcador ni habilita consulta.
4. **Selección y ficha (D-11).** Pulsar en lista **solo selecciona**, sin recentrar ni abrir ficha. La acción «Whereis» centra la última posición ya conocida sin obtener otra. Pulsar marcador abre ficha inferior **modal**, sincroniza lista y bloquea interacción con controles situados detrás; al cerrar la ficha permanece selección. Los marcadores usan foto opcional o número, borde de color y agrupaciones expandibles.
5. **Actualización manual.** La acción **«Actualizar ubicación»** se refiere **al dispositivo seleccionado**. Si B tiene autorización activa de A, puede intentar una **consulta puntual** de A; no se inician solicitudes a otros dispositivos por selección o apertura de pantalla.
6. **Sin seguimiento continuo.** Entrar al mapa, desplazarse, hacer zoom o consultar la lista **no inicia seguimiento en tiempo real ni consultas de ubicación periódicas automáticas** (D-01, D-07).
7. **Sin permisos.** Si un dispositivo está simplemente registrado como conocido y no ha autorizado B, no se permite a B consultar nuevas ubicaciones (D-03). Si A ha desactivado el permiso de B, no se permiten nuevas consultas (D-05).
8. **Última ubicación y bloqueo (D-09/D-10).** Tras **desactivación ordinaria**, la última posición legítima anterior permanece visible y fechada si no hay bloqueo/eliminación. El **bloqueo** puede ocultar el marcador previo sin borrar la posición; la **eliminación** confirmada borra la ubicación y personalización en el consultante. No equiparar bloqueo con simple desactivación.
9. **Fallo de consulta.** Si una consulta autorizada falla, la interfaz informa del fallo y, si existe, muestra la **última ubicación conocida** con fecha, hora y advertencia; en ausencia de posición previa indica **«Ubicación no disponible»** (D-06).
10. **Instalaciones nuevas (D-04/SEG-04).** La reinstalación produce nuevo ID sin recuperar ubicaciones ni autorizaciones anteriores desde backup. Un consultante no reinstalado puede conservar una última posición legítima de emisor desinstalado (D-10), sin consultar el ID antiguo.
11. **Actualizar todos (D-12/SEG-01/02 CONFIRMADOS).** «Actualizar todos» inicia manualmente una consulta puntual por destino elegible con identidad de instalación **y autorización direccional vigente verificables**. Excluye no autorizados, bloqueados, revocados, instalaciones inválidas y estados no verificables. Si no hay elegibles, queda visible deshabilitado. No duplica un destino que ya se esté actualizando; incorpora los restantes y no concede permisos.
12. **Resultados y resumen (D-12).** Se informa por destino «Actualizando/Actualizado/Error» y resumen final de éxitos/errores. Un éxito individual centra la nueva posición; actualizar varios/todos **no mueve el mapa**. Ante fallo, última ubicación legítima anterior con hora y aviso o «Ubicación no disponible», sin mostrar marcadores ocultos por bloqueo/eliminación.
13. **Sin refresco automático ni duplicados (D-12).** Abrir el mapa no lanza «Actualizar todos». Se permiten consultas a distintos destinos sin duplicar una en curso al mismo ID. Sin Internet local, banner persistente, botones deshabilitados, **sin cola automática ni reintentos al reconectar**; solo reintento manual. No se cancela manualmente una consulta iniciada: finaliza por resultado o timeout. **PENDIENTE técnico:** límites, timeout, mecanismo de concurrencia y rendimiento Android.

## Ejemplo funcional sin datos reales

El dispositivo consultante B conoce tres dispositivos por ID:
- **A:** autorización activa y ubicación obtenida anteriormente; tiene un marcador identificable y se puede seleccionar para solicitar actualización manual.
- **C:** autorización desactivada, pero B había obtenido una ubicación con anterioridad; permanece visible la **última ubicación de C con fecha y hora**, sin habilitar «Actualizar ubicación» para C.
- **D:** dispositivo conocido sin ubicación previa. Puede aparecer en la **lista de conocidos**, pero **no** se presenta un marcador ficticio para D.

Al abrir el flujo principal, B ve **el mapa conjunto** con las posiciones disponibles y puede entrar a la lista para seleccionar/gestionar dispositivos sin conferirles nuevos permisos. Si B pulsa **«Actualizar todos»**, se intenta obtener **solo** una posición nueva de A si su autorización está activa: C queda excluido porque su permiso está desactivado y D queda excluido por no estar autorizado. Los resultados de cada dispositivo permitido son independientes.

Los nombres A/B/C/D son ilustrativos, **no** IDs reales, etiquetas obligatorias ni usuarios de prueba.

## Criterios de aceptación (observables)

- **D08-CA01 — Inicio:** al entrar en el flujo principal Whereis presenta primero el mapa interactivo conjunto, no la lista.
- **D08-CA02 — Lista accesible:** desde ese mapa el usuario puede abrir una lista de dispositivos conocidos aunque alguno carezca de ubicación disponible.
- **D08-CA03 — Vista de varios dispositivos:** cuando B tiene ubicaciones legítimas previas de A y C, ambos pueden identificarse como marcadores distintos en un mismo mapa.
- **D08-CA04 — Selección:** al seleccionar A se presentan la identificación del dispositivo y la fecha/hora de la última posición disponible, rotulada como anterior cuando lo es.
- **D08-CA05 — Refresco manual individual:** pulsar «Actualizar ubicación» para A autorizado intenta consultar una posición puntual de **A**, no de C; el mapa no dispara rastreo continuo por estar abierto.
- **D08-CA06 — Dispositivo conocido no autorizado:** el hecho de aparecer en la lista no habilita consultas ni marcadores de posición sin datos legítimos.
- **D08-CA07 — Revocación:** tras desactivación ordinaria puede seguir viendo última ubicación legítima anterior fechada; tras bloqueo el marcador se oculta, y tras eliminación se borra ubicación/personalización; en ninguno de esos estados se obtiene nueva posición sin autorización verificable.
- **D08-CA08 — Consulta fallida:** si falla la actualización, el mapa no convierte el último dato en «actual» y muestra el aviso previsto en D-06.
- **D08-CA09 — Sin actualización automática:** abrir el mapa, entrar en la lista o cambiar de marcador no genera nuevas solicitudes de ubicación por sí solo.
- **D08-CA10 — Botón global:** desde la vista principal se puede distinguir y pulsar **«Actualizar todos»** además del botón individual.
- **D08-CA11 — Alcance por autorización:** el botón global intenta una consulta puntual por cada dispositivo con permiso activo y válido, **sin incluir** dispositivos solo conocidos, pendientes, revocados, con instalación inválida o autorización no confirmada; no cambia permisos.
- **D08-CA12 — Fallo parcial:** si responde A pero C no responde, la vista refleja el dato nuevo de A y, para C, aviso de fallo con última ubicación anterior fechada, o «Ubicación no disponible» si nunca hubo una, sin atribuir a C una posición nueva.
- **D08-CA13 — Solo por pulsación:** el botón global no se activa al abrir/mover el mapa ni induce periodicidad, historial o seguimiento continuo.

## Estados ya resueltos y pendientes reales (decisiones posteriores)

**CONFIRMADO por D-09 a D-13 / issues #19–#23:** pantalla principal mapa arriba y lista abajo (solo mapa maximizable), alias/ID ordenados, filtros y búsqueda, selección desde lista sin recentrar, «Whereis» que solo centra, ficha modal al tocar marcador, foto o número y borde de color, agrupación expandible; estado por destino y resumen de «Actualizar todos», sin peticiones duplicadas ni reintentos automáticos. En ausencia de posiciones se enfoca ubicación propia cuando Android la permita, sin inventarla. La fecha y hora se muestran siempre en formato DD/MM/AAAA HH:mm:ss y zona local del consultante (D-13); solo se conserva una última ubicación legítima según D-10.

**CONFIRMADO por SEG-01/SEG-02 / #24:** si identidad de instalación o autorización direccional vigente no son verificables, no se entrega posición nueva aunque el estado local parezca autorizado. Las peticiones no se encolan automáticamente por desconexión. **SEG-04:** nueva instalación no restaura ID/ubicaciones/permisos desde copia; otra instalación consultante no reinstalada puede conservar última ubicación legítima anterior del emisor.

**PENDIENTE técnico, legal o de diseño no resuelto:** versión/permisos Android y mecanismos de sincronización/concurrencia, timeout y límites, accesibilidad, tamaño de controles, detalle visual de pantallas secundarias, persistencia opcional del encuadre, retención conforme a ley y borrado verificable, protección de menores, cartografía/teselas/geocodificación y sus licencias/costes. No se presupone proveedor ni infraestructura. Baseline funcional global e implementación siguen PENDIENTES.

## Aceptación complementaria de ampliaciones confirmadas

- **D08-CA14 (D-11):** vista dividida mapa superior/lista inferior; solo mapa maximizable, lista seleccionable sin abrir ficha, tocar marcador abre ficha modal.
- **D08-CA15 (D-12):** con A ya consultándose, «Actualizar todos» no repite A e intenta otros elegibles, muestra estados separados y resumen final sin mover el mapa.
- **D08-CA16 (D-12):** sin Internet consultante, botón deshabilitado y aviso persistente; tras reconexión no se solicita ninguna ubicación hasta una pulsación nueva.
- **D08-CA17 (D-09/D-10):** desactivación común conserva posición previa marcada como anterior; bloqueo oculta marcador y eliminación borra posición/personalización.
- **D08-CA18 (D-13/SEG-01/02):** hora exacta local DD/MM/AAAA HH:mm:ss; sin prueba verificable de identidad y permiso activo no se obtiene nueva posición.

## Impacto y verificación de coherencia

- **UX/producto:** da prioridad al mapa conjunto como entrada, conservando el acceso a todos los dispositivos conocidos.
- **Consentimiento/privacidad:** marcador y nuevas consultas dependen de la posición previamente obtenida y de la autorización vigente; conocer un dispositivo no da acceso.
- **Seguridad y arquitectura:** selección, renderización y comunicaciones deben respetar autorización activa y límites de Android sin imponer implementación.
- **Costes:** `PENDIENTE`.

El contrato de D-07 sigue `CONFIRMADO`, y D-08 **añade** la vista inicial, acceso a lista y **actualización manual de todos los dispositivos autorizados**. D-07 solo prohibía consultas a todos **por el hecho de abrir el mapa**, no una solicitud conjunta iniciada expresamente por el usuario.

## Handoff

- **PROPIETARIO:** opción A CONFIRMADA el 16/10/2026.
- **FUNCIONAL:** issue y documento de especificación en PR para revisión.
- **TECH LEAD:** siguiente responsable de revisión documental conforme a G-02 vigente, con apoyo de ARQUITECTO activo para evaluar Android y seguridad; sin autorización de proveedores, gastos ni implementación.
- **QA:** mantiene independencia en futuras implementaciones.
- **Baseline funcional global / autorización de desarrollo:** `PENDIENTE`.
