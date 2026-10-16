# D-08 — Mapa como pantalla inicial y acceso a la lista de dispositivos

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

El Propietario aprobó expresamente el 16/10/2026 la opción A, solicitó conservar **selección individual**, **actualización manual** y respeto de las **autorizaciones D-01 a D-07**, y autorizó su formalización en GitHub.

## Actores

- **Dispositivo consultante B:** dispone de Whereis e identifica otros dispositivos mediante ID fijo o QR según D-03.
- **Dispositivos A, C, etc.:** conocidos por B; pueden estar autorizados o no para compartir su posición con B. Una posición solo existe en el mapa si B ya la obtuvo legítimamente de la instalación correspondiente.

«Dispositivo conocido» no es sinónimo de «dispositivo con posición disponible» ni de «dispositivo autorizado».

## Contrato funcional CONFIRMADO

1. **Mapa de inicio.** La vista de entrada de la funcionalidad principal de Whereis es el **mapa callejero interactivo conjunto** aprobado en D-07. La lista de dispositivos no reemplaza esa pantalla inicial.
2. **Acceso a dispositivos.** Desde el mapa inicial se puede **acceder fácilmente a una lista de dispositivos conocidos**, incluidos los que no tienen posición disponible.
3. **Representación en mapa.** Las ubicaciones ya obtenidas legítimamente de distintos dispositivos pueden mostrarse en **un mismo mapa**, con **marcadores distinguibles** por dispositivo. Estar en la lista de conocidos, por sí solo, no genera un marcador ni habilita consulta.
4. **Selección individual.** Se puede **seleccionar un dispositivo concreto** y consultar la información disponible de ese dispositivo (identificación y, si existe, **fecha y hora de la posición** y estado de antigüedad).
5. **Actualización manual.** La acción **«Actualizar ubicación»** se refiere **al dispositivo seleccionado**. Si B tiene autorización activa de A, puede intentar una **consulta puntual** de A; no se inician solicitudes a otros dispositivos por selección o apertura de pantalla.
6. **Sin seguimiento continuo.** Entrar al mapa, desplazarse, hacer zoom o consultar la lista **no inicia seguimiento en tiempo real ni consultas de ubicación periódicas automáticas** (D-01, D-07).
7. **Sin permisos.** Si un dispositivo está simplemente registrado como conocido y no ha autorizado B, no se permite a B consultar nuevas ubicaciones (D-03). Si A ha desactivado el permiso de B, no se permiten nuevas consultas (D-05).
8. **Última ubicación antigua.** Si B conserva una posición previamente obtenida de A después de la desactivación, permanece visible con **fecha y hora** y señalización inequívoca de **posición anterior, no actual**, conforme a D-05.
9. **Fallo de consulta.** Si una consulta autorizada falla, la interfaz informa del fallo y, si existe, muestra la **última ubicación conocida** con fecha, hora y advertencia; en ausencia de posición previa indica **«Ubicación no disponible»** (D-06).
10. **Instalaciones nuevas.** La reinstalación de Whereis genera un nuevo ID sin heredar relaciones ni permisos de la anterior (D-04); D-08 no altera esa regla.

## Ejemplo funcional sin datos reales

El dispositivo consultante B conoce tres dispositivos por ID:
- **A:** autorización activa y ubicación obtenida anteriormente; tiene un marcador identificable y se puede seleccionar para solicitar actualización manual.
- **C:** autorización desactivada, pero B había obtenido una ubicación con anterioridad; permanece visible la **última ubicación de C con fecha y hora**, sin habilitar «Actualizar ubicación» para C.
- **D:** dispositivo conocido sin ubicación previa. Puede aparecer en la **lista de conocidos**, pero **no** se presenta un marcador ficticio para D.

Al abrir el flujo principal, B ve **el mapa conjunto** con las posiciones disponibles y puede entrar a la lista para seleccionar/gestionar dispositivos sin conferirles nuevos permisos.

Los nombres A/B/C/D son ilustrativos, **no** IDs reales, etiquetas obligatorias ni usuarios de prueba.

## Criterios de aceptación (observables)

- **D08-CA01 — Inicio:** al entrar en el flujo principal Whereis presenta primero el mapa interactivo conjunto, no la lista.
- **D08-CA02 — Lista accesible:** desde ese mapa el usuario puede abrir una lista de dispositivos conocidos aunque alguno carezca de ubicación disponible.
- **D08-CA03 — Vista de varios dispositivos:** cuando B tiene ubicaciones legítimas previas de A y C, ambos pueden identificarse como marcadores distintos en un mismo mapa.
- **D08-CA04 — Selección:** al seleccionar A se presentan la identificación del dispositivo y la fecha/hora de la última posición disponible, rotulada como anterior cuando lo es.
- **D08-CA05 — Refresco manual individual:** pulsar «Actualizar ubicación» para A autorizado intenta consultar una posición puntual de **A**, no de C; el mapa no dispara rastreo continuo por estar abierto.
- **D08-CA06 — Dispositivo conocido no autorizado:** el hecho de aparecer en la lista no habilita consultas ni marcadores de posición sin datos legítimos.
- **D08-CA07 — Revocación:** B puede seguir viendo una ubicación anterior de A, si existe, con su fecha/hora después de la revocación aplicada, pero no puede obtener una nueva.
- **D08-CA08 — Consulta fallida:** si falla la actualización, el mapa no convierte el último dato en «actual» y muestra el aviso previsto en D-06.
- **D08-CA09 — Sin actualización automática:** abrir el mapa, entrar en la lista o cambiar de marcador no genera nuevas solicitudes de ubicación por sí solo.

## PENDIENTE — no aprobado por D-08

- **Navegación exacta:** si se usa una barra inferior con pestañas, un botón, un menú lateral u otra disposición para ir a la lista de dispositivos. Las maquetas previas eran ilustrativas.
- **Diseño de pantallas secundarias:** agrupación de permisos, solicitudes, dispositivo propio/QR, ajustes, orden de listas, filtros, favoritos, alias y etiquetas visuales.
- **Encuadre inicial del mapa:** centro, zoom inicial, comportamiento si no hay posiciones, persistencia de la última vista.
- **Estados de carga, accesibilidad e interacción:** comportamiento exacto de selección en mapa/lista, superposición de marcadores, errores, información contextual.
- **Onboarding, primera instalación y gestión de permisos Android:** D-08 define la vista inicial del **flujo principal**; no sustituye las comprobaciones de permisos ni resuelve pantallas de primera instalación.
- **Conectividad/offline y posición antigua:** reglas de sincronización/retención general aún pendientes en D-05/D-06.
- **Elección técnica:** SDK/cartografía libre, fuentes de teselas, proveedor, licencias, costes, datos y arquitectura quedan en manos de evaluación del **TECH LEAD** según D-07 y gobernanza. No hay selección ni gasto aprobado.
- **Actualización masiva del grupo, navegación, rutas, seguimiento continuo, historial geográfico:** no aprobados por esta decisión.

## Impacto y verificación de coherencia

- **UX/producto:** da prioridad al mapa conjunto como entrada, conservando el acceso a todos los dispositivos conocidos.
- **Consentimiento/privacidad:** marcador y nuevas consultas dependen de la posición previamente obtenida y de la autorización vigente; conocer un dispositivo no da acceso.
- **Seguridad y arquitectura:** selección, renderización y comunicaciones deben respetar autorización activa y límites de Android sin imponer implementación.
- **Costes:** `PENDIENTE`.

El contrato de D-07 sigue `CONFIRMADO`, y D-08 **solo añade** la organización de la vista principal y el acceso a lista.

## Handoff

- **PROPIETARIO:** opción A CONFIRMADA el 16/10/2026.
- **FUNCIONAL:** issue y documento de especificación en PR para revisión.
- **TECH LEAD:** siguiente responsable de revisión de criterios e integración documental conforme a G-01 V3; validación técnica posterior sin elegir proveedores no autorizados.
- **QA:** mantiene independencia en futuras implementaciones.
- **Baseline funcional global / autorización de desarrollo:** `PENDIENTE`.
