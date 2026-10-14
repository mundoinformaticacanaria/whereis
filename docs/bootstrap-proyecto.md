# Checklist de bootstrap de un proyecto nuevo

No autorizar desarrollo hasta completar este checklist.

## 1. Identidad del proyecto

- [ ] Nombre del proyecto.
- [ ] Repositorio fuente de verdad.
- [ ] PROPIETARIO identificado.
- [ ] Objetivo y problema a resolver.
- [ ] Alcance MVP inicial.
- [ ] Fuera de alcance / POST-MVP inicial.

## 2. Gobernanza

- [ ] `AGENTS.md` revisado y adaptado.
- [ ] Labels de siguiente acción creadas.
- [ ] Roles realmente utilizados identificados.
- [ ] Identidades de programadores definidas.
- [ ] Prefijos de rama definidos.
- [ ] Máximo de trabajo en curso definido.
- [ ] Política de merge definida.
- [ ] Zona horaria de heartbeat definida.
- [ ] Rama `ops/logs` y logs necesarios creados, si se usa heartbeat.

## 3. Funcional

- [ ] Actores/perfiles identificados.
- [ ] Requisitos confirmados separados de hipótesis.
- [ ] Flujos principales definidos.
- [ ] Validaciones y errores principales definidos.
- [ ] Criterios de aceptación verificables.
- [ ] Límites de dominio explícitos.
- [ ] Datos sensibles/reales identificados y política de uso definida.

## 4. Arquitectura

- [ ] `docs/arquitectura.md` completado.
- [ ] Stack tecnológico decidido o marcado PENDIENTE.
- [ ] Fronteras/módulos definidos.
- [ ] Persistencia decidida o explícitamente pendiente.
- [ ] Proveedores externos decididos o explícitamente pendientes.
- [ ] Seguridad/autenticación decidida o explícitamente pendiente.
- [ ] Infraestructura/despliegue decidida o explícitamente pendiente.
- [ ] Costes/riesgos materiales señalados.

## 5. Calidad y desarrollo

- [ ] Gates concretos definidos para el stack.
- [ ] CI configurado antes del primer desarrollo MATERIAL cuando sea viable.
- [ ] Flujo `PROGRAMADOR → QA → TECH LEAD` confirmado o sustituido explícitamente.
- [ ] Convenciones de ramas/PR definidas.
- [ ] Política de datos de prueba definida.
- [ ] Prohibición de secretos versionados confirmada.

## 6. Estado vivo

- [ ] `docs/estado-proyecto.md` refleja la realidad.
- [ ] Primer backlog pequeño y priorizado creado.
- [ ] Dependencias entre issues explícitas.
- [ ] Ninguna issue ejecutable queda sin siguiente acción.

## Gate de salida

Solo cuando los puntos necesarios para el primer incremento estén resueltos, Tech Lead puede crear/asignar la primera issue `PROGRAMADOR`.
