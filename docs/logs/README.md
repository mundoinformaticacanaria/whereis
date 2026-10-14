# Política de heartbeat por rol

Los logs son histórico auxiliar y señal de actividad. Nunca son fuente de verdad ni autorizan trabajo.

## Rama recomendada

Mantener el histórico vivo en una rama separada, recomendada: `ops/logs`.

## Regla por ciclo/visita

Todo rol con fichero de log definido en el proyecto registra exactamente dos entradas por cada ciclo/visita a GitHub:

1. `INICIO`, antes de consultar `main`, cola, issues, PR o tareas;
2. `FIN`, al completar el ciclo, después de todas las operaciones GitHub.

## Formato

INICIO:

`DD/MM/YYYY HH:MM rol nombre INICIO`

FIN con actividad:

`DD/MM/YYYY HH:MM rol nombre FIN tareas_realizadas`

FIN sin actividad material:

`DD/MM/YYYY HH:MM rol nombre FIN NINGUNA`

## Zona horaria

**PENDIENTE DE PROYECTO**. Debe definirse explícitamente una única zona horaria operativa.

## Concurrencia

Antes de iniciar un ciclo:

1. releer exclusivamente el propio log;
2. comprobar si existe un `INICIO` sin `FIN` posterior;
3. si existe y no ha expirado, no solapar otro ciclo;
4. si ha expirado, conservarlo como evidencia y comenzar un nuevo ciclo sin fabricar `FIN` retroactivo.

Umbral recomendado de expiración: **30 minutos**, salvo decisión distinta del proyecto.

## Fallos de escritura

- un conflicto/concurrencia de escritura en GitHub debe resolverse antes de continuar;
- un bloqueo técnico externo a GitHub puede permitir continuar excepcionalmente si se ha verificado que no existe un `INICIO` reciente bloqueante;
- nunca fabricar heartbeats retroactivos.

## Retención

Recomendación: conservar las **100 entradas más recientes** por fichero, ordenadas de más reciente a más antiguo.

## Datos prohibidos

Nunca registrar secretos, credenciales, datos personales reales, información sensible de negocio ni contenido que no deba versionarse.

## Ficheros recomendados

- `docs/logs/tech-lead.log`
- `docs/logs/arquitecto.log`
- `docs/logs/funcional.log`
- `docs/logs/comercial.log`
- `docs/logs/qa.log`
- `docs/logs/devops.log`
- `docs/logs/programador-<identidad>.log`

Cada proyecto debe crear únicamente los logs de los roles/ejecutores realmente activos.
