# Criterios permanentes de desarrollo y revisión

## Objetivo

Construir software sencillo, robusto, comprobable y evolutivo, evitando tanto deuda evitable como sobrearquitectura.

## RUTINARIA vs MATERIAL

- **RUTINARIA**: acción factual o mecánica sin interpretación material.
- **MATERIAL**: requisitos, baseline, arquitectura, seguridad, privacidad, persistencia, proveedores, infraestructura, costes, alcance, refactor estructural, código o merge.

Ante duda: MATERIAL.

## Presupuesto de complejidad

Preferir la solución más simple que cumpla el contrato confirmado. Una nueva capa, abstracción, servicio, dependencia o infraestructura necesita evidencia de una frontera o problema real.

## Clean Code y SOLID

Aplicar de forma proporcional:

- nombres que expresen intención;
- unidades pequeñas y cohesionadas;
- responsabilidad única real;
- dependencias orientadas hacia contratos propios;
- errores y tipos explícitos;
- duplicación eliminada cuando pueda divergir;
- tests de comportamiento e invariantes.

No aplicar patrones por estética ni crear interfaces o capas sin necesidad demostrada.

## Refactor

- **REFACTOR AHORA**: una frontera vigente está rota o la siguiente ampliación sería peligrosa.
- **REFACTOR CON LA FEATURE**: mejora pequeña necesaria para implementar bien la feature.
- **DEUDA REGISTRADA**: deuda real no bloqueante con trigger observable.
- **NO REFACTOR**: sin beneficio actual demostrado.

## Granularidad

El trabajo ejecutable debe ser el bloque mínimo útil, determinista, verificable y cerrable.

Cada issue de desarrollo debe tender a:

- una responsabilidad principal;
- comportamiento observable;
- criterios de aceptación;
- exclusiones explícitas;
- dependencias claras;
- PR pequeña y cohesionada.

## Paralelismo

Tech Lead debe buscar proactivamente trabajo independiente útil cuando haya capacidad libre, pero no debe fabricar tareas para ocupar agentes.

## Asignación por complejidad

Definir en cada proyecto qué ejecutores están disponibles y qué perfil de complejidad pueden asumir.

Reglas base:

- el ejecutor nunca justifica reducir calidad;
- el trabajo crítico debe ir al ejecutor con mayor capacidad y contexto;
- los trabajos paralelos deben ser realmente independientes;
- no solapar ramas sobre la misma superficie sin necesidad demostrada.

## Calidad

Cada proyecto debe adaptar los gates al stack real. Baseline recomendado:

- lint/análisis estático;
- type checking si el lenguaje lo soporta;
- tests automatizados;
- pruebas de comportamiento e invariantes;
- comprobación del diff/whitespace;
- sin secretos;
- sin datos reales no autorizados;
- sin llamadas externas accidentales;
- documentación factual actualizada cuando el cambio la vuelva obsoleta.

No degradar herramientas para obtener verde.

## Revisión estructural

Tech Lead revisa periódicamente estructura, higiene de GitHub, documentos superados, labels, ramas y duplicaciones, especialmente al cerrar hitos relevantes.

## Gates y handoff

Flujo base de código:

`PROGRAMADOR → QA → TECH LEAD`

QA no sustituye la revisión final del Tech Lead.

Un cambio del head SHA invalida revisiones previas para merge.

## Proveedores

No introducir proveedores, SDKs, servicios de pago o infraestructura real sin autorización explícita y sin encapsularlos detrás de contratos propios cuando corresponda.
