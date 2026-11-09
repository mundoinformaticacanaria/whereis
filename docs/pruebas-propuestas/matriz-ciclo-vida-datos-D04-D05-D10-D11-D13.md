# Matriz QA propuesta — ciclo de vida de dispositivo, posición y ficha (D-04/D-05/D-10/D-11/D-13)

- **Fecha del corte:** 09/11/2026. **Clasificación:** `MATERIAL / PROPUESTA DOCUMENTAL DE VALIDACIÓN`; **NO** modifica decisiones del PROPIETARIO, ni representa un diseño/algoritmo aprobado.
- **Issues coordinadas:** [#8 D-04](https://github.com/mundoinformaticacanaria/whereis/issues/8), [#10 D-05](https://github.com/mundoinformaticacanaria/whereis/issues/10), [#20 D-10](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#21 D-11](https://github.com/mundoinformaticacanaria/whereis/issues/21) y [#23 D-13](https://github.com/mundoinformaticacanaria/whereis/issues/23).
- **Contratos canónicos ya CONFIRMADOS funcionalmente:** [D-04](../decisiones-funcionales/D-04-vigencia-autorizaciones.md), [D-05](../decisiones-funcionales/D-05-control-autorizacion-revocacion.md), [D-10](../decisiones-funcionales/D-10-retencion-eliminacion-ultima-ubicacion.md), [D-11](../decisiones-funcionales/D-11-ux-mapa-lista-marcadores.md), [D-13](../decisiones-funcionales/D-13-ficha-ubicacion-direccion.md). Complementan D-06, D-09, D-12 y SEG-01/02/03/04; ante conflicto prevalecen issue viva, decisiones posteriores y `main`.
- **Límite de esta matriz:** describe oráculos de salida observables y trazabilidad de pruebas futuras, sin elegir persistencia, SDK, generación/epoch, política de sincronización, geocodificador, algoritmos de revocación, cifrado, reloj remoto ni una librería de UI. **No se han ejecutado pruebas de código, Android, backup ni red.**
- **Estado real:** baselines, seguridad, protección de menores y CI pendientes. [Piloto excepcional #90](https://github.com/mundoinformaticacanaria/whereis/issues/90) aprobado **solo para una ordenación Kotlin/JVM pura** (D-11), condicionada a #93/#28 y QA independiente. **Esta matriz no amplía el piloto**.

## 1. Datos ficticios de referencia (no fijan formatos de IDs del producto)

| Clave de prueba | Interpretación simulada | Dato inicial |
|---|---|---|
| A1 | Instalación emisora original | ID ficticio `DEV-A1`, comparte únicamente con B1 mediante relación A1→B1 |
| B1 | Consultante que **no** se reinstala inicialmente | ID `DEV-B1`; última ubicación legítima de A1 `P0`, capturada `2026-10-16T14:00:00Z` |
| C1 | Otro consultante, independiente de B1 | ID `DEV-C1`; su permiso A1→C1 se conserva cuando solo se desactiva A1→B1 |
| A2/B2 | Nuevas instalaciones después de reinstalar A1/B1 | IDs **distintos** `DEV-A2`/`DEV-B2` sin permisos heredados |
| P0/P1 | Posiciones **ficticias**, versiones conceptuales | P0 es la última posición legítima recibida; P1 es una posición distinta, solo válida si pasó verificaciones actuales |
| G0/G1 | Resultados de búsqueda de dirección | G0 asociado a P0, G1 asociado a P1, nunca se transfieren entre capturas |

No incluir en el fichero coordenadas reales, identidades de menores, direcciones postales reales, credenciales ni llamadas de red. Para implementar una prueba basta usar objetos de prueba sintéticos con marca temporal fija y registrar los eventos: `enviar`, `autorizar`, `recibir`, `bloquear`, `borrar`, `restaurar`, `callback` y `mostrar`. Estos nombres ilustran la prueba y **no definen API**.

## 2. Matriz mínima de secuencias, resultados y puertas de seguridad

| Caso | Secuencia de prueba propuesta | Oráculo observable / no regresión | Fuente |
|---|---|---|---|
| **LC-01** | A1 permite B1 y C1; pasa un intervalo simulado prolongado sin revocación/desinstalación | Las autorizaciones no caducan **solo por tiempo**; las comprobaciones de identidad, permisos y conectividad siguen aplicando | D-04 CA01/02 |
| **LC-02** | A1 desactiva *efectivamente* A1→B1, manteniendo A1→C1 | Ninguna **posición nueva** se entrega a B1; C1 no pierde por ello su autorización. B1 puede conservar P0 como **anterior y fechada** sin confundirla con P1 | D-05 CA01/02/03, SEG-01/02 |
| **LC-03** | A1 reactiva A1→B1 sin reinstalar ni bloquear | No se exige **nueva solicitud de vinculación**; una nueva posición solo es posible si se verifican identidad, autorización efectiva y restricciones Android | D-05 CA04/05; D-04 |
| **LC-04** | A1 bloquea B1; después lo desbloquea sin conceder permiso | Durante bloqueo no se obtiene posición nueva ni se muestra el marcador anterior donde D-09 lo prohíbe. Desbloquear **no** restituye por sí solo permiso; P0 solo reaparece como anterior si sigue legítimamente visible | D-09/#19; D-10 CA03 |
| **LC-05** | A1 se desinstala y luego aparece A2, sin reinstalar B1 | A2 tiene nuevo ID y **no hereda** relaciones. B1 conserva **P0 anterior fechada** de A1 si no eliminó la relación; no se entrega nueva posición desde A1/A2 sin vinculación y permiso nuevos | D-04 CA03/05; D-10/SEG-04 |
| **LC-06** | B1 se desinstala y aparece B2, incluso con restauración de backup cloud/D2D simulada | B2 no recupera ID B1, autorizaciones ni P0: interfaz sin posición heredada. Requiere solicitud/aceptación nuevas; una restauración no recupera permisos | D-04 CA04/05, SEG-04 |
| **LC-07** | B1 pulsa «Eliminar dispositivo», cancela una vez y confirma otra | Cancelar no borra. Confirmar elimina relación, P0 y personalización local (alias/foto/color); ficha, selección y marcador dejan de exponer ese dispositivo. No afirmar supresión universal de backups externos | D-10 CA04; D-11 |
| **LC-08** | B1 confirma eliminación mientras llega respuesta tardía de consulta anterior | La respuesta/callback no **recrea** ubicación, relación, ficha, marcador o datos personalizados. No se convierte respuesta tardía en nueva autorización | D-10; D-06 opción A/#12; SEG-01 |
| **LC-09** | B1 elimina la relación mientras existe geocodificación G0 de P0 pendiente | Cuando llega G0, no restablece la ficha, coordenadas, marcador, acción «Copiar ubicación» ni caché de la relación eliminada | D-10; D-13; D-11 |
| **LC-10** | B1 recibe nueva posición legítima P1; llega luego dirección G0 de P0 | Mostrar **inmediatamente P1** sin dirección heredada; G0 no sobrescribe fecha, precisión, coordenadas ni dirección de P1; solo G1 asociado a P1 puede completar su ficha | D-13 CA02 y reglas 5/6 |
| **LC-11** | B1 cierra ficha mientras G1 está pendiente, **sin** bloquear/eliminar y sin cambiar posición | Cerrar la ficha no cancela por sí solo la búsqueda; al reabrir puede verse el resultado de G1 si aún corresponde a P1. No lanzar captura GPS adicional ni reintento automático de dirección | D-13 reglas 5/6 |
| **LC-12** | B1 falla en geocodificar P1 y pulsa «Reintentar dirección» manualmente | Preservar **P1, precisión y timestamp**; el reintento usa sus coordenadas existentes sin nueva captura; dirección ausente se informa y no inventa calle/número | D-13 CA02 y reglas 4–6 |
| **LC-13** | B1 cambia alias de A1 sin cambiar ID; alterna búsqueda y filtro | Orden de conocidos por alias o ID cuando no haya alias; **ordinal global** cambia si cambia el orden completo, pero **no** por filtrar; no se reasigna posición/autorización a otro ID | D-11 CA02, D-10 |
| **LC-14** | B1 selecciona A1 y abre ficha; a continuación lo elimina o lo bloquea legítimamente | La ficha/modal y selección se actualizan según visibilidad; no exponen datos borrados o bloqueados ni permiten interacción accidental en mapa/lista detrás de una ficha modal | D-11, D-09 y D-10 |
| **LC-15** | Cambia la zona horaria de B1 después de capturar P0; luego ocurre un timeout | Mostrar hora local `DD/MM/AAAA HH:mm:ss` correspondiente al instante **original** de P0, no a la petición fallida. No modificar el instante guardado ni dar a P0 calidad de posición actual | D-13 y D-06 |
| **LC-16** | A1 revoca mientras una petición está en vuelo, con verificación remota ausente o no demostrable | **Fail-closed**: no liberar una posición nueva al consultante sin identidad auténtica y autorización direccional vigente verificables; una respuesta de transporte no equivale a autorización | SEG-01/02, D-05, D-12 |

## 3. Resultados pendientes por diseño o por prueba real

Estas cuestiones **NO quedan resueltas** por especificar el resultado observable: detección de desinstalación remota; semántica de propagación offline y carrera exacta entre revocación y bytes ya emitidos; atomicidad del gate; elección de IDs/revisiones/épocas/TTL; serialización y persistencia/cifrado; supresión efectiva de caché y copias cloud/D2D/OEM; legitimación/retención de datos de menores; accesibilidad y geocodificador; coste/privacidad del proveedor de mapas.

En pruebas de entrega real, cada `LC-XX` registrará **dispositivo o versión Android, actor, permisos, conexiones, precondición, secuencia controlada, resultado esperado, resultado obtenido, salida/exit code si existe y HEAD SHA**; la QA independiente reproducirá casos críticos. Un PASS sintético aislado **no** es evidencia de seguridad Android, borrado físico o cumplimiento jurídico.

## 4. Fronteras de integración y QA

- **Uso permitido ahora:** revisar documentalmente esta matriz para confirmar fidelidad a contratos **CONFIRMADOS** y ausencia de nuevas reglas. Sólo tras QA independiente del HEAD exacto y gates aplicables se podrá considerar la integración documental.
- **Uso posterior:** la implementación autorizada podrá derivar pruebas unitarias puras para orden/alias (D-11), y pruebas Android/almacenamiento/red **solo con autorización posterior y bootstrap/seguridad apropiados**. La excepción [#90](https://github.com/mundoinformaticacanaria/whereis/issues/90) **NO** autoriza ejecutar LC-01..LC-16 sobre servicios, dispositivo, runner o datos reales.
- **Contradicción o hueco:** marcar `DEFECTOS` o `PENDIENTE MATERIAL`, referir a `main`/issue viva y escalar a FUNCIONAL→PROPIETARIO si altera comportamiento; no completarlo por intuición. **No** usar esta matriz para seleccionar proveedor, implementar almacenamiento o activar seguimiento.
- **Gates no cumplidos:** #24 SEG, #41 jurídico, #42 CI/enforcement, #28/#93 Linux, baseline global. No fusionar sin la comprobación del protocolo y revisión TECH LEAD posterior.

**Comprobación estática:** este archivo solo contiene Markdown y ejemplos de IDs ficticios. **No se han ejecutado los casos LC-01..LC-16.**
