# Baseline arquitectónico

**Estado:** PENDIENTE DE PROYECTO

## Objetivo

Este documento debe describir la arquitectura vigente del proyecto destino y actuar como referencia técnica canónica.

## Decisiones mínimas a completar

- estilo arquitectónico;
- módulos/contextos principales;
- dirección de dependencias;
- límites entre dominio, aplicación, presentación e infraestructura;
- estrategia de persistencia;
- contratos con proveedores externos;
- seguridad y autenticación;
- observabilidad;
- despliegue e infraestructura;
- restricciones de coste y operación;
- decisiones explícitamente POST-MVP.

## Principios por defecto

Mientras no exista una decisión más específica:

- preferir monolito modular antes que arquitectura distribuida;
- dependencias hacia el núcleo del negocio;
- dominio independiente de frameworks e infraestructura cuando exista lógica de dominio;
- aplicación dependiente de dominio y puertos propios;
- adaptadores implementando puertos;
- configuración específica del cliente fuera del core reusable;
- contratos provider-neutral cuando exista riesgo real de acoplamiento;
- evitar microservicios, colas distribuidas, Kubernetes, event sourcing, SPA separada u otras piezas sin necesidad demostrada.

## Regla

Este documento no debe contener arquitectura aspiracional presentada como vigente. Toda decisión debe indicar si está `CONFIRMADA`, `PROPUESTA`, `PENDIENTE`, `POST-MVP` o `SUPERSEDED`.
