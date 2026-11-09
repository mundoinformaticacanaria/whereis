# Evidencia del operador — 09/11/2026

**MATERIAL AUTORIZADA / APLICADO PARCIALMENTE / NO OPERATIVO.** Autorización #28, comentario 6507792703. Verificación posterior a instalación: 10:15:07 UTC (Atlantic/Canary +00:00). Autor: operador Codex; **no QA independiente**, no CI.

## Aplicación acreditada

- SSH efectivo con el usuario/HOME autorizados. Intervención TECH LEAD previa sobre #28 comprobada con FIN antes de mutar; no se crea un rol/log ficticio ni se ejecuta PROGRAMADOR.
- Respaldo exclusivamente WHEREIS: 10 archivos verificados por SHA-256 y permisos, bundle Git verificado y restauración en fixture independiente. Copias originales reverificadas al cierre; sin sobrescribir recovery.
- Checkout limpio `3722ca8bf6939fbcbd915af6b423209e74a00750` actualizado **solo fast-forward** a `main@3212773e2dba2246358cf9e7b8d4d2294ba27707`. Sin reset, clean, force, pérdida de ramas ni push a main. Fetch público sin reutilizar autenticación compartida.
- Fuente aplicada: commit `6f4236c3b9d41867e169f010209f696d6680dda6`, rama `codex/28-linux-isolation`. **13/13 archivos operativos instalados y reverificados** contra el candidato. `review.py` SHA-256 `50270a8265226e9a28ffca320bfd93b3889e1fc1d08bfd3622ef3975082fd313`.
- Entrada antigua sustituida; runner directo protegido antes de leer configuración/estado. Configuración de autenticación WHEREIS separada y referencia externa anterior retirada, sin leer/copiar/revocar credenciales compartidas. Los directorios propios se preparan vacíos: **no se ha emitido ni validado una credencial nueva**.
- Heartbeat adaptado en código y nueva huella adoptada después de las pruebas. Sin escrituras reales en logs del ejecutor inactivo. Política no convertida en autorización ni lock distribuido.
- Usuario, HOME y binario OpenCode compartido conservados. Selector actual exacto `openrouter/qwen/qwen3.8-27b:free`; Nemotron no seleccionado ni invocado.

## Resultados separados, sin sumar baterías

| Prueba | Resultado y límite |
|---|---|
| Unitarias y gates del runner | **36/36 PASS**, local y servidor. AST de definiciones, datos ficticios, sin importar/ejecutar la entrada del runner; no API real ni inferencia. Incluye SHA de política exacta con salto final, veto de baseline/CI, asignación, conflictos 409 simulados, FIN tardío y DST. |
| Sandbox instalado | **37/37 PASS**. Namespaces privados, UID/HOME, capacidades cero, NoNewPrivs, controles/repo RO, rutas excluidas, userns/sudo rechazados, sockets canario TCP/Unix/abstracto y PID canario del host ocultos, límites de ficheros/procesos efectivos. La comprobación de ruta de archivo host es ocultación de ruta, no lectura de secretos ni ensayo de un archivo CRM. |
| Runner completo sintético | `--self-test` **PASS dentro de bubblewrap**, sin cola real, publicación ni modelo. |
| OpenCode | v2.0.21; paths/config exit 0; **agente exacto = 1** tras readiness acotada. Metadatos solo en vista efímera propia, sin alterar estado/sesiones del host. |
| TLS sin autenticación | **8/8 PASS**: GitHub API, GitHub y OpenRouter accesibles vía relés fijos/8443; rechazo de certificado incorrecto (curl 60), dominio no autorizado, loopback no autorizado, privada y metadatos. No prueba Git/GH/OpenCode operativo, redirecciones reales o filtrado SNI por el relé. |
| Entradas negativas | Entrada anterior exit 78, runner directo rechazado por guard, `--scoped` fuera de límites rechazado, modo desconocido rechazado. Razones de rechazo comprobadas, no solo código de salida. |
| Concurrencia local | Segundo arranque rechazado con el lock propio ya ocupado, antes de iniciar sandbox. No demuestra concurrencia distribuida/heartbeat real. |
| Recuperación | Bundle y 10 copias verificados; restauración en fixture y reverificación posterior PASS. No ensayo de caída del host ni recuperación de trabajo real. |
| Servicios/timer | WHEREIS `not-found / inactive` en sistema y usuario antes y después; no instalación ni activación. Los scopes de validación son temporales. |

Límites reales leídos del cgroup: `memory.max=335544320`, `memory.swap.max=0`, `pids.max=48`, `cpu.max=25000 100000`. RLIMIT_FSIZE 16 MiB, core 0, NOFILE 128; tmpfs acotados. Rechazo real de archivo excesivo y de tareas adicionales. No se estresa RAM/CPU de la VM compartida ni se afirma capacidad para una tarea de desarrollo real.

## Fallos anteriores conservados

1. Conexión SSH perdida durante la primera transferencia; al recuperar acceso se comprobó que el candidato no existía. Se cambió a transferencia verificable desde la rama pública propia.
2. Generador inicial del candidato: `IndentationError` antes de escribir el runner; corregido conservando la indentación original, AST PASS posterior. Original operativo sin sustituir durante ese fallo.
3. Bubblewrap rechazó `--disable-userns` con `--unshare-all`; corregido usando namespaces explícitos, sin debilitar userns.
4. `debug agents` exit 0 con `[]`: falló el gate. Se probaron localización/metadata/registro explícito, sin considerar exit 0 como éxito. Los logs propios mostraron inicialización asíncrona; la espera acotada resolvió el descubrimiento manteniendo el agente original.
5. Puerto interno 443: `Permission denied` incluso con capacidades en la vista final. Se descartó esa vía; sin sysctl global, red del host ni capacidades adicionales en la implementación final.
6. Ensayo provisional 8443: objetivo remoto también cambiado por error a 8443, timeouts y un `ValueError` en el bucle negativo. Corregidos en el candidato; la versión final conecta los relés host únicamente a 443 y pasó TLS/rechazos antes de instalación.

Todos los gates del instalador pasaron antes de sustituir archivos operativos. Ningún fallo se presenta como PASS. No se han reejecutado ni sumado las 51/51, 38/38 o 74/74 históricas.

## Pendientes y responsable

- **PROPIETARIO:** emitir/consentir credenciales exclusivas WHEREIS de mínimo alcance, sin introducir secretos en chat/GitHub. GitHub: solo este repositorio y operaciones de contenido/PR/issues requeridas, lectura de checks/statuses; sin administración/bypass. Proveedor: clave independiente con límites apropiados, sin aprobar proveedor/gasto nuevo.
- **Operador / TECH LEAD:** resolver y revisar la compatibilidad del cliente Git/GH/OpenCode con egress restringido; revisar limitaciones TCP/SNI de destinos compartidos; preparar checkout escribible y recuperación persistente con cuota antes de una ejecución real. No ampliar la red ni fabricar una pasarela por conveniencia.
- **QA independiente:** revisar el HEAD exacto de la PR, reproducir pruebas y emitir APTO/DEFECTOS/BLOQUEADO. El autor no se autorrevisa; los resultados anteriores son evidencia de implementación.
- **TECH LEAD / roles del proyecto:** gates #24/#38/#41/#42, CI/enforcement, baselines, privilegios y autorización separada de piloto #90. Sin asignar PROGRAMADOR ni habilitar timers.

**CRM:** no modificaciones, reinicios, detenciones ni lectura de secretos. El árbol offline probado no alcanza las rutas/servicios del host ensayados. El mismo UID fuera de ese árbol conserva privilegios históricos; no se afirma aislamiento absoluto del usuario ni aprobación integral de seguridad. **PROGRAMADOR-LINUX continúa NO OPERATIVO para issues reales.**
