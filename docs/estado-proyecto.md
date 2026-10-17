# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 15/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md) del 17/10/2026 activa además `ARQUITECTO` (Codex) y las identidades lógicas de PROGRAMADOR `QWEN-LINUX` y `CODEX`; roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. Identidades lógicas y reparto definidos; cuentas GitHub, acceso real de Qwen/Codex, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. Las decisiones D-01 y D-02 constan en [issues #1](https://github.com/mundoinformaticacanaria/whereis/issues/1) y [#2](https://github.com/mundoinformaticacanaria/whereis/issues/2), con documentación propuesta en [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión/integración; no equivalen a aprobación del baseline global.
- **Baseline arquitectónico:** `PENDIENTE`.
- **Estado MVP/beta:** `PENDIENTE`; implementación no autorizada.

## Organización activa confirmada

- `PROPIETARIO`: decide autorizaciones y materiales reservados.
- `FUNCIONAL`: análisis funcional independiente y criterios de aceptación.
- `TECH LEAD`: coordinación y cola de issues sin labels; asigna Qwen/Codex, revisa calidad y hace merge.
- `ARQUITECTO`: Codex, propuestas y evaluación arquitectónica sin sustituir las aprobaciones del Propietario.
- `PROGRAMADOR`: QWEN-LINUX o CODEX, exactamente uno en el cuerpo de la issue; desarrollo solo autorizado.
- `QA`: Codex (para PR Qwen) o ChatGPT conversacional independiente (en particular para PR Codex); dictamen antes de merge.

`DEVOPS` y `COMERCIAL` no están activados permanentemente. El Arquitecto sí está activado como Codex por G-02.

## Cola operativa

- **Gobernanza G-01:** [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [PR #5](https://github.com/mundoinformaticacanaria/whereis/pull/5) proporcionan trazabilidad de la formalización documental; una vez integrados/cerrados no suponen nueva autorización operativa.
- [Issues #1/#2 — D-01/D-02](https://github.com/mundoinformaticacanaria/whereis/issues/1): decisiones funcionales con [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) pendiente de revisión por TECH LEAD.
- **Primera issue de programación:** todavía no autorizada.

## Configuración y decisiones PENDIENTES

- Autenticación y usuario GitHub de Qwen desde Linux; ruta/comando/instalación reales; acceso y disponibilidad de Codex; separación de QA en la práctica. Convenciones de ramas decididas en G-02: `qwen/<issue>-<slug>`, `codex/<issue>-<slug>` y `arquitectura/<issue>-<slug>`.
- Labels operativas en GitHub, permisos y reglas de merge, protección de `main`, CI/gates concretos.
- Zona horaria única de heartbeat, rama `ops/logs` y ficheros de log de los roles activos.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance

TECH LEAD: revisar las PR funcionales abiertas (#3, #7, #9, #11, #13, #15, #18, #25), resolver contradicciones y priorizar [seguridad/menores #24](https://github.com/mundoinformaticacanaria/whereis/issues/24). Verificar labels/identidades/accesos antes del primer handoff a Qwen o Codex. Sin emitir la primera asignación PROGRAMADOR mientras falten baselines, autorizaciones y gates mínimos.
