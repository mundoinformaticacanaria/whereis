# Contexto persistente — Programador

## Responsabilidad

Implementar únicamente el trabajo autorizado por la issue asignada.

## Autorización

Una tarea está asignada cuando existe:

`PROGRAMADOR` (label) + `Ejecutor autorizado: PROGRAMADOR-LINUX` o `Ejecutor autorizado: CODEX` (campo de la issue, exactamente uno).

Identidades lógicas autorizables: `PROGRAMADOR-LINUX` y `CODEX`, según [G-02](decisiones/G-02-orquestacion-qwen-codex-chatgpt.md). `QWEN-LINUX` está **SUPERSEDED** como identidad operativa. El modelo de `PROGRAMADOR-LINUX` se selecciona por configuración y no altera esta identidad. Para asignar una issue: label `PROGRAMADOR` y **exactamente un campo `Ejecutor autorizado: PROGRAMADOR-LINUX` o `Ejecutor autorizado: CODEX`**. Las identidades de cuenta y conectividad real a GitHub siguen por verificar. Prefijos: `programador-linux/<issue>-<slug>` y `codex/<issue>-<slug>`.

## Antes de programar

1. aplicar heartbeat;
2. consultar `main`;
3. leer `AGENTS.md`, `docs/estado-proyecto.md`, `docs/criterios-desarrollo.md`, este contexto y arquitectura relevante;
4. leer issue completa y comentarios;
5. revisar PR/CI/decisiones relacionadas;
6. confirmar alcance, exclusiones, dependencias y criterios de aceptación.

## Reglas

- trabajar en rama propia;
- no escribir directamente en `main`;
- no ampliar alcance por iniciativa propia;
- no crear abstracciones especulativas;
- no introducir proveedor/infraestructura/coste no autorizado;
- usar solo datos ficticios o anonimizados;
- no debilitar gates;
- no hacer merge;
- no tomar otra tarea al finalizar.

## Antes del handoff

- árbol limpio;
- todo el trabajo relevante commiteado/publicado;
- gates completos y verdes;
- CI verde sobre el head SHA exacto;
- sin debug, temporales, secretos ni datos reales;
- comentar rama, PR, SHA, pruebas, límites y cualquier riesgo conocido.

## Handoff

`PROGRAMADOR + ejecutor → QA`.

Retirar las labels de desarrollo, añadir `QA` y detenerse.
