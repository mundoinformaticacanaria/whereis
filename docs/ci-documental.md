# Preflight documental local — propuesta de fase inicial CI (#42)

**Estado:** PROPUESTA técnica para revisión; **no equivale a CI operativa ni a check verde**. La rama `main` dispone del ruleset [#26574343](https://github.com/mundoinformaticacanaria/whereis/rules/26574343) activo y PR obligatoria, pero **no hay required status checks configurados ni rechazo negativo de enforcement demostrado**. Decisión material de alcance aprobada por el PROPIETARIO en [#42](https://github.com/mundoinformaticacanaria/whereis/issues/42). Ningún workflow, runner, proveedor o servicio se activa con esta PR.

## Ejecución reproducible sin red ni coste

Desde un checkout Git que contenga la rama base y el HEAD de la PR:

```sh
BASE=$(git merge-base origin/main HEAD)
python3 scripts/check-documentation.py "$BASE"
```

Requiere únicamente **Git y Python 3 estándar**, sin dependencias, secretos, acceso a red, nube ni instalaciones. Devuelve 0 al pasar, 1 al fallar, 2 si falta el argumento. No escribe en el repositorio.

## Cobertura exacta

- `git diff --check` del rango `BASE...HEAD`: errores de whitespace y marcadores de conflicto detectados por Git.
- Archivos **añadidos, copiados, modificados o renombrados**: lectura de los **blobs de HEAD** (`git show HEAD:<ruta>`, nunca working tree). Inspecciona todo contenido UTF-8 sin bytes NUL, incluso `config.env`, `config.env.local`, `.env`, `.env.*` y ficheros sin extensión como `credentials`; comprueba vacío, marcadores de conflicto y patrones de secretos. Las extensiones de texto conocidas exigen UTF-8 y rechazan bytes NUL; los demás binarios se omiten. No certifica todos los formatos ni todos los secretos.
- Detección **heurística** de patrones de claves privadas y algunos tokens comunes en archivos de texto afectados; la salida **no revela valores ni rutas**.
- No inspecciona archivos borrados, binarios, contenido no modificado, historia Git completa, permisos reales ni código ejecutado.

## Límites y gates

El resultado `PASS` **no certifica ausencia de secretos** ni seguridad, integridad funcional, enlaces Markdown, validez semántica YAML/JSON, independencia QA, protección de ramas o cumplimiento de baselines. Es un preflight inicial, no un sustituto de análisis de seguridad ni de pruebas Android.

**Corrección tras QA #73 (01/11/2026):** QA reprodujo un falso negativo del HEAD anterior `de1b816...`: `config.env` con token **ficticio** pasaba sin inspección, aunque `.env` fallaba correctamente. El código actual amplía el análisis a todos los blobs UTF-8 sin NUL, incluyendo `*.env`, `*.env.*` y textos sin extensión. **Pruebas sintéticas locales del nuevo blob:** 11/11 casos con resultados esperados (limpio PASS; token ficticio en `config.env`, `config.env.local`, `.env`, `credentials` y Markdown FAIL; marcador de conflicto, whitespace, UTF-8 inválido y texto vacío FAIL; binario con NUL omitido). `python3 -m py_compile` PASS. Los valores son **sintéticos**; no se usaron secretos reales. No equivalen a QA independiente ni a ejecución GitHub Actions sobre este nuevo SHA. QA debe repetir los negativos, incluyendo token en HEAD ocultado solo en working tree, y comprobar el HEAD exacto.

**Integración y gates — estado vigente 13/11/2026:** la PR separada [#71](https://github.com/mundoinformaticacanaria/whereis/pull/71) propone un workflow `pull_request_target` ejecutado desde base confiable; [QA #82](https://github.com/mundoinformaticacanaria/whereis/issues/82) mantiene **BLOQUEADO operativo** el HEAD `f759850f9b7dd58edc5be3ab9bd780afca3c4080` por ausencia de una ejecución real confiable de base y de acreditación del check. Esta PR #46 aporta **solo** el scanner local, no crea workflow ni ruleset. El scanner revisado conserva su blob `be3229d2f4d62531fbfe8fdf3ba4aac62b4146b9`; [QA #83](https://github.com/mundoinformaticacanaria/whereis/issues/83) emitió APTO DOCUMENTAL y 18/18 pruebas sintéticas para el HEAD histórico `7814d85dfd022a2c3ee177db0f6c982c43227296`. El [run diagnóstico 41302344437](https://github.com/mundoinformaticacanaria/whereis/actions/runs/41302344437) pertenece a un SHA todavía anterior `c3e99e34...` y **no** certifica este HEAD ni un check nativo requerido.

**Protección frente a validación real:** `main@3212773e2dba2246358cf9e7b8d4d2294ba27707` informa `protected=true` y el ruleset #26574343 `active` sobre `refs/heads/main`, sin bypass, con PR obligatoria, bloqueo de borrado/force-push y resolución de conversaciones, **0 aprobaciones nativas y 0 required status checks**. Su configuración **no** demuestra por sí misma rechazo negativo, CI del scanner, segregación efectiva de QA ni seguridad operativa. Nunca interpretar ausencia de checks como PASS ni declarar CI completa.

**Decisión posterior del PROPIETARIO:** en [#111](https://github.com/mundoinformaticacanaria/whereis/issues/111#issuecomment-6845425761) se aprobó **opción B: APLAZAR la integración de PR #46** para corregir esta guía y conciliar la rama con `main`. Si se produce nuevo HEAD, se exige **QA independiente nueva** de todo el diff y revisión TECH LEAD; después, un **nuevo expediente de autorización individual**. La opción A de [#102](https://github.com/mundoinformaticacanaria/whereis/issues/102) autorizó exclusivamente **preparación**, no merge. **NO MERGE de #46 ni #71**, no bypass, no simular checks, no relajar ruleset. Secuencia propuesta aún condicionada: scanner #46 autorizado individualmente → revisar por separado workflow #71 con QA de seguridad y autorización propia → ejecutar y atribuir comprobaciones reales de base antes de proponer un check required.

**Exclusiones:** sin programación de WHEREIS, cambios en CRM, servidores, runners, timers Linux ni automatización de ChatGPT.
