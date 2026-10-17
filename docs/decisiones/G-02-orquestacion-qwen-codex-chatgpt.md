# G-02 — Orquestación de Qwen, Codex y ChatGPT

- **Fecha:** 17/10/2026
- **Estado:** `CONFIRMADO` para distribución de funciones y política de labels indicada por el PROPIETARIO; integraciones técnicas y permisos concretos `PENDIENTE`.
- **Tipo:** `MATERIAL` — gobernanza y asignación de ejecutores.
- **Autorización:** [issue #26](https://github.com/mundoinformaticacanaria/whereis/issues/26), por instrucción expresa del PROPIETARIO.
- **Relación con G-01 V3:** modifica la composición operativa: incorpora `ARQUITECTO` como rol activo desempeñado por Codex. Conserva PROPIETARIO, FUNCIONAL, TECH LEAD, PROGRAMADOR y QA, la autoridad humana y QA independiente. G-01 conserva su historia; para composición vigente prevalece G-02.

## Roles y ejecutores

| Label de siguiente acción | Ejecución prevista | Límite |
|---|---|---|
| `PROPIETARIO` | Humano propietario | Aprueba decisiones materiales reservadas |
| `FUNCIONAL` | Chat conversacional ChatGPT | Requisitos; no aprueba por sí mismo ni programa |
| `TECH LEAD` **o ninguna label de rol** | ChatGPT conversacional del Tech Lead activo | Triage, reparto, revisión, merge |
| `ARQUITECTO` | Codex | Diseño/viabilidad técnica; no autoriza gastos ni cambios funcionales |
| `PROGRAMADOR` | Ejecutores `QWEN-LINUX` o `CODEX` | Solo issue asignada, rama/PR; sin merge |
| `QA` | Codex independiente o ChatGPT conversacional independiente | Revisión independiente del autor; sin merge |

`DEVOPS` y `COMERCIAL` no se activan permanentemente sin nueva decisión.

## Labels y asignación

- **Una y solo una label de rol** indica la siguiente acción en cada issue ejecutable. Las demás labels de rol se retiran al hacer handoff.
- **Cero labels de rol significa `TECH LEAD`**. La label `TECH LEAD` explícita es válida, aunque redundante, para mantener compatibilidad con issues existentes.
- **Las labels son nombres de roles**, no nombres de modelos ni estados; Qwen y Codex se diferencian en el cuerpo de una issue `PROGRAMADOR`, sección `Ejecutor autorizado`.
- Identidades lógicas de programador: `QWEN-LINUX` y `CODEX` (no son cuentas GitHub verificadas). Nunca asignar una issue a dos programadores a la vez. Máximo una tarea activa por ejecutor salvo decisión posterior del Tech Lead.
- Ramas de código previstas: `qwen/<issue>-<descripcion>` y `codex/<issue>-<descripcion>`; arquitectura documental `arquitectura/<issue>-<descripcion>`. No cambiar ramas ya existentes para ajustarlas retroactivamente.

## Política de elección del programador

**QWEN-LINUX — prioridad económica y tareas delimitadas**: UI de bajo riesgo, estilos y recursos, accesibilidad, documentación técnica localizada, tests deterministas y modificaciones pequeñas sin efectos en autorizaciones o ubicación sensible. Requiere especificación precisa, tests y revisión independiente.

**CODEX — fiabilidad y responsabilidad crítica**: autenticación, identidad, vínculos y revocación, privacidad/datos de menores, permisos Android/segundo plano, envío de posiciones, sincronización y concurrencia, seguridad, persistencia sensible, diseño de APIs y cambios transversales o de alta incertidumbre. Si una tarea inicialmente Qwen toca un límite crítico, se detiene y devuelve al Tech Lead para reasignación.

**Regla:** los tokens disponibles no sustituyen a criterios de riesgo, ni justifican bajar cobertura o gates. Tech Lead decide la asignación definitiva y puede justificar excepciones en la issue.

## Independencia de QA

- Para código `QWEN-LINUX`: QA `CODEX` (en función revisora separada) o `CHATGPT-QA`.
- Para código `CODEX`: QA `CHATGPT-QA` independiente, nunca el mismo Codex que programó.
- Un chat QA debe leer desde GitHub el contrato, diff completo, commits, tests y CI; no basta que el autor afirme que pasó las pruebas.
- Si el QA no puede obtener las evidencias o no es independiente: `BLOQUEADO`. Cada nueva modificación del head SHA exige nueva revisión.
- El dictamen QA no sustituye la revisión final y merge del Tech Lead.

## Autorización y limitaciones

- No hay desarrollo autorizado hasta que requisitos/baseline arquitectónico/seguridad y bootstrap del incremento estén aprobados.
- El [riesgo de seguridad y menores #24](https://github.com/mundoinformaticacanaria/whereis/issues/24) permanece pendiente; no implementar funcionalidades sensibles por la mera activación de Codex.
- No se ha verificado conexión de Qwen en Linux a GitHub, mecanismos Codex, permisos de push, protección de `main`, CI ni credenciales. Ninguna contraseña/token se almacenará en el repositorio.
- Zona horaria, rama de logs y heartbeat de ejecutores siguen `PENDIENTE`, salvo decisión operativa posterior.
- Esta decisión habilita documentar la orquestación; no habilita instalaciones, gastos, despliegues o proveedores.

## Referencias
- [G-01 V3](G-01-gobernanza-minima-cinco-roles.md)
- [Playbook](../orquestacion/README.md)
- [Perfiles de ejecutores](../orquestacion/)
