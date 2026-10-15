# Instrucciones operativas del repositorio

## Propósito

Este repositorio gobierna el desarrollo del proyecto **Whereis**, una aplicación Android de consulta de ubicación autorizada entre dispositivos. Los contratos funcionales y arquitectónicos concretos se documentan en sus baselines y decisiones; no se infieren de este archivo.

La [decisión G-01 V3](docs/decisiones/G-01-gobernanza-minima-cinco-roles.md) confirmó cinco roles activos iniciales. Los demás campos `PENDIENTE DE PROYECTO` deben resolverse mediante decisiones expresas; no se completan por intuición.

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

## Roles y siguiente acción

**CONFIRMADO — G-01 V3:** los cinco roles activos iniciales de Whereis son:

- `PROPIETARIO`: autoridad humana sobre alcance, prioridades, requisitos materiales, proveedores, gastos y autorizaciones reservadas.
- `FUNCIONAL`: responsable **independiente** de análisis funcional, reglas, flujos y criterios de aceptación; propone, no aprueba decisiones materiales por sí solo.
- `TECH LEAD`: coordinación técnica, arquitectura/DevOps iniciales, planificación, integración y merge dentro de lo autorizado; no sustituye al Propietario.
- `PROGRAMADOR`: implementación exclusivamente de tareas asignadas a un ejecutor identificado; no hace merge.
- `QA`: revisión independiente del autor, con dictamen `APTO`, `DEFECTOS` o `BLOQUEADO`; nunca hace merge.

`ARQUITECTO`, `DEVOPS` y `COMERCIAL` no son roles activos permanentes inicialmente. Sus contextos se conservan como referencia y pueden activarse ante necesidad real y autorización, sin presumir identidades ni recursos.

Las cinco labels de siguiente acción correspondientes se **deben configurar**; su existencia en GitHub es `PENDIENTE`. Una issue ejecutable debe tener normalmente una única label de siguiente acción una vez configuradas. `PROPIETARIO` indica decisión o autorización humana requerida.

## Programadores

Las identidades de programadores son **PENDIENTE DE PROYECTO**.

Reglas base:

- una tarea de desarrollo está asignada únicamente con `PROGRAMADOR + exactamente una identidad ejecutora`;
- máximo una issue activa por ejecutor salvo decisión explícita posterior;
- Tech Lead decide el paralelismo;
- solo paralelizar trabajos realmente independientes;
- capacidad libre es válida si no existe trabajo útil e independiente;
- ningún Programador hace merge;
- ningún Programador toma otra tarea por iniciativa propia.

Los prefijos de rama de cada ejecutor deben definirse en `docs/estado-proyecto.md` o en una decisión de gobernanza del proyecto.

## Handoffs funcionales y de desarrollo

- Decisiones funcionales materiales: `FUNCIONAL → PROPIETARIO (aprueba) → TECH LEAD`, con requisitos y criterios de aceptación registrados antes de asignar implementación.
- Desarrollo autorizado: `PROGRAMADOR + ejecutor → QA independiente → TECH LEAD → merge o devolución`.
- El Programador implementa; QA revisa de forma adversarial e independiente del autor, y devuelve `APTO`, `DEFECTOS` o `BLOQUEADO`. Ante defectos o bloqueo no hay merge.
- QA nunca hace merge; Tech Lead conserva la revisión final de calidad, integración, prioridad y merge.
- Un cambio del head SHA invalida revisiones previas para integración. Si falta un revisor QA realmente independiente, el merge queda bloqueado.
- G-01 no habilita desarrollo ni autoriza proveedores, infraestructura, costes o nuevos requisitos sin sus aprobaciones específicas.

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
