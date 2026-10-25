# Política de heartbeat por rol — decisión material #38 (25/10/2026)

**Fuente:** [decisión expresa del PROPIETARIO en #38](https://github.com/mundoinformaticacanaria/whereis/issues/38#issuecomment-6395402627). La política documental solo entra en vigor como contrato canónico al integrar la PR correspondiente en `main`; la existencia de la política **no demuestra** que rama, logs o mecanismos de coordinación estén implantados.

## Alcance y almacenamiento

- Heartbeat = **observabilidad y coordinación por issue**, no autorización de trabajo ni exclusión mutua atómica.
- Rama separada: `ops/logs`; fichero por rol/ejecutor realmente activo: `docs/logs/<rol>.log` (por ejemplo `docs/logs/tech-lead.log`). No crear índice global adicional por issue.
- Cada intervención **sobre una issue** registra `INICIO` y `FIN` asociados al mismo ID único de intervención, con número de issue, rol y resultado breve. Conservar **100 entradas más recientes por fichero**; no fabricar entradas, reescribir historia ni registrar secretos/datos personales.
- **Existencia verificada en GitHub:** rama `ops/logs` y ficheros `docs/logs/tech-lead.log`, `qa.log`, `funcional.log` y `arquitecto.log` creados y leídos, según evidencias de #38. **PENDIENTES:** permisos/segregación operativa, concurrencia real, retención, validación integral e integración de esta política en `main`. TECH LEAD coordina sin escribir documentos canónicos directamente en `main`.

## Formato normativo

```text
YYYY-MM-DDTHH:mm:ssZ [Atlantic/Canary YYYY-MM-DDTHH:mm:ss±HH:MM] ROL #<issue> intervencion=<id-unico> INICIO
YYYY-MM-DDTHH:mm:ssZ [Atlantic/Canary YYYY-MM-DDTHH:mm:ss±HH:MM] ROL #<issue> intervencion=<mismo-id> FIN <resultado-breve|NINGUNA|BLOQUEADO>
```

- **UTC** es la referencia temporal; la hora local **Atlantic/Canary** aparece entre corchetes, con zona IANA explícita y offset correcto de invierno/verano. Ambas horas tienen precisión de segundos y corresponden al mismo instante.
- `<id-unico>` identifica inequívocamente la intervención; no reutilizarlo para otra ejecución, incluso del mismo rol/issue.
- Un `FIN` tardío solo cierra el `INICIO` con su **mismo** ID; no cierra otro ciclo. Indicar resultado real y no declarar éxito si una escritura falla.
- Una visita que aborde varias issues usa intervenciones diferenciadas por issue; no inventar un número de issue para un trabajo inexistente.

## Labels de rol y triage

Las labels de rol son `PROPIETARIO`, `FUNCIONAL`, `TECH LEAD`, `ARQUITECTO`, `PROGRAMADOR`, `QA`.

- **Una label de rol** = siguiente responsable único.
- **Cero labels de rol** = responsabilidad de TECH LEAD.
- **Dos o más labels de rol** = error de enrutamiento: **solo TECH LEAD** puede inspeccionar/abordar la issue para resolverlo y dejar un único responsable; otros roles **no** ejecutan trabajo sustantivo hasta la corrección. No inferir autorización de ninguna de las labels en conflicto.

## Coordinación por issue y concurrencia

1. Antes de abordar una issue, leer **el log del rol responsable** en `ops/logs` y localizar la última intervención de **esa issue**. No usar logs de otro rol ni un índice global duplicado.
2. Si hay `INICIO` sin `FIN` del mismo ID y su antigüedad es **menor de 30 minutos** desde el instante UTC de `INICIO`, no solapar trabajo sobre esa issue.
3. Si existe `FIN` emparejado, se puede iniciar una nueva intervención **inmediatamente**, incluso antes de 30 minutos.
4. A los **30 minutos exactos o más** desde `INICIO` sin `FIN`, se considera bloqueada la intervención anterior a efectos de coordinación y se puede retomar con **nuevo** ID, sin `FIN` retroactivo.
5. Procurar intervenciones cohesionadas y acotadas de **menos de 30 minutos**, sin fragmentación artificial; sobrepasar la ventana no renueva exclusividad.
6. Esta comprobación no constituye lock atómico: antes de cualquier mutación verificar de nuevo las precondiciones de la superficie y el HEAD/sha correspondiente; evitar escrituras inseguras ante concurrencia no resuelta.

## Escritura, fallos y automatización

- Usar control optimista de versión/SHA para escribir en el fichero de log; ante conflicto releer el contenido más reciente y reintentar conciliando sin borrar entradas ajenas. No hacer escrituras paralelas sobre el mismo fichero.
- Si la lectura/escritura/API/permisos fallan o el estado es incierto, **no fabricar heartbeat** ni declarar persistencia. Informar el fallo cuando sea posible. No realizar mutaciones inseguras sobre la misma superficie sin verificación suficiente; otras inspecciones o tareas seguras pueden continuar.
- **La automatización horaria TECH LEAD de ChatGPT nunca se desactiva, pausa, elimina ni reprograma por fallos de GitHub, logs, ausencia de tareas o bloqueos.** Solo una petición nueva y directa del PROPIETARIO puede autorizar cambiarla.
- Esta automatización de ChatGPT **no es** el timer Linux de PROGRAMADOR: los timers Linux siguen desactivados hasta autorización independiente. Ninguna regla de heartbeat autoriza PROGRAMADOR, código real, servidores, CRM, gasto, proveedores ni baseline.

## Validación pendiente (no ejecutada)

Casos exigidos antes de declarar operatividad: UTC y Atlantic/Canary en invierno/verano (incluido cambio DST); FIN inmediato; INICIO abierto a **29:59** (bloquea) y **30:00** (permite retomar); FIN tardío asociado solo a su ID; dos labels de rol; dos instancias del mismo rol sobre una issue; escrituras concurrentes, conflictos de SHA y fallo de API. Registrar resultados reales y evidencias sanitizadas en #38/#28; no atribuir pruebas no ejecutadas.
