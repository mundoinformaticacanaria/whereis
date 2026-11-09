# Protocolo seguro de verificación de `main` — #42

- **Fecha de la fotografía de entrada:** 09/11/2026.
- **Clasificación:** MATERIAL, procedimiento de validación autorizado expresamente por el PROPIETARIO en [#42](https://github.com/mundoinformaticacanaria/whereis/issues/42#issuecomment-6736625765).
- **Estado:** PROPUESTA DOCUMENTAL para QA independiente; no equivale a resultado de pruebas de enforcement ni autoriza integración.
- **Ámbito:** exclusivamente `mundoinformaticacanaria/whereis`; no tocar CRM, servidor Linux, ramas ajenas, configuración de protección, cuentas o automatización.
- **Regla primordial:** ninguna prueba de este procedimiento envía a `main` un push real, force-push, borrado, bypass, cambio de settings o llamada de escritura potencialmente peligrosa. Si una prueba necesita esa capacidad, **detener y solicitar aprobación material específica**.

## 1. Lecturas permitidas y captura reproducible

Estas operaciones son **GET de solo lectura**. El operador debe registrar fecha/hora UTC y zona Atlantic/Canary, URL/endpoint exacto, respuesta **sanitizada** y SHA observado. Un error 403/401 no es prueba de regla activa.

1. **Rama y SHA:** `GET /repos/mundoinformaticacanaria/whereis/branches/main`: recoger `commit.sha` y `protected`, sin inferir de ellos el rechazo real de escritura.
2. **Rulesets:** `GET /repos/mundoinformaticacanaria/whereis/rulesets` y `GET /repos/mundoinformaticacanaria/whereis/rulesets/26574343`: leer `enforcement`, `target`, `conditions.ref_name.include/exclude`, `bypass_actors` y las reglas/parametrización; nunca cambiar la regla.
3. **PR y ejecución:** para cada HEAD que vaya a revisarse, leer metadatos de PR, compare/diff, checks, statuses y workflow runs **del SHA exacto**. No derivar `CI verde` de `0 checks`, de una prueba sintética o de un run antiguo.
4. **Revisión segregada:** leer issue hija de QA y su dictamen de HEAD exacto; comprobar independencia lógica de autor/revisor y correspondencia temporal. Una sola cuenta GitHub no acredita por sí sola aprobadores nativos distintos.
5. **Workflow y escáner:** comparar el contenido de `.github/workflows/**` y `scripts/check-documentation.py` en la base de confianza vs PR; verificar si un atacante podría alterar el YAML o la fuente de checks. La mera presencia de workflow no acredita ejecución ni integridad.

Al registrar resultados, suprimir tokens, cookies, direcciones privadas o datos personales. Conservar enlaces GitHub y hash verificable; no copiar credenciales en logs.

## 2. Matriz de evidencia y límites

| Control | Inspección inocua posible | Evidencia actual (09/11/2026) | Qué falta para afirmarlo operativo |
|---|---|---|---|
| Solo `main` | GET ruleset: `refs/heads/main`, `exclude=[]` | **CONFIGURACIÓN CONFIRMADA** | Rechazo real para ref protegida, no ensayado |
| Requerir PR | GET `rules[].type=pull_request` | **CONFIGURACIÓN CONFIRMADA**, `required_approving_review_count=0` | Rechazo real de push directo; no probarlo sobre `main` |
| Impedir force-push | GET `non_fast_forward` | **CONFIGURACIÓN CONFIRMADA** | Rechazo real de operación; no probar sobre `main` |
| Impedir borrado | GET `deletion` | **CONFIGURACIÓN CONFIRMADA** | Rechazo real; nunca enviar una solicitud de borrado de `main` |
| Sin bypass permanente | GET `bypass_actors=[]` y `current_user_can_bypass=never` | **CONFIGURACIÓN CONFIRMADA** | No se ha ensayado ningún actor/permisos en operación |
| Conversaciones resueltas | GET `required_review_thread_resolution=true` | **CONFIGURACIÓN CONFIRMADA** | Demostrar rechazo de merge con conversación no resuelta sin mutar `main` |
| QA independiente | Leer dictamen del rol QA y HEAD | **PROCESO DOCUMENTAL EXISTE** | Garantía operativa segregada para cambios sensibles; `0` aprobaciones nativas no la demuestra |
| CI obligatoria | GET reglas de checks/statuses, commits y runs | **NO EXISTE required check en ruleset** | Workflow confiable, run real atribuible al SHA correcto y regla requerida aprobada |
| CI por PR no falsificable | Inspeccionar workflow propuesto, privilegios, base confiable | **PR #71 DRAFT / QA #82 BLOQUEADO operativo** | Ensayo real tras bootstrap seguro, amenaza de YAML no-op y atribución de contextos |

**No hay prueba real de enforcement en `main`** en esta fase. La configuración es condición necesaria, no prueba suficiente. Una ejecución de `git push --dry-run`, si se autorizara en otro entorno, tampoco demuestra necesariamente rechazo remoto real: no elevar su resultado a enforcement probado.

## 3. Métodos no destructivos y pruebas separadas

### Nivel A — lectura del repositorio real (autorizado aquí)
Recoger tabla anterior para el SHA/fecha actual; contrastar coherencia de configuración y reportar por separado `CONFIRMADO (configuración)`, `NO DEMOSTRADO (aplicación)`, `BLOQUEADO (permiso/evidencia)`. Ante respuesta inconsistente, registrar y detener nuevas conclusiones. No ejecutar HTTP POST/PATCH/PUT/DELETE contra settings ni refs.

### Nivel B — simulación local (puede proponerse, no equiparar a GitHub)
Con repositorios Git **temporales y ficticios fuera de WHEREIS** se pueden construir tests de comportamiento del escáner, exclusión de archivos y escenarios de conflicto. Verificar ausencia de efectos externos, sin credenciales reales; las pruebas del árbol local no prueban el motor de reglas de GitHub ni seguridad de un runner real. Publicar comandos y exit codes solo si se ejecutan realmente.

### Nivel C — eventual prueba concluyente
Solo tras **nueva autorización del PROPIETARIO** sobre alternativa concreta: usar un repositorio o rama de ensayo totalmente aislados, con identidad y permisos propios y reversión planificada. Antes de cualquier prueba, comprobar qué reglas aplican a ese entorno; no transferir una conclusión del repositorio de ensayo a `main`. Una prueba que pudiera modificar `main` si falla el enforcement continúa **prohibida** por la decisión #42; ni cuenta administrativa ni consentimiento genérico la vuelven admisible.

## 4. Secuencia de gates para PR #46 / #71 y futuras PR

1. **#46 escáner offline:** QA #83 acreditó `APTO DOCUMENTAL` en HEAD `7814d85dfd022a2c3ee177db0f6c982c43227296`; comprobar HEAD actual y controles aplicables antes de cualquier integración. Sus 18/18 pruebas sintéticas no son una ejecución de CI del HEAD. No afirmar que el scanner está desplegado antes del merge.
2. **#71 workflow:** QA #82 `BLOQUEADO` operativo para HEAD `f759850f9b7dd58edc5be3ab9bd780afca3c4080`; `pull_request_target` debe ser evaluado sin ejecutar el contenido no confiable de la PR con permisos privilegiados, con workflow desde base confiable. No integrar por el hecho de que QA sintética pase.
3. **Run real posterior:** solo cuando el workflow legítimo exista y esté autorizado, obtener para una PR nueva una ejecución nativa y probar el vínculo exacto entre evento, `head SHA`/merge ref, check y workflow de base. No marcar `required` un check inexistente o cuya procedencia no esté demostrada.
4. **Revisión de cambios sensibles:** establecer una garantía verificable para `.github/workflows/**` y `scripts/check-documentation.py`, teniendo presente que los roles independientes pueden usar una identidad GitHub compartida. No fingir aprobaciones de usuarios distintos ni instalar un bypass para suplirlas.
5. **Cierre del gate:** registrar en #42 el dictamen QA independiente del protocolo, evidencia observable por control y los límites; las condiciones no verificadas mantienen #42/28 abiertos. Ninguna pieza autoriza programación de producto por sí sola.

## 5. QA del protocolo (sin pruebas peligrosas)

QA debe comprobar contra `main`, #42 y el SHA exacto de la PR que: (a) distingue configuración vs prueba real; (b) no contiene pasos mutadores para `main`, ni siquiera tentativas de rechazo; (c) incluye controles PR/force/borrado/bypass/conversaciones/QA/checks y origen confiable del workflow; (d) documenta fallos de permisos y recuperación sin inventar evidencias; y (e) sus afirmaciones de fecha, SHA y estado son fieles. Emitir `APTO DOCUMENTAL`, `DEFECTOS` o `BLOQUEADO`; un HEAD posterior requiere nueva revisión independiente.

**No realizado:** pruebas negativas operativas, configuración, revisión nativa independiente, CI real, cambios de `main`, servidor, CRM, gasto o timers Linux. El eventual piloto de programación [#90](https://github.com/mundoinformaticacanaria/whereis/issues/90) sigue condicionado a #42/#28/#24/#41 y a baseline/stack autorizado.
