# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 26/10/2026

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), enmendada materialmente el 18/10/2026 en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), activa además `ARQUITECTO` (chat ChatGPT dedicado e independiente, enmienda material aprobada por PROPIETARIO en #37 el 25/10/2026 y formalizada en PR #43) y las identidades lógicas de PROGRAMADOR `PROGRAMADOR-LINUX` y `CODEX`; `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa. Roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La aprobación de gobernanza **no autoriza desarrollo del producto**, contratación ni infraestructura. `PROGRAMADOR-LINUX` usa un modelo configurable separado de su identidad. A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es solo **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16), sin autorización de desarrollo real ni timer. Cuentas GitHub, acceso real de PROGRAMADOR-LINUX/CODEX, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. D-01/D-02 están integradas documentalmente por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) en `main@97a29e450fee24887f785e73f5222a35b2605369` (23/10/2026); D-03/D-04 también constan en `main`. D-05/D-06/D-07/D-08 están integradas **solo documentalmente** mediante [PR #11](https://github.com/mundoinformaticacanaria/whereis/pull/11), [#13](https://github.com/mundoinformaticacanaria/whereis/pull/13), [#15](https://github.com/mundoinformaticacanaria/whereis/pull/15) (23/10) y [#18](https://github.com/mundoinformaticacanaria/whereis/pull/18) (24/10, `main@9dfdb37b98bd998f990a17b1e9daba7c13bbd435`). D-09–D-13 y SEG se integraron **solo documentalmente** mediante [PR #49](https://github.com/mundoinformaticacanaria/whereis/pull/49) (26/10/2026, `main@fa373c13e56cbf5cf5cf9fb2a31c9e495d9d28c0`), sustituta de PR #25 cerrada sin merge. QA independiente emitió **APTO documental** sobre HEAD `f5850449c5a8b58cdc62d3b9a1b57f08d7a44d3e`, tras corregir en D-03 la contradicción anti-enumeración SEG-02. SEG-01–04, revisión jurídica y viabilidad técnica siguen PENDIENTES; no se autoriza implementación. Ninguna integración aislada aprueba el baseline global.
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
- **Aislamiento del runner Linux:** criterio multiproyecto confirmado por PROPIETARIO en #28; [PR #36](https://github.com/mundoinformaticacanaria/whereis/pull/36) cerrada sin merge como `SUPERSEDED`, sustituida por [PR #47](https://github.com/mundoinformaticacanaria/whereis/pull/47), **integrada documentalmente** tras QA independiente APTO el 26/10/2026 (`main@8ca3ec778464ebea39d573672b0a7bcf07c81aa5`). El aislamiento real del servidor continúa PENDIENTE bajo #28.
- **ARQUITECTO y heartbeat:** decisiones materiales del PROPIETARIO **CONFIRMADAS** en [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37) y [#38](https://github.com/mundoinformaticacanaria/whereis/issues/38) el 25/10/2026. **PR #43 y PR #44 integradas documentalmente** en `main` (la segunda en `74f4bf13bd92d9f34f0028b5c8eaf70ff57372e8`). Rama `ops/logs` y cuatro ficheros de rol existentes/verificados; heartbeat **NO acreditado como operativo integralmente**: faltan concurrencia real, retención >100, FIN tardío real y fallos API/permisos. #38 permanece abierta.

## Configuración y decisiones PENDIENTES

- Autenticación y usuario GitHub de PROGRAMADOR-LINUX desde Linux; ruta/comando/instalación reales; acceso y disponibilidad de Codex; separación de QA en la práctica. Convenciones de ramas decididas en G-02: `programador-linux/<issue>-<slug>`, `codex/<issue>-<slug>` y `arquitectura/<issue>-<slug>`.
- Labels operativas en GitHub, permisos y reglas de merge. **Verificado el 23/10/2026:** `main` no está protegida; la consulta de rulesets devuelve lista vacía; no existe `.github/workflows` en `main` y el commit de `main` no registra checks. La lectura de branch protection específica devuelve 403 por permisos del conector; no equivale a prueba de una configuración oculta. El inventario global de labels no es accesible mediante el conector y sigue PENDIENTE.
- **Heartbeat #38:** referencia temporal UTC y hora `Atlantic/Canary` adicional con offset estacional, por issue e ID de intervención; política integrada en `main` por PR #44. **Verificado el 25/10/2026:** rama `ops/logs` y logs `tech-lead.log`, `qa.log`, `funcional.log`, `arquitecto.log` existen. Pruebas sintéticas de DST/umbral y rechazo de SHA antiguo documentadas; concurrencia real, recorte efectivo >100, FIN tardío y fallos API/permisos **PENDIENTES**. Hay FIN históricos con zona canaria malformada; conservar evidencia, no fabricar correcciones.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance

**TECH LEAD:** PR #49 (D-09–D-13/SEG) y PR #47 (aislamiento multiproyecto documental) integradas tras QA; la corrección de [PR #48](https://github.com/mundoinformaticacanaria/whereis/pull/48) requiere **nuevo QA independiente sobre su HEAD actualizado** y revisión final antes de merge. Completar pruebas reales de heartbeat #38 sin modificar la automatización horaria; mantener gates #28 y #42 (PR #46 bloqueada por evidencia de checkout real y protección efectiva de `main` sin acreditar). **QA:** revalidar PR #48; PR #51 sigue DRAFT sin APTO acreditado. **TECH LEAD/ARQUITECTO:** continuar el estudio L-02 de PR #50/#45 y coordinar #34/#35, conforme a L-02b/c/d aprobadas **solo para estudio** en #41; adoptar canal, cuenta, SDK, emisor o proveedor requiere nueva aprobación del PROPIETARIO. **PROPIETARIO:** resolver revisión jurídica y decisiones de privacidad pendientes de #24/#41, especialmente SEG-03/04. Sin asignar `PROGRAMADOR`, desarrollar producto ni activar timers Linux mientras falten baselines, seguridad y gates.
