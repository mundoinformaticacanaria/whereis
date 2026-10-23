# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 23/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), enmendada materialmente el 18/10/2026 en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), activa además `ARQUITECTO` (Codex) y las identidades lógicas de PROGRAMADOR `PROGRAMADOR-LINUX` y `CODEX`; `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa. Roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. `PROGRAMADOR-LINUX` usa un modelo configurable separado de su identidad. A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es solo **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16), sin autorización de desarrollo real ni timer. Cuentas GitHub, acceso real de PROGRAMADOR-LINUX/CODEX, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. D-01/D-02 están integradas documentalmente por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) en `main@97a29e450fee24887f785e73f5222a35b2605369` (23/10/2026); D-03/D-04 también constan en `main`. D-05/D-06/D-07/D-08 siguen en [PR #11](https://github.com/mundoinformaticacanaria/whereis/pull/11), [#13](https://github.com/mundoinformaticacanaria/whereis/pull/13), [#15](https://github.com/mundoinformaticacanaria/whereis/pull/15) y [#18](https://github.com/mundoinformaticacanaria/whereis/pull/18), devueltas a FUNCIONAL para conciliación; D-09–D-13 están en [PR #25](https://github.com/mundoinformaticacanaria/whereis/pull/25) en borrador y devuelta a FUNCIONAL. Ninguna integración aislada aprueba el baseline global.
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
- [Issues #1/#2 — D-01/D-02](https://github.com/mundoinformaticacanaria/whereis/issues/1): documentación integrada por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) el 23/10/2026; sin aprobación de baseline global.
- **Primera issue de programación:** todavía no autorizada.

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

**FUNCIONAL:** corregir los HEAD de PR #11/#13/#15/#18/#25 conforme a revisiones de TECH LEAD y devolverlos para revalidación. **PROPIETARIO:** decidir el conflicto D-09/SEG-02 documentado en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24), actualmente con label `PROPIETARIO`. **TECH LEAD:** seguir #28, verificar configuración real de GitHub y coordinar viabilidad sin asignar `PROGRAMADOR` ni activar el timer Linux mientras falten baselines, seguridad y gates.
