# Orquestación operativa — Whereis

**Lee primero:** `AGENTS.md`, `docs/estado-proyecto.md`, `docs/criterios-desarrollo.md`, [G-02](../decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), tu `docs/contexto-*.md` y **la issue completa con comentarios**. GitHub `main` + issue es la fuente de verdad. No utilices un resumen de chat como baseline. Para dudas técnicas, ver `docs/arquitectura.md`.

## Cola única: GitHub Issues

| Labels de rol en issue | Siguiente responsable |
|---|---|
| Sin ninguna label de rol | TECH LEAD (por defecto, triage o revisión final) |
| `TECH LEAD` | TECH LEAD explícito |
| `PROPIETARIO` | Persona propietaria; decisión o autorización |
| `FUNCIONAL` | ChatGPT Funcional |
| `ARQUITECTO` | Codex Arquitecto |
| `PROGRAMADOR` | Ejecutor único del cuerpo de issue: `QWEN-LINUX` o `CODEX` |
| `QA` | Codex QA o ChatGPT QA independiente del autor |

Solo **una label de rol** por issue ejecutable; no añadir labels `QWEN`, `CODEX`, `PENDIENTE`, etc. Para los cambios de responsable: quitar la label anterior y añadir la nueva; para devolver al TECH LEAD basta quitar todas las labels de rol. La label `TECH LEAD` ya existente equivale a sin label. No asumir que las labels están todas creadas: comprobar la configuración real antes de depender de ella.

## Handoff de implementación

1. `TECH LEAD` confirma contrato autorizado, dependencias cerradas, riesgo, ejecutor y QA independiente; asigna `PROGRAMADOR`, indica `Ejecutor autorizado` y rama.
2. `QWEN-LINUX` o `CODEX` lee el contrato, ejecuta solo lo autorizado, presenta PR vinculada a issue y adjunta pruebas, comando/resultado, head SHA, riesgos y limitaciones.
3. El ejecutor retira `PROGRAMADOR`, asigna `QA` y se detiene. No toma más trabajo de forma autónoma.
4. QA independiente obtiene diff, SHA y evidencias de primera mano. Dictamen `APTO`, `DEFECTOS` o `BLOQUEADO` con razones y test negativo cuando aplique.
5. `DEFECTOS`: QA devuelve `PROGRAMADOR` con el mismo ejecutor o a TECH LEAD si la reasignación es necesaria. `APTO`: QA retira su label para devolver a TECH LEAD.
6. TECH LEAD revisa PR/issue/decisiones/CI/SHA y hace merge o devuelve. Cambiar SHA invalida el APTO previo.

## Planificación y límites

- Máximo una issue activa por ejecutor, salvo decisión explícita de TECH LEAD; una PR por unidad útil.
- Qwen es preferente para tareas poco riesgosas y deterministas; Codex para arquitectura, permisos, seguridad, identidad, backend sensible, ubicación y concurrencia. Ver [G-02](../decisiones/G-02-orquestacion-qwen-codex-chatgpt.md).
- Ningún ejecutor instala servicios, expone datos, altera settings o cambia requisitos sin autorización.
- En la fase actual **no hay programación autorizada**. Primero resolver las decisiones del PROPIETARIO y el baseline funcional/arquitectónico del incremento.
- El Tech Lead revisa periódicamente issues sin labels: esa es su bandeja de entrada, no trabajo para los programadores.

## Arranque por entorno

- [Qwen Linux](qwen-linux.md): requisitos de acceso y prompt reproducible.
- [Codex](codex.md): instrucciones del Arquitecto y del Programador.
- [ChatGPT conversacional](chatgpt-roles.md): Funcional, Tech Lead y QA.
- [Plantilla de issue](../../.github/ISSUE_TEMPLATE/tarea-ejecutable.md): campos obligatorios para el enrutamiento.
- No hay integración automática de mensajes con Qwen ni Codex confirmada. El disparador de ejecución es una issue efectivamente asignada, no una etiqueta o mención en un chat.
