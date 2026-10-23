# D-01 — Localización bajo demanda e identificador fijo de dispositivo

- **Fecha de aprobación del Propietario:** 15/10/2026.
- **Estado de la decisión funcional:** `CONFIRMADO` por aprobación expresa del Propietario; incorporación a `main` pendiente de revisión/merge.
- **Clasificación:** `MATERIAL`.
- **Fuente de trazabilidad:** [Issue #1](https://github.com/mundoinformaticacanaria/whereis/issues/1).
- **Origen:** definición del producto Whereis y decisiones expresadas en la conversación con el Propietario el 15/10/2026.
- **Baseline funcional del proyecto:** `PENDIENTE`; esta decisión no constituye aprobación global del MVP.
- **Decisiones sustituidas (`SUPERSEDED`):** ninguna registrada.

## Necesidad

Permitir que un dispositivo Android autorizado consulte una posición puntual de otro dispositivo Android sin seguimiento continuo, con posibilidad de autorizar varios consultantes.

## Actores

- **A:** dispositivo que comparte su posición y desde cuya app se autoriza la relación.
- **B, C, ...:** dispositivos consultantes, cada uno con autorización individual.

## Comportamiento CONFIRMADO

1. Cada dispositivo tiene un **identificador fijo propio generado por Whereis**. Añadir nuevas vinculaciones no cambia ese identificador.
2. No se utilizará el **número de teléfono** para identificar ni vincular dispositivos.
3. A puede conceder acceso a **varios dispositivos** al mismo tiempo, de forma individual.
4. Conocer el ID de A no concede acceso: A debe **autorizar expresamente desde la app** cada dispositivo consultante.
5. Una vez concedida la autorización, B puede solicitar la ubicación puntual de A **en el momento de su consulta**, sin que A deba aceptar otra vez cada solicitud.
6. B puede **refrescar manualmente** la ubicación, realizando una nueva solicitud.
7. No habrá seguimiento continuo, actualización automática periódica ni visualización del desplazamiento en tiempo real.

## Reglas funcionales

- Las relaciones de autorización son específicas entre el dispositivo emisor y cada dispositivo consultante.
- La autorización concedida a B no concede automáticamente acceso a C.
- Un identificador de dispositivo no es un secreto de acceso ni sustituye la autorización.
- Una ubicación anterior nunca se presenta como actual. **D-05 / #10** y **D-06 / #12** confirman que, si se revoca la autorización o falla una consulta, se puede mostrar la última ubicación obtenida legítimamente, con su fecha/hora real y aviso inequívoco de antigüedad. **D-10 / #20** confirma que se conserva solo la última posición y no un historial, sujeto a la revisión legal de su retención.

## Criterios de aceptación propuestos para el desarrollo posterior

- **D01-CA01:** A conserva el mismo ID de Whereis al autorizar a B y posteriormente a C.
- **D01-CA02:** B y C pueden ser autorizados a consultar A sin invalidarse mutuamente.
- **D01-CA03:** un dispositivo D que solo conozca el ID de A, sin autorización, no obtiene su ubicación.
- **D01-CA04:** una consulta autorizada solicita una posición puntual; al pulsar «Actualizar ubicación» se inicia otra consulta.
- **D01-CA05:** no se inicia una secuencia automática de posiciones ni seguimiento continuo por la mera existencia de una autorización.

## Validaciones, errores y excepciones

- Si el dispositivo consultante no está autorizado, no se facilita ubicación.
- Ante un fallo de consulta autorizada se muestra el error y, si existe, la última ubicación legítima con fecha/hora y aviso de que no es actual; en caso contrario, «Ubicación no disponible» (**D-06 / #12**).
- Si no se puede **verificar la autorización vigente**, no se facilita una ubicación nueva (**SEG-01 / #24**, `CONFIRMADO`), sin prometer detección instantánea de revocación remota.
- Reinstalar Whereis produce un **nuevo ID y una relación nueva**; la instalación nueva no recupera ubicaciones ni autorizaciones mediante copias de seguridad (**D-04 / #8; SEG-04 / #24**). La última ubicación legítima en otro consultante que no se ha reinstalado se rige por **D-10 / #20**.
- Cambiar de titular sin reinstalar, la seguridad de la prueba de identidad y la detección remota de reinstalación requieren validación/decisiones posteriores; no se infiere que cambiar de titular por sí solo sea detectable.

## Límites y cuestiones PENDIENTES

- **D-03 / #6 y D-09 / #19 — CONFIRMADO:** alta por QR/ID sin permiso implícito, solicitud de autorización individual y recepción incluso desde dispositivo aún desconocido; aceptar lo añade a conocidos **sin** conceder ubicación. La autenticación de la instalación y la defensa contra suplantación deben cumplir **SEG-02 / #24**; arquitectura concreta `PENDIENTE`.
- **D-04 / #8 y SEG-04 / #24 — CONFIRMADO:** vigencia sin caducidad automática hasta revocación o desinstalación; reinstalación genera nuevo ID y no restaura ubicaciones ni permisos. Detección/sincronización remota y garantías de backup `PENDIENTE` de validación.
- **D-05 / #10 — CONFIRMADO:** revocación individual y posible reactivación sin nueva solicitud mientras se conserve la relación; propagación, concurrencia y conectividad requieren estudio. **SEG-01 / #24** confirma denegar posición nueva cuando no pueda verificarse el permiso vigente.
- **D-02 / #2 — CONFIRMADO:** consultas cuando app emisora no está visible, siempre sujetas a límites reales de Android, que requieren contraste técnico.
- **D-06 / #12 y D-10 / #20 — CONFIRMADO:** error con última ubicación legítima fechada/no actual, o «Ubicación no disponible»; **una sola** última posición sin historial y conservada funcionalmente hasta eliminar el dispositivo. Retención conforme a ley, borrado efectivo, copias externas y localización del almacenamiento siguen `PENDIENTE`.
- **D-07 / #14, D-08 / #16, D-11 / #21, D-12 / #22 y D-13 / #23 — CONFIRMADO en su alcance funcional:** mapa/lista, actualización manual individual y grupal, estados operativos y ficha con precisión. Viabilidad Android, latencia/timeout técnico, exactitud, seguridad, costes y proveedores requieren evaluación.
- El **baseline funcional global**, las garantías de seguridad/menores **#24** y la arquitectura completa siguen `PENDIENTE`; no se autoriza implementación.
- **POST-MVP propuesto, no aprobado como exclusión global:** seguimiento continuo y visualización de trayectos.

## Riesgos e impacto

- **Privacidad:** el ID no debe actuar como llave de consulta.
- **Alcance:** no convertir ubicaciones puntuales en vigilancia continua.
- **Arquitectura y costes:** `PENDIENTE` de evaluación por ARQUITECTO y TECH LEAD.
- No se decide tecnología, proveedor ni infraestructura en este documento.

## Handoff

Revisión documental con `TECH LEAD`; análisis técnico posterior con `ARQUITECTO` cuando corresponda. Ninguna implementación autorizada por esta decisión de forma aislada.
