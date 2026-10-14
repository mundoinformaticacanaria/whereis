# Configuración recomendada en GitHub

Esta configuración no forma parte del contenido versionado y debe aplicarse manualmente o mediante automatización autorizada en cada repositorio destino.

## Repositorio plantilla

Para este repositorio de gobernanza, activar en GitHub:

`Settings → General → Template repository`

Así podrá usarse mediante **Use this template** para crear nuevos repositorios sin arrastrar historial de commits.

## Labels recomendadas

Crear, como mínimo:

- `ARQUITECTO`
- `FUNCIONAL`
- `COMERCIAL`
- `TECH LEAD`
- `QA`
- `PROGRAMADOR`
- `DEVOPS`
- `PROPIETARIO`

Las identidades de programadores son específicas de cada proyecto y no deben fijarse en esta plantilla.

## Merge

Recomendación por defecto:

- permitir squash merge;
- evitar merge directo de Programadores;
- exigir revisión Tech Lead antes de integrar código;
- mantener PR pequeñas y vinculadas a issue.

## Branch protection / rulesets

Configurar cuando el proyecto lo permita:

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
