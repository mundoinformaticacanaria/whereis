# Propuesta de entrega de credenciales propias — #100 (NO OPERATIVA)

Estado: diseño para revisión; **no habilita `--run`, emisión de tokens, montajes reales, red ni PROGRAMADOR-LINUX**. Base de análisis: PR #94 y QA #151, HEAD anterior `5ff83121bafb21705f27243f3ad18b4a127a3138`.

## Límite de confianza y decisión pendiente

El modo offline de `sandbox.py` monta únicamente configuración no secreta y crea `GH_CONFIG_DIR` efímero; **no** presenta `gh/hosts.yml` ni `auth/provider.json`. `runner_support.py::invoke_engine` hereda `os.environ` y añade credenciales al subprocess; esto **no** demuestra segregación frente a código del mismo UID, subprocesos o un agente con acceso al namespace. Mantener bloqueada la entrada real hasta un diseño de identidad/ejecución segregado y aprobado.

### Contrato candidato (no implementado)

1. El operador autorizado prepara **dos archivos individuales** propios de WHEREIS fuera de todo HOME compartido, con identidad de proceso segregada, propietario verificado, `0600`, enlace único y ancestros no enlazados. Nunca copiar tokens a GitHub, argumentos, logs, variables del lanzador host o fixtures.
2. Antes de construir el namespace, abrir cada ruta mediante FDs de directorios fijados, `O_NOFOLLOW`, y comprobar `fstat` de propietario/tipo/modo/enlaces; abortar si falta cualquiera. Revalidar el objeto abierto, no solo el nombre. La validación actual de `engine.py` no equivale a un montaje seguro.
3. Solo una entrada real **separada** y aprobada podrá enlazar cada archivo como lectura individual al destino propio dentro del namespace; nunca montar directorios de autenticación, HOME, SSH, CRM, sockets del host ni configuraciones de otros proyectos. Los modos offline conservarán ausencia absoluta de secretos.
4. No pasar tokens por `--setenv` ni por `env=dict(os.environ)`. El proceso que consume secretos debe ser explícito y mínimo; los procesos hijo no autorizados no deben heredarlos. Un archivo `0600` **no protege contra otros procesos del mismo UID**; si la identidad no puede segregarse, elevar decisión material antes de cualquier activación.
5. GitHub: proponer una identidad restringida al repositorio WHEREIS, con permisos separados de lectura de issues/PR/contents/checks y escritura estricta de issues/PR/ramas propias/logs; sin Admin, settings, workflows, bypass u otros repositorios. Verificar modelo real de token, alcance, expiración y revocación **antes** de solicitar emisión al PROPIETARIO.
6. Mantener perfil Qwen sin llamada real ni selección de proveedor. No presentar credenciales hasta que #99 demuestre controles de egress que impidan desvíos por SNI, Host, redirecciones y destinos virtuales; #159 es solo estudio arquitectónico.

## Oráculos de QA futura (NO EJECUTADOS)

| Caso | Resultado exigido |
|---|---|
| Archivo ausente, JSON inválido, valor no textual, owner ajeno, 0644/0640, hardlink, symlink final/ancestral o swap de ancestro | Rechazo fail-closed, sin ejecución de motor |
| Archivo de otro proyecto, directorio de autenticación compartido o variable host con token ficticio | Rechazo/no visibilidad dentro del namespace |
| Offline probe/selftest/version/agents/tls-smoke con archivos ficticios presentes en host | Ningún secreto legible dentro del namespace ni en salida |
| Montaje individual autorizado con credenciales ficticias | Solo consumidor previsto puede leer; ningún proceso no autorizado ni mismo UID externo |
| Salida, stderr, heartbeat, recovery y fallo de subprocess | Ausencia de marcas ficticias; errores redactados |
| Cliente Git/GH/OpenCode y egress | Rechazo de destino/SNI/Host/redirect no aprobado; sin autenticación real |
| Bloqueo de `--run`, bypass antiguo, ausencia de cgroup o fallo de bind | Exit no cero, sin fallback fuera de sandbox |

**Gates:** pruebas reproducibles sobre SHA final, QA independiente de código y evidencias de proceso/UID, #99/#159, #24/#38/#41/#42, autorización individual de integración y posterior autorización separada de piloto. El presente documento **no** cierra #100 ni sustituye esas pruebas.
