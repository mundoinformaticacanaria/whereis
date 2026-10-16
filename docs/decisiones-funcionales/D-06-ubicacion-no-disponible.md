# D-06 — Consulta fallida: última ubicación conocida con fecha y hora

- **Fecha de aprobación del Propietario:** 16/10/2026.
- **Clasificación:** `MATERIAL` — definición funcional.
- **Estado de decisión:** `CONFIRMADO` por aprobación expresa; documento todavía `PENDIENTE` de revisión/integración en `main`.
- **Issue:** [#12 — D-06](https://github.com/mundoinformaticacanaria/whereis/issues/12).
- **Decisiones relacionadas:** [D-01 #1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02 #2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-04 #8](https://github.com/mundoinformaticacanaria/whereis/issues/8), [D-05 #10](https://github.com/mundoinformaticacanaria/whereis/issues/10).
- **Baseline funcional completo del MVP:** `PENDIENTE`; esta decisión no lo aprueba.
- **Decisiones históricas sustituidas:** ninguna. Se concreta un aspecto que permanecía `PENDIENTE` en D-02.

## Necesidad

Cuando no se puede obtener una nueva ubicación en una consulta puntual autorizada, la aplicación debe dejar clara la falta de respuesta actual y, cuando exista, ofrecer la última ubicación previamente obtenida sin inducir a error sobre su antigüedad.

## Actores y precondiciones

- **A:** dispositivo cuya ubicación se consulta.
- **B:** dispositivo consultante que está autorizado conforme a D-03/D-05 para solicitar una nueva ubicación.
- Se refiere a **fallos en una consulta que B podía realizar**, por ejemplo debido a falta de conectividad, indisponibilidad del dispositivo A, permisos Android o limitaciones de ejecución.
- **No** se interpreta como autorización para solicitar nuevas ubicaciones cuando A ha desactivado el permiso: en ese caso se aplica **D-05**.

## Decisión del Propietario — CONFIRMADO

1. **Aviso de fallo:** si una consulta puntual autorizada no puede obtener una nueva ubicación de A, Whereis informa explícitamente de que no se pudo actualizar la posición.
2. **Fallback informativo:** si B ya obtuvo con autorización una ubicación anterior de A, conserva y muestra **la última ubicación conocida**, acompañada de su **fecha y hora**, y una advertencia visible de que **no es actual**.
3. **Separación temporal:** la fecha y hora que acompañan esa ubicación representan la obtención previa; **no se sustituyen por la hora de la consulta fallida** ni se da a entender que la posición antigua es una posición reciente.
4. **Sin posición previa:** si B **nunca obtuvo una ubicación válida** de A, Whereis muestra «**Ubicación no disponible**» en lugar de coordenadas o ubicaciones ficticias.
5. **Sin consulta continua:** el fallo no provoca un modo de seguimiento continuo, ni actualizaciones periódicas automáticas. Las consultas siguen siendo iniciadas manualmente según D-01.

## Ejemplo de comportamiento

Se utiliza un ejemplo ficticio, no datos de una persona real:
- B obtuvo la ubicación de A el 16/10/2026 a las 14:00.
- A las 19:00, B solicita actualizar, pero la consulta falla por una condición de conectividad.
- Whereis muestra un aviso equivalente a «No se pudo actualizar la ubicación», conserva la posición previa y la identifica «Última ubicación conocida: 16/10/2026 14:00 — no es actual».
- Si nunca existió ubicación anterior, se muestra «Ubicación no disponible».

El texto exacto de las pantallas puede ajustarse durante el diseño UX sin alterar la obligación de informar del fallo y de la antigüedad.

## Reglas funcionales

- **D06-RN01:** un error en una consulta **no es** una ubicación nueva ni permite marcar el resultado anterior como ubicación actual.
- **D06-RN02:** solo se puede mostrar como último dato una ubicación **realmente obtenida en una consulta anterior autorizada**; no se infieren ni inventan coordenadas.
- **D06-RN03:** no se actualiza la fecha y hora asociada a la última posición al fallar la nueva consulta.
- **D06-RN04:** si la ubicación previa no existe o ya no puede mostrarse legítimamente, el resultado será «Ubicación no disponible». La política general de retención continúa `PENDIENTE`.
- **D06-RN05:** la revocación de D-05 impide nuevas ubicaciones; **no** se debe usar D-06 para intentar consultas sin permiso. La opción B aprobada de D-05 permite conservar visible la última ubicación fechada cuando el permiso ha sido desactivado.
- **D06-RN06:** la desinstalación/reinstalación mantiene las reglas de identidad y autorización de D-04; D-06 **no** autoriza restaurar permisos ni posiciones antiguas tras una nueva instalación.

## Criterios de aceptación

- **D06-CA01:** B realiza una consulta autorizada que falla y ya dispone de última ubicación válida: Whereis comunica el fallo, presenta la última ubicación previa con fecha y hora.
- **D06-CA02:** dicha posición se identifica de forma inequívoca como «última conocida», «anterior» o equivalente, y no como ubicación actual.
- **D06-CA03:** el intento fallido **no cambia** la fecha/hora de la ubicación previa.
- **D06-CA04:** B realiza una consulta autorizada que falla sin historial de ubicación válida: se muestra «Ubicación no disponible», sin coordenadas inventadas.
- **D06-CA05:** el error no inicia reintentos periódicos automáticos ni un seguimiento continuo.
- **D06-CA06:** al desactivarse el permiso de B conforme a D-05, una nueva petición de B no obtiene una nueva posición por la vía de D-06.

## Validaciones, errores y asuntos PENDIENTES

- Cuánto tiempo se conserva una última ubicación, y en qué circunstancias se elimina o deja de estar disponible.
- Detalle de errores diferenciados (sin conexión, apagado, permisos denegados, ejecución restringida, timeout), reintentos y tiempos de espera.
- Reglas de ubicación aproximada/precisa y presentación de precisión o exactitud.
- Diferencias entre hora de captura, hora de recepción y zona horaria mostrada: el contrato exige **fecha y hora de la ubicación previamente obtenida**, no el instante de fallo. La fuente y formato exactos los validará TECH LEAD.
- Retención global, cifrado, persistencia, recuperación/restauración de posiciones, acceso offline, almacenamiento local o remoto.
- Revocación simultánea a consulta y aplicación de cambios sin conexión, pendiente de D-05/estudio técnico.
- Requisitos de accesibilidad/UX precisos para señalización de fallo y antigüedad.
- No se aprueba guardar un **historial** de trayectos ni nuevas categorías de datos; solo el uso funcional de la última ubicación ya obtenida.

## Riesgos e impacto

- **Privacidad:** conservar una posición antigua revela un dato personal aun si está etiquetado como anterior; requiere normas de acceso y retención.
- **Seguridad:** la consulta fallida no debe sortear el consentimiento; distinguir permiso activo de dato obtenido históricamente.
- **Alcance:** consulta puntual (D-01), ejecución condicionada por Android (D-02) y conservación de última ubicación tras revocar (D-05).
- **Arquitectura / costes:** `PENDIENTE`; TECH LEAD evaluará mecanismo mínimo que cumpla el contrato sin introducir proveedores o infraestructura sin autorización.

## Trazabilidad y siguiente acción

[Issue #12](https://github.com/mundoinformaticacanaria/whereis/issues/12). La regla de D-02 «no presentar una ubicación antigua como actual» sigue `CONFIRMADA` y queda especificada con este comportamiento de último dato conocido, no sustituida.

**TECH LEAD** revisará el documento y la PR asociada sobre su head SHA correspondiente. No se habilita desarrollo, proveedor, gasto, almacenamiento o baseline funcional general.
