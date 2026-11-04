# ADR-PROP-84 — D-13: geocodificación inversa local/offline y privacidad

- **Fecha del estudio:** 04/11/2026. **Clasificación:** MATERIAL.
- **Estado:** `PROPUESTA / PENDIENTE` (estudio documental, **no** elección de tecnología, baseline ni implementación).
- **Encargo:** [issue #84](https://github.com/mundoinformaticacanaria/whereis/issues/84), delegada por [TECH LEAD en #23](https://github.com/mundoinformaticacanaria/whereis/issues/23#issuecomment-6637459432).
- **Contrato funcional CONFIRMADO:** D-13 en [#23](https://github.com/mundoinformaticacanaria/whereis/issues/23) e integración **solo documental** por PR #49. Prioridad: coordenadas inmediatas, dirección parcial si existe, ausencia de dirección sin inventar calle/número, hora real y precisión originales, reintento **solo manual** sin captura GPS nueva. Los estudios no completan el baseline MVP.
- **Restricciones CONFIRMADAS:** localización/identidades/autorizaciones persistentes solo en teléfonos, uso familiar en España, coste incremental operativo 0 € como condición, ninguna autorización para enviar coordenadas a un tercero, activar servicios, proveedores o servidores. Ver [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41), [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24) y [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52); L-02b/c/d autorizan **estudiar señalización**, no geocodificación remota.
- **Evidencia disponible:** lectura de `main`, issues/comentarios y fuentes primarias citadas en §8. **NO DEMOSTRADO:** funcionamiento Android en dispositivos/OS concretos, tamaño de paquetes, cobertura de portales/direcciones, exactitud, licencias de artefactos preparados, ausencia real de tráfico, coste integral 0 € y eliminación verificable. **Pruebas: NO EJECUTADAS**.

## 1. Pregunta y límite de confianza

La entrada es una posición **ya legítimamente recibida** por B (teléfono consultante); la geocodificación no justifica una nueva consulta de ubicación de A. Convertir sus coordenadas a una dirección puede revelar información sobre una persona, incluso menor, a un backend del sistema, un servicio remoto, un proveedor de datos o registros/cachés de SDKs.

La preferencia por un producto gratuito o software libre **no** acredita privacidad ni operación offline. El trabajo compara viabilidad, pero no decide el backend, un SDK ni una fuente cartográfica. La selección y toda transmisión material corresponden a PROPIETARIO tras gates #24/#41/#42.

## 2. Alternativas contrastadas

| Alternativa | A favor | Límites y riesgos verificados / pendientes | Privacidad/offline/coste |
|---|---|---|---|
| **A. `android.location.Geocoder` del sistema** | API Android existente; devuelve `Address` parcial y puede ofrecer backend según dispositivo; interfaz de escucha asíncrona API 33+. | `isPresent()` solo indica implementación, **no** servicio disponible, resultado ni funcionamiento offline. La API **puede utilizar red**; no garantiza calidad, latencia ni localización por idioma. Política de datos, backend OEM y cuota **NO DEMOSTRADOS**. | **NO DEMOSTRADO** que no transmita coordenadas ni que sirva sin red. No aprobar automáticamente por estar en Android. |
| **B. Índice de direcciones autocontenido en B, derivado de extractos regionales OSM u otra fuente autorizada** | Consulta puede ejecutarse enteramente en B con red desconectada si **todos** los datos y código están realmente instalados; no necesita un servicio de terceros por búsqueda. Potencial minimización de datos de ubicación. | Diseño propio de índice espacial y reglas de selección de calle/portal; las etiquetas de dirección pueden faltar o estar desactualizadas. Ámbito geográfico, descarga/distribución/actualizaciones, almacenamiento, RAM, energía, tiempo de generación y licencia del paquete **NO MEDIDOS**. ODbL exige atribución y puede imponer obligaciones sobre bases derivadas/distribuidas: revisar caso concreto. | **PROPUESTA condicionada**. Cumplimiento offline técnico posible por diseño, pero cobertura, interoperabilidad Android, licencias y coste operativo **PENDIENTES** de verificar; sin paquete instalado no da dirección. |
| **C. Motor abierto tipo Nominatim/Photon operando como servidor** | Con datos OSM puede efectuar geocodificación inversa; capacidades documentadas. | Requiere proceso/base de datos/actualizaciones y operación ajena a la aplicación; no equivale a librería Android autocontenida. Nominatim se documenta con PostgreSQL/PostGIS y recursos relevantes. Instancia propia/remota sería **infraestructura no autorizada**. | No cumple modo local en B; privacidad/retención, disponibilidad y coste 0 € **NO DEMOSTRADOS**. No adoptar. |
| **D. API remota pública/comercial de geocodificación** | No exige distribuir índice local. | Revelaría al receptor coordenadas y metadatos de conexión; posibles logs, jurisdicciones, tarifas y términos. El servicio público Nominatim OSMF limita a 1 petición/s **por aplicación**, exige identificación/atribución y **prohíbe enviar datos personales o confidenciales**; no es un backend autorizado para las coordenadas familiares. Otros proveedores requerirían análisis individual. | **NO AUTORIZADA** por L-02; no cumple privacidad offline; gratuidad/cuotas/retención **NO DEMOSTRADAS**. |
| **E. Degradación D-13: solo coordenadas y «Dirección no disponible»** | Sin procesamiento por tercero, sin consulta de geocodificador ni datos extra; cumple los estados de fallo **CONFIRMADOS** de D-13. | No produce calle/portal. El botón «Reintentar dirección» reutiliza la posición y solo puede volver a intentarlo cuando exista una fuente **autorizada**; no debe activar red/SDK automáticamente. | Privacidad de geocodificación y ausencia de coste externo por consulta **compatibles por diseño**; no equivale a prometer dirección disponible. |

**Descartes concretos:** `libpostal` es un parser/normalizador, **no** un motor completo de geocodificación inversa; no soluciona por sí solo lat/lon→portal. Un servidor Photon/Nominatim local a otro equipo no es «offline en el teléfono». La cobertura del mapa o disponibilidad de teselas no implica disponer de un índice de direcciones.

## 3. Recomendación para evaluación (NO aprobada)

1. **Mantener la opción E como degradación segura obligatoria de D-13** mientras no haya fuente demostrada; no introducir un backend de red por defecto ni llamar a Geocoder del sistema suponiendo que es privado/offline.
2. **Estudiar B como única vía candidata a geocodificación inversa demostrablemente offline en B**, con datos precargados, ejecución sin red y cobertura limitada explícita. Priorizar **un paquete regional acotado y reproducible** para pruebas futuras, no todo el planeta ni servicio permanente. La preparación/distribución de datos y su alcance geográfico son **PENDIENTES**; no descargar ni construir todavía.
3. **No seleccionar A, C ni D para producción** en este estudio. A podría reexaminarse solo si se acredita, por fabricante/API/versión y modelo de confianza, que no envía coordenadas ni retiene metadatos; `isPresent()` no basta. C/D requieren autorización material expresa del PROPIETARIO y revisión #24/#41.
4. Si en el futuro no se obtiene cobertura suficiente, **no inventar direcciones**: seguir D-13 y elevar cualquier propuesta de cambiar la exigencia funcional a FUNCIONAL/PROPIETARIO. La geocodificación no es una condición para dibujar el marcador.

No proponer hoy bibliotecas, índices SQL específicos, descargador de datos, proveedores, licencias definitivas ni tamaño/latencia objetivo sin mediciones y autorización diferenciada.

## 4. Frontera mínima y contratos candidatos

**PROPUESTA de contrato, no API final ni código a implementar ahora.** Un único componente de resolución de dirección en B, desacoplado del estado de vínculos y de la UI, recibiría una instantánea de coordenadas **ya autorizadas para visualizar**. Solo si se adopta un motor concreto se justificaría un adaptador para él; evitar una arquitectura de plugins genérica.

- **Entrada:** `knownDeviceRef` local; `positionGeneration` opaca y monótona por sustitución/borrado; coordenadas de la **posición guardada**, `fixInstant` original, precisión horizontal opcional; `lookupAttemptId` para reintento manual; revisión local de estado/visibilidad. No crear una captura GPS para obtener dirección.
- **Salida:** `AddressAvailable(components, sourceVersion)`, `NoAddress` o `LookupFailure`. Campo/valor parcial si lo provee la fuente; sin inventar portal, calle o exactitud. Errores técnicos no se muestran como un falso éxito.
- **Regla de aplicación:** antes de aplicar cualquier callback, comprobar identidad de relación, `positionGeneration`, `lookupAttemptId`, existencia de posición y revisión/visibilidad actuales en B. Si cambió P1→P2, hubo borrado o bloqueo, **descartar** resultado y derivados de P1, no recrear dato ni mostrarlo. Una respuesta tardía no debe alterar estado de permisos o posición.
- **Commit local:** la nueva ubicación legítima P2 sustituye a P1, fija su instante/precisión y deja **vacía** la dirección de P2. Mostrar P2 inmediatamente. La dirección se agrega solo si coincide con P2; ni fallo ni reintento reemplazan coordenadas/instante/precisión. No conservar caché de geocodificación de ubicaciones borradas.
- **Visibilidad:** bloqueo (D-09/D-10) **oculta** posición/dirección sin exigir borrar el último dato legítimo que D-10 manda conservar; eliminar dispositivo sí borra la ubicación y dirección/derivados controlados por la app e invalida callback. Revocación ordinaria impide nueva ubicación sin borrar por defecto la anterior legítima; cualquier futura modificación de retención pertenece a #41.
- **Ficha:** cerrarla/reabrirla **no cancela** búsqueda válida (D-13); eliminar/bloquear sí invalida la posibilidad de mostrar el resultado. No auto-reintentar al reabrir; «Reintentar dirección» crea solo un nuevo intento sobre la misma P.
- **Tiempo y precisión:** `fixInstant` permanece el instante de obtención, no fecha de consulta ni de dirección. Formatear `DD/MM/AAAA HH:mm:ss` en zona `ZoneId` **actual del consultante**, también tras DST; mantener `hasAccuracy()`/precisión original y el carácter aproximado. No derivar la precisión GPS de una dirección interpolada.
- **Contención de filtraciones:** no enviar lat/lon, IDs completos ni direcciones a logs/analytics, URI, trazas, push ni terceros; sin búsqueda de datos por coordenada fuera de B. Tratar copia al portapapeles como superficie distinta ya prevista por D-13, sin prometer borrar copias externas. Las teselas del mapa y otros SDKs se evalúan **por separado** en #24/SEG-07.

## 5. Matriz mínima de amenazas

| Riesgo | Defensa propuesta | Evidencia pendiente |
|---|---|---|
| Sistema Geocoder ejecuta llamada de red oculta | No integrarlo como fuente privada sin verificación; perfil offline aislado | Captura de tráfico/DNS y pruebas por API/OEM, solo con autorización |
| Descarga automática de extracto revela región de residencia | No seleccionar/descargar por coordenada automáticamente; paquete regional preestablecido sujeto a elección explícita futura | Flujo aprobado, registro de red sin localización, privacidad del proveedor de descargas |
| Resultado asíncrono de P1 pisa P2 | Comparación de generación + intento vigente antes de persistir y mostrar | Test GEO-V01 con callbacks permutados |
| Dato borrado/bloqueado se resucita | Generación invalidada, comprobación de existencia y visibilidad antes de commit; borrar derivados propios | GEO-V02/V03, restore/cloud/D2D de #61 |
| Dirección parcial errónea inventa portal | Solo componentes aportados, tratar «cercano» como aproximado; no inferir edificio/portal | Conjunto de coordenadas sintéticas y datos incompletos |
| Paquete/caché offline obsoleto | Versionar procedencia del dataset, actualización explícita/política aprobada, capacidad de retiro | Pruebas de integridad, espacio y cobertura, sin tamaños inventados |
| ODbL/atribución y actualización de datos | Inventario de fuentes y obligaciones de distribución antes de empaquetar | Validación de licencia específica y procedencia |
| Geocodificador remoto/SDK captura coordenadas de menores | Ningún endpoint o SDK no autorizado, sin fallback de red | Revisión de dependencias/tráfico y decisiones #24/#41 |

## 6. Pruebas negativas propuestas — **NO EJECUTADAS**

Reusar los invariantes publicados en [#23, GEO-V01..V05](https://github.com/mundoinformaticacanaria/whereis/issues/23#issuecomment-6553922636), no atribuirlos a pruebas ya pasadas.

| Escenario sintético | Resultado exigible |
|---|---|
| **GEO-V01**: P1 buscando, llega P2, callback de P1 luego | P2 visible de inmediato; dirección P1 no aparece en P2; hora y precisión de P2 intactas. |
| **GEO-V02**: se elimina dispositivo y última posición mientras resuelve dirección | Callback, cache y reabrir ficha **no** regeneran coordenadas/dirección/marcador ni «Copiar ubicación». |
| **GEO-V03**: bloqueo remoto autenticado aplicado en B durante búsqueda | Se oculta marcador/ficha como D-10; callback no lo reabre. Desactivación ordinaria no equivale a bloqueo/borrado. |
| **GEO-V04**: cierre de ficha sin eliminación, luego resultado; fallo y «Reintentar dirección» | Búsqueda original continúa; resultado de la misma posición se ve al reabrir. Fallo muestra coordenadas y botón manual; no nuevo GPS ni reintento al abrir. |
| **GEO-V05**: cambio de zona y DST, sin precisión y con precisión aproximada | Se recalcula solo hora visual en zona B desde `fixInstant`, sin modificarlo; «Precisión no disponible» si falta; dirección incompleta no finge precisión postal. |
| Dos reintentos manuales de la misma P terminan fuera de orden | Solo intento que sigue vigente aplica resultado; resultado del intento desplazado no pisa estado. |
| `Geocoder.isPresent()=true` pero servicio inaccesible o sin red | No prometer offline, no bloquear UI ni enviar lat/lon sin autorización; «Dirección no disponible» si falla. |
| Índice local ausente, corrupto, incompleto, región sin cobertura o fuente sin portal | Degradación segura a coordenadas sin invención; no fallback remoto, no loops ni consultas ocultas. |
| Captura de tráfico con geocodificación local y red conectada/desconectada | **Cero solicitudes de resolución con coordenadas** fuera de B (no confundir con tráfico independiente de mapas); sin datos reales. |
| Actualización de paquete local durante consulta; instalación/restauración con caché anterior | No resucitar última posición suprimida ni usar dirección de una versión invalidada; política #61 de backup/retención condiciona prueba. |
| Revisión de licencia, construcción y distribución de un extracto hipotético | Attribution/ODbL y origen verificables; tamaño comprimido/instalado, RAM, latencia, cobertura y esfuerzo de actualización medidos para la región aprobada; **sin valores supuestos**. |

No hay ensayos Android, tráfico observado ni dataset preparado en esta entrega. Probar servicios reales, distribuir datos, integrar SDK y ejecutar código requiere nuevas autorizaciones/issue de implementación, baselines y QA de la versión exacta.

## 7. Handoff, pendientes y dependencias

- **TECH LEAD [#23](https://github.com/mundoinformaticacanaria/whereis/issues/23):** revisar esta ADR, acotar qué evidencia de cobertura/licencias/distribución permitiría comparar un índice offline regional; solicitar QA documental independiente del HEAD de la PR; integrar solo tras gates. No confundir un APTO documental con funcionamiento en Android.
- **PROPIETARIO:** decide cualquier selección material de proveedor/SDK, transferencia de coordenadas, empaquetado/uso de datos que cambie privacidad/costes/alcance y autorización de futuras pruebas reales. Coste operativo incremental obligatorio 0 € sigue **NO DEMOSTRADO** para alternativa concreta.
- **FUNCIONAL:** solo si se propone modificar el contrato D-13 o la UX aprobada; la degradación a coordenadas **ya está CONFIRMADA** y no necesita inventar nuevos textos.
- **Seguridad y privacidad:** [#20](https://github.com/mundoinformaticacanaria/whereis/issues/20) D-10 (última ubicación y borrado), [#21](https://github.com/mundoinformaticacanaria/whereis/issues/21) D-11 (selección/ficha), [#22](https://github.com/mundoinformaticacanaria/whereis/issues/22) D-12 (sin nueva consulta implícita), [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24) SEG-01/02/07, [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41) menores/retención y R-60a/b/c **PENDIENTES**, [#52](https://github.com/mundoinformaticacanaria/whereis/issues/52) señalización de alcance diferente, [#61](https://github.com/mundoinformaticacanaria/whereis/issues/61) backup/supresión, [#42](https://github.com/mundoinformaticacanaria/whereis/issues/42) protección/CI.
- **PENDIENTE para elegir B:** región, calidad mínima, procedencia legal, ODbL/distribución, capacidad de almacenamiento real, actualización, daños por dirección inexacta, observabilidad de tráfico y batería. **NO DEMOSTRADO:** una solución de dirección postal completa offline universal a coste incremental 0 €.

**Conclusión:** D-13 permite mostrar la posición sin dirección; no es aceptable adoptar geocodificación remota por comodidad o fingir que el `Geocoder` del sistema es offline. **Evaluar un índice local regional como hipótesis, sin adoptar**, y conservar el fallback sin direcciones. Esta ADR **no** aprueba baseline, programación, cuentas, servicios, infraestructura, servidor/CRM ni timers.

## 8. Fuentes primarias examinadas (documentación, sin uso de APIs)

1. Android Developers — [`Geocoder`: disponibilidad, red, resultado parcial, API 33 asíncrona](https://developer.android.com/reference/android/location/Geocoder) y [`GeocodeListener`: orden/duración de respuestas no garantizados](https://developer.android.com/reference/android/location/Geocoder.GeocodeListener).
2. Android Developers — [`Location`: instante de fix y precisión opcional](https://developer.android.com/reference/android/location/Location).
3. OpenStreetMap Foundation — [licencia ODbL, atribución y límites de APIs](https://www.openstreetmap.org/copyright); [política Nominatim público y prohibición de datos personales/confidenciales](https://operations.osmfoundation.org/policies/nominatim/).
4. Geofabrik — [extractos regionales OSM de descarga, actualizados normalmente a diario](https://download.geofabrik.de/) (no equivale a tamaño final o permiso contractual de distribución).
5. Nominatim — [requisitos de instalación de servidor PostgreSQL/PostGIS](https://nominatim.org/release-docs/latest/admin/Installation/); Photon — [motor de búsqueda basado en OpenSearch y API inversa](https://github.com/komoot/photon) (no bibliotecas Android aprobadas).
6. libpostal — [alcance de parsing/normalización, no geocodificación completa](https://github.com/openvenues/libpostal).

**Todo resultado de prueba indicado en §6 es PROPUESTA/NO EJECUTADO.**
