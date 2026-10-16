# D-03 — Dispositivos conocidos y primera solicitud de consulta de ubicación

- **Aprobación original:** 15/10/2026.
- **Ampliación / matización del PROPIETARIO:** 16/10/2026.
- **Estado:** `CONFIRMADO` por el PROPIETARIO; documento pendiente de integración en `main`.
- **Clasificación:** `MATERIAL` — cambio funcional de relación entre dispositivos.
- **Issue:** [#6](https://github.com/mundoinformaticacanaria/whereis/issues/6). **PR:** [#7](https://github.com/mundoinformaticacanaria/whereis/pull/7).
- **Relacionado:** [D-01 #1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02 #2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8) y D-05.
- **Baseline funcional global:** `PENDIENTE`.

## Necesidad y actores

Reconocer dispositivos mediante su ID fijo Whereis, independientemente de concederles acceso, y utilizar una primera petición de permiso de consulta que pueda aceptarse desde la app mediante un interruptor. Evitar solicitudes repetidas al suspender y reactivar permisos de un dispositivo conocido.

- **A:** dispositivo cuya ubicación B quiere consultar y único que autoriza ese acceso.
- **B, C, ...:** dispositivos que A puede reconocer e individualmente autorizar.
- No existen cuentas personales en el MVP; identificarse como dispositivo no autentica la identidad civil de su usuario.

## Comportamiento CONFIRMADO

1. **ID de dispositivo:** cada instalación de Whereis dispone de su ID fijo, sin asociarlo a número telefónico ni cuenta. El ID sigue fijo mientras vive esa instalación (D-01 y D-04).
2. **Registro de dispositivos conocidos:** antes de solicitar consultar su ubicación, B añade/reconoce A mediante **escaneo de QR** con ID Whereis o **introducción manual del código/ID**. Aparece en su lista de dispositivos conocidos.
3. **Conocer no equivale a autorizar:** añadir A a la lista de B no entrega ubicación ni activa acceso. La lista de conocidos y los permisos de ubicación son conceptos independientes.
4. **Primera petición:** B, desde su lista, envía a A una solicitud para **consultar su ubicación puntual**, no para seguimiento continuo. A recibe **una notificación**, desde la que se puede abrir la sección de dispositivos conocidos/vinculados en Whereis.
5. **Control de acceso en A:** en la lista de A se ve cada dispositivo conocido/solicitante con un **interruptor de autorización activado/desactivado** específico para ese dispositivo. A activa o no el permiso de B expresamente desde su propia app.
6. **Activación inicial condicionada a permisos:** la primera vez que A vaya a activar la consulta a favor de otro dispositivo, Whereis debe **comprobar ubicación del sistema y los permisos Android necesarios para la modalidad aprobada** y guiar al usuario si faltan. La app no concede permisos de Android automáticamente.
7. **Reactivación simple:** después de desactivar un permiso, A podrá volver a activarlo en el mismo dispositivo conocido **sin exigir a B otra solicitud ni generar otra notificación por este cambio** (D-05). El permiso activo es unidireccional: A permite a B consultar A, no al revés.
8. **Múltiples dispositivos:** A puede conocer y autorizar B y C individualmente; el cambio del permiso de B no altera el de C ni cambia el ID de A.
9. **Evitar peticiones duplicadas:** el flujo de primera solicitud no debe llenar la bandeja de A con múltiples solicitudes idénticas del mismo dispositivo. Como regla funcional se mantendrá **como máximo una solicitud pendiente de ese solicitante para A**; los detalles de limpieza, reintentos o caducidad siguen pendientes.
10. **Notificación no es consentimiento:** recibir o abrir la notificación nunca activa por sí solo permiso de localización. Si no se muestran notificaciones del sistema, la solicitud debería seguir siendo visible en la app.

## Flujo principal

1. B abre Whereis y agrega A a **Dispositivos conocidos** leyendo su QR o introduciendo su ID.
2. B ve A como conocido, inicialmente **sin autorización** para consultar su posición.
3. B solicita por primera vez consultar A; Whereis envía a A una notificación de solicitud.
4. Desde la notificación o desde la app, A accede a los dispositivos conocidos y reconoce a B por su ID. La autenticidad de las identidades técnicas requiere evaluación.
5. A decide activar o mantener desactivado el interruptor de permiso para B.
6. Si activa por primera vez, Whereis verifica permisos/servicios Android para la modalidad de ubicación prevista; debe señalar si faltan. El comportamiento ante denegación sigue `PENDIENTE` de detalle.
7. Solo con autorización activa y permisos de Android suficientes B puede intentar consultas puntuales (D-01/D-02).
8. Si A apaga el interruptor, B pierde acceso a **nuevas ubicaciones**; se conserva la última posición obtenida con fecha y hora (D-05).
9. A puede reactivar ese mismo permiso sin nueva solicitud; B puede volver a consultar posiciones puntuales cuando la autorización activa sea efectiva.

## Criterios de aceptación

- **D03-CA01:** al escanear QR o ingresar ID de A, B registra un dispositivo conocido **sin** recibir permiso de consulta.
- **D03-CA02:** desde la lista B puede enviar primera solicitud; A recibe aviso dirigido a su sección de dispositivos conocidos, sujeto a permisos de notificaciones Android; la solicitud permanece accesible en Whereis.
- **D03-CA03:** A ve a B con estado de permiso individual activado/desactivado y puede decidirlo sin conceder permisos al recibir aviso.
- **D03-CA04:** sin activación expresa del permiso para B no se facilita ninguna posición nueva, aunque B conozca el ID de A.
- **D03-CA05:** B y C son independientes y el ID de A es inalterado mientras dura la instalación.
- **D03-CA06:** tras desactivar y reactivar B desde A, no se exige nueva solicitud a B ni se reenvía notificación para reactivación.
- **D03-CA07:** para A solo existe como máximo una solicitud pendiente por el par A/B; no aparecen duplicados por solicitudes reiteradas.
- **D03-CA08:** en la primera activación se comprueban servicios/permiso de ubicación en el dispositivo que comparte y se indica qué habilitaciones Android faltan; no se conceden silenciosamente.
- **D03-CA09:** el flujo del MVP no exige cuenta personal ni número telefónico.

## Reglas de plataforma y privacidad — límites

- D-02 requiere intentar consultas aun cuando Whereis no sea visible en A. El control de **ubicación en segundo plano** tiene restricciones/permisos Android independientes y requiere validación técnica para las versiones soportadas.
- El **permiso de notificaciones** puede ser necesario para mostrar avisos; si no está concedido, ello no debe conceder acceso y la app debe permitir consultar las solicitudes recibidas.
- El **escáner QR** puede necesitar permisos de cámara según la implementación; no se selecciona lector, SDK ni tecnología en D-03.
- Conocer un ID no constituye autenticación técnica suficiente. Las medidas anti-suplantación/anti-spam necesitan diseño.
- Se mantiene la regla D-04: **desinstalar/reinstalar** es instalación nueva con nuevo ID, sin heredar conocidos ni autorizaciones, y exige nuevas vinculaciones y aceptación. **Desactivar un interruptor sin desinstalar** conserva el dispositivo conocido.
- No implica seguimiento continuo ni automático: todas las ubicaciones siguen siendo consultas puntuales.

## Fuera de alcance y asuntos PENDIENTES

- Mecanismo técnico de intercambio seguro de IDs/QR y prueba de control de instalaciones, autenticidad y protección contra suplantación.
- Forma de gestionar duplicados ya resueltos, peticiones no respondidas/caducadas, denegaciones de permisos Android, tiempos de entrega, notificaciones sin conectividad, UX exacta.
- Gestión de solicitudes cuando A no ha agregado a B previamente: debe mostrarse de forma segura el ID de B al recibirla; disposición exacta de lista `PENDIENTE`.
- Estados visibles durante revocación o reactivación con conectividad limitada (D-05); cómo evitar autorización efectiva antes de confirmar cambios.
- Gestión de ubicaciones almacenadas más allá de la **última posición obtenida** y su retención general; no se aprueba historial geográfico.
- No se autoriza desarrollo, proveedor, infraestructura, coste ni baseline MVP.

## Historia de decisiones (no reinterpretar aprobaciones)

- El **núcleo de D-03 de 15/10** se conserva: identificación por ID fijo, sin cuentas, consentimiento expreso del dispositivo emisor y acceso individual.
- La descripción anterior «introducir ID y solicitar directamente vinculación/aceptarla como relación única» queda **SUPERSEDED solo como flujo** por el nuevo de **registrar conocido → primera solicitud notificada → activar/desactivar interruptor**.
- La desactivación y reactivación sin una solicitud nueva está aprobada el 16/10 y desarrollada en D-05.
- El detalle de reinstalación sigue lo confirmado en D-04; no equivale a una reactivación por interruptor.

## Handoff

**TECH LEAD** revisa compatibilidad técnica, seguridad, límites Android y la PR #7 sobre su head SHA actual; después corresponde integración conforme a G-01 V3. **QA** será independiente para implementación futura. El cambio documental **no autoriza desarrollo**.
