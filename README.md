# Project AI Governance Template

Plantilla reusable de gobernanza para proyectos de software coordinados con agentes de IA y humanos.

## Propósito

Este repositorio define reglas operativas, roles, handoffs, calidad, observabilidad y estructura documental reutilizables entre proyectos. No contiene requisitos de negocio ni código de producto.

## Cómo usarla

1. Crear un repositorio nuevo para el proyecto.
2. Copiar esta estructura como punto de partida.
3. Completar los campos marcados como `PENDIENTE DE PROYECTO`.
4. Definir y aprobar el baseline funcional y arquitectónico antes de autorizar desarrollo.
5. Crear las labels e identidades de ejecutores realmente disponibles.
6. No copiar automáticamente reglas específicas de otro proyecto.

Para proyectos nuevos y para adaptar proyectos ya existentes, seguir `docs/guia-adopcion-proyectos.md`.

## Principio central

GitHub es la fuente de verdad del proyecto. Conversaciones, prompts, recuerdos, logs y herramientas auxiliares nunca prevalecen sobre el estado vivo del repositorio.

## Estructura

- `AGENTS.md`: reglas operativas globales.
- `docs/estado-proyecto.md`: estado vivo y siguiente avance.
- `docs/criterios-desarrollo.md`: criterios permanentes de calidad y ejecución.
- `docs/arquitectura.md`: baseline arquitectónico del proyecto.
- `docs/onboarding-roles.md`: entrada rápida para agentes/roles.
- `docs/contexto-*.md`: responsabilidades persistentes por rol.
- `docs/logs/README.md`: política de heartbeat.
- `docs/guia-adopcion-proyectos.md`: procedimiento para proyectos nuevos y proyectos ya avanzados.
- `docs/decisiones/`: decisiones materiales de arquitectura/gobernanza.
- `docs/decisiones-funcionales/`: decisiones funcionales materiales.

## Antes de empezar un proyecto real

No autorizar implementación hasta que estén definidos, como mínimo:

- objetivo y alcance MVP;
- actores y responsabilidades;
- baseline funcional;
- baseline arquitectónico;
- clasificación de trabajo y flujo de handoffs;
- gates de calidad;
- identidades de programadores disponibles;
- tratamiento de seguridad, privacidad, costes, proveedores e infraestructura;
- política de logs/heartbeat.

Esta plantilla debe adaptarse de forma explícita. No se considera correcto usarla sin revisar y eliminar reglas que no apliquen al proyecto destino.
