# D6 — Evaluación de rendimiento

## Pregunta que responde
¿Cómo se mide el rendimiento del sistema?

## Decisiones de diseño
Se ha utilizado un diagrama de flujo con dos zonas separadas visualmente (subgraphs) para contrastar el estado actual de observabilidad (basado exclusivamente en logs sincrónicos por consola y métricas de negocio) frente al objetivo propuesto (arquitectura de observabilidad estándar con métricas, SLIs y visualización en tiempo real).

## Límites explícitos
- El diagrama solo representa componentes de monitoreo de aplicación (APM/Observabilidad), no detalla métricas de infraestructura física (uso de CPU de la instancia, disco, etc.).
- La "ZONA 2" es estrictamente una propuesta arquitectónica; **no existe** código implementado para OpenTelemetry, Prometheus ni Grafana en el HEAD actual.

## GAPs a marcar explícitamente
- No hay OpenTelemetry, Prometheus ni APM instalado en `backend/package.json`.
- No hay SLIs ni SLOs definidos formalmente en el código o configuración.
- No hay instrumentación de latencia (P50/P95/P99), tasas de error formales ni Throughput midiendo el sistema.
- Los flujos CI/CD (`.github/workflows/`) **no incluyen jobs de pruebas de carga o rendimiento**.

## Fuentes

| Componente | Fuente |
| --- | --- |
| Morgan setup | `backend/src/app.ts:49` |
| Dependencias de observabilidad | `backend/package.json` (solo `morgan` instalado) |
| CI/CD Performance Jobs | `.github/workflows/backend-ci-cd.yml` (Ausentes) |

## Nota sobre el tamaño
El SVG renderizado pesa alrededor de 200 KB debido a que la herramienta `mmdc` incluye la tipografía completa de forma embebida.
Para versiones optimizadas, se puede regenerar con `mmdc --no-svg-fonts` (verificando visualmente antes de commitear).

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
