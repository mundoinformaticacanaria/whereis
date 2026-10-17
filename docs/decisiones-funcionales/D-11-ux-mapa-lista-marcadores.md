# D-11 — Mapa, lista y marcadores

- **Fecha:** 17/10/2026 (acuerdos del 16–17/10/2026)
- **Estado:** `CONFIRMADO` para las elecciones expresas del PROPIETARIO, `PENDIENTE` para los límites identificados.
- **Clasificación:** `MATERIAL`.
- **Fuente viva:** [issue #21](https://github.com/mundoinformaticacanaria/whereis/issues/21). Su cuerpo y comentarios prevalecen ante cambios posteriores.
- **Integración:** revisión por TECH LEAD, no constituye baseline MVP ni habilita implementación.

## Clasificación y estado
**MATERIAL — diseño de comportamiento de interfaz.**
**CONFIRMADO por PROPIETARIO** durante decisiones del 17/10/2026; actualización GitHub expresamente solicitada. Completa D-07/D-08 sin seleccionar stack.

## Contrato aprobado
1. Pantalla principal **dividida**: mapa interactivo siempre visible en parte superior y lista debajo. Puede **maximizarse solo el mapa** ocultando lista; restaurarlo recupera división. La lista no maximiza ocultando el mapa. Al abrir, el mapa encuadra ubicaciones disponibles; si ninguna, usa ubicación propia de referencia cuando Android lo permita, con marcador propio visible cuando exista; si no, mapa general sin coordenadas falsas.
2. Lista única de conocidos en **orden alfabético por alias y, si no existe, ID Whereis**; filtros Todos/Autorizados/No autorizados/Pendientes (pendientes de solicitud pueden residir en sección separada hasta ser conocidos). Búsqueda incremental por alias o ID compatible con filtros, que afectan tanto a lista como a marcadores; al ocultar seleccionado se deselecciona. Bloqueados no figuran en vista habitual. El orden completo, no la vista filtrada, define la numeración de marcadores; al cambiar alias se recalcula.
3. Alias **opcional, editable e independiente por usuario consultante**; si falta, mostrar ID Whereis. Foto **opcional desde galería**, editable, recortable/ajustable, eliminable; color de borde personalizable por usuario; foto/color también en la lista.
4. Marcadores **circulares**: si hay foto, mostrarla sin número; si no hay, número de orden alfabético completo. Siempre borde de color personalizado. Si falta autorización pero hay posición anterior legítima, añadir pequeño **candado** sin reloj de antigüedad sobre marcador; antigua se informa textualmente en lista/ficha. Nunca marcador para posición inexistente.
5. Marcadores próximos se **agrupan** con contador; pulsar grupo despliega alrededor los individuales («araña»). Reagrupar al pulsar fuera, cambiar zoom o volver a pulsar agrupador; tras cerrar la ficha individual, el grupo permanece desplegado. «Whereis» sobre seleccionado agrupado centra, despliega y destaca su marcador.
6. Pulsar elemento de **lista solo selecciona**, sin centrar ni abrir ficha. Botón **«Whereis»** centra mapa en última ubicación ya conocida sin actualizar; si no hay ubicación, deshabilitado con «Ubicación no disponible». Actualizar uno desde pantalla principal funciona incluso sin marcador, si está autorizado.
7. Pulsar marcador selecciona elemento de lista (desplazar para hacerlo visible) y abre **ficha inferior modal**; mientras abierta no se interactúa con mapa/lista/filtros ni se cambia a otra ficha. Cerrar con deslizar hacia abajo, pulsar fuera o X; mantiene la selección y conserva modo mapa maximizado. Abrir ficha en mapa maximizado no restaura división. Ficha expandible/contraíble dentro de su superficie; el contenido del mapa no es interactivo hasta cerrar.
8. **SUPERSEDED** propuestas anteriores: «lista en pantalla separada», «abrir ficha al pulsar lista», «marcador con ID largo», «mapa interactivo con ficha abierta» y «reloj en marcador». Vigentes: foto o número, borde de color, modal.

## Criterios de aceptación
- D11-CA01: pantalla partida y maximización unilateral del mapa, sin perder selección.
- D11-CA02: lista ordenada por alias/ID; búsqueda incremental/filtrado consistente mapa y lista, numeración estable ante filtros.
- D11-CA03: foto opcional sustituye número; color/alias individuales; sin foto aparece número.
- D11-CA04: seleccionar en lista no abre ficha; «Whereis» solo centra la posición anterior; seleccionar marcador abre ficha modal y sincroniza lista.
- D11-CA05: agrupaciones desplegadas/reagrupadas según reglas y mantención al cerrar ficha.
- D11-CA06: sin ubicación no hay marcador, pero sí operación «Actualizar ubicación» manual si autorizado; ubicación propia solo si Android permite obtenerla.

## PENDIENTE / validación
Accesibilidad, legibilidad de números/fotos pequeñas y colores, pantallas pequeñas, coste de mapas, cartografía abierta, posición de controles y factibilidad del overlay. No elegir biblioteca/proveedor. Handoff **TECH LEAD**; relacionadas D-07 #14 y D-08 #16.
