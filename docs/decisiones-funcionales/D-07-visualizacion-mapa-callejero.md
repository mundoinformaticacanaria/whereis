# D-07 — Mapa callejero conjunto y actualización manual de dispositivos

- **Fecha de aprobación del Propietario:** 16/10/2026.
- **Estado:** `CONFIRMADO` para comportamiento de visualización; selección técnica/operativa e incorporación a `main` `PENDIENTES`.
- **Clasificación:** `MATERIAL — FUNCIONAL`.
- **Issue:** [#14 — D-07](https://github.com/mundoinformaticacanaria/whereis/issues/14).
- **Trazabilidad:** [D-01 #1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02 #2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-03 #6](https://github.com/mundoinformaticacanaria/whereis/issues/6), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-05 #10](https://github.com/mundoinformaticacanaria/whereis/issues/10), [D-06 #12](https://github.com/mundoinformaticacanaria/whereis/issues/12).
- **Baseline funcional global:** `PENDIENTE`; esta decisión no supone autorización de desarrollo.
- **Ampliación posterior:** [D-08 / issue #16](https://github.com/mundoinformaticacanaria/whereis/issues/16), [PR #18](https://github.com/mundoinformaticacanaria/whereis/pull/18), incorpora el botón manual «Actualizar todos» sin cambiar la prohibición de seguimiento automático de D-07.
- **Decisiones `SUPERSEDED`:** ninguna.

## Necesidad / origen y referencia funcional

El Propietario solicita una pantalla integrada donde ver la ubicación de los dispositivos sobre un **mapa callejero similar en uso a Google Maps**, priorizando software libre. Explicita como **referencia de experiencia de usuario** la funcionalidad de **Google Family Link**: una vista de mapa que permite ver dispositivos del grupo y usar un botón de actualización de ubicación.

Aprueba expresamente D-07: «visualización en mapa callejero interactivo integrado en Whereis, con marcador de ubicación, fecha/hora, actualización manual y aviso de antigüedad. Priorizar software libre y delegar en TECH LEAD la selección técnica, licencias y costes».

**Límite de la analogía:** Whereis **no** adopta las cuentas familiares de Google, parentalidad, límites/funciones de Family Link, su proveedor cartográfico ni su interfaz o código. La referencia concreta se limita a la utilidad del **mapa conjunto de dispositivos y el control de actualización**, con las autorizaciones por instalación definidas en D-01 a D-06.

## Actores

- **B:** dispositivo Android desde el que se consulta una o varias ubicaciones autorizadas, y se visualizan posiciones obtenidas previamente conforme a las decisiones de consentimiento.
- **A, C, ...:** dispositivos conocidos por B, cada uno con una relación individual de autorización y, cuando proceda, una ubicación anteriormente obtenida de forma legítima.

No se presupone que «familia» sea un requisito de cuenta o vínculo parental: los participantes son **dispositivos Whereis**, no cuentas personales.

## Comportamiento CONFIRMADO

1. **Mapa integrado:** Whereis presenta una pantalla con **mapa callejero interactivo**, compatible con desplazamiento/zoom, donde ubicar marcadores de posiciones reales.
2. **Vista de conjunto:** si B dispone de ubicaciones de varios dispositivos obtenidas legítimamente, puede **ver sus marcadores en un mismo mapa** y distinguir a qué dispositivo pertenece cada uno.
3. **Información por dispositivo:** al consultar/seleccionar un marcador, Whereis ofrece el **ID de dispositivo** (o identificación funcional inequívoca), la **fecha y hora** de su posición y una señalización comprensible de si la posición es una última conocida/anterior. No se presenta una posición antigua como si fuera actual.
4. **Actualización individual manual:** el usuario puede seleccionar un dispositivo y pulsar **«Actualizar ubicación»** para solicitar una nueva posición **solo de ese dispositivo** y **solo si mantiene autorización activa**, respetando D-01/D-02. Una consulta fallida sigue D-06.
5. **No seguimiento continuo:** mostrar el mapa, moverlo, seleccionar marcadores o alternar entre dispositivos **no activa consultas de posición automáticas ni periódicas**, ni obtiene posiciones simultáneas de todos por el mero hecho de ver la pantalla.
6. **Dispositivos conocidos sin posición:** que B conozca el ID de A por QR/entrada manual (D-03) **no autoriza** a situar a A en el mapa. Sin una posición real disponible para B, no se inventa marcador; la app puede indicar «Ubicación no disponible» en la lista o detalle.
7. **Desactivación ordinaria de autorización (D-05):** tras revocación aplicada, B **no puede actualizar** A y puede seguir viendo la última ubicación legítima, fechada y rotulada como anterior **si no existe bloqueo ni eliminación**. En cambio, **D-09 / #19** y **D-10 / #20** confirman que un **bloqueo** oculta el marcador anterior sin exigir borrar la posición, y una **eliminación** confirmada borra última ubicación y personalización en el consultante.
8. **Fallo de actualización:** se informa del error; si existe última ubicación obtenida previamente se conserva visible en el mapa con fecha/hora y advertencia; si no, se indica «Ubicación no disponible» (D-06).
9. **Preferencia por tecnología libre:** deben **priorizarse** biblioteca y cartografía de código/datos abiertos compatibles con el proyecto, pero **TECH LEAD** elige y justifica solución, licencias, atribuciones, escalabilidad y costes según gobernanza; **ninguna opción tecnológica queda aprobada en D-07**.

## Estados funcionales y mapa

| Situación de A respecto de B | Mostrar ubicación de A en el mapa de B | Actualizar A desde B |
| --- | --- | --- |
| A conocido por ID/QR pero sin autorización y sin posición previa | No: sin marcador inventado | No |
| A autorizado y con posición previamente obtenida | Sí: marcador identificable, fecha/hora de última posición | Sí, solicitud puntual manual; éxito sujeto a Android/conexión |
| A autorizado, sin posición anterior, consulta fallida | No: «Ubicación no disponible» | Posibilidad de nueva consulta manual, sujeto a permiso/condiciones |
| A con autorización **simplemente desactivada**, sin bloqueo ni eliminación, con posición previa legítima | Sí: última posición **anterior** fechada (D-05) | No |
| A **bloqueado** (D-09) tras posición obtenida previamente | **No:** marcador oculto; posición anterior conservada solo en la medida prevista por D-10 | No |
| A **eliminado** de conocidos (D-10) | **No:** ubicación y personalización borradas del consultante tras confirmación | No |
| A reinstalado con ID nuevo (D-04) | Sin heredar antiguas autorizaciones ni generar nuevas coordenadas automáticamente | No hasta nuevo reconocimiento y autorización |

Se describe el **contrato observable**, no una decisión sobre cómo almacenar los marcadores.

## Criterios de aceptación

- **D07-CA01:** el usuario abre un mapa callejero interactivo integrado y puede desplazarse y cambiar el nivel de zoom.
- **D07-CA02:** con posiciones legítimas de dos dispositivos diferentes, ambos son distinguibles mediante marcadores en **un mismo mapa**, sin necesidad de abrir mapas separados.
- **D07-CA03:** al seleccionar un dispositivo con posición, se puede conocer al menos su identificación, fecha/hora y estado de actualidad/antigüedad.
- **D07-CA04:** desde un dispositivo con autorización activa se puede pulsar «Actualizar ubicación» para iniciar **una consulta puntual de ese dispositivo**; no es actualización automática del grupo.
- **D07-CA05:** abrir o mover el mapa y seleccionar marcadores no activa seguimiento ni consultas automáticas periódicas.
- **D07-CA06:** sin ubicación legítima previa no se pinta un marcador ficticio, aunque el dispositivo sea conocido; se muestra un estado de no disponibilidad donde corresponda.
- **D07-CA07:** si falla una actualización, se mantiene la última posición en el mapa y se rotula con fecha/hora + advertencia de antigüedad; si no hay posición, «Ubicación no disponible» (D-06).
- **D07-CA08:** la **desactivación ordinaria** del permiso impide nuevas consultas y mantiene visible una posición anterior legítima con fecha/hora cuando no haya bloqueo ni eliminación (D-05). Ante **bloqueo**, el marcador se oculta; ante **eliminación**, se borra la posición en el consultante, según D-09/D-10.
- **D07-CA10 (SEG-01/02):** cuando no se puede verificar identidad auténtica de la instalación y autorización activa/vigente, no se recibe ninguna posición nueva, aunque exista un estado local cacheado de «autorizado».
- **D07-CA11 (D-11/D-13):** pantalla principal dividida con mapa superior/lista inferior; foto o número, borde de color, agrupación de marcadores y ficha modal conforme D-11; fecha/hora de posición `DD/MM/AAAA HH:mm:ss` en zona local del consultante conforme D-13.
- **D07-CA09:** la visualización de varios dispositivos no concede permiso a quienes solo se conocen por ID, ni cambia las autorizaciones independientes.

## PENDIENTE — diseño técnico, licencias y diseño visual

- **Biblioteca/renderizador Android:** estudiar alternativas libres (por ejemplo MapLibre, sin elegirlo ni declararlo dependencia).
- **Fuente de datos y distribución de mapas:** cartografía abierta como OpenStreetMap es una alternativa; **su uso no implica disponer de un servicio de teselas gratuito ni ilimitado**. Verificar atribución, términos, volumen, política de caché, disponibilidad, costes y rendimiento antes de seleccionar.
- **D-11 / #21 CONFIRMADO:** pantalla principal dividida (mapa superior siempre visible y lista inferior), solo mapa maximizable; marcadores circulares con foto o número y borde de color, agrupaciones expandibles, selección desde lista sin recentrar y ficha inferior modal al pulsar marcador. Búsqueda, filtros, alias y numeración estable están fijados en D-11, sin convertirlos en selección de tecnología.
- **D-13 / #23 CONFIRMADO:** fecha/hora real de la ubicación `DD/MM/AAAA HH:mm:ss` en zona horaria del consultante (no relativa), precisión y dirección solo cuando existan; última posición no hereda dirección de otra captura.
- **PENDIENTE de diseño/viabilidad:** accesibilidad, composición adaptativa a distintas pantallas, rendimiento/legibilidad del agrupamiento, ubicación exacta de controles, comportamiento no especificado, pruebas de uso y límites técnicos de geocodificación.
- **D-10 / #20 y SEG-04 / #24 CONFIRMADOS:** solo la última posición legítima, sin caducidad funcional automática hasta eliminación; reinstalar consultante no recupera ID/ubicaciones/permisos, aunque el consultante que no se reinstala puede conservar última posición de emisor desinstalado. **PENDIENTE** retención conforme a normativa, borrado físico y copias externas, cifrado, ubicación de almacenamiento, límites Android y protección de menores.
- **Entornos sin conexión:** carga de mapa/teselas y comportamiento offline sin infraestructura.
- **Ampliación posterior CONFIRMADA en D-08 / #16 y D-12 / #22:** desde el mapa inicial existe «Actualizar todos» por pulsación manual; D-12 evita duplicar destinos ya en curso, añade consultas elegibles restantes y registra resultado independiente/resumen final. Sin Internet local no se encolan peticiones ni se refresca automáticamente tras reconectar. **PENDIENTE técnico:** límites reales de ejecución, timeout, paralelismo seguro, rendimiento y compatibilidad Android; no se habilita seguimiento automático.
- **Servicios opcionales:** navegación y rutas, imágenes satelitales, Street View, geocercas, historial y seguimiento en tiempo real **no aprobados para D-07**; su futuro estado MVP/POST-MVP requiere decisión adicional.
- **Infraestructura y costes:** no hay autorización de proveedor, gasto ni despliegue.

## Prioridad de autenticación y autorización — SEG-01/SEG-02 CONFIRMADAS

Para entregar **cualquier** nueva ubicación, no basta conocer un ID/QR, ni un interruptor activado mostrado desde estado local: hay que verificar identidad auténtica de instalación **y** autorización direccional vigente (**[#24](https://github.com/mundoinformaticacanaria/whereis/issues/24)**). Si esa verificación falla o no es posible, **no se obtiene dato nuevo**. Puede mostrarse la última posición legítima únicamente si las reglas D-09/D-10 permiten visualizarla; nunca fingir posición actual. El mecanismo y garantías de concurrencia y revocación son **PENDIENTES** de estudio TECH LEAD/ARQUITECTO. No se selecciona ahora proveedor o sistema de autenticación.

## Impacto

- **Producto:** experiencia cartográfica compartida de **varios dispositivos con posiciones disponibles**, similar en intención visual a Family Link, sin reproducir su modelo de identidad.
- **Arquitectura:** SDK de mapas, servicio de datos/teselas, compatibilidad y límites Android por estudiar (TECH LEAD).
- **Privacidad:** exponer únicamente datos ya recibidos lícitamente; advertir siempre de antigüedad y no sortear D-05.
- **Coste/operación:** librería/código abierto no equivale a servicio cartográfico alojado sin coste.

## Referencias de contexto, no fuentes de decisiones técnicas

- [Ayuda oficial de Google Family Link: ubicación](https://support.google.com/families/answer/7103413?hl=es). Solo referencia **orientativa** de experiencia descrita por el Propietario, no especificación copiada ni obligación tecnológica.
- [OpenStreetMap Foundation: política de uso de sus servidores públicos de mapas](https://operations.osmfoundation.org/policies/tiles/). La fundación diferencia datos abiertos de capacidad/condiciones de sus servidores públicos.

## Trazabilidad y handoff

- [D-07 — issue #14](https://github.com/mundoinformaticacanaria/whereis/issues/14).
- **PROPIETARIO:** comportamiento confirmado.
- **FUNCIONAL:** documentación y criterios de aceptación.
- **TECH LEAD:** siguiente acción de revisión de PR bajo **G-02 vigente**, con apoyo de ARQUITECTO activo para viabilidad/seguridad Android; evaluación cartográfica, licencias, límites y costes sin autoaprobar gasto/proveedores ni iniciar desarrollo. SEG-01/SEG-02 requieren verificar identidad y autorización activa para cada ubicación nueva; si no verificable, **denegar nuevas ubicaciones** (fail-closed).
- **QA:** revisión independiente posterior cuando haya implementación autorizada.
- **Baseline funcional global:** `PENDIENTE`.
