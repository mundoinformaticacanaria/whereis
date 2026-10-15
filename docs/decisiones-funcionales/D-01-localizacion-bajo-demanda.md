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
- Mostrar una ubicación antigua como si fuera una posición obtenida en la consulta contradice el propósito de la consulta puntual; el tratamiento de últimas ubicaciones conocidas se decidirá aparte.

## Criterios de aceptación propuestos para el desarrollo posterior

- **D01-CA01:** A conserva el mismo ID de Whereis al autorizar a B y posteriormente a C.
- **D01-CA02:** B y C pueden ser autorizados a consultar A sin invalidarse mutuamente.
- **D01-CA03:** un dispositivo D que solo conozca el ID de A, sin autorización, no obtiene su ubicación.
- **D01-CA04:** una consulta autorizada solicita una posición puntual; al pulsar «Actualizar ubicación» se inicia otra consulta.
- **D01-CA05:** no se inicia una secuencia automática de posiciones ni seguimiento continuo por la mera existencia de una autorización.

## Validaciones, errores y excepciones

- Si el dispositivo consultante no está autorizado, no se facilita ubicación.
- Si no puede obtenerse una posición nueva, no se debe afirmar que se ha obtenido; la respuesta exacta y la posible última ubicación quedan `PENDIENTE` de decisiones posteriores.
- Se deberá definir qué ocurre cuando un dispositivo se reinstala, restablece o cambia de titular.

## Límites y cuestiones PENDIENTES

- **D-03:** procedimiento para intercambiar/presentar el ID y verificar control del dispositivo; ciclo de vida del identificador, incluido cambio o reinstalación.
- **D-04:** duración, gestión y alcance de autorizaciones.
- **D-05:** revocación y propagación.
- **D-02:** ejecución de consultas cuando la app emisora no está visible (documentada por separado).
- Persistencia, caducidad de posiciones, latencia, tolerancia a fallos, precisión y experiencia de usuario detallada.
- **POST-MVP propuesto, no aprobado como exclusión global:** seguimiento continuo y visualización de trayectos.

## Riesgos e impacto

- **Privacidad:** el ID no debe actuar como llave de consulta.
- **Alcance:** no convertir ubicaciones puntuales en vigilancia continua.
- **Arquitectura y costes:** `PENDIENTE` de evaluación por ARQUITECTO y TECH LEAD.
- No se decide tecnología, proveedor ni infraestructura en este documento.

## Handoff

Revisión documental con `TECH LEAD`; análisis técnico posterior con `ARQUITECTO` cuando corresponda. Ninguna implementación autorizada por esta decisión de forma aislada.
