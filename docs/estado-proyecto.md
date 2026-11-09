# Estado del proyecto

- **Proyecto:** Whereis
- **Repositorio:** https://github.com/mundoinformaticacanaria/whereis
- **Fecha de estado:** 09/11/2026 (fotografía verificable de GitHub; los estados operativos cambian en issues/PR)

## Estado resumido

Proyecto Android en fase de definición y bootstrap. **G-01 V3** confirmó cinco roles iniciales. La [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), enmendada materialmente el 18/10/2026 en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28), activa además `ARQUITECTO` (chat ChatGPT dedicado e independiente, enmienda material aprobada por PROPIETARIO en #37 el 25/10/2026 y formalizada en PR #43) y las identidades lógicas de PROGRAMADOR `PROGRAMADOR-LINUX` y `CODEX`; `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa. Roles vigentes: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`. Véanse [issue #4](https://github.com/mundoinformaticacanaria/whereis/issues/4) y [decisión G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md).

La gobernanza por sí sola **no autoriza desarrollo del producto**, contratación ni infraestructura. **Excepción MATERIAL acotada posterior:** el PROPIETARIO confirmó el 09/11/2026 la opción A en [#90](https://github.com/mundoinformaticacanaria/whereis/issues/90#issuecomment-6738056323), para una única prueba supervisada de lógica Kotlin/JVM pura de ordenación alias/ID con datos sintéticos, solo después de verificar aislamiento/credenciales #93/#28 y QA independiente. **NO se ha liberado ni ejecutado el programador**; PR DRAFT sin merge hasta gates normales. `PROGRAMADOR-LINUX` usa un modelo configurable separado de su identidad. A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es solo **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16), sin autorización de desarrollo real ni timer. Cuentas GitHub, acceso real de PROGRAMADOR-LINUX/CODEX, capacidades, QA efectivo y permisos continúan `PENDIENTE` de verificación.

## Baselines

- **Gobernanza:** G-01 V3 y G-02 `CONFIRMADAS` en su alcance. Política de roles y orquestación en [playbook](orquestacion/README.md); configuración técnica de acceso/labels/CI aún `PENDIENTE`.
- **Baseline funcional completo / alcance MVP:** `PENDIENTE`. D-01/D-02 están integradas documentalmente por [PR #3](https://github.com/mundoinformaticacanaria/whereis/pull/3) en `main@97a29e450fee24887f785e73f5222a35b2605369` (23/10/2026); D-03/D-04 también constan en `main`. D-05/D-06/D-07/D-08 están integradas **solo documentalmente** mediante [PR #11](https://github.com/mundoinformaticacanaria/whereis/pull/11), [#13](https://github.com/mundoinformaticacanaria/whereis/pull/13), [#15](https://github.com/mundoinformaticacanaria/whereis/pull/15) (23/10) y [#18](https://github.com/mundoinformaticacanaria/whereis/pull/18) (24/10, `main@9dfdb37b98bd998f990a17b1e9daba7c13bbd435`). D-09–D-13 y SEG se integraron **solo documentalmente** mediante [PR #49](https://github.com/mundoinformaticacanaria/whereis/pull/49) (26/10/2026, `main@fa373c13e56cbf5cf5cf9fb2a31c9e495d9d28c0`), sustituta de PR #25 cerrada sin merge. QA independiente emitió **APTO documental** sobre HEAD `f5850449c5a8b58cdc62d3b9a1b57f08d7a44d3e`, tras corregir en D-03 la contradicción anti-enumeración SEG-02. SEG-01–04, revisión jurídica y viabilidad técnica siguen PENDIENTES; no se autoriza implementación. Ninguna integración aislada aprueba el baseline global.
- **Baseline arquitectónico:** `PENDIENTE`.
- **Estado MVP/beta:** `PENDIENTE`; no hay autorización general de implementación. El único piloto condicionado #90 no aprueba baselines ni producto Android.

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
- **Primera issue de programación:** [#90](https://github.com/mundoinformaticacanaria/whereis/issues/90), **opción A confirmada por PROPIETARIO para ensayo puntual supervisado** de lógica Kotlin/JVM pura sin Android ni datos reales. La issue sigue `TECH LEAD`, NO `PROGRAMADOR`, condicionada a evidencia de #93, #28, QA independiente y Kotlin existente; sin timer ni merge.
- **Evidencias de evaluación sintética:** [PR #51](https://github.com/mundoinformaticacanaria/whereis/pull/51) integrada **solo documentalmente** tras QA independiente APTO en [#53](https://github.com/mundoinformaticacanaria/whereis/issues/53) el 27/10/2026 (`main@3212773e2dba2246358cf9e7b8d4d2294ba27707`); 66 archivos históricos, sin autorización de modelo, desarrollo ni timer.
- **Aislamiento del runner Linux:** [PR #36](https://github.com/mundoinformaticacanaria/whereis/pull/36) cerrada sin merge como `SUPERSEDED`, sustituida por [PR #47](https://github.com/mundoinformaticacanaria/whereis/pull/47), integrada solo documentalmente. [PR DRAFT #94](https://github.com/mundoinformaticacanaria/whereis/pull/94), HEAD `1011344895858302a5db1d7db2feb5e26a4e0784`, recoge integración parcial y ensayos reportados por operador; **QA independiente #95 BLOQUEADO para APTO operativo** por falta de reproducción SSH independiente, credenciales propias, egress Git/GH/OpenCode y otros gates. [#93](https://github.com/mundoinformaticacanaria/whereis/issues/93) corresponde al PROPIETARIO para comprobación SSH de solo lectura; **PROGRAMADOR-LINUX NO OPERATIVO**.
- **ARQUITECTO y heartbeat:** decisiones materiales del PROPIETARIO **CONFIRMADAS** en [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37) y [#38](https://github.com/mundoinformaticacanaria/whereis/issues/38) el 25/10/2026. **PR #43 y PR #44 integradas documentalmente** en `main` (la segunda en `74f4bf13bd92d9f34f0028b5c8eaf70ff57372e8`). Rama `ops/logs` y cuatro ficheros de rol existentes/verificados; heartbeat **NO acreditado como operativo integralmente**: faltan concurrencia entre agentes independientes, retención concurrente, FIN tardío real y fallos API/permisos. #38 permanece abierta.

## Configuración y decisiones PENDIENTES

- Autenticación y usuario GitHub de PROGRAMADOR-LINUX desde Linux; ruta/comando/instalación reales; acceso y disponibilidad de Codex; separación de QA en la práctica. Convenciones de ramas decididas en G-02: `programador-linux/<issue>-<slug>`, `codex/<issue>-<slug>` y `arquitectura/<issue>-<slug>`.
- **Protección de `main` / CI — GET verificado 09/11/2026:** `main@3212773e2dba2246358cf9e7b8d4d2294ba27707` tiene `protected=true`; [ruleset #26574343](https://github.com/mundoinformaticacanaria/whereis/rules/26574343) activo para `refs/heads/main`, sin bypass, con exigencia de PR, protección contra force-push y borrado, y resolución de conversaciones; **0 aprobaciones nativas y sin required checks**. Esto acredita **configuración, NO rechazo real por enforcement**. [PR #46](https://github.com/mundoinformaticacanaria/whereis/pull/46) scanner documental QA #83 APTO solo documental para HEAD `7814d85...`; [PR #71](https://github.com/mundoinformaticacanaria/whereis/pull/71) workflow QA #82 BLOQUEADO operativo para HEAD `f759850...`, sin run del HEAD. [PR #91](https://github.com/mundoinformaticacanaria/whereis/pull/91) protocolo inocuo, QA #92 APTO DOCUMENTAL para HEAD `15c7c638...`, sin merge ni tests de rechazo real. `main` aún no tiene `.github/workflows` integrado. Los runs GitHub Actions históricos corresponden a otros HEAD y no son CI efectiva de los actuales. **#42 sigue abierta**.
- **Trazabilidad de roles:** 17 issues y 16 PR abiertas al inicio de este corte (09/11/2026); las issues y PR están etiquetadas con rol visible. La etiqueta por sí sola no acredita permiso real ni asigna PROGRAMADOR.

- **Heartbeat #38:** referencia temporal UTC y hora `Atlantic/Canary` adicional con offset estacional, por issue e ID de intervención; política integrada en `main` por PR #44. **Verificado el 25/10/2026:** rama `ops/logs` y logs `tech-lead.log`, `qa.log`, `funcional.log`, `arquitecto.log` existen. Pruebas sintéticas de DST/umbral, retención efectiva de 100 entradas con **un escritor** y rechazo HTTP 409 con conciliación desde **un orquestador** documentadas; concurrencia entre agentes independientes, FIN tardío, fallos API/permisos y QA operativa integral **PENDIENTES**. Hay FIN históricos con zona canaria malformada; conservar evidencia, no fabricar correcciones.
- Objetivo y alcance definitivo del MVP, baselines funcional/arquitectónico, política de privacidad y seguridad, servicios/infraestructura, costes y proveedores.
- Activaciones puntuales de especialistas, si se justifican.

No interpretar ninguno de estos puntos como decidido por G-01.

## POST-MVP

`PENDIENTE` de clasificación por FUNCIONAL y aprobación del PROPIETARIO.

## Próximo avance — fotografía 09/11/2026

1. **#93 PROPIETARIO**, en paralelo con **#28 TECH LEAD**: evidencias SSH sanitizadas de aislamiento/credenciales exclusivos, egress y QA independiente de PR #94; no modificar CRM/servidor/timers fuera del alcance ya autorizado. La opción A de [#90](https://github.com/mundoinformaticacanaria/whereis/issues/90) está **CONFIRMADA** pero la ejecución supervisada sigue **BLOQUEADA** hasta esos requisitos y herramientas Kotlin/JVM disponibles sin instalación.
2. **#42 TECH LEAD**: aplicar protocolo PR #91 conforme a QA #92, mejorar evidencia no destructiva de ruleset/CI, integrar scanner PR #46 y workflow PR #71 **solo tras gates**; no confundir QA documental, runs antiguos o status vacío con CI verde ni hacer merge sin controles.
3. **#38 TECH LEAD**: heartbeat documentado, logs presentes; faltan pruebas reales de concurrencia, API/permisos y FIN tardío. PR #58 y esta PR #48 requieren dictámenes QA sobre **sus HEAD vigentes**, además de gates aplicables.
4. **#41/#24 TECH LEAD**: R-60a/b/c confirmadas funcionalmente por PROPIETARIO, formalizadas en [PR #87](https://github.com/mundoinformaticacanaria/whereis/pull/87), QA #88 APTO DOCUMENTAL; estudio ADR [PR #66](https://github.com/mundoinformaticacanaria/whereis/pull/66), QA #89 APTO DOCUMENTAL. [PR #77](https://github.com/mundoinformaticacanaria/whereis/pull/77) cerrada sin merge como superada. Siguen pendientes legitimación, conservación y derechos de menores, backups cloud/D2D/OEM, seguridad y pruebas Android/red; ninguna PR adopta proveedor ni resuelve cumplimiento jurídico.
5. **D-06/#12** PR #62, **D-13/#23** PR #85, **D-12/#22** PR #35 y gobernanza #28 PR #64 siguen pendientes de gates/merges según SHA y QA documentales vigentes. No introducir producto Android, proveedor, gasto, infraestructura, datos reales ni timer por estas evidencias.

**Este estado es una fotografía documental, no la autoridad sobre nuevos comentarios, SHAs o decisiones posteriores. Consultar siempre GitHub vigente antes de actuar.**
