# Operación del ejecutor Linux — documentación y recuperación

Relacionado con [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28). Inspección: 19/10/2026. Clasificación: **RUTINARIA**, conservación factual de documentación y evidencias; no cambia autorizaciones.

## Fuente de verdad y conservación

**CONFIRMADO por instrucción del PROPIETARIO:** toda documentación generada durante este trabajo debe quedar en este repositorio. Runbooks, mantenimiento, inventario, limitaciones y validaciones persistentes se conservan en issue/PR o documentación versionada según su valor permanente. Cambios canónicos mediante issue, rama y PR, sin escritura directa en main.

El servidor conserva solamente configuración, scripts, agentes, unidades, locks, caché, estado/recovery y credenciales fuera del repositorio necesarios para la ejecución. Una referencia documental local solo se justifica si el software la necesita y debe declarar que **GitHub prevalece**. No publicar secretos ni rutas de credenciales.

La autoridad vigente es [G-02](../decisiones/G-02-orquestacion-qwen-codex-chatgpt.md), el [perfil PROGRAMADOR-LINUX](programador-linux.md) y la issue completa con comentarios. Esta página no duplica su contrato ni levanta sus bloqueos.

## Contraste del RUNBOOK local

El RUNBOOK inspeccionado tenía 88 líneas y fecha declarada 17/10/2026. Es una fuente histórica auxiliar, no autoridad.

| Contenido local | Tratamiento |
|---|---|
| Identidad QWEN-LINUX y nuevas ramas qwen/ | **SUPERSEDED** por G-02 / PR #30; usar el perfil vigente. |
| Activación tras elegir modelo y pasar una prueba | **SUPERSEDED como procedimiento suficiente**: #28 prohíbe timer, desarrollo real y operación desatendida mientras sigan sus bloqueos. |
| Error Qwen 404 y ausencia de modelo gratuito | Evidencia histórica declarada; no se comprobó disponibilidad actual en este ciclo. |
| Validaciones de sintaxis, locks, cola NO_WORK, aislamiento, calendario y CRM | Resultados históricos declarados por el RUNBOOK, no reejecutados ni certificados en este ciclo. |
| Evaluación Nemotron | Ya conservada en #28 / PR #29; no se duplica. |
| Inventario y mecanismo configure-model | Conservados abajo tras inspección; no autorizan ejecución. |

## Aislamiento multiproyecto obligatorio — criterio confirmado el 23/10/2026

**CONFIRMADO por el PROPIETARIO** en [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28#issuecomment-6372583456): el servidor Linux **no es dedicado a WHEREIS**. A la instancia de `PROGRAMADOR-LINUX` le corresponde operar **exclusivamente** `mundoinformaticacanaria/whereis`. La unidad de operación es **una instancia de runner por proyecto**. El runner de `mundoinformaticacanaria/crm-remisiones-veterinarias` es de otro proyecto, autónomo y ajeno a los contratos funcionales y gobernanza de WHEREIS.

**CRM intocable:** no cambiar, reiniciar ni detener repositorio, runner, agente, modelo, configuración, servicios/timers, locks, caché, estado ni recovery de CRM. Solo inspección técnica de lectura si es imprescindible para comprobar aislamiento, colisiones o recursos comunes. No usar scripts, tests ni decisiones CRM como si fueran de WHEREIS.

**Componentes compartidos permitidos:** herramientas globales como OpenCode, Git, GitHub CLI y Python, sin compartir las **configuraciones por instancia**. Priorizar HOME/XDG/configuración propia frente a alteraciones globales. Cualquier cambio global con posibilidad de impacto cruzado es **MATERIAL** y requiere aprobación específica; no lo ejecuta la actual autorización de reconciliación local. El aislamiento no obliga a desarrollar ahora un framework común ni a copiar indiscriminadamente runners.

### Matriz de validación previa a declarar WHEREIS preparado

| Superficie | Evidencia necesaria, pendiente de comprobación directa |
|---|---|
| Repo y selección de issues | Solo WHEREIS: checkout, remoto, política de labels, ejecutor autorizado y ramas `programador-linux/`; ninguna selección cruzada |
| Identidad/modelo/agente | `PROGRAMADOR-LINUX` estable; modelo seleccionable sin cambiar identidad, contrato, locks ni nombres de unidades; agente y protocolo model-neutral |
| Configuración y entorno | Instancia propia, variables específicas, directorios HOME/XDG y sesión/configuración OpenCode independientes |
| Estado, caché y recuperación | Rutas distintas por proyecto, incluidas sesiones, archivos temporales, estado, cache y recovery; sin sobrescritura cruzada |
| Locks y concurrencia | Locks únicos por instancia; un bloqueo/recovery de WHEREIS no detiene ni desbloquea otro proyecto |
| Servicios, timers y runtime | Nombres únicos de `systemd`, timers, `RuntimeDirectory`, entorno de unidades, procesos y puertos (si existieran), sin colisiones |
| Aislamiento de fallo | Un fallo o cambio de modelo de WHEREIS no afecta CRM ni compromete futuras instancias |
| Estado efectivo | Timer WHEREIS comprobado inactivo/deshabilitado mediante las unidades/planificadores aplicables; sin ejecución real ni desatendida |

La referencia histórica «CRM a `:15`, WHEREIS a `:45`» solo ayuda a evitar solapamientos si algún día se autoriza operar ambos; **no** implica un runner común ni habilita el timer de WHEREIS. Añadir un tercer proyecto debería requerir crear su instancia, no modificar las existentes salvo necesidad compartida real y autorización MATERIAL.

**PENDIENTE / NO VERIFICADO en servidor en este documento:** las propiedades anteriores son criterios de aceptación, **no resultados de una auditoría ya realizada**. Toda evidencia real debe registrarse de forma sanitizada en #28. No se introducen decisiones de CRM en la gobernanza de WHEREIS.

## Inventario operativo

Rutas relativas a HOME, sin revelar ubicaciones de credenciales:

| Componente | Ruta |
|---|---|
| Selector de modelo y configuración de instancia | `.config/whereis-programador/instance.env` |
| Registro de proveedor y permisos OpenCode | `.config/whereis-programador/xdg/opencode/opencode.json` |
| Agente | `.config/whereis-programador/xdg/opencode/agents/whereis-programador.md` |
| Entrada y lock | `.local/libexec/whereis-programador/github-review` |
| Evaluación de cola y publicación | `.local/libexec/whereis-programador/review.py` |
| Generador del registro de modelo | `.local/libexec/whereis-programador/configure-model` |
| Unidades preparadas | `.config/whereis-programador/systemd/whereis-programador-github-review.service` y `.timer` |
| Estado y recovery | `.local/state/whereis-programador` |
| Sesiones OpenCode | `.local/share/whereis-programador` |
| Caché | `.cache/whereis-programador` |

**CONFIRMADO por inspección:** configure-model lee MODEL de instance.env, separa proveedor/modelo por la primera barra y regenera el registro OpenCode. Solo acepta openrouter; otro proveedor exige revisión explícita. El registro referencia una variable de entorno de autenticación, no incorpora su valor. Esta inspección no constituye auditoría completa de ausencia de secretos.

## Estado observado y limitaciones

**CONFIRMADO el 19/10/2026:**
- instance.env conserva `MODEL=openrouter/qwen/qwen3.8-27b:free`.
- review.py reconoce QWEN-LINUX, exige ese ejecutor y ramas qwen/; también lo usa en títulos/cuerpos de PR y pruebas internas.
- `systemctl is-enabled whereis-programador-github-review.timer` devolvió `not-found`; `systemctl is-active` devolvió `inactive`. Se refiere a la unidad de sistema consultada, no a una auditoría de todos los mecanismos de programación.
- No se encontraron referencias textuales a RUNBOOK en los archivos de configuración y scripts inspeccionados, excluyendo instance.env de esa búsqueda. No hay dependencia operativa acreditada.

**PENDIENTE:** aplicar y validar la reconciliación local autorizada en #28. La identidad vigente en GitHub no demuestra que el servidor ya la implemente. Nemotron sigue siendo candidato aislado; no se seleccionó ni invocó en este ciclo.

**PENDIENTE:** validar el camino completo de programación/publicación/QA cuando exista una tarea real autorizada; no se ha probado aquí. Accesos, privilegios mínimos, QA, heartbeat, CI y demás bloqueos se siguen en #28, sin darlos por resueltos.

## Mantenimiento y recuperación

Antes de cambiar modelo, leer la issue y gobernanza vivas; mantener identidad lógica, rama de tarea y gates. Valorar cambios de proveedor, privacidad, coste, capacidades y riesgo conforme G-02. El mecanismo configure-model es una descripción técnica, no una orden de ejecutarlo ni autorización para activar un modelo.

Ante trabajo sucio, lock o estado interrumpido: inspeccionar y conservar evidencia sanitizada en GitHub; no borrar estado, resetear ni limpiar automáticamente. La recuperación concreta queda **PENDIENTE** de inspección del incidente.

**DEUDA REGISTRADA / PROPUESTA histórica no aprobada:** posible extracción compartida del runner con CRM. No realizarla por estética ni usar comandos del stack CRM como gates de WHEREIS. Un cambio de credenciales o identidad de sistema requiere su autorización correspondiente.

No instalar unidades, iniciar el agente, activar timer ni ejecutar issues reales desde este documento. Las instrucciones históricas de activación no sustituyen una autorización posterior explícita y la resolución de los gates.
