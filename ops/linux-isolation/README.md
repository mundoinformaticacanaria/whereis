# Aislamiento WHEREIS — #28

Implementación MATERIAL acotada autorizada por el PROPIETARIO en [#6507792703](https://github.com/mundoinformaticacanaria/whereis/issues/28#issuecomment-6507792703). Estos archivos son infraestructura del operador, no código Android ni una asignación PROGRAMADOR. `main` y la issue completa prevalecen.

## Frontera implementada

`github-review` sustituye la entrada anterior; `review.py` exige el guard antes de acceder a configuración, GitHub, modelo o estado. El guard comprueba namespaces, UID/HOME, NoNewPrivs y capacidades. El lanzador no tiene fallback fuera del sandbox. **La entrada real permanece BLOQUEADA expresamente.** Los modos disponibles son exclusivamente diagnósticos offline y un smoke TLS sin autenticación.

Se conserva usuario/HOME e instalación OpenCode. Bubblewrap proyecta solamente binarios en lectura, checkout WHEREIS en lectura, controles propios en lectura y configuración WHEREIS protegida. HOME efectivo es una vista privada; estado/metadatos/caché/tmp son efímeros y acotados. No se montan HOME completo, configuración compartida, credenciales compartidas, CRM, buses, sysfs, sockets ni procesos del host. No existe `--share-net` ni una pasarela propia.

Cada validación usa un scope temporal exclusivo, nunca una unidad de servicio/timer instalada: RAM 320 MiB, swap 0, CPU 25 %, 48 tareas; archivo máximo 16 MiB, core 0, 128 descriptores. HOME tmpfs 96 MiB, tmp 32 MiB, shm 8 MiB y workspace diagnóstico 16 MiB. El lock único impide validaciones simultáneas desde la entrada normal. No se hace una prueba destructiva de agotamiento de RAM/CPU en la VM compartida.

OpenCode mantiene JSON/agente protegidos y metadatos escribibles propios. `opencode_check.py` espera de forma acotada la carga asíncrona y exige exactamente `whereis-programador`; un comando exit 0 con lista vacía se considera NO preparado.

## Red y motores

Los relés estándar systemd fijan una IP pública por destino (`api.github.com`, `github.com`, `openrouter.ai`). Se rechazan respuestas DNS privadas, locales, especiales, multicast o mixtas; no se vuelve a resolver el destino durante la vida del relé. Dentro del namespace se usan listeners privados 8443 sin capacidades adicionales. El smoke usa `curl --connect-to` conservando hostname/SNI y validación TLS; no usa credenciales ni endpoints de inferencia. No sigue redirecciones ni habilita destinos nuevos.

**PENDIENTE:** compatibilidad real de Git/GitHub CLI/OpenCode con estos relés; 443 no está disponible en la vista final con userns deshabilitados. No abrir red del host, elevar capacidades ni reemplazar por un proxy propio para resolverlo. El smoke TLS no es prueba del cliente operativo ni de autorización por repositorio.

Los relés son TCP: la prueba acredita TLS del cliente, no inspección de SNI/HTTP por el relé ni segregación de virtual hosts que compartan una IP pública. Esa limitación debe evaluarse en QA de conectividad antes de operación; no afirmar una allowlist de URLs ni protección universal frente a exfiltración por un destino permitido.

`MODEL` y perfiles declarativos seleccionan motores; el registro no contiene secretos. Qwen vigente se conserva; Nemotron no se selecciona ni prueba. Otros perfiles se prueban solo con fixtures `example.invalid`; eso no acredita adaptadores ni aprueba proveedores. La autenticación de proveedor se carga como JSON privado propio, sin ejecutar un archivo shell ni consultar la autenticación compartida. GitHub apunta a un directorio exclusivo vacío; faltan credenciales propias de privilegios mínimos y su comprobación efectiva.

## Heartbeat y recuperación

`heartbeat.py` implementa ID por issue, UTC/Canary, umbral 29:59/30:00, FIN inmediato/tardío por mismo ID, retención 100 y conflictos SHA. El transporte usa `ops/logs` y no publica nada en las pruebas. No crea un log de un ejecutor todavía inactivo. Un fallo de observabilidad no fabrica éxito ni convierte el heartbeat en autorización o lock atómico.

La adaptación conserva los vetos de baseline, CI, asignación y QA. Los documentos Git se leen con bytes completos, incluido salto final; la nueva huella se adopta solamente después de pruebas del comportamiento, no como sustituto de la implementación.

`install_candidate.py` comprueba copias e invariantes antes y después de todas las pruebas, adquiere lock y escribe una entrada bloqueada antes de sustituir archivos. Si una aplicación queda incompleta, conserva el bloqueo; no restaura automáticamente una entrada insegura. El respaldo privado previo contiene 10 archivos verificados y bundle Git. La restauración se ensaya en un directorio independiente; no se pierde ni reescribe recovery existente. Recuperación de una ejecución real interrumpida con checkout escribible sigue PENDIENTE.

## Validación reproducible

```sh
python3 -m unittest discover -s ops/linux-isolation -p 'test_*.py' -q
python3 ops/linux-isolation/sandbox.py --offline probe
python3 ops/linux-isolation/sandbox.py --offline selftest
python3 ops/linux-isolation/sandbox.py --offline agents
python3 ops/linux-isolation/sandbox.py --offline tls-smoke
```

Los modos de integración requieren las rutas verificadas de `codex-dev`; las pruebas unitarias son independientes y usan datos ficticios. `review.py` nunca se importa para correr tests: los gates se extraen mediante AST con I/O simulado. No ejecutar `install_candidate.py` por rutina; exige el punto de recuperación exacto y la autorización viva #28.

## Gates que no cierra esta implementación

Credenciales/privilegios mínimos; cliente de red completo; checkout escribible y recuperación real con límites; QA independiente del HEAD; CI/enforcement #42; heartbeat concurrente real #38; baselines y seguridad #24/#41; autorización separada del primer piloto #90. No inferencia, issues reales, servicios/timers, Android ni operación desatendida.

La evidencia de no acceso se refiere al árbol confinado probado. El mismo UID fuera del sandbox conserva privilegios históricos del host; esta intervención no cambia sudo, AppArmor, cuentas ni recursos compartidos. Las copias históricas son recuperación privada, no entradas operativas autorizadas. No se presenta independencia QA ni aislamiento universal frente a un operador privilegiado del host.
