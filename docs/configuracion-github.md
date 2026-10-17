# Configuración recomendada en GitHub

Esta configuración no forma parte del contenido versionado y debe aplicarse manualmente o mediante automatización autorizada en cada repositorio destino.

## Repositorio Whereis

Whereis es el repositorio del producto. No se presupone que deba convertirse en repositorio plantilla. Su configuración concreta requiere decisión operativa explícita.

## Labels de siguiente acción — G-02

Labels de **roles** aprobados: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`.

- Una issue con **cero labels de rol** es propiedad de TECH LEAD; la label `TECH LEAD` expresa lo mismo de forma opcional.
- Para cada issue ejecutable, solo una label de rol; no añadir labels de modelos, identidades o estados como mecanismo de asignación.
- Con label `PROGRAMADOR`, el campo del cuerpo `Ejecutor autorizado: QWEN-LINUX` o `Ejecutor autorizado: CODEX` determina inequívocamente el ejecutor.
- `DEVOPS` y `COMERCIAL` no son roles activos. Si existen sus labels antiguas, no asignar nuevas tareas sin aprobación.
- La existencia/configuración completa de las labels de GitHub debe verificarse: algunas constan ya en issues actuales, pero la herramienta disponible no puede crear o inventariar labels globales. Su configuración sigue PENDIENTE de completar y confirmar.
- Prefijos de ramas: `qwen/<issue>-<slug>`, `codex/<issue>-<slug>`; propuestas de Arquitecto `arquitectura/<issue>-<slug>`. No renombrar las ramas funcionales existentes.

Ver [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md) y [orquestación](orquestacion/README.md).

## Merge

Recomendación por defecto:

- permitir squash merge;
- evitar merge directo de Programadores;
- exigir revisión Tech Lead antes de integrar código;
- mantener PR pequeñas y vinculadas a issue.

## Branch protection / rulesets

**PENDIENTE DE CONFIGURACIÓN / AUTORIZACIÓN OPERATIVA.** Configurar cuando el proyecto lo permita y se aprueben las reglas:

- proteger `main`;
- impedir force-push;
- exigir CI requerido antes de merge;
- exigir conversación resuelta cuando corresponda;
- ajustar requisitos de revisión al equipo real.

No copiar reglas de protección que el proyecto no pueda satisfacer operativamente.

## GitHub Actions

Configurar CI específico al stack del proyecto. La plantilla no impone lenguaje ni herramientas concretas.

## Issues y PR

Este repositorio ya incluye plantillas base en `.github/` para:

- tarea ejecutable;
- decisión MATERIAL;
- pull request.
