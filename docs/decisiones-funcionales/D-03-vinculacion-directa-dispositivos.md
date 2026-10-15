# D-03 — Identificación y vinculación directa de dispositivos mediante ID Whereis

- **Fecha de decisión del Propietario:** 15/10/2026.
- **Estado:** `CONFIRMADO` por aprobación expresa del Propietario; incorporación documental a `main` `PENDIENTE` de revisión y merge.
- **Clasificación:** `MATERIAL`.
- **Issue de decisión:** [#6 — D-03](https://github.com/mundoinformaticacanaria/whereis/issues/6).
- **Origen:** selección explícita del Propietario: «identificación y vinculación directa entre dispositivos mediante sus IDs fijos de Whereis, sin cuentas de usuario para el MVP, con solicitud y aceptación expresa desde el dispositivo que comparte ubicación».
- **Relaciones:** [D-01 / #1](https://github.com/mundoinformaticacanaria/whereis/issues/1) y [D-02 / #2](https://github.com/mundoinformaticacanaria/whereis/issues/2).
- **Baseline funcional global:** `PENDIENTE` (esta aprobación no valida el MVP completo).
- **Decisiones `SUPERSEDED`:** ninguna registrada.

## Necesidad y actores

Permitir que dispositivos Android se descubran e intercambien solicitudes de vinculación sin crear cuentas personales.

- **A (emisor):** dispositivo Android que puede conceder o rechazar acceso a su ubicación desde la aplicación instalada en A.
- **B, C (consultantes):** dispositivos Android que solicitan vincularse con A y, si obtienen permiso, pueden consultar su ubicación.

No se presupone una cuenta de usuario, rol parental, relación familiar o identificación legal de la persona que opera cada dispositivo.

## Decisión funcional CONFIRMADA

1. **Identificación directa de dispositivos:** el MVP no exigirá crear cuentas de usuario. Cada dispositivo usa el identificador fijo propio generado por Whereis aprobado en D-01.
2. **Sin teléfono:** no se usará el número de teléfono como identificador ni para la vinculación.
3. **Inicio de solicitud:** B proporciona el ID de Whereis de A y solicita vinculación/acceso a A.
4. **Aceptación expresa en A:** el dispositivo A debe permitir a quien lo maneja examinar y aceptar o rechazar expresamente la solicitud desde su aplicación. La solicitud o el conocimiento del ID no conceden acceso por sí solos.
5. **Permiso individual posterior:** una vez A acepta la solicitud de B, B queda autorizado a consultar A conforme a D-01 y D-02, sin aprobación adicional en cada consulta mientras la autorización sea válida.
6. **Pluralidad:** A puede autorizar a más de un dispositivo consultante (por ejemplo B y C). Las relaciones son independientes y el ID fijo de A no cambia al añadir vinculaciones.

## Flujo funcional principal

1. A y B disponen de Whereis y de sus respectivos identificadores de dispositivo.
2. B obtiene por un medio aún por concretar el ID de A y lo indica en su aplicación.
3. B solicita acceso a A; la solicitud no concede permisos.
4. A consulta la petición desde Whereis y **elige expresamente aceptar o rechazar**.
5. Si A acepta, queda establecida la autorización **A → B** (B puede consultar ubicación de A) con las condiciones que se determinen en D-04.
6. Si A rechaza o no llega a aceptar, B no adquiere acceso a la ubicación de A.

## Reglas derivadas de lo confirmado

- **D03-RN01:** el ID de Whereis identifica al dispositivo; **no es una contraseña ni una credencial de acceso**.
- **D03-RN02:** un vínculo de acceso nace únicamente tras aceptación expresa de A en respuesta a la solicitud.
- **D03-RN03:** aceptar B no acepta a C; cada consultante exige su propia autorización.
- **D03-RN04:** vincular otros dispositivos no cambia el ID de A.
- **D03-RN05:** el flujo no exige registro de cuenta personal ni validación mediante número telefónico.

## Criterios de aceptación verificables propuestos

- **D03-CA01:** B puede iniciar una solicitud al indicar el ID de A; antes de la aceptación no se habilita la consulta de ubicación.
- **D03-CA02:** A puede resolver de forma explícita la solicitud de B mediante aceptación o rechazo; el rechazo no concede acceso.
- **D03-CA03:** tras la aceptación, B puede solicitar la ubicación de A según D-01/D-02; A no tiene que aceptar de nuevo cada consulta autorizada.
- **D03-CA04:** A acepta a B y a C separadamente; el ID de A no cambia y ninguno hereda los permisos del otro.
- **D03-CA05:** el flujo no requiere cuenta de usuario ni número de teléfono.
- **D03-CA06:** un dispositivo D que conoce el ID de A, sin autorización, no puede consultar su posición.

Estos criterios expresan comprobaciones del comportamiento aprobado. Los estados de interfaz y mensajes exactos siguen `PENDIENTE`.

## Flujos alternativos y errores: PENDIENTE de detalle

- El ID introducido no existe, es erróneo o identifica al propio dispositivo.
- El dispositivo A está desconectado, no recibe todavía la petición o no puede mostrarla.
- La solicitud queda sin respuesta, expira o se duplica.
- El solicitante envía solicitudes repetidas o maliciosas.
- El titular rechaza; B intenta solicitar de nuevo.
- El dispositivo se pierde, se desinstala la aplicación o se restablece: no se ha acordado recuperación ni persistencia del ID fuera de la vigencia definida en D-01.
- La app debe distinguir **solicitud**, **aceptación**, **vínculo vigente** y **revocación**, pero caducidad y gestión quedan para D-04/D-05.

Ninguna solución concreta para estos casos queda autorizada por D-03.

## Impacto y riesgos

- **Alcance:** simplifica el MVP prescindiendo de cuentas de usuario; no determina identidad civil ni relación familiar.
- **Seguridad / privacidad:** conocer un ID no puede bastar para consultar la ubicación. Autenticidad del dispositivo, posesión real y protección frente a suplantación requieren diseño y validación posteriores.
- **Arquitectura:** generación, estabilidad, asociación y mecanismos de solicitud/aceptación se remiten a evaluación de TECH LEAD; no se seleccionan servicios, SDK, proveedores ni persistencia.
- **Operación y costes:** `PENDIENTE`.

## Fuera de alcance de esta decisión

- Autorizaciones temporales/permanentes y administración detallada: **D-04**.
- Revocación y sus consecuencias: **D-05**.
- Persistencia del ID tras reinstalar, restaurar copia o cambiar teléfono.
- Método visual de intercambio (copiar ID, QR, etc.), avisos, notificaciones y presentación exacta de solicitudes.
- Tratamiento de menores, identidad de la persona, control parental y autenticación adicional.
- Implementación técnica y baseline funcional global.

## Siguiente acción / handoff

- **PROPIETARIO:** la decisión D-03 ya está aprobada.
- **FUNCIONAL:** formalización y trazabilidad en la issue y PR.
- **TECH LEAD:** revisión documental e integración bajo gobernanza G-01 V3. Evaluar después implicaciones técnicas y de seguridad, sin activar automáticamente ARQUITECTO u otros roles no permanentes.
- **QA:** mantiene independencia de revisión para entregas de implementación posteriores; esta documentación no autoriza programar.
