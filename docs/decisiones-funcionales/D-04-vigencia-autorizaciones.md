# D-04 — Duración y extinción de autorizaciones

- **Fecha de decisión:** 16/10/2026.
- **Clasificación:** MATERIAL.
- **Estado:** CONFIRMADO **solo** respecto de la ausencia de caducidad temporal y extinción por revocación o desinstalación; detalles de reinstalación y tratamiento remoto PENDIENTES.
- **Issue:** [#8](https://github.com/mundoinformaticacanaria/whereis/issues/8).
- **Relación:** [D-01/#1](https://github.com/mundoinformaticacanaria/whereis/issues/1), [D-02/#2](https://github.com/mundoinformaticacanaria/whereis/issues/2), [D-03/#6](https://github.com/mundoinformaticacanaria/whereis/issues/6).
- **Baseline funcional global:** PENDIENTE.
- **Decisiones sustituidas:** ninguna registrada.

## Necesidad
Definir durante cuánto tiempo B puede consultar la ubicación de A una vez que A ha aceptado su solicitud de vinculación.

## Actores
- A: dispositivo cuya ubicación se comparte.
- B: dispositivo que ha sido autorizado individualmente.

## Comportamiento CONFIRMADO por el Propietario
1. Las autorizaciones entre dispositivos no tienen **caducidad automática por el transcurso del tiempo**.
2. Su vigencia termina por **revocación expresa** o **desinstalación de la aplicación Whereis**.
3. La ausencia de caducidad no implica capturas continuas: solo se realizan las consultas puntuales de D-01/D-02, cuando sea posible.

## Casos / criterios verificables derivados del comportamiento confirmado
- **D04-CA01:** una autorización vigente no caduca simplemente porque transcurra cierto número de días.
- **D04-CA02:** no se exige una nueva autorización en cada consulta si sigue vigente (D-01/D-03).
- **D04-CA03:** cuando se aplica una revocación válida, el dispositivo previamente autorizado ya no puede realizar nuevas consultas (detalle operativo en D-05).
- **D04-CA04:** tras confirmarse que una instalación ya no es válida, no se facilita nueva ubicación atribuible a esa instalación; la forma de detectar y aplicar la desinstalación exige contraste técnico.

## PROPUESTA — NO APROBADA TODAVÍA
- Una **reinstalación de Whereis es una instalación nueva**, con un ID diferente y sin recuperar autorizaciones antiguas, tanto concedidas como recibidas. Se exigirán nuevas solicitudes y aceptaciones.
- La extinción por desinstalación se aplicará a cualquiera de los dos extremos de la autorización, emisor o consultante.

El Propietario expresó dudas sobre recuperar autorizaciones tras reinstalar y considera que probablemente no procede; no se debe convertir esa inclinación en confirmación de la regla precisa sin su aprobación.

## Errores, límites y riesgos PENDIENTES
- Una desinstalación no garantiza aviso inmediato al resto del sistema: el dispositivo que se elimina no recibe su propio broadcast de eliminación; también pueden fallar las señales remotas de disponibilidad.
- Android permite en ciertos casos restablecer datos desde una copia de seguridad al reinstalar la app. El diseño técnico deberá evitar reactivar autorizaciones si el Propietario aprueba la política de instalación nueva.
- La aplicación desinstalada del emisor no puede obtener nuevas posiciones, pero otros sistemas pueden mantener registros anteriores hasta detectar la baja; no se promete invalidación remota instantánea.
- Política para mostrar o eliminar ubicaciones previamente compartidas: PENDIENTE.
- Detalles de revocación, confirmación sin conexión, conservación de datos y tratamiento de recuperación: D-05 / decisiones posteriores.
- Arquitectura, autenticidad, persistencia, mecanismos de detección, proveedores e infraestructura: PENDIENTE de TECH LEAD.

## Fuera de alcance de esta decisión
No se aprueban periodos temporales, cuentas de usuario, recuperación de vinculaciones, tecnologías ni desarrollo.

## Siguiente acción
**PROPIETARIO** debe concretar el comportamiento tras reinstalación y el alcance en ambos extremos. **FUNCIONAL** actualizará la propuesta documental; después **TECH LEAD** revisará para integración. Esta decisión parcial no constituye aprobación del baseline MVP.
