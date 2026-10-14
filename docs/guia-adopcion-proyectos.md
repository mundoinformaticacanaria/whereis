# Guía de adopción de la plantilla de gobernanza

## Objetivo

Definir cómo aplicar esta plantilla a proyectos nuevos y a proyectos ya existentes sin imponer reglas de forma ciega ni perder decisiones válidas del proyecto destino.

La plantilla aporta una base de gobernanza. El repositorio destino sigue siendo siempre la fuente de verdad de su propio producto.

---

## Escenario A — Proyecto nuevo

Usar este repositorio como **Template repository** y crear el nuevo proyecto desde `Use this template`.

### Pasos

1. Crear el repositorio nuevo desde esta plantilla.
2. Mantenerlo privado por defecto salvo decisión expresa distinta.
3. Revisar `README.md`, `AGENTS.md` y `docs/bootstrap-proyecto.md`.
4. Sustituir todos los `PENDIENTE DE PROYECTO` por decisiones reales o dejarlos explícitamente pendientes si todavía requieren resolución.
5. Definir el objetivo y el alcance del MVP.
6. Definir actores, roles funcionales y responsabilidades.
7. Construir el baseline funcional y registrar qué queda `CONFIRMADO`, `PENDIENTE`, `POST-MVP` o `SUPERSEDED`.
8. Definir y aprobar el baseline arquitectónico mínimo necesario.
9. Definir stack, dependencias, proveedores e infraestructura solo cuando exista necesidad demostrada.
10. Crear en GitHub las labels operativas necesarias:
   - `ARQUITECTO`
   - `FUNCIONAL`
   - `COMERCIAL`
   - `TECH LEAD`
   - `QA`
   - `PROGRAMADOR`
   - `DEVOPS`
   - `PROPIETARIO`
11. Crear las labels de identidad de los programadores realmente disponibles.
12. Crear los ficheros de heartbeat correspondientes a los roles/identidades que vayan a ejecutarse.
13. Completar `docs/estado-proyecto.md` con el estado real inicial.
14. Definir los gates de calidad aplicables al stack concreto.
15. No abrir trabajo de implementación hasta completar el checklist mínimo de `docs/bootstrap-proyecto.md`.
16. A partir de ese momento, todo trabajo material se gestiona mediante issue explícita y siguiendo los handoffs definidos en `AGENTS.md`.

### Resultado esperado

El proyecto queda gobernado desde GitHub y cualquier agente nuevo puede determinar:

- qué está confirmado;
- qué está pendiente;
- qué está autorizado;
- qué está bloqueado;
- quién debe actuar;
- cuál es el baseline vigente;
- y cuál es el estado técnico real.

---

## Escenario B — Proyecto existente o avanzado

**No copiar la plantilla automáticamente ni sustituir de golpe la gobernanza existente.**

Primero debe realizarse una evaluación de compatibilidad.

### Paso 1 — Inventario del proyecto vivo

Leer como mínimo:

- documentación de entrada para agentes;
- estado actual del proyecto;
- requisitos/baseline funcional;
- arquitectura vigente;
- reglas de desarrollo y calidad;
- flujo Git/PR/CI;
- roles y responsabilidades existentes;
- issues, milestones y backlog vivos;
- políticas de logs/observabilidad si existen;
- decisiones materiales históricas que sigan vigentes.

No asumir que una conversación o documentación antigua prevalece sobre el repositorio vivo.

### Paso 2 — Comparación contra la plantilla

Clasificar cada bloque de esta plantilla como:

- **ADOPTAR**: mejora clara y compatible sin cambiar el comportamiento del proyecto;
- **ADAPTAR**: el principio es útil pero necesita ajustarse al proyecto;
- **MANTENER ACTUAL**: la gobernanza existente ya resuelve correctamente esa necesidad;
- **NO APLICA**: la regla no aporta valor al proyecto;
- **CONFLICTO**: la plantilla contradice una decisión material vigente y requiere decisión humana antes de actuar.

La comparación debe cubrir al menos:

- fuente de verdad;
- roles;
- labels de siguiente acción;
- handoffs;
- clasificación `RUTINARIA / MATERIAL`;
- granularidad de issues;
- política de QA;
- responsabilidad de merge;
- CI/gates;
- control de paralelismo;
- heartbeat/logs;
- documentación de estado;
- decisiones materiales;
- proveedores/costes/seguridad/privacidad.

### Paso 3 — Elegir estrategia de adopción

#### Opción 1 — Adopción completa

Usarla solo cuando el proyecto tenga poca gobernanza previa o la existente sea claramente insuficiente y la migración no ponga en riesgo el trabajo activo.

La adopción debe hacerse mediante issues y PR pequeñas. Nunca sustituir toda la documentación en una sola operación sin revisión.

#### Opción 2 — Adopción parcial

Es la opción recomendada para un proyecto avanzado que ya funciona razonablemente bien.

Incorporar únicamente las piezas que mejoren de forma demostrable el proyecto, por ejemplo:

- fuente de verdad explícita;
- estado vivo del proyecto;
- roles/handoffs más claros;
- clasificación MATERIAL;
- QA independiente;
- heartbeat;
- plantilla de decisiones;
- micro-issues y límites de WIP.

No cambiar reglas consolidadas solo para igualar esta plantilla.

#### Opción 3 — Mantener la gobernanza actual

Es válido cuando la evaluación concluye que el proceso actual ya ofrece igual o mejor trazabilidad, separación de responsabilidades, calidad y control de riesgos.

En ese caso puede documentarse la comparación y cerrar la adopción como `NO NECESARIA`.

### Paso 4 — Migración controlada

Si se decide adoptar total o parcialmente:

1. abrir una issue MATERIAL de gobernanza;
2. documentar estado actual y estado objetivo;
3. identificar qué documentos se crean, modifican o quedan superados;
4. no mezclar migración de gobernanza con cambios funcionales o de código no relacionados;
5. preservar decisiones vigentes y marcar explícitamente lo que quede `SUPERSEDED`;
6. mantener el proyecto operativo durante la transición;
7. actualizar onboarding y estado vivo al finalizar;
8. validar que ninguna tarea ejecutable quede sin siguiente responsable.

### Paso 5 — Criterio de cierre

La adopción termina cuando un agente que llegue por primera vez al repositorio puede determinar de forma inequívoca:

- qué debe leer;
- cuál es el baseline vigente;
- cuál es el estado actual;
- qué trabajo está autorizado;
- qué rol debe actuar;
- cómo se valida y se entrega el trabajo;
- y qué decisiones requieren al propietario.

---

## Regla para proyectos muy avanzados

Cuando un proyecto esté ya en una fase avanzada, estable o cercana a entrega, **la estabilidad tiene prioridad sobre la homogeneización**.

No se debe introducir una migración amplia de gobernanza si:

- genera retrabajo documental significativo;
- obliga a renombrar o reestructurar muchas issues activas sin beneficio operativo;
- rompe automatizaciones o runners existentes;
- introduce confusión entre agentes;
- o aumenta el riesgo de entrega.

En estos casos, registrar las mejoras para el siguiente milestone o adoptar solo cambios de alto valor y bajo riesgo.

---

## Prompt recomendado para evaluar un proyecto existente

Puede darse a un Tech Lead o agente con acceso al repositorio la siguiente instrucción:

> Revisa el estado vivo de este repositorio y compáralo con `mundoinformaticacanaria/project-ai-governance-template`. No copies la plantilla automáticamente. Evalúa, bloque por bloque, qué conviene ADOPTAR, ADAPTAR, MANTENER ACTUAL, considerar NO APLICA o marcar como CONFLICTO. Prioriza la estabilidad del proyecto y no cambies código ni gobernanza hasta presentar una propuesta de migración con beneficios, riesgos y alcance concreto.

---

## Principio final

El objetivo de la plantilla no es que todos los repositorios tengan exactamente los mismos ficheros o procesos.

El objetivo es que todos los proyectos tengan **gobernanza suficiente, explícita, verificable y mantenible**, adaptada a su contexto real.
