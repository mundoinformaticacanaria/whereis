# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 25/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), enmendada materialmente el 18/10/2026 en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), activa además `ARQUITECTO` (chat ChatGPT dedicado e independiente, enmienda material aprobada por PROPIETARIO en #37 el 25/10/2026 y formalizada en PR #43) y las identidades lógicas de PROGRAMADOR `PROGRAMADOR-LINUX` y `CODEX`; `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa. Roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. `PROGRAMADOR-LINUX` usa un modelo configurable separado de su identidad. A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es solo **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16), sin autorización de desarrollo real ni timer. Cuentas GitHub, acceso real de PROGRAMADOR-LINUX/CODEX, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. D-01/D-02 están integradas documentalmente por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) en `main@97a29e450fee24887f785e73f5222a35b2605369` (23/10/2026); D-03/D-04 también constan en `main`. D-05/D-06/D-07/D-08 están integradas **solo documentalmente** mediante [PR #11](https://github.com/mundoinformaticacanaria/whereis/pull/11), [#13](https://github.com/mundoinformaticacanaria/whereis/pull/13), [#15](https://github.com/mundoinformaticacanaria/whereis/pull/15) (23/10) y [#18](https://github.com/mundoinformaticacanaria/whereis/pull/18) (24/10, `main@9dfdb37b98bd998f990a17b1e9daba7c13bbd435`). D-09–D-13 siguen en [PR #25](https://github.com/mundoinformaticacanaria/whereis/pull/25), borrador devuelto a FUNCIONAL para incorporar la opción B de seguridad aprobada en #24. Ninguna integración aislada aprueba el baseline global.
- **Baseline arquitectónico:** `PENDIENTE`.
- **Estado MVP/beta:** `PENDIENTE`; implementación no autorizada.

## Organización activa confirmada

- `PROPIETARIO`: decide autorizaciones y materiales reservados.
- `FUNCIONAL`: análisis funcional independiente y criterios de aceptación.
- `TECH LEAD`: coordinación y cola de issues sin labels; asigna PROGRAMADOR-LINUX/CODEX, revisa calidad y hace merge.
- `ARQUITECTO`: chat ChatGPT dedicado e independiente de TECH LEAD y de QA de su propio trabajo (decisión #37); propuestas y evaluación arquitectónica, sin aprobar baselines ni sustituir al PROPIETARIO.
- `PROGRAMADOR`: PROGRAMADOR-LINUX o CODEX, exactamente uno en el cuerpo de la issue; desarrollo solo autorizado.
- `QA`: Codex (para PR PROGRAMADOR-LINUX) o ChatGPT conversacional independiente (en particular para PR Codex); dictamen antes de merge.

`DEVOPS` y `COMERCIAL` no están activados permanentemente. La asignación anterior de Codex como ARQUITECTO (G-02 del 18/10) queda `SUPERSEDED` por la decisión #37; Codex conserva PROGRAMADOR y QA independiente cuando corresponda. No se atribuyen retroactivamente dictámenes al nuevo Arquitecto.

## Cola operativa

- **Gobernanza G-02:** [issue #26](https://github.com/mundoinformaticacanaria/whereis/issues/26) y [PR #27](https://github.com/mundoinformaticacanaria/whereis/pull/27) documentan la decisión original; [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28) mantiene la enmienda `PROGRAMADOR-LINUX` y los bloqueos operativos vivos. No autoriza desarrollo.
- **Gobernanza G-01:** [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [PR #5](https://github.com/mundoinformaticacanaria/whereis/pull/5) proporcionan trazabilidad de la formalización documental; una vez integrados/cerrados no suponen nueva autorización operativa.
- [Issues #1/#2 — D-01/D-02](https://github.com/mundoinformaticacanaria/whereis/issues/1): documentación integrada por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) el 23/10/2026; sin aprobación de baseline global.
- **Primera issue de programación:** todavía no autorizada.
- **Aislamiento del runner Linux:** criterio multiproyecto confirmado por PROPIETARIO en #28; formalización en [PR #36](https://github.com/mundoinformaticacanaria/whereis/pull/36), aún en borrador. No equivale a verificación del servidor.
- **ARQUITECTO y heartbeat:** decisiones materiales del PROPIETARIO **CONFIRMADAS** en [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37) y [#38](https://github.com/mundoinformaticacanaria/whereis/issues/38) el 25/10/2026. La enmienda #37 se formaliza en PR #43; la política #38 continúa en PR #44 pendiente de integración; rama `ops/logs` y heartbeat operativo aún no verificados.

## Configuración y decisiones PENDIENTES

- Autenticación y usuario GitHub de PROGRAMADOR-LINUX desde Linux; ruta/comando/instalación reales; acceso y disponibilidad de Codex; separación de QA en la práctica. Convenciones de ramas decididas en G-02: `programador-linux/<issue>-<slug>`, `codex/<issue>-<slug>` y `arquitectura/<issue>-<slug>`.
- Labels operativas en GitHub, permisos y reglas de merge. **Verificado el 23/10/2026:** `main` no está protegida; la consulta de rulesets devuelve lista vacía; no existe `.github/workflows` en `main` y el commit de `main` no registra checks. La lectura de branch protection específica devuelve 403 por permisos del conector; no equivale a prueba de una configuración oculta. El inventario global de labels no es accesible mediante el conector y sigue PENDIENTE.
- Zona horaria única de heartbeat, rama `ops/logs` y ficheros de log de los roles activos. **Verificado el 23/10/2026:** la rama `ops/logs` no existe y `docs/logs` solo contiene `README.md`; no fabricar heartbeat ni darlo por operativo.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance

**FUNCIONAL:** corregir el HEAD de PR #25 para reflejar la opción B de D-09/SEG-02 ya aprobada por PROPIETARIO en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24). **TECH LEAD:** integrar documentalmente las decisiones #37/#38 mediante PR #43/#44 tras QA, revisión y conciliación de sus cambios compartidos; coordinar la evaluación técnica de #41. **PROPIETARIO:** conserva las decisiones materiales de privacidad/seguridad pendientes de #24. **TECH LEAD:** revisar PR #25 cuando haya nuevo HEAD, mantener #28 y los gates operativos, coordinar revisión formal de propuestas arquitectónicas #34/#35 y PR #36 cuando deje de estar en borrador; sin asignar `PROGRAMADOR` ni activar el timer Linux mientras falten baselines, seguridad y gates.
