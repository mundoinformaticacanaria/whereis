# G-01 V3 — Gobernanza mínima de Whereis

- **Fecha:** 15/10/2026
- **Estado:** `CONFIRMADA` por el `PROPIETARIO`
- **Clasificación:** `MATERIAL` — gobernanza
- **Fuente de autorización:** [Issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4)
- **Sustituye:** propuestas G-01 anteriores de ocho roles activos y de cuatro roles sin `FUNCIONAL`. No sustituye decisiones funcionales D-01 y D-02.

## Contexto

Whereis es un proyecto Android de consultas de geolocalización entre dispositivos autorizados. La plantilla inicial contiene ocho perfiles, pero para el arranque el Propietario ha elegido un modelo con cinco funciones activas, manteniendo separación entre negocio, análisis, dirección técnica, programación y verificación.

## Decisión confirmada

Solo cinco **roles activos iniciales**:

| Rol | Responsabilidad y límites |
| --- | --- |
| `PROPIETARIO` | Aprueba alcance, prioridades de producto, requisitos y decisiones materiales reservadas, servicios, proveedores y gasto. Las propuestas de agentes no implican autorización. |
| `FUNCIONAL` | Independiente de `TECH LEAD`: analiza y documenta actores, comportamientos, permisos funcionales, reglas, flujos, validaciones y criterios de aceptación. No aprueba requisitos materiales por sí solo ni decide implementación. |
| `TECH LEAD` | Planifica y asigna trabajo autorizado, coordina inicialmente arquitectura y DevOps, asegura calidad e integración, revisa y decide el merge. No sustituye la autoridad del Propietario. |
| `PROGRAMADOR` | Implementa únicamente una issue autorizada y asignada a una identidad ejecutora, en rama propia y mediante PR. No amplía alcance ni hace merge. |
| `QA` | Revisa de forma **independiente del autor** los entregables de código; dictamina `APTO`, `DEFECTOS` o `BLOQUEADO`. No aprueba sus propios cambios ni realiza merge. |

No se fija aquí ningún número de personas, nombre de agente, identidad ejecutora ni contratación. Un rol representa una responsabilidad; la independencia efectiva de QA deberá verificarse antes de implementar.

### Circuitos

- **Funcional:** `FUNCIONAL → PROPIETARIO (aprobación cuando corresponda) → TECH LEAD`. El paso por Propietario es obligatorio para decisiones materiales que requieren autoridad humana.
- **Implementación:** `TECH LEAD (asigna) → PROGRAMADOR → QA independiente → TECH LEAD (merge o devolución)`. QA con resultado `DEFECTOS` o `BLOQUEADO` impide tratar la entrega como apta.
- Los cambios posteriores al head SHA revisado invalidan la revisión anterior para integración.
- La implementación no comienza sin baseline funcional/arquitectónico mínimo y bootstrap aplicable aprobados.

### Especialidades no activas de modo permanente

`ARQUITECTO`, `DEVOPS` y `COMERCIAL` se conservan como contextos de referencia y capacidades activables únicamente ante necesidad real y autorización. El Tech Lead coordina arquitectura/operación inicial sin adjudicarse permisos de contratación, infraestructura o proveedores. Cuando sea necesario criterio especialista, se solicita y registra la intervención correspondiente; no se presume disponibilidad.

### Controles conservados

- GitHub como fuente de verdad; issue y comentarios forman el contrato de trabajo vivo; documentación canónica de `main` prevalece sobre chats y logs.
- Clasificación `RUTINARIA` / `MATERIAL`; estados explícitos `CONFIRMADO`, `HIPÓTESIS`, `PROPUESTA`, `PENDIENTE`, `POST-MVP`, `SUPERSEDED`.
- Una única label de **siguiente acción** por issue ejecutable cuando estén configuradas las labels; para Programador, una identidad ejecutora inequívoca.
- Ningún programador realiza merge; revisiones QA independientes antes de integrar código; revisión final del Tech Lead; no alterar controles para obtener verde.
- Privacidad y seguridad de datos de ubicación siguen siendo cuestiones materiales sujetas a aprobación y revisión, no una excepción por tamaño de equipo.

## Alternativas consideradas

1. Ocho roles activos desde el arranque: no elegida por su mayor carga operativa.
2. Cuatro roles activos, absorbiendo `FUNCIONAL` en `TECH LEAD`: no elegida; el Propietario exigió independencia funcional.
3. Cinco roles activos: **elegida y confirmada**.

## Consecuencias y riesgos

- Menos handoffs administrativos, con responsabilidad técnica adicional en el Tech Lead.
- La independencia de QA es un control irrenunciable; si un mismo ejecutor implementa y revisa, se requiere una persona/agente independiente antes del merge, no una autoaprobación.
- Si la arquitectura, seguridad Android o costes exceden la capacidad del equipo, se solicita intervención especialista sin convertirla en un rol activo permanente automáticamente.
- La decisión **no** autoriza implementación, servicios de pago, proveedores, infraestructura ni modificación del alcance funcional.

## PENDIENTE — fuera de la aprobación G-01

- Identidades reales, disponibilidad y prefijos de ramas para los ejecutores, y separación de QA en la práctica.
- Configuración de labels y permisos de GitHub, protección de `main`, reglas técnicas de merge y CI/gates específicos al stack.
- Zona horaria de heartbeat, rama `ops/logs` y logs de los roles realmente activos.
- Baseline funcional, baseline arquitectónico, alcance aprobado del MVP, primer backlog ejecutable y autorización inicial de desarrollo.
- Activación de expertos por una necesidad concreta.

No se consideran ejecutadas ni autorizadas estas configuraciones por la aprobación de G-01.

## Trazabilidad

- [Decisión material en issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4).
- PR de incorporación a `main`: enlazada en la issue una vez creada.
- Decisiones funcionales D-01/D-02 y su PR son independientes y no se modifican aquí.
