# Orquestación operativa — Whereis

**Lee primero:** `AGENTS.md`, `docs/estado-proyecto.md`, `docs/criterios-desarrollo.md`, [G-02](../decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), tu `docs/contexto-*.md` y **la issue completa con comentarios**. GitHub `main` + issue es la fuente de verdad. No utilices un resumen de chat como baseline. Para dudas técnicas, ver `docs/arquitectura.md`.

## Cola única: GitHub Issues

| Labels de rol en issue | Siguiente responsable |
|---|---|
| Sin ninguna label de rol | TECH LEAD (por defecto, triage o revisión final) |
| `TECH LEAD` | TECH LEAD explícito |
| `PROPIETARIO` | Persona propietaria; decisión o autorización |
| `FUNCIONAL` | ChatGPT Funcional |
| `ARQUITECTO` | Chat ChatGPT dedicado e independiente de TECH LEAD/QA (enmienda G-02 #37) |
| `PROGRAMADOR` | Ejecutor único del cuerpo de issue: `PROGRAMADOR-LINUX` o `CODEX` |
| `QA` | Codex QA o ChatGPT QA independiente del autor |

Si una issue presenta **dos o más labels de rol**, solo TECH LEAD puede inspeccionarla/abordarla para resolver el error de enrutamiento; ningún otro rol ejecuta trabajo sustantivo hasta dejar una sola label (decisión #38). Solo **una label de rol** por issue ejecutable; no añadir labels `PROGRAMADOR-LINUX`, `QWEN`, `CODEX`, `PENDIENTE`, etc. Para los cambios de responsable: quitar la label anterior y añadir la nueva; para devolver al TECH LEAD basta quitar todas las labels de rol. La label `TECH LEAD` ya existente equivale a sin label. No asumir que las labels están todas creadas: comprobar la configuración real antes de depender de ella.

## Heartbeat y coordinación (#38)

Antes de abordar una issue, el rol consulta **su propio** log en `ops/logs` para esa issue, verifica el ID de intervención y la ventana desde INICIO: <30 minutos sin FIN bloquea, ≥30 minutos permite nueva intervención sin cierre retroactivo; FIN emparejado permite otra inmediatamente. UTC + hora Atlantic/Canary entre corchetes, segundos y 100 entradas recientes por rol. El log no es un lock atómico ni autorización. Ante errores de GitHub no se modifica la automatización horaria TECH LEAD; no se ejecutan mutaciones inseguras con estado desconocido. **Implantación pendiente**, véase [política](../logs/README.md) y [#38](https://github.com/mundoinformaticacanaria/whereis/issues/38).

## Identidad Linux y modelo

`PROGRAMADOR-LINUX` es la identidad lógica estable del ejecutor Linux. El modelo/proveedor se selecciona por configuración y puede cambiar por disponibilidad, coste o calidad sin crear otra identidad ni modificar la label `PROGRAMADOR`, la rama de una tarea en curso o los gates. `QWEN-LINUX` está **SUPERSEDED** como identidad operativa; se conserva solo por trazabilidad histórica.

A 18/10/2026, `nvidia/nemotron-3-super-120b-a12b:free` es únicamente **CANDIDATO ACTUAL VALIDADO EN ENTORNO AISLADO** (14/16). No autoriza desarrollo real, ejecución desatendida ni timer. Véase [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28).

## Handoff arquitectónico

`ARQUITECTO` corresponde a un chat ChatGPT dedicado e independiente, no a TECH LEAD ni a QA del mismo trabajo. Lee `main`, contexto, issue y comentarios; publica en GitHub propuesta, evidencias y pendientes. Eleva decisiones materiales reservadas a `PROPIETARIO`; devuelve a TECH LEAD para revisión/integración retirando la label `ARQUITECTO` o cambiándola a `TECH LEAD` cuando el entregable sea revisable. Las PR #34/#35 son DRAFT y no tienen dictamen formal acreditado por el nuevo ejecutor. Sin baseline ni desarrollo por la enmienda #37.

## Handoff de implementación

1. `TECH LEAD` confirma contrato autorizado, dependencias cerradas, riesgo, ejecutor y QA independiente; asigna `PROGRAMADOR`, indica `Ejecutor autorizado` y rama.
2. `PROGRAMADOR-LINUX` o `CODEX` lee el contrato, ejecuta solo lo autorizado, presenta PR vinculada a issue y adjunta pruebas, comando/resultado, head SHA, riesgos y limitaciones.
3. El ejecutor retira `PROGRAMADOR`, asigna `QA` y se detiene. No toma más trabajo de forma autónoma.
4. QA independiente obtiene diff, SHA y evidencias de primera mano. Dictamen `APTO`, `DEFECTOS` o `BLOQUEADO` con razones y test negativo cuando aplique.
5. `DEFECTOS`: QA devuelve `PROGRAMADOR` con el mismo ejecutor o a TECH LEAD si la reasignación es necesaria. `APTO`: QA retira su label para devolver a TECH LEAD.
6. TECH LEAD revisa PR/issue/decisiones/CI/SHA y hace merge o devuelve. Cambiar SHA invalida el APTO previo.

## Planificación y límites

- Máximo una issue activa por ejecutor, salvo decisión explícita de TECH LEAD; una PR por unidad útil.
- PROGRAMADOR-LINUX es preferente para tareas poco riesgosas y deterministas; Codex para arquitectura, permisos, seguridad, identidad, backend sensible, ubicación y concurrencia. Ver [G-02](../decisiones/G-02-orquestacion-qwen-codex-chatgpt.md).
- Ningún ejecutor instala servicios, expone datos, altera settings o cambia requisitos sin autorización.
- En la fase actual **no hay programación autorizada**. Primero resolver las decisiones del PROPIETARIO y el baseline funcional/arquitectónico del incremento.
- El Tech Lead revisa periódicamente issues sin labels: esa es su bandeja de entrada, no trabajo para los programadores.

## Arranque por entorno

- [PROGRAMADOR-LINUX](programador-linux.md): ejecutor Linux model-neutral, requisitos de acceso y prompt reproducible.
- [QWEN-LINUX — SUPERSEDED](qwen-linux.md): referencia histórica; no usar como identidad en nuevas issues.
- [Codex](codex.md): instrucciones del Programador CODEX y QA independiente, no titular de ARQUITECTO desde la enmienda #37.
- [ChatGPT conversacional](chatgpt-roles.md): Funcional, Tech Lead, Arquitecto independiente y QA.
- [Plantilla de issue](../../.github/ISSUE_TEMPLATE/tarea-ejecutable.md): campos obligatorios para el enrutamiento.
- No hay integración automática de mensajes con PROGRAMADOR-LINUX ni Codex confirmada. El disparador de ejecución es una issue efectivamente asignada, no una etiqueta o mención en un chat.
