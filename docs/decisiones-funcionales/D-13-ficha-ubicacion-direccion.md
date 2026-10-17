# D-13 — Ficha, precisión y dirección

- **Fecha:** 17/10/2026 (acuerdos del 16–17/10/2026)
- **Estado:** `CONFIRMADO` para las elecciones expresas del PROPIETARIO, `PENDIENTE` para los límites identificados.
- **Clasificación:** `MATERIAL`.
- **Fuente viva:** [issue #23](https://github.com/mundoinformaticacanaria/whereis/issues/23). Su cuerpo y comentarios prevalecen ante cambios posteriores.
- **Integración:** revisión por TECH LEAD, no constituye baseline MVP ni habilita implementación.

## Clasificación y estado
**MATERIAL — precisión, visualización y tratamiento de datos de ubicación.**
**CONFIRMADO por PROPIETARIO** 17/10/2026, formalización en GitHub solicitada.

## Contrato aprobado
1. La **ficha inferior** de un marcador mostrará **ID Whereis** (llamado «nombre» en decisión previa), alias si existe, dirección disponible (calle/número y resto conocido), **fecha y hora real de obtención** y precisión. Botón «Actualizar ubicación» en ficha si hay autorización; al pulsarlo la ficha se cierra: en éxito individual se centra el mapa, en fallo permanece encuadre, error D-06.
2. Fecha y hora siempre **DD/MM/AAAA HH:mm:ss**, jamás «hace 2 horas», en **zona horaria del dispositivo consultante**, sin alterar instante real de posición. Mostrar «Ubicación anterior» cuando proceda. En lista también mostrar fecha/hora exacta; no representar posiciones antiguas como nuevas.
3. Precisión estimada cuando exista en **metros** (por ejemplo «Precisión: ±15 m»); si falta, **«Precisión no disponible»**. Aceptar ubicaciones aproximadas dejando claro el carácter aproximado.
4. Si dirección postal se puede obtener, mostrar información disponible aunque **incompleta** (por ejemplo calle sin número); no inventar datos. Si no hay dirección en absoluto, mostrar coordenadas decimales + **«Dirección no disponible»**. Cuando haya dirección suficiente, coordenadas no necesitan verse pero siempre podrán copiarse mediante **«Copiar ubicación»**, sin consulta GPS nueva.
5. Nueva posición se muestra **inmediatamente** con coordenadas, sin esperar a resolver calle/número. Mientras se averigua: «Buscando dirección…» junto a coordenadas; cuando finaliza, se actualiza la ficha. Nunca reutilizar dirección de una posición anterior para una nueva.
6. Fallo en búsqueda de dirección: mostrar «Dirección no disponible», coordenadas y botón **«Reintentar dirección»** que utiliza coordenadas existentes sin actualización GPS. No hay reintento automático por reabrir ficha. Si ya estaba buscando, cerrar ficha no cancela la búsqueda; el resultado queda disponible al volver a abrirla.

## Criterios de aceptación
- D13-CA01: ficha con ID Whereis/alias, fecha completa local, precisión o estado sin precisión.
- D13-CA02: dirección parcial se muestra parcial; si ausente se ven coordenadas y botón copiar; no se muestra dirección vieja para posición nueva.
- D13-CA03: marcador con coordenadas aparece antes que dirección; mensaje de búsqueda y posterior actualización.
- D13-CA04: fallo sin auto-reintentos, reintento manual no modifica coordenadas ni fecha original.
- D13-CA05: cerrar ficha durante búsqueda no cancela esa operación ni permite interacción con mapa mientras la ficha esté abierta.

## PENDIENTE / técnico
Precisión/semántica Android, permisos y geocodificación; dependencia de proveedores, licencias, datos de direcciones y coste: TECH LEAD propone alternativas. No se ha elegido tecnología, no se garantizan direcciones ni exactitud. Relacionadas D-06 #12, D-07 #14 y D-08 #16.
