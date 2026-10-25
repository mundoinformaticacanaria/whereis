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
- Archivos de texto **añadidos, copiados, modificados o renombrados** del diff: existencia/lectura, contenido no vacío, codificación UTF-8 y marcadores de conflicto.
- Detección **heurística** de patrones de claves privadas y algunos tokens comunes en archivos de texto afectados; la salida **no revela valores ni rutas**.
- No inspecciona archivos borrados, binarios, contenido no modificado, historia Git completa, permisos reales ni código ejecutado.

## Límites y gates

El resultado `PASS` **no certifica ausencia de secretos** ni seguridad, integridad funcional, enlaces Markdown, validez semántica YAML/JSON, independencia QA, protección de ramas o cumplimiento de baselines. Es un preflight inicial, no un sustituto de análisis de seguridad ni de pruebas Android.

**Pruebas sintéticas locales del script:** caso limpio `PASS`; marcador de conflicto y patrón de token detectados como `FAIL`. Estas pruebas no son una ejecución GitHub Actions ni acreditan el HEAD de la PR. La revisión independiente debe ejecutar el script sobre un checkout del HEAD exacto y adjuntar evidencia.

**Pendiente de decisión operativa/verificación:** confirmar que cualquier ejecución automatizada futura no genere cargos (presupuesto 0 €), revisar el workflow propuesto cuando exista y comprobar checks sobre SHA real. No crear `.github/workflows` ni declarar required checks en esta PR. La configuración de ruleset/branch protection aprobada en #42 requiere acceso administrativo y pruebas propias; este script no la aplica.

**Exclusiones:** sin programación de WHEREIS, cambios en CRM, servidores, runners, timers Linux ni automatización de ChatGPT.
