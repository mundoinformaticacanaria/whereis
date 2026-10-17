# Seguridad y cierre del MVP — pendientes materiales

- **Fecha:** 17/10/2026
- **Estado:** `PROPUESTA` / `PENDIENTE` de estudio y aprobación.
- **Fuente viva:** [issue #24](https://github.com/mundoinformaticacanaria/whereis/issues/24).
- **No constituye baseline aprobado**, ni permiso de implementación, ni selección de proveedor.

## Clasificación
**MATERIAL — PROPUESTA / PENDIENTE**. La petición general del PROPIETARIO (17/10/2026) de priorizar seguridad, resolver lo rutinario y actualizar GitHub no equivale a aprobar por defecto decisiones con impacto legal, de seguridad o de arquitectura. No constituye baseline.

## Objetivo
Cerrar los riesgos de acceso a ubicación autorizada, especialmente por el uso familiar mencionado por el PROPIETARIO, **sin convertir Whereis en seguimiento oculto ni omitir protecciones de menores**. El consentimiento/control legítimo previsto en D-01 a D-05 sigue siendo condición del proyecto.

## Propuestas FUNCIONAL sujetas a aprobación / validación
1. **SEG-01 — Estado remoto no verificable (P0):** `PROPUESTA` denegar nuevas ubicaciones cuando no sea verificable la autorización vigente; conservar solo última ubicación legítima con fecha/hora y aviso, sin afirmar «revocación instantánea» hasta que se valide sincronización. **TECH LEAD** debe estudiar conectividad y consultas simultáneas; **PROPIETARIO** aprueba garantías/UX finales.
2. **SEG-02 — Identidad y abuso (P0):** `PROPUESTA` verificación robusta de instalación y autorización por relación; defensas ante suplantación, consulta con ID copiado, enumeración de IDs, repetición de solicitudes y bloqueo abusivo. Estudiar compatibilidad con decisiones D-09 de «ID no encontrado» y reenvío inmediato tras rechazo; si hay contradicción, elevar alternativas al PROPIETARIO sin modificar las aprobadas.
3. **SEG-03 — Menores y tratamiento de datos (P0):** `PENDIENTE` revisar base de legitimación/consentimiento o representación legal aplicable, transparencia y derechos del menor, roles de responsables del tratamiento, accesibilidad del control en emisor, conservación y borrado. **Prioridad de seguridad no elimina obligaciones de privacidad**. No permitir acceso secreto o sin autorización conforme a condiciones de producto y legislación aplicable.
4. **SEG-04 — Retención indefinida hasta eliminación (P0):** D-10 recoge intención del PROPIETARIO (solo última ubicación), pero falta revisar limitación de conservación, almacenamiento en dispositivos/servicios, eliminación efectiva y copia de seguridad. No dar por definido dónde se almacena.
5. **SEG-05 — Android y notificaciones (P1):** TECH LEAD verificará permisos y restricciones reales (incluidos estados sin interacción/ubicación desactivada), que un aviso por emisor/24h sea viable y que el reinicio del límite tras activar/desactivar pueda detectarse, además de política de fallos y ahorro de batería.
6. **SEG-06 — Acuses y desconexión (P1):** especificar «recibida» solo si la solicitud está realmente disponible en la app destinataria; distinguir «entrega no confirmada» y «rechazada»; idempotencia estricta. Estado remoto «sin conexión» solo si verificable.
7. **SEG-07 — Proveedores, mapas, direcciones, coste (P1):** selección de fuente de mapas/direcciones, licencias y costes reservada a TECH LEAD para evaluación y PROPIETARIO para autorización material.

## Criterios previos al baseline funcional
- Matriz de amenazas mínimas para ID/suplantación/permiso/revocación/bloqueo y pruebas negativas verificables.
- Demostración de comportamiento al fallar red y frente a operaciones concurrentes.
- Política de conservación/eliminación revisada para datos de localización de menores.
- Compatibilidad real por versión Android y permisos, sin prometer capacidades inexistentes.
- Costes/proveedores revisados y autorización separada.
- Aprobación material específica del PROPIETARIO antes de declarar cerrado cada punto y del baseline final; QA independiente en desarrollo.

## Estado / Handoff
`PROPUESTA`, `PENDIENTE` de TECH LEAD y PROPIETARIO. Relacionadas D-01 a D-13, en especial #19–#23; no habilita programación ni infraestructura. ARQUITECTO solo si se autoriza activación puntual.
