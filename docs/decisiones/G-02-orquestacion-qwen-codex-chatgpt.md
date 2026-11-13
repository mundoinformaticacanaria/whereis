# G-02 — Orquestación de PROGRAMADOR-LINUX, Codex y ChatGPT

- **Fecha original:** 17/10/2026.
- **Enmiendas materiales:** 18/10/2026, identidad Linux en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28); 25/10/2026, ejecutor formal ARQUITECTO aprobado en [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37#issuecomment-6395244289).
- **Estado:** `CONFIRMADO` para distribución de funciones, identidades lógicas y política de labels; integraciones técnicas, permisos, baselines y gates concretos siguen `PENDIENTE`.
- **Tipo:** `MATERIAL` — gobernanza y asignación de ejecutores.
- **Relación con G-01 V3:** G-02 mantiene `ARQUITECTO` activo (chat ChatGPT independiente desde #37), conserva PROPIETARIO, FUNCIONAL, TECH LEAD, PROGRAMADOR y QA, autoridad humana y QA independiente. G-01 conserva su historia; para composición vigente prevalece G-02.

## Trazabilidad histórica de la enmienda

La G-02 original, aprobada en [issue #26](https://github.com/mundoinformaticacanaria/whereis/issues/26) e integrada por [PR #27](https://github.com/mundoinformaticacanaria/whereis/pull/27), denominó al ejecutor Linux `QWEN-LINUX` y usó Qwen como modelo previsto. Esa decisión no se borra ni se reescribe retroactivamente.

Desde el 18/10/2026, **`QWEN-LINUX` queda SUPERSEDED como identidad operativa vigente**. La identidad lógica estable pasa a ser **`PROGRAMADOR-LINUX`**. Las referencias históricas, evidencias y ramas antiguas pueden conservar el nombre anterior.

## Roles y ejecutores

| Label de siguiente acción | Ejecución prevista | Límite |
|---|---|---|
| `PROPIETARIO` | Humano propietario | Aprueba decisiones materiales reservadas |
| `FUNCIONAL` | Chat conversacional ChatGPT | Requisitos; no aprueba por sí mismo ni programa |
| `TECH LEAD` **o ninguna label de rol** | ChatGPT conversacional del Tech Lead activo | Triage, reparto, revisión, merge |
| `ARQUITECTO` | Chat ChatGPT dedicado, independiente de TECH LEAD y QA | Diseño/viabilidad técnica y handoff documentado; sin merge ni aprobación humana |
| `PROGRAMADOR` | Ejecutores `PROGRAMADOR-LINUX` o `CODEX` | Solo issue asignada, rama/PR; sin merge |
| `QA` | Codex independiente o ChatGPT conversacional independiente | Revisión independiente del autor; sin merge |

`DEVOPS` y `COMERCIAL` no se activan permanentemente sin nueva decisión.

### Enmienda #37 — segregación del ARQUITECTO

El PROPIETARIO confirmó el 25/10/2026 la opción B en [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37#issuecomment-6395244289): el titular formal de `ARQUITECTO` pasa a ser un **chat de ChatGPT dedicado e independiente**, sustituyendo a Codex en esa función, **sin crear un rol nuevo ni doble titularidad**. La decisión se formaliza en esta enmienda documental y solo es canónica tras integrar su PR en `main`.

El chat ARQUITECTO debe leer `main`, `AGENTS.md`, `docs/contexto-arquitecto.md`, la issue con todos sus comentarios y el playbook; atender únicamente issues con label `ARQUITECTO`; documentar alternativas, riesgos, evidencias, decisiones PENDIENTES y handoff en GitHub. Entrega a TECH LEAD para coordinación/revisión o eleva a PROPIETARIO lo reservado a autoridad humana. **No** actúa simultáneamente como TECH LEAD, no es QA de su propio trabajo, no hace merge ni aprueba baselines por sí mismo. Codex conserva `CODEX` PROGRAMADOR y QA independiente cuando se cumplan los gates y segregación real. Ninguna propuesta o revisión anterior se atribuye retroactivamente al nuevo titular.

Las propuestas DRAFT [PR #34](https://github.com/mundoinformaticacanaria/whereis/pull/34) y [PR #35](https://github.com/mundoinformaticacanaria/whereis/pull/35) requieren evaluación arquitectónica formal acreditada por el nuevo ejecutor y revisión posterior de TECH LEAD sobre HEAD exacto; no son baselines. Esta enmienda no autoriza PROGRAMADOR, infraestructura, gasto, proveedor, servidor, CRM ni timers.

## Labels y asignación

- **Una y solo una label de rol** indica la siguiente acción en cada issue ejecutable.
- **Cero labels de rol significa `TECH LEAD`**. La label `TECH LEAD` explícita es válida, aunque redundante.
- **Las labels son nombres de roles**, no modelos, proveedores, identidades ni estados. No crear label `PROGRAMADOR-LINUX`, `QWEN-LINUX`, `QWEN` o `CODEX`.
- Una issue `PROGRAMADOR` identifica exactamente un ejecutor en el cuerpo: `Ejecutor autorizado: PROGRAMADOR-LINUX` o `Ejecutor autorizado: CODEX`.
- Nunca asignar una issue a dos programadores a la vez. Máximo una tarea activa por ejecutor salvo decisión posterior del Tech Lead.

## Separación entre identidad y modelo

- `PROGRAMADOR-LINUX` es el **ejecutor lógico**.
- El modelo/proveedor Linux se selecciona mediante **configuración operativa separada**.
- Cambiar de Qwen a Nemotron u otro modelo futuro **no cambia la identidad**, la función `PROGRAMADOR`, la label, el contrato de la issue, los gates ni la autoridad.
- No se crea una identidad lógica por proveedor o modelo.
- La selección del modelo puede variar por disponibilidad, coste o calidad, siempre sujeta a los controles del proyecto.
- Las restricciones y gates pertenecen al ejecutor/proyecto, no al nombre del modelo.
- Si un cambio de modelo altera capacidades, privacidad, coste, permisos o riesgo material, TECH LEAD lo eleva antes de usarlo; la neutralidad nominal no elude aprobaciones.

## Instancia Linux en servidor multiproyecto (aclaración del PROPIETARIO, 23/10/2026)

**CONFIRMADO — criterio MATERIAL de aislamiento** en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28#issuecomment-6372583456): el servidor Linux es **compartido** con otros proyectos; el ejecutor `PROGRAMADOR-LINUX` de WHEREIS es **una instancia por proyecto**, no parte de un runner global que despache issues de varios repositorios. La identidad estable y el modelo configurable definidos arriba pertenecen solo a la instancia WHEREIS.

- El runner de `mundoinformaticacanaria/crm-remisiones-veterinarias` es **externo a WHEREIS**. No modificar ni detener sus componentes; solo inspección técnica indispensable, en lectura, para detectar colisiones. Las decisiones funcionales o de gobernanza CRM no se heredan.
- Separar entre proyectos repositorios, configuración/agentes/modelos, variables, XDG, sesiones, caché/estado/recovery, locks, logs, unidades systemd/timers, `RuntimeDirectory`, temporales, procesos, puertos y contratos de selección de issues/ramas, cuando corresponda.
- Se admite compartir binarios/herramientas comunes (OpenCode, Git, GitHub CLI, Python), **no** compartir configuración por proyecto. Los cambios de alcance global que puedan afectar a CRM u otros proyectos son **MATERIALES** y requieren autorización expresa antes de ejecutarse.
- Diseñar para que otro proyecto pueda incorporar su propia instancia sin modificar WHEREIS ni CRM; evitar un framework genérico especulativo o replicar referencias cruzadas específicas. Aislamiento primero, reutilización solo ante necesidad justificada.
- La separación horaria histórica CRM `:15` / WHEREIS `:45` es referencia de aislamiento temporal, **no** aprobación del timer ni señal de un runner común.

La inspección de rutas y servicios actuales del servidor y el resultado de pruebas de no colisión siguen **PENDIENTES de evidencia**. Esta aclaración no levanta `NO ASIGNAR PROGRAMADOR`, ni autoriza desarrollo, cambios globales, instalación o ejecución desatendida. La [documentación operativa](../orquestacion/operacion-linux.md) contiene la matriz de validación.

## Ramas

- Nuevas tareas de `PROGRAMADOR-LINUX`: `programador-linux/<issue>-<descripcion>`.
- Nuevas tareas de `CODEX`: `codex/<issue>-<descripcion>`.
- Arquitectura documental: `arquitectura/<issue>-<descripcion>`.
- Cambiar el modelo de `PROGRAMADOR-LINUX` no cambia la rama de una tarea en curso.
- Ramas históricas o ya abiertas con prefijo `qwen/` **no se renombran retroactivamente**.

## Política de elección del programador

**PROGRAMADOR-LINUX — tareas delimitadas y de bajo riesgo**: UI sin lógica sensible, estilos/recursos, accesibilidad, documentación técnica localizada, tests deterministas y modificaciones pequeñas sin efectos en autorizaciones, identidad, permisos, seguridad, ubicación sensible o datos de menores.

**CODEX — fiabilidad y responsabilidad crítica**: autenticación, identidad, vínculos/revocación, privacidad/datos de menores, permisos Android/segundo plano, envío de posiciones, sincronización/concurrencia, seguridad, persistencia sensible, diseño de APIs y cambios transversales o de alta incertidumbre. Si una tarea de PROGRAMADOR-LINUX toca un límite crítico, se detiene y vuelve a TECH LEAD.

**Regla:** coste o tokens disponibles no justifican reducir cobertura o gates. TECH LEAD decide la asignación definitiva.

## Modelo Linux: estado actual

A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` se registra como **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO**.

- Resultado conservado: 14/16, sin fallos eliminatorios observados.
- Respetó rama y alcance, usó tools, mantuvo estado, ejecutó tests, produjo commits coherentes y no intentó push/merge.
- Se observaron imprecisiones menores de revisión Git/informe.
- Evidencias: comentarios de [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28) y PR documental [#29](https://github.com/mundoinformaticacanaria/whereis/pull/29).

Esto **NO** significa aprobado para operación desatendida, desarrollo real ni activación del timer.

La primera ejecución sobre una issue real, únicamente cuando los bloqueos generales estén resueltos, será pequeña, de bajo riesgo, perfectamente delimitada, autorizada en GitHub, supervisada y revisada externamente; no tocará seguridad, identidad, permisos, ubicación sensible ni datos de menores.

## Independencia de QA

- Para código `PROGRAMADOR-LINUX`: QA `CODEX` en función revisora separada o `CHATGPT-QA` independiente.
- Para código `CODEX`: QA `CHATGPT-QA` independiente, nunca el mismo Codex que programó.
- QA debe leer desde GitHub contrato, diff completo, commits, tests y CI aplicable al SHA exacto.
- Si QA no puede obtener evidencias o no es independiente: `BLOQUEADO`.
- El dictamen QA no sustituye revisión final/merge del Tech Lead.

## Autorización y limitaciones

- **NO ASIGNAR `PROGRAMADOR`** mientras falten baseline funcional/arquitectónico, seguridad #24, labels verificadas, protección de `main`, CI/gates mínimos, QA operativa, permisos/accesos y demás prerrequisitos de #28.
- A 18/10/2026 `main` figura sin branch protection y sin rulesets; no existe `.github/workflows` en `main`.
- Zona horaria, rama de logs y heartbeat siguen `PENDIENTE`.
- Ninguna contraseña/token se almacena en el repositorio.
- G-02 permite documentar y configurar la orquestación aprobada; no autoriza por sí sola instalaciones no aprobadas, gasto, despliegue, desarrollo real ni proveedores.

## Referencias

- [Issue #26](https://github.com/mundoinformaticacanaria/whereis/issues/26) y [PR #27](https://github.com/mundoinformaticacanaria/whereis/pull/27): G-02 original.
- [Issue #28](https://github.com/mundoinformaticacanaria/whereis/issues/28): enmienda model-neutral y bloqueos operativos vivos.
- [Issue #37](https://github.com/mundoinformaticacanaria/whereis/issues/37): decisión expresa sobre ejecutor formal ARQUITECTO.
- [PR #29](https://github.com/mundoinformaticacanaria/whereis/pull/29): evidencias sintéticas de modelos; no autoriza desarrollo.
- [G-01 V3](G-01-gobernanza-minima-cinco-roles.md)
- [Playbook](../orquestacion/README.md)
- [Perfil PROGRAMADOR-LINUX](../orquestacion/programador-linux.md)
- [Perfil CODEX](../orquestacion/codex.md)
