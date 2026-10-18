# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 18/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), enmendada materialmente el 18/10/2026 en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), activa además `ARQUITECTO` (Codex) y las identidades lógicas de PROGRAMADOR `PROGRAMADOR-LINUX` y `CODEX`; `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa. Roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. `PROGRAMADOR-LINUX` usa un modelo configurable separado de su identidad. A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es solo **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16), sin autorización de desarrollo real ni timer. Cuentas GitHub, acceso real de PROGRAMADOR-LINUX/CODEX, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. Las decisiones D-01 y D-02 constan en [issues #1](https://github.com/mundoinformaticacanaria/whereis/issues/1) y [#2](https://github.com/mundoinformaticacanaria/whereis/issues/2), con documentación propuesta en [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión/integración; no equivalen a aprobación del baseline global.
- **Baseline arquitectónico:** `PENDIENTE`.
- **Estado MVP/beta:** `PENDIENTE`; implementación no autorizada.

## Organización activa confirmada

- `PROPIETARIO`: decide autorizaciones y materiales reservados.
- `FUNCIONAL`: análisis funcional independiente y criterios de aceptación.
- `TECH LEAD`: coordinación y cola de issues sin labels; asigna PROGRAMADOR-LINUX/CODEX, revisa calidad y hace merge.
- `ARQUITECTO`: Codex, propuestas y evaluación arquitectónica sin sustituir las aprobaciones del Propietario.
- `PROGRAMADOR`: PROGRAMADOR-LINUX o CODEX, exactamente uno en el cuerpo de la issue; desarrollo solo autorizado.
- `QA`: Codex (para PR PROGRAMADOR-LINUX) o ChatGPT conversacional independiente (en particular para PR Codex); dictamen antes de merge.

`DEVOPS` y `COMERCIAL` no están activados permanentemente. El Arquitecto sí está activado como Codex por G-02.

## Cola operativa

- **Gobernanza G-02:** [issue #26](https://github.com/mundoinformaticacanaria/whereis/issues/26) y [PR #27](https://github.com/mundoinformaticacanaria/whereis/pull/27) documentan la decisión original; [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28) mantiene la enmienda `PROGRAMADOR-LINUX` y los bloqueos operativos vivos. No autoriza desarrollo.
- **Gobernanza G-01:** [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [PR #5](https://github.com/mundoinformaticacanaria/whereis/pull/5) proporcionan trazabilidad de la formalización documental; una vez integrados/cerrados no suponen nueva autorización operativa.
- [Issues #1/#2 — D-01/D-02](https://github.com/mundoinformaticacanaria/whereis/issues/1): decisiones funcionales con [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión por TECH LEAD.
- **Primera issue de programación:** todavía no autorizada.

## Configuración y decisiones PENDIENTES

- Autenticación y usuario GitHub de PROGRAMADOR-LINUX desde Linux; ruta/comando/instalación reales; acceso y disponibilidad de Codex; separación de QA en la práctica. Convenciones de ramas decididas en G-02: `programador-linux/<issue>-<slug>`, `codex/<issue>-<slug>` y `arquitectura/<issue>-<slug>`.
- Labels operativas en GitHub, permisos y reglas de merge. A 18/10/2026 `main` figura sin protección/ruleset y no existe `.github/workflows`; CI/gates concretos siguen PENDIENTES.
- Zona horaria única de heartbeat, rama `ops/logs` y ficheros de log de los roles activos.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance

TECH LEAD: revisar las PR funcionales abiertas (#3, #7, #9, #11, #13, #15, #18, #25), resolver contradicciones y priorizar [seguridad/menores #24](https://github.com/mundoinformaticacanaria/whereis/issues/24). Verificar labels/identidades/accesos antes del primer handoff a PROGRAMADOR-LINUX o CODEX. Sin emitir la primera asignación PROGRAMADOR mientras falten baselines, autorizaciones y gates mínimos.
