# ADR-PROP-08 — Identidad de instalación, restauración y revocación

- **Estado:** `PROPUESTA / NO APROBADA`.
- **Clasificación:** `MATERIAL` — seguridad, identidad, privacidad y persistencia.
- **Issue:** [#8 — D-04](https://github.com/mundoinformaticacanaria/whereis/issues/8).
- **Dependencias:** [#24 — SEG-01/02/03/04](https://github.com/mundoinformaticacanaria/whereis/issues/24), [#19 — D-09](https://github.com/mundoinformaticacanaria/whereis/issues/19), [#20 — D-10](https://github.com/mundoinformaticacanaria/whereis/issues/20), [#22 — D-12](https://github.com/mundoinformaticacanaria/whereis/issues/22).
- **Alcance:** propuesta revisable; NO cambia `docs/arquitectura.md`, no elige proveedor, no aprueba baseline ni autoriza implementación.
- **Autoridad y transición G-02:** [#37, decisión B CONFIRMADA el 25/10/2026](https://github.com/mundoinformaticacanaria/whereis/issues/37#issuecomment-6395244289) designa como nuevo ejecutor del rol `ARQUITECTO` a un chat independiente de ChatGPT. **La enmienda documental de G-02 aún no está integrada en `main`** y la issue #37 ya se ha devuelto a TECH LEAD para formalizarla. Este estudio sigue siendo PROPUESTA y no habilita integración o implementación.

## 1. Invariantes CONFIRMADOS (no son opciones de arquitectura)

1. D-04: ID Whereis estable **por instalación** y nuevo después de reinstalar cualquiera de los extremos. Actualizar la app sin desinstalar no debe cambiarlo.
2. D-04 + SEG-04: la instalación recién instalada no recupera ID, relaciones, autorizaciones ni ubicaciones de la anterior, incluso tras restauración de copia del sistema. Ningún permiso se reactiva por la copia.
3. D-03/D-09: conocer un ID/QR, aceptar una solicitud y activar el interruptor son hechos distintos; el permiso es explícito y direccional.
4. SEG-02: ID/QR no es prueba de identidad. Una ubicación nueva requiere **autenticidad de la instalación solicitante** y **relación autorizada vigente**.
5. SEG-01: si no es verificable la autorización actual, no entregar nueva ubicación; no prometer revocación remota instantánea sin conectividad.
6. D-10: A desinstalado no borra por sí mismo la última ubicación legítima en B que sigue instalado. B reinstalado no recupera su copia previa. Bloquear puede ocultar ubicación anterior sin volverla actual.
7. **Opción B de D-09/SEG-02 CONFIRMADA** por PROPIETARIO el 23/10/2026 en [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24#issuecomment-6371711122): una verificación de ID no autenticada o sin derecho de conocer su existencia no debe distinguir un ID inexistente de otro existente pero no divulgable. La UX literal corresponde a FUNCIONAL; no modificar por esta opción los reintentos legítimos ni la caducidad de 24 h de D-09.
8. Borrado, retención legal y salvaguardas de menores siguen `PENDIENTE` de revisión especializada en [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41); no equiparar una exclusión de backup a supresión jurídica completa. SEG-02 continúa técnicamente PENDIENTE.

## 2. Amenazas y límites

- Copia de ID/QR, suplantación de B por C, replay de pruebas y solicitudes, extracción/restore de preferencias o bases de datos, clonación de copia cloud y transferencia D2D.
- Restauración incompleta que deja metadatos antiguos pero no la clave privada; KeyStore inaccesible; instalaciones anteriores que el otro extremo aún cree vigentes; operaciones de autorización/revocación concurrentes.
- Supuestos que **no** podemos validar todavía: garantías en OEM particulares, resistencia a dispositivo rooteado o totalmente comprometido, disponibilidad de verificador remoto, plazos de retención y borrado en terceros.
- Distinguir identidad técnica de instalación de identidad civil de usuario (no hay cuentas personales aprobadas).

## 3. Alternativas y recomendación

| Alternativa | Ventajas | Riesgo/limitación | Evaluación |
|---|---|---|---|
| ID + secreto bearer en preferencias/BD restaurables | Poco código inicial | Un backup/duplicado puede recrear identidad y permisos | **No recomendar** |
| ID público aleatorio + clave no exportable por instalación; verificador de identidad y relación | Separa identificador visible de autenticación y autorización; evita recuperar permiso mediante copiar QR | Depende de gestión de claves, alcance del Keystore y verificación de estado entre dispositivos | **Preferida como PROPUESTA**, sujeta a validación |
| Relación exclusivamente P2P sin punto de verificación disponible | Menos infraestructura central | Difícil acreditar permiso vigente, concurrencia, offline y dispositivos no visibles | No demuestra SEG-01/02/D-02 por sí sola |

**Diseño candidato**, no selección tecnológica final: generación en cada instalación de un identificador público con entropía suficiente y una prueba de posesión no restaurable (p. ej. par asimétrico en Android Keystore). Una contraparte de confianza registra la clave pública de la instalación y comprueba un desafío fresco unido al contexto de cada petición; verifica por separado la autorización direccional. El diseño no obliga todavía a backend concreto, proveedor o cloud. Una mera firma sin control de permiso vigente **no** satisface SEG-01.

## 4. Fronteras y contratos propuestos

- **`InstallationIdentity`**: `installationId` opaco y público, `credentialKeyRef` privado y local, `generationProof` ligado al ciclo de vida de la instalación. Prohibir exportar la credencial. El QR solo contiene identificador/elementos públicos, nunca secreto.
- **`KnownDevice`**: reconocer no crea `AuthorizationRelation`.
- **`AuthorizationRelation`**: `grantorInstallationId`, `granteeInstallationId`, sentido, `status`, `revision` monótona y evidencia de la acción expresa. Las verificaciones deben usar revisiones actuales, nunca un estado de caché offline como permiso suficiente.
- **`AuthorizedLocationRelease`**: cada posición tiene un único punto de autorización de **liberación** ante la autoridad de la relación, no solo un chequeo al recibir la solicitud. Petición autenticada, no caducada, ligada a ambas instalaciones, y relación direccional activa con revisión vigente. Preparar/cifrar un resultado antes del gate **no** autoriza transmitírselo a B; respuestas pendientes o reintentos exigen gate nuevo o invalidación demostrable. Si no se puede acreditar identidad/permiso actual, **denegar** y no diferir entrega hasta reconectar.
- **`ExistenceDisclosurePolicy` (opción B CONFIRMADA)**: ante una verificación no autenticada o sin derecho de consultar existencia, IDs inexistentes y existentes no divulgables producen un resultado externo indistinguible; revisar mensajes, códigos de respuesta, longitud, cabeceras, metadatos, patrones de red y latencia observable. El texto exacto lo decide FUNCIONAL. Antiabuso/rate-limit no reemplaza esta regla y no es aceptable usar validaciones rápidas de «no existe» frente a lentas de «existe» sin mitigación y prueba. No impedir flujos legitimados de QR/ID ni reducir controles de autorización.
- **`LastLegitimateLocation`**: solo última captura legítima almacenada en el consultante, con instante real, precisión conocida y estado de antigüedad. No se debe rehidratar desde la copia de una instalación extinguida.

**Orden de concurrencia propuesto para revisar con PR #35:** `AuthorizationAuthority` serializa por relación los eventos `Grant(revision)`, `Revoke(revision+1)`, `Block(revision+1)` y `Release(requestId,revision)`. `Release` no es el chequeo al aceptar ni al capturar: es la decisión final, verificable y atómica respecto a los cambios de revisión antes de permitir que el contenido abandone el dominio protegido del emisor/verificador. Si `Revoke` confirma primero, `Release` falla incluso con muestra preparada; si `Release` confirma primero, se puede haber transmitido el dato legalmente **antes** de la revocación. No compartir un resultado previamente autorizado mediante una cola de red sin nuevo control al retransmitir; descartar reintentos en nueva revisión, también si luego se reactiva el interruptor.

**Límite distribuido no resuelto:** en una red asíncrona, un paquete emitido *antes* de revocación puede llegar físicamente después. No se promete retirarlo del transporte ni borrar el dato ya conocido. Como defensa adicional, la instalación B valida la vigencia de su relación y la generación de la solicitud **antes de aceptar y mostrar** un resultado retrasado; sin verificación disponible no muestra una ubicación nueva. Aun así, una revocación remota no propagada a B puede ser desconocida: las garantías exactas y el punto de liberación requieren análisis/ensayos de TECH LEAD y decisión MATERIAL si el requisito se interpretara como prohibición absoluta de recepción posterior, imposible de garantizar sin condiciones de conectividad. **Es una PROPUESTA, no una demostración de atomicidad.**

## 5. Bootstrap de identidad y backups

1. Al primer arranque de una instalación, comprobar existencia y validez conjunta del material local no recuperable y sus metadatos. Si solo llegan metadatos de backup sin prueba no exportable, **no** reusar el ID/relaciones/datos; tratar como instalación nueva. No «arreglar» la autenticación tomando el viejo ID del backup.
2. Excluir de backup cloud **y D2D** claves/referencias, ID y estado de instalación, autorizaciones, relaciones, posiciones y miniaturas/alias que pudieran reconstruir datos anteriores. Definir reglas diferenciadas para versiones/target según corresponda: `fullBackupContent` y `dataExtractionRules` con `cloud-backup` y `device-transfer`. Evaluar `noBackupFilesDir` para el marcador de instalación. `allowBackup=false` aislado **no acredita** todos los flujos D2D/OEM.
3. Actualización de APK sin reinstalar mantiene identidad; una pérdida imprevista de la clave con app aún instalada NO se resolverá reasignando permisos automáticamente. **PENDIENTE FUNCIONAL/TECH LEAD:** UX de identidad irrecuperable y procedimiento seguro de alta nueva, si se considera necesario.
4. No afirmar que la desinstalación del otro extremo genera una señal instantánea y fiable. Al detectar y verificar una instalación anterior, invalidar su capacidad de consultar; mantener en B no reinstalado solamente la posición antigua en los casos permitidos por D-10.
5. Dar precedencia a revocaciones/bloqueos/eliminaciones frente a mensajes antiguos; registrar una versión/tombstone local para impedir que entregas atrasadas resuciten relaciones o datos borrados. Política de expiración de tombstones y de datos remotos: `PENDIENTE` de privacidad.

## 6. Pruebas negativas necesarias — NO EJECUTADAS

| Caso | Resultado exigido | Pendiente |
|---|---|---|
| Actualización de app, mismo usuario/dispositivo | No cambia ID ni recupera/eleva permisos | Matriz de Android |
| Reinstalación limpia A y B | ID nuevo, cero autorizaciones y ubicaciones propias | QA en ambos roles |
| Restore cloud y D2D, con y sin copia antigua | No resucita ID, relaciones, claves ni posición en instalación nueva | API/target/OEM |
| Copia de QR/ID, BD, preferencias o tokens en C | C no autentica como B ni puede consultar A | Simulación de suplantación |
| Clave privada inaccesible, restore parcial o corrupted state | No se acepta identidad o permiso antiguo; fail-closed | Recuperación |
| Revocación aplicada entre captura y gate de liberación, incluso con contenido ya preparado | Gate niega liberar dato; reintento o respuesta reordenada no usan validación anterior | Prueba de serialización por relación |
| Revocación después de liberar, entrega retrasada, reactivación y respuesta de revisión anterior | Precisar límite de red; B vuelve a validar antes de mostrar y descarta respuesta de época anterior; documentar riesgo residual de paquete ya emitido | Matriz de orden y límites distribuidos |
| ID inexistente frente a ID existente no divulgable, solicitante sin derecho | Respuesta indistinguible por cuerpo, código, longitud, cabeceras, tiempo y metadatos observables; no oráculo de existencia | Opción B / SEG-02; pruebas estadísticas negativas |
| Falla verificador o conectividad | No nueva ubicación; última legítima solo si permitida, con timestamp anterior | SEG-01/D-10 |
| A se reinstala y B sigue instalado | B puede mostrar la última anterior, no consultar a A antiguo | D-10 |
| B reinstalado | No recupera ubicación ni alias anterior | SEG-04 |
| B elimina posición mientras llega respuesta | No resucita ni cambia timestamp | D-10 |
| Backup/restauración de OEM diferente o dispositivo rooteado | Documentar cobertura real y riesgo residual; no afirmar invulnerabilidad | Pruebas y amenaza |

No se ha ejecutado código, test Android, `adb` ni una auditoría de dispositivos. Cualquier prototipo exige issue y autorización diferenciadas.

## 7. Pendientes y handoff

- **TECH LEAD — [#24](https://github.com/mundoinformaticacanaria/whereis/issues/24), label `TECH LEAD`:** coordinar SEG-01/02/05–07 y validación del gate de revocación, identidad, disponibilidad de verificador y anti-enumeración; la **opción B D-09/SEG-02 ya está CONFIRMADA** por PROPIETARIO, sin que ello cierre la seguridad técnica.
- **PROPIETARIO — [#41](https://github.com/mundoinformaticacanaria/whereis/issues/41), label `PROPIETARIO`:** decisiones jurídicas de menores, conservación/borrado, base de legitimación, tratamiento por terceros y costes cuando corresponda. [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37) mantiene pendiente la decisión expresa del ejecutor formal de ARQUITECTO.
- **FUNCIONAL/TECH LEAD:** si se pretende definir el caso de clave perdida sin desinstalación o modificar experiencia confirmada, registrar nueva decisión material; revisar integración D-09/PR #25.
- **TECH LEAD:** validar disponibilidad y modelo de verificador, versiones Android objetivo, superficie de datos, presupuesto, métricas y plan de ensayos; no asignar PROGRAMADOR con #28 abierto.
- **ARQUITECTO (chat ChatGPT independiente designado en #37 B):** completar revisión adversarial del ADR con [#22](https://github.com/mundoinformaticacanaria/whereis/issues/22), sin autoaprobarla ni actuar como QA/TECH LEAD. El handoff formal e integración por TECH LEAD dependen de regularizar G-02 en `main` y de revisar la propuesta sobre su HEAD. Esta PR **no marca** seguridad resuelta.
- **Gobernanza [#37](https://github.com/mundoinformaticacanaria/whereis/issues/37):** la opción **B está CONFIRMADA** por PROPIETARIO: chat ChatGPT independiente sustituirá a Codex como ejecutor del rol ARQUITECTO. #37 tiene ahora label `TECH LEAD` para registrar en rama/PR e integrar esa enmienda en G-02. El texto actual de `main` todavía identifica a Codex hasta que se complete ese paso. [#28](https://github.com/mundoinformaticacanaria/whereis/issues/28) permanece bajo TECH LEAD para gates. Mantener esta PR en borrador.

## 8. Fuentes de viabilidad externas (no sustituyen GitHub)

- [Android Backup](https://developer.android.com/identity/data/backup)
- [Auto Backup y exclusiones](https://developer.android.com/identity/data/autobackup)
- [Android 12: cambios de extracción](https://developer.android.com/about/versions/12/behavior-changes-12)
- [Context.getNoBackupFilesDir](https://developer.android.com/reference/android/content/Context#getNoBackupFilesDir())
- [Pruebas de backup](https://developer.android.com/identity/data/testingbackup)

**Estado de esta ADR: solo `PROPUESTA`; no actualizar `docs/arquitectura.md` como arquitectura vigente.**
