# Configuración recomendada en GitHub

Esta configuración no forma parte del contenido versionado y debe aplicarse manualmente o mediante automatización autorizada en cada repositorio destino.

## Repositorio Whereis

Whereis es el repositorio del producto. No se presupone que deba convertirse en repositorio plantilla. Su configuración concreta requiere decisión operativa explícita.

## Roles y labels para Whereis — G-01 V3

La decisión confirmada [G-01](decisiones/G-01-gobernanza-minima-cinco-roles.md) define **cinco roles activos iniciales**: `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `PROGRAMADOR` y `QA`. Las correspondientes labels de siguiente acción son una **configuración PENDIENTE**; este documento no acredita que ya existan.

`ARQUITECTO`, `DEVOPS` y `COMERCIAL` quedan inactivos por defecto; no se configura ni se asigna trabajo a dichas especialidades sin decisión específica.

Las identidades ejecutoras de PROGRAMADOR, sus labels adicionales y los prefijos de rama son propios de Whereis y también siguen `PENDIENTE`. Cada issue ejecutable tendrá una única label de siguiente acción cuando esté operativa la configuración.

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
