# Whereis

Proyecto Android para compartir y consultar ubicaciones de dispositivos autorizados. **Fase actual: definición funcional, seguridad y arquitectura; desarrollo del producto todavía no autorizado.**

GitHub es la fuente de verdad: [repositorio](https://github.com/mundoinformaticacanaria/whereis). Las issues completas (incluidos comentarios) y documentos vigentes de `main` prevalecen sobre chats, notas locales y ejemplos.

## Primeros pasos para cualquier agente

1. Lee [AGENTS.md](AGENTS.md), [estado del proyecto](docs/estado-proyecto.md) y [criterios de desarrollo](docs/criterios-desarrollo.md).
2. Lee el [playbook de orquestación](docs/orquestacion/README.md) y [G-02](docs/decisiones/G-02-orquestacion-qwen-codex-chatgpt.md).
3. Lee tu documento [contexto de rol](docs/onboarding-roles.md) y todas las issues/PR relacionadas con la tarea.
4. Ejecuta únicamente la siguiente acción autorizada; si faltan permiso, contexto, decisiones, accesos o pruebas, informa `BLOQUEADO` a TECH LEAD.

## Equipo y cola

| Rol (label exacta) | Ejecuta |
|---|---|
| PROPIETARIO | Persona propietaria |
| FUNCIONAL | ChatGPT conversacional |
| TECH LEAD o issue sin label de rol | ChatGPT Tech Lead activo |
| ARQUITECTO | ChatGPT dedicado e independiente de TECH LEAD y de QA de su propio trabajo (decisión #37) |
| PROGRAMADOR | PROGRAMADOR-LINUX o CODEX según campo `Ejecutor autorizado` de la issue |
| QA | Codex o ChatGPT **independiente del autor** |

**No se asignan issues a modelos mediante labels propias.** Cada issue ejecutable tiene una sola label de siguiente rol. En `PROGRAMADOR` se requiere `Ejecutor autorizado: PROGRAMADOR-LINUX` o `Ejecutor autorizado: CODEX`. Sin labels de rol = responsabilidad del Tech Lead.

## Guías listas para entregar

- [PROGRAMADOR-LINUX](docs/orquestacion/programador-linux.md) — ejecutor Linux con modelo configurable
- [Codex Programador / QA independiente cuando proceda](docs/orquestacion/codex.md)
- [Chats ChatGPT Funcional / Tech Lead / Arquitecto dedicado / QA independiente](docs/orquestacion/chatgpt-roles.md)

## Desarrollo y calidad

El circuito técnico es `TECH LEAD → PROGRAMADOR → QA independiente → TECH LEAD`. El Programador no hace merge ni ocupa otra tarea por iniciativa propia. QA debe verificar la PR y el commit exacto y devolver `APTO`, `DEFECTOS` o `BLOQUEADO`. Para código Codex, QA debe ser un chat ChatGPT independiente, no el Codex que programó.

**No desarrollar** antes de aprobar el baseline funcional y arquitectónico del incremento, resolver bloqueos de seguridad/privacidad (incluidos [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24)) y completar los gates necesarios del [bootstrap](docs/bootstrap-proyecto.md).

## Referencias

- [G-01 (histórica)](docs/decisiones/G-01-gobernanza-minima-cinco-roles.md) y [G-02 (orquestación vigente)](docs/decisiones/G-02-orquestacion-qwen-codex-chatgpt.md).
- [Arquitectura](docs/arquitectura.md) — pendiente de baseline aprobado.
- [Decisiones funcionales](docs/decisiones-funcionales/) — revisar issues y PR abiertas antes de asumir integración.
- [Configuración GitHub](docs/configuracion-github.md) — accesos, labels, protecciones, CI y logs se verifican por separado; ningún secreto en el repositorio.
