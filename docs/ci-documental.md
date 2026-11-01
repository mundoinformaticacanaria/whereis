# Preflight documental local — propuesta de fase inicial CI (#42)

**Estado:** PROPUESTA técnica para revisión; **no equivale a CI operativa, check verde ni protección de `main`**. Decisión material de alcance aprobada por el PROPIETARIO en [#42](https://github.com/mundoinformaticacanaria/whereis/issues/42). Ningún workflow, runner, proveedor o servicio se activa con esta PR.

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

**Integración y gates:** la PR separada #71 propone un workflow GitHub Actions con runner estándar de repositorio público (coste incremental 0 € según condiciones actuales), que debe ejecutar el **script confiable de `origin/main`** cuando exista y fallar cerrado en otros casos. Esta PR #46 no crea workflow ni ruleset. Verificar QA independiente del nuevo HEAD, checkout Git auténtico y checks correspondientes; no declarar verde a partir del run diagnóstico histórico [41297700331](https://github.com/mundoinformaticacanaria/whereis/actions/runs/41297700331), que probó un HEAD anterior. Protección/ruleset de `main` sigue pendiente de aplicación efectiva por operador autorizado #42. No marcar required checks inexistentes.

**Exclusiones:** sin programación de WHEREIS, cambios en CRM, servidores, runners, timers Linux ni automatización de ChatGPT.
