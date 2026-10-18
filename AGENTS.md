# Instrucciones operativas del repositorio

## Propósito

Este repositorio gobierna el desarrollo del proyecto **Whereis**, una aplicación Android de consulta de ubicación autorizada entre dispositivos. Los contratos funcionales y arquitectónicos concretos se documentan en sus baselines y decisiones; no se infieren de este archivo.

La [decisión G-01 V3](docs/decisiones/G-01-gobernanza-minima-cinco-roles.md) fijó cinco roles iniciales. **G-02** ([orquestación](docs/decisiones/G-02-orquestacion-qwen-codex-chatgpt.md)) activa además `ARQUITECTO` (Codex), identifica los programadores `PROGRAMADOR-LINUX` y `CODEX` y establece el enrutamiento mediante labels. Seis roles operativos; `DEVOPS` y `COMERCIAL` siguen no activos. Los campos `PENDIENTE` no se completan por intuición.

## Fuente de verdad

- GitHub es la fuente de verdad para alcance, prioridad, estado, decisiones y handoffs.
- La issue y todos sus comentarios forman el contrato vivo de trabajo.
- Los documentos canónicos de `main` prevalecen sobre chats, prompts, recuerdos, resúmenes y logs.
- Los logs son observabilidad auxiliar y nunca autorizan trabajo.
- No inventar requisitos ni convertir propuestas, hipótesis o pendientes en requisitos confirmados.
- Si una instrucción externa contradice el estado vivo de GitHub, debe resolverse explícitamente antes de actuar.

## Antes de actuar

Todo rol debe, según corresponda a su tarea:

1. aplicar la política de heartbeat de `docs/logs/README.md`;
2. consultar `main`;
3. leer este `AGENTS.md`;
4. leer `docs/estado-proyecto.md`;
5. leer `docs/criterios-desarrollo.md`;
6. leer su `docs/contexto-*.md`;
7. leer la issue completa y todos sus comentarios;
8. revisar PR, CI y decisiones relacionadas cuando existan.

No asumir que una decisión histórica sigue vigente sin verificar el repositorio.

## Clasificación obligatoria

Antes de cualquier acción distinta de inspección o heartbeat, clasificar el trabajo:

- **RUTINARIA**: acción factual o mecánica sin interpretar requisitos, arquitectura, seguridad, privacidad, alcance, costes, proveedores, persistencia ni baseline.
- **MATERIAL**: cambia o interpreta requisitos, baseline, arquitectura, seguridad, privacidad, persistencia, proveedores, infraestructura, costes, alcance, refactor estructural, código o merge.

Ante duda: **MATERIAL**.

## Estados de decisión

Usar de forma explícita cuando sea relevante:

- `CONFIRMADO`
- `HIPÓTESIS`
- `PROPUESTA`
- `PENDIENTE`
- `POST-MVP`
- `SUPERSEDED`

No resolver contradicciones por intuición.

## Roles, ejecutores y siguiente acción

**CONFIRMADO — G-02:** roles operativos `PROPIETARIO` (humano), `FUNCIONAL` (chat ChatGPT independiente), `TECH LEAD` (chat ChatGPT), `ARQUITECTO` (Codex), `PROGRAMADOR` (PROGRAMADOR-LINUX o CODEX) y `QA` (Codex o ChatGPT independiente del autor).

- `PROPIETARIO`: decide alcance, requisitos materiales, proveedores, gastos y autorizaciones reservadas.
- `FUNCIONAL`: requisitos, permisos funcionales, flujos y aceptación; propone sin autoaprobar decisiones materiales.
- `TECH LEAD`: dueño del backlog de issues sin label de rol; arquitectura y desarrollo coordinados, asignación por riesgo, revisión final y merge.
- `ARQUITECTO`: Codex; propuestas y validación arquitectónica, sin facultad de aprobar gastos/proveedores o alterar requisitos.
- `PROGRAMADOR`: exige en el cuerpo **Ejecutor autorizado: PROGRAMADOR-LINUX** o **Ejecutor autorizado: CODEX**; solo implementación asignada, PR y no merge.
- `QA`: revisor independiente, `APTO` / `DEFECTOS` / `BLOQUEADO`, sin modificar el código evaluado ni realizar merge.

`DEVOPS` y `COMERCIAL` quedan como especialidades no activas por defecto; su intervención requiere autorización.

**Labels de issues:** una sola label de **rol** para la siguiente acción: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR` o `QA`. **Una issue sin ninguna label de rol es responsabilidad del TECH LEAD.** `TECH LEAD` explícita es redundante pero válida para las issues heredadas. No usar labels de modelo, severidad o estados como mecanismo de asignación; identidades de Programador en el cuerpo. Las labels y permisos no verificados siguen pendientes de configuración operativa.

Consultar [playbook](docs/orquestacion/README.md) y [perfiles](docs/orquestacion/) para onboarding y handoff.

## Programadores

Identidades lógicas de programadores **CONFIRMADAS**: `PROGRAMADOR-LINUX` (ejecutor en servidor Linux) y `CODEX` (Codex de ChatGPT). `QWEN-LINUX` queda **SUPERSEDED** como identidad operativa desde la enmienda material de G-02 del 18/10/2026. El modelo/proveedor de `PROGRAMADOR-LINUX` es configuración operativa separada y puede cambiar sin crear una identidad nueva ni alterar sus gates. Acceso, usuario de GitHub, permisos y disponibilidad real continúan **PENDIENTE de verificación**.

Reglas base:

- una tarea está asignada únicamente con **label `PROGRAMADOR` + exactamente un campo `Ejecutor autorizado: PROGRAMADOR-LINUX` o `Ejecutor autorizado: CODEX`** en el cuerpo de la issue;
- máximo una issue activa por ejecutor salvo decisión explícita posterior;
- Tech Lead decide el paralelismo;
- solo paralelizar trabajos realmente independientes;
- capacidad libre es válida si no existe trabajo útil e independiente;
- ningún Programador hace merge;
- ningún Programador toma otra tarea por iniciativa propia.

Prefijos de rama de trabajo: `programador-linux/<issue>-<slug>` para PROGRAMADOR-LINUX; `codex/<issue>-<slug>` para Codex; `arquitectura/<issue>-<slug>` para propuestas del Arquitecto. No renombrar ramas ya abiertas. No iniciar implementación sin baselines/seguridad/bootstrap autorizados.

## Handoffs funcionales y de desarrollo

- Decisiones funcionales materiales: `FUNCIONAL → PROPIETARIO (aprueba) → TECH LEAD`, con criterios de aceptación registrados. Análisis estructural: `ARQUITECTO (Codex) → TECH LEAD`, o `PROPIETARIO` si requiere autoridad humana.
- Desarrollo autorizado: `PROGRAMADOR + ejecutor → QA independiente → TECH LEAD → merge o devolución`.
- El Programador implementa; QA revisa de forma adversarial e independiente del autor, y devuelve `APTO`, `DEFECTOS` o `BLOQUEADO`. Para PR creadas por `CODEX`, QA = chat de ChatGPT independiente; para `PROGRAMADOR-LINUX`, QA = Codex o ChatGPT independiente. La misma implementación no puede autorrevisarse. Ante defectos o bloqueo no hay merge.
- QA nunca hace merge; Tech Lead conserva la revisión final de calidad, integración, prioridad y merge.
- Un cambio del head SHA invalida revisiones previas para integración. Si falta un revisor QA realmente independiente, el merge queda bloqueado.
- G-01/G-02 no habilitan desarrollo ni autorizan proveedores, infraestructura, costes o nuevos requisitos sin aprobaciones específicas. Handoff de una issue a TECH LEAD = retirar labels de rol (o usar `TECH LEAD` explícita).

## Principios de arquitectura

La arquitectura concreta es **PENDIENTE DE PROYECTO** y debe quedar definida en `docs/arquitectura.md`.

Por defecto:

- preferir la solución más simple que cumpla el contrato;
- separar dominio, aplicación e infraestructura cuando exista una frontera real;
- mantener las dependencias orientadas hacia el núcleo del negocio;
- encapsular proveedores externos detrás de contratos propios cuando corresponda;
- evitar infraestructura, capas, abstracciones y dependencias sin necesidad demostrada.

No introducir microservicios, colas, cache distribuida, orquestadores, event sourcing u otras piezas complejas por defecto.

## Proveedores, datos, costes y seguridad

- Ningún proveedor, servicio de pago o infraestructura se considera autorizado por defecto.
- No asumir que cloud, DB, storage, email, IA, observabilidad u otros servicios son gratuitos o están incluidos.
- No versionar secretos ni credenciales.
- Usar únicamente datos ficticios o anonimizados en desarrollo, pruebas, documentación y demos salvo autorización expresa del proyecto.
- Señalar requisitos que aumenten materialmente coste, complejidad, riesgo, seguridad o protección de datos.

## Refactorización

Clasificar hallazgos como:

- `REFACTOR AHORA`
- `REFACTOR CON LA FEATURE`
- `DEUDA REGISTRADA`
- `NO REFACTOR`

No introducir abstracciones especulativas ni refactorizar por estética.

## Calidad

Cada proyecto debe definir sus gates concretos en `docs/criterios-desarrollo.md`.

Como mínimo, cuando exista código:

- análisis estático/lint apropiado al lenguaje;
- comprobación de tipos cuando aplique;
- tests automatizados;
- pruebas de comportamiento e invariantes relevantes;
- comprobación de whitespace/diff;
- tipos, nombres y responsabilidades explícitos;
- sin secretos;
- sin datos reales no autorizados;
- sin llamadas externas accidentales.

No debilitar controles de calidad para obtener verde.

## Granularidad del trabajo

Todo trabajo ejecutable debe tender a la mínima unidad útil, cohesionada, determinista, verificable y cerrable.

- una responsabilidad principal por issue;
- criterios de aceptación claros;
- exclusiones explícitas;
- dependencias documentadas;
- PR pequeñas y cohesionadas;
- no fragmentar por debajo de una unidad útil;
- no crear trabajo de relleno.

## Git y PR

- Programadores trabajan en rama propia.
- No escribir código directamente en `main`.
- Toda implementación debe tener issue y PR.
- Mantener PR pequeñas y cohesionadas.
- El merge corresponde al Tech Lead o responsable humano autorizado.
- CI debe corresponder al head SHA exacto revisado.

## Logs

Política: `docs/logs/README.md`.

Los logs son heartbeat e histórico auxiliar, nunca fuente de verdad.

Cada rol con heartbeat **operativamente definido** cumple su política de inicio y fin de ciclo. En Whereis, la zona horaria, rama y ficheros de heartbeat están `PENDIENTE`; no fabricar registros ni dar por activada una configuración no aprobada.

## Regla final

Al instanciar esta plantilla, el repositorio del proyecto destino debe poder responder desde GitHub:

- qué está confirmado;
- qué está pendiente;
- qué está autorizado;
- qué está bloqueado;
- quién debe actuar;
- cuál es el baseline vigente;
- cuál es el estado técnico real.
