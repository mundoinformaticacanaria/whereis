# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 15/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3 CONFIRMADA** por el PROPIETARIO: cinco roles activos iniciales (`PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `PROGRAMADOR`, `QA`). Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. Los roles son funciones; las identidades ejecutoras reales y disponibilidad siguen `PENDIENTE`.

## Baselines

- **Gobernanza:** G-01 V3 `CONFIRMADA`; documentación de aplicación e implantación técnica en curso.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. Las decisiones D-01 y D-02 constan en [issues #1](https://github.com/mundoinformaticacanaria/whereis/issues/1) y [#2](https://github.com/mundoinformaticacanaria/whereis/issues/2), con documentación propuesta en [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión/integración; no equivalen a aprobación del baseline global.
- **Baseline arquitectónico:** `PENDIENTE`.
- **Estado MVP/beta:** `PENDIENTE`; implementación no autorizada.

## Organización activa confirmada

- `PROPIETARIO`: decide autorizaciones y materiales reservados.
- `FUNCIONAL`: análisis funcional independiente y criterios de aceptación.
- `TECH LEAD`: coordinación técnica, arquitectura/DevOps iniciales, asignaciones, calidad y merge.
- `PROGRAMADOR`: desarrollo de issues autorizadas con identidad ejecutora única.
- `QA`: evaluación independiente del implementador y dictamen previo a cualquier merge de código.

`ARQUITECTO`, `DEVOPS` y `COMERCIAL` no están activados permanentemente; pueden intervenir cuando exista necesidad y autorización explícita.

## Cola operativa

- **Gobernanza G-01:** [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [PR #5](https://github.com/mundoinformaticacanaria/whereis/pull/5) proporcionan trazabilidad de la formalización documental; una vez integrados/cerrados no suponen nueva autorización operativa.
- [Issues #1/#2 — D-01/D-02](https://github.com/mundoinformaticacanaria/whereis/issues/1): decisiones funcionales con [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión por TECH LEAD.
- **Primera issue de programación:** todavía no autorizada.

## Configuración y decisiones PENDIENTES

- Identidades de ejecutores, disponibilidad, capacidad real, separación de QA y prefijos de ramas.
- Labels operativas en GitHub, permisos y reglas de merge, protección de `main`, CI/gates concretos.
- Zona horaria única de heartbeat, rama `ops/logs` y ficheros de log de los roles activos.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance

TECH LEAD: priorizar revisión de la [PR funcional #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) y ordenar los pendientes de bootstrap para decisión del PROPIETARIO. Sin emitir la primera asignación PROGRAMADOR mientras falten las autorizaciones y gates mínimos.
