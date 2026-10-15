# Onboarding de roles

## Gobernanza específica de Whereis (G-01 V3)

Roles activos confirmados por el Propietario: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `PROGRAMADOR` y `QA`. La relación de roles que sigue conserva las especialidades de referencia, pero `ARQUITECTO`, `DEVOPS` y `COMERCIAL` no son perfiles activos permanentes. Véase [G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md). `FUNCIONAL` es independiente de `TECH LEAD`; `QA` debe ser independiente del autor de cada implementación. Las configuraciones e identidades concretas aún están pendientes.

---

## Entrada común

Todo rol que llegue al proyecto debe:

1. identificar el repositorio correcto;
2. consultar `main`;
3. leer `AGENTS.md`;
4. leer `docs/estado-proyecto.md`;
5. leer `docs/criterios-desarrollo.md`;
6. leer su `docs/contexto-*.md`;
7. aplicar `docs/logs/README.md` si su rol tiene heartbeat;
8. leer la issue completa y todos sus comentarios antes de actuar;
9. revisar PR, CI y decisiones relacionadas cuando existan.

GitHub prevalece sobre recuerdos, chats y resúmenes.

## Tech Lead

Responsable de priorización técnica, integración, calidad final, paralelismo, higiene de GitHub y merge.

## Arquitectura

Responsable de límites, dependencias, contratos, decisiones estructurales y evaluación de infraestructura/proveedores desde criterio técnico.

## Funcional

Responsable de actores, reglas, permisos funcionales, flujos, validaciones, criterios de aceptación y documentación funcional.

## Programador

Implementa únicamente la issue asignada. No amplía alcance, no hace merge y se detiene tras el handoff.

## QA

Revisa de forma independiente y adversarial contrato, comportamiento, calidad, riesgos y gates. Devuelve `APTO`, `DEFECTOS` o `BLOQUEADO`.

## DevOps

Responsable de CI/CD, DX, entornos, observabilidad, despliegue e infraestructura autorizada. No decide producto ni proveedores por intuición.

## Comercial

Responsable de costes, licencias, contratación, impacto comercial y supuestos económicos cuando corresponda.

## Propietario

Decide lo que requiere autoridad humana: alcance, prioridades, autorizaciones, gasto, proveedores cuando proceda y contradicciones no resolubles técnicamente.

## Regla de handoff

Una issue debe indicar quién tiene la siguiente acción. Un rol no continúa por iniciativa propia fuera de su responsabilidad.
