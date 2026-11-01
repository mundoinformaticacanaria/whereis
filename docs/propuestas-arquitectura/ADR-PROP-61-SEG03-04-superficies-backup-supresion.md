# ADR-PROP-61 — SEG-03/04: superficies de datos, backups, revocación y supresión

- **Estado:** `PROPUESTA / PENDIENTE`. **Clasificación:** MATERIAL, estudio documental técnico, **no dictamen jurídico ni baseline aprobado**.
- **Issue asignada:** [#61](https://github.com/mundoinformaticacanaria/whereis/issues/61), hija de [#41 SEG-03/04](https://github.com/mundoinformaticacanaria/whereis/issues/41). Complementa la [matriz TECH LEAD de #41](https://github.com/mundoinformaticacanaria/whereis/issues/41#issuecomment-6509996398) y la revisión funcional [#60](https://github.com/mundoinformaticacanaria/whereis/issues/60).
- **Contratos relacionados:** [#8 / PR #34](https://github.com/mundoinformaticacanaria/whereis/pull/34) (identidad/reinstalación), [#22 / PR #35](https://github.com/mundoinformaticacanaria/whereis/pull/35) (consulta), [#24 SEG-01/02](https://github.com/mundoinformaticacanaria/whereis/issues/24), [#52 / PR #55](https://github.com/mundoinformaticacanaria/whereis/pull/55) (señalización/terceros), [PR #50](https://github.com/mundoinformaticacanaria/whereis/pull/50) y [PR #45](https://github.com/mundoinformaticacanaria/whereis/pull/45). **No se duplican** las comparativas de proveedores.
- **Autoridad CONFIRMADA:** PROPIETARIO mantiene uso personal/familiar en España, consulta remota esencial (sin SLA), coste incremental de operación 0 €, ubicaciones, identidades y autorizaciones funcionales **persistentes sólo en teléfonos**; L-02b/c/d y P-52a/b/c/d **autorizan estudio, no adopción de servicios ni retención real externa**.
- **Evidencias:** lectura de contratos GitHub y documentación técnica oficial Android/Firebase. **Sin** código de producto, acceso a dispositivos, pruebas de backup, capturas, tráfico de terceros, llamadas a APIs, licencias elegidas, servidor, credenciales, inferencia ni coste observado. Todos los escenarios de prueba propuestos aquí están **NO EJECUTADOS**.

## 1. Modelo y límite de confianza

```text
TELEFONO A / EMISOR                    TRANSPORTE HIPOTÉTICO                 TELEFONO B / CONSULTANTE
Identidad y claves locales            IP, tokens, IDs técnicos              Su propia identidad y claves
Inbox de vinculación D-09             Message IDs/TTL/tópicos                Vínculos locales/alias
Autoridad A→B y revisiones            Proveedor NO elegido                   Última ubicación legítima por A
Bloqueos / revocación local        -- solo aviso opaco -->               Timestamp/precisión/dirección
Captura transitoria en memoria     <-- respuesta autenticada --          Registro de solicitud local mínimo
  └─ gate final de liberación
No historial automático de posiciones; ninguna autorización o ubicación persistente fuera de A/B
```

**Límite fundamental:** que A revoque el permiso o desinstale la aplicación **no hace desaparecer los bytes ya entregados y almacenados en B**, especialmente cuando B está offline. Que B los borre localmente tampoco acredita supresión de copias previas del SO, dispositivo rooteado, screenshots, exportaciones o registros ajenos. Proponer UX de solicitud de supresión remota como **best effort con acuse firmado**, nunca «borrado garantizado»; la facultad de exigirlo, la transparencia y el posible plazo requieren FUNCIONAL/#60 y decisión jurídica/humana #41.

## 2. Inventario de superficies, ciclo de vida y amenazas

| Categoría / responsable local | Dónde existe / cuándo se crea | Riesgo de copia o exposición | Mecanismo técnico PROPUESTO, NO IMPLEMENTADO | Gate |
|---|---|---|---|---|
| **ID de instalación, clave privada, prueba de posesión** (A y B) | Estado privado local; creación por instalación | Restore cloud/D2D/OEM, clonado de preferencias/BD, claves inaccesibles, copia del QR público | Generar ID nuevo si falta prueba no restaurable; clave no exportable en Android Keystore como candidato; material de instalación fuera de backup; QR sin secreto | D-04/SEG-02, probar reinstalación limpia y restore |
| **Permiso A→B, revisión, bloqueo y tombstone** (A) | BD local de A tras autorización explícita | Restore revierte revocación; replay de grant antiguo; borrado del tombstone reabre permiso | Persistencia transaccional de estado y revisión monotónica por relación; negar al liberar si permiso no es verificable; versión/epoch invalida respuestas anteriores; nunca restaurar permisos al reinstalar | SEG-01/02 y retención legal de tombstones PENDIENTE |
| **Lista de conocidos, alias, avatar/color, vínculos vistos** (A/B) | BD/preferences locales, UI/galería | Cache imágenes, thumbnail, backups, archivos compartidos, índices o miniaturas OEM | Copias internas bajo control de app cuando correspondan; borrar referencia + ficheros derivados; controlar URI grants y evitar exponer alias en avisos terceros | D-09/D-10/D-11, revisar UX #60 |
| **Solicitudes, rechazos, acuses** (A/B) | Inbox en A, outbox/estado en B | Notificación antes del inbox, logs, repetición, retención después de 24 h | Guardar solicitud D-09 local sólo mientras sea necesaria; acuse firmado sólo después de persistencia real; dedup por requestID, no reiniciar 24 h; definir limpieza de resultados tras periodo y preservación mínima anti-replay sin historial innecesario | D-09, plazo de conservación PENDIENTE |
| **Captura de ubicación, precisión y hora** (A) | Memoria durante consulta autorizada, objetos Location, buffers | Buffer de red, archivo temporal, logs/crash, screenshot, volcado de memoria | No persistir historial en A por defecto; no incluir coordenadas en push, error ni logs; limpiar buffers y no reproducir respuesta una vez cerrada; ubicación nueva con timestamp del sensor | D-01/02/12; RAM no ofrece borrado criptográfico garantizado |
| **Última ubicación legítima de A en B** (B) | Al aceptar respuesta nueva y legítima | BD local, copia cloud/D2D, widgets/notificaciones, cache de mapa, posición residual tras bloqueo | Una sola muestra por A con fecha real; escritura atómica condicionada a vínculo/revisión y solicitud activa; tras borrar, eliminar registro, derivados y claves asociadas; no revivir con respuesta tardía | D-06/D-10, duración legal **NO APROBADA** |
| **Dirección postal / geocodificación** (B, si disponible) | Resultado opcional de D-13, caché local | Filtra coordenadas si proveedor externo; caché inversa retiene precisión | Tratar dirección y coordenada como dato de ubicación igualmente sensible; no petición externa sin autorización expresa; caché privada con supresión ligada a ubicación | D-13, SDK/proveedor NO ELEGIDO |
| **Mapa / teselas / recursos offline** (B) | Datos cartográficos genéricos, caché de visualización | Tiles consultados pueden revelar área; mapa/render de terceros produce telemetría | Distinguir datos de mapa públicos de coordenadas y consulta del usuario; evitar marcadores/lat-lon en rutas, cachés, reportes y URL externos; al borrar posición purgar overlays y snapshots locales | SEG-07, fuentes/licencias/costes PENDIENTES |
| **Notificación local de A** (A, D-12) | Sólo si procesa intento autenticado, ubicación sistema apagada, sujeto a permisos | Alias/ID visible en pantalla bloqueada, historial de notificaciones y listener, capturas, logs | Minimizar contenido visible en lockscreen; no coordenadas; limitar por solicitante/24h; controlar privacidad/canal, cancelación local posible pero no retirada de notificación ya leída | UX exacta por FUNCIONAL, permisos Android |
| **Clipboard, shares, screenshots, teclado, accesibilidad** (ambos) | Copiar ID/alias, ficha y QR, OS/App terceros | Extrae información fuera del sandbox; capturas o portapapeles de otros | No copiar secretos ni autoexportar coordenadas; limpiar/evitar clipboard de datos sensibles; considerar medidas de pantalla sensible conforme política Android, sin prometer defensa frente a fotografía física/OEM | Política UX y accesibilidad a revisar |
| **Logs, crash/reportes, ficheros temporales y métricas** (ambos) | Errores y trazas de la app/SO; SDK si se eligiera | Lat/lon, requestId correlacionable, ID, token, estados de relación, stack trace persistente | Logging allowlist, redacción de coordenadas, tokens y IDs completos; no activación de SDK de analítica/crash externo por defecto; inventariar temporales, cachés, backups y eliminación | SEG-03/04, plazos no aprobados |
| **Token FCM / Firebase Installation ID / tópico ntfy / IP** (terceros HIPOTÉTICOS) | Registro señalización, envío/recepción, red | Identificador técnico persistente, correlación, logs IP/tópicos, metadata en servidores, transferencias | Sólo propuesta: avisos opacos, minimización, cifrado de payload, revocación/rotación de tokens y procedimiento de baja condicionado al proveedor. **No** equiparar `Cache: no` a purga de logs | L-02b/P-52a permitido **estudiar**, no enviar/adoptar; coste 0 no demostrado |

**Distinción de retención:** «solicitud D-09 caduca en 24 h» no implica eliminación automática de cualquier evidencia de bloqueo/abuso; tampoco autoriza conservar indefinidamente los eventos. Proponer y aprobar separadamente plazos mínimos legales y técnicos por categoría y actor. No inventar duraciones. Controles de minimización de logs no suprimen registros de sistema/proveedores fuera del control de la app.

## 3. Exclusiones de backup y prueba de no resurrección

1. **Android Auto Backup puede estar habilitado por defecto** para apps con target API 23+; las reglas de exclusión dependen de versión del SO y `targetSdk`. [Documentación oficial Android](https://developer.android.com/identity/data/autobackup).
2. **No confiar únicamente en `android:allowBackup="false"`:** Android advierte que en determinados dispositivos de fabricantes y apps con target API 31+ la restricción cloud puede no bloquear la **transferencia dispositivo-a-dispositivo (D2D)**. Declarar y revisar reglas específicas cuando corresponda: `android:fullBackupContent` (Android 11 o menor) y `android:dataExtractionRules` (Android 12+ con target API 31+), incluidas secciones `cloud-backup` y `device-transfer` para todas las superficies sensibles. Android 16 QPR2 contempla además reglas de transferencia multiplataforma: comprobar sólo si el soporte objetivo lo incluye, no asumir hoy.
3. **Almacenamiento de marcador/ciclo de instalación:** candidato `Context.getNoBackupFilesDir()` + prueba de posesión Keystore (clave privada no exportable). Si el estado restaurado no coincide con marcador/credencial, crear instalación **nueva** y **no** rehidratar ID, relaciones, permisos, posiciones, alias anteriores ni datos restaurados parciales. No reconstruir «sesión anterior» usando un ID copiado.
4. **Actualización in-place no es reinstalación:** debe preservar identidad y vínculos mientras la clave sea válida. Si el Keystore pierde su clave sin reinstalación, **no** regenerar silenciosamente identidad con permisos antiguos; requerir flujo seguro distinto y decisión funcional.
5. **Borrar datos de app, desinstalar, migrar D2D o restaurar copia** necesitan casos separados por API/target/OEM. No prometer que un flags/archivo cubre las variantes de todos los fabricantes. `noBackupFilesDir` y reglas XML no equivalen a auditoría de borrado de todo el sistema.
6. **Gate de seguridad:** ni una copia restaurada ni un mensaje de red antiguo permiten resucitar autorizaciones o **última ubicación eliminada**. Conservación de tombstones/revisiones y su expiración requiere política material, sin permitir que se conviertan en historial de posiciones.

## 4. Operaciones propuestas de supresión, revocación y fallo cerrado

**No son una API aprobada; contratos candidatos para revisión adversarial y futuras pruebas autorizadas.**

- `Revoke(A,B,revision)`: aplicar revisión/bloqueo local **antes** de que cualquier `ReleaseLocation` posterior pueda ser admitido. Si falla lectura de estado, identidad o almacenamiento transaccional, **ninguna ubicación nueva**. Revocar en A detiene **nuevas entregas**, no borra mágicamente la última recibida por B; B puede conservarla conforme D-10 y política legal futura.
- `DeleteLocalLastLocation(B,A,generation)`: borrar entrada y derivados (dirección, overlay, vistas precargadas, miniaturas relacionadas) en B, invalidando generación para que callback/red/caché atrasados **no reconstruyan** el dato. Garantizar orden local de operaciones en una instalación; **no** atribuir eliminación a copias físicas o terceros sin pruebas.
- `DeleteKnownDevice/Relation`: diferenciar eliminar contacto/lista de conocidos, bloquear, revocar permiso, supresión local y solicitud de supresión a otro teléfono; no reinterpretar D-09/D-10. Un emisor A puede quedar offline; el estado remoto no es verificable y no se promete propagación instantánea.
- `ReinstallationDetected`: hacer fail-closed frente a ID/clave de instalación antigua; la instalación reinstalada no recibe relaciones previas por restauración. Un B no reinstalado puede conservar **solo ubicación anterior legítima** de A si D-10 lo permite, marcada con fecha/hora; su eventual plazo de conservación/legalidad continúa pendiente.
- `DeleteDataAtThirdParty`: **no disponible/NO AUTORIZADO todavía**, porque no hay proveedor elegido. Si se evaluara FCM, diferenciar el ID funcional WHEREIS del Firebase Installation ID y posibles tokens persistentes; Google documenta retención de Firebase Installation IDs hasta solicitud de borrado y retirada de sistemas activos/copias dentro de hasta 180 días posteriores. No afirmar borrado inmediato ni que un tercero puede suprimir ubicaciones que no debería conservar.
- `UserDeletionRequest`: **PROPUESTA de UX**, requerirá que FUNCIONAL #60 determine quién puede solicitar borrar, qué confirma cada actor, estados cuando B está offline y qué límite de garantía se comunica. PROPIETARIO debe decidir alcance legal y plazos; la app no puede certificar borrado de datos fuera de control.

### 4.1. Matriz de operaciones y efectos alcanzables

| Evento | En A | En B | En intermediarios hipotéticos | Mensaje/garantía admitida |
|---|---|---|---|---|
| A revoca B | Impide nuevas liberaciones tras revocación local aplicada | Ubicación legítima anterior conservable según D-10, salvo ocultación de bloqueo | Token técnico antiguo podría recibir avisos; no concede permiso | «Acceso revocado» local; no decir «datos antiguos eliminados en B» |
| B borra A y última ubicación | No necesariamente recibe aviso de inmediato | Borra dato, dirección/overlays y evita resurrección de respuesta tardía | No implica borrar token/ID de tercero | Confirmación de **borrado local**, no global |
| A desinstala / reinstala | Nueva instalación/ID; no permisos previos | Antigua ubicación sólo anterior si se obtuvo legítimamente | Token/ID técnico de proveedor podría durar más; no asumir supresión | «Nueva instalación» cuando autenticable, no «revocación instantánea» |
| B reinstala / restaura copia | No debe aceptar identidad reinstalada antigua | Nueva instalación sin recuperar ubicaciones ni permisos | Señalización externa, si alguna, con desregistro/borrado futuro a evaluar | Ningún derecho resucitado por backup |
| A/B offline durante revocación o borrado remoto | Autoridad sin contacto y estados no sincronizados | No confirmar acción en el otro dispositivo | Avisos duplicados/tardíos descartados sin captura | «No se ha podido confirmar»; fail-closed |
| Cambio de proveedor o rotación de tokens | No reabre relación, revalidar A | No revive ubicación borrada | Rotación/borrado del token técnico si hay mecanismo futuro aprobado | La API ajena y su retención requieren aprobación |

## 5. Matriz de amenazas / pruebas negativas — **NO EJECUTADAS**

| Caso de prueba sintético, sin datos reales | Resultado necesario | Qué evidencia futura haría falta |
|---|---|---|
| Restore cloud con ID/BD antigua, clave Keystore ausente | Instalar ID nuevo; cero relaciones/ubicaciones propias importadas | APIs Android y versiones/targets con backup controlado |
| Transferencia D2D Android 12+ con `allowBackup=false` y distintos OEM | Identidad/permisos/posiciones anteriores no se recuperan | Evaluación de reglas `dataExtractionRules` + pruebas OEM |
| Update in-place de la app | Mantiene identidad legítima; no restaura permisos antiguos | Tests de actualización |
| B borró posición; luego llega respuesta con requestId válido pero generación anterior | No se resucita dato ni cambia timestamp | Test de carrera y transacción |
| A revoca tras captura pero antes de `ReleaseLocation` | Ningún dato nuevo cruza gate posterior a revocación | Orden observable por revisión sin coordenadas reales |
| A emite resultado antes de revocación; B lo recibe tarde | Revalidación/timestamp, límites de imposibilidad documentados; no promesa de retiro de paquete emitido | Test de orden y conectividad, riesgos residuales |
| A offline→reconecta antes de TTL, se entrega aviso retenido | No ejecuta captura nueva ni reintento automático | Simulación de red y época original D-12 |
| A reinstalado; B consulta usando vinculación antigua | Deniega; ID/clave anterior no bastan | Test de identidad/QR/seguridad |
| Estado Android ubicación desactivada; aviso local con alias | No revela coordenadas por lockscreen; una/24 h por solicitante sujeto a permisos | Notificaciones APIs 29/33+, lockscreen, listener |
| App genera crash/log por consulta fallida | Sin coordenadas, tokens, IDs completos ni listas familiares en reportes | Revisión de logging/archivos temporales |
| B elimina ubicación; mapas, imágenes, cache reverse-geocode y overlays | No queda dato personal accesible en superficies **controladas por la app** | Inventario SQLite/files/cache y verificación instrumentada |
| B copia dirección/QR al portapapeles o hace captura | No prometer borrar una copia externa al sandbox | UX y pruebas de privacidad; límites conocidos |
| Notificación push duplicada y token FCM antiguo tras revocación | A no libera posición, evita spam según control futuro; proveedor puede retener ID técnico | Logs sanitizados, propuesta de abuso, límites de tercero |
| Borrar/rotar token hipotético FCM | No asumir desaparición inmediata; confrontar política publicada de hasta 180 días tras solicitud | Contrato y pruebas del proveedor **solo tras autorización** |
| Uso remoto detrás de NAT/CGNAT, A no visible | Fallo veraz, no persistencia externa de ubicaciones ni captura diferida | Android y red real **no autorizados aún** |
| Reloj alterado / timeout/caducidad de vinculación | No reabrir autorización ni prolongar 24h por replay; sin historial innecesario | Diseño y pruebas de fuente de tiempo |

**Pruebas no ejecutadas, sin CI, sin QA APTO ni validación Android.** El alcance de la plataforma/target, cifrado en reposo, reglas XML, schema local y mecanismos de borrado físico aún no están aprobados. No publicar datos reales de menores en evidencias.

## 6. Decisiones y dependencias sin resolver

| Área | Estado | Responsable siguiente tras revisión TECH LEAD |
|---|---|---|
| Política exacta de conservación de última posición y copias/derivados | **PENDIENTE MATERIAL**, D-10 no autoriza plazos indefinidos por omisión | PROPIETARIO, con FUNCIONAL #60 y análisis jurídico #41 |
| Transparencia, representación de menores, ejercicio de derechos y posibilidad de supresión remota | **PENDIENTE**; no equiparar uso doméstico con exención universal | FUNCIONAL #60 propone; TECH LEAD coordina; PROPIETARIO decide materiales |
| Elección de provider, cookies/tokens/IDs técnicos externos, jurisdicción, contrato y coste 0 € | P-52a/b/c/d **CONFIRMADAS SOLO PARA ESTUDIO**; adopción PENDIENTE | TECH LEAD #52 y PROPIETARIO antes de operar, QA #56 sobre PR #55 |
| Matriz real API/target/OEM, test D2D/cloud, privacidad de notificaciones, borrado verificable | **NO EJECUTADO**; cualquier ensayo real necesita autorización nueva | TECH LEAD #28/#24, después PROPIETARIO |
| Puntos de orden transaccional revocación/liberación y anti-enumeración por metadatos/canal lateral | **PROPUESTA técnica NO DEMOSTRADA** | TECH LEAD #24 tras #22/PR #35 y #8/PR #34 |

**Handoff solicitado:** ARQUITECTO entrega análisis de superficies y pruebas negativas a **TECH LEAD**, para consolidar en #41/#24, coordinar FUNCIONAL #60 y elevar sólo decisiones reservadas; **no** atribuir dictamen legal o aprobación a esta PR. Mantener #41/#24 abiertos. No abrir nuevos trabajos de programación ni modificar `docs/arquitectura.md` como baseline.

## 7. Referencias verificables (sin uso de servicios)

- Android Developers — [Auto Backup y reglas cloud/D2D](https://developer.android.com/identity/data/autobackup), [Backup](https://developer.android.com/identity/data/backup), [noBackupFilesDir](https://developer.android.com/reference/android/content/Context#getNoBackupFilesDir()) y [pruebas de Backup](https://developer.android.com/identity/data/testingbackup).
- Android Developers — [Notification visibility y lockscreen](https://developer.android.com/develop/ui/views/notifications), [permisos de ubicación](https://developer.android.com/develop/sensors-and-location/location/permissions) y [permisos de notificaciones](https://developer.android.com/develop/ui/views/notifications/notification-permission).
- Firebase — [Privacy and Security](https://firebase.google.com/support/privacy), categoría Firebase Cloud Messaging y su retención de identificadores técnicos.
- Fuentes jurídicas/alcance en #41 (RGPD, LOPDGDD, AEPD), **sin dictamen ni inferencia de exención**.

**Estado final: `PROPUESTA / PENDIENTE`. Las PR de arquitectura permanecen en DRAFT hasta QA independiente y revisión de TECH LEAD, sin que su integración futura autorice desarrollo o terceros.**
