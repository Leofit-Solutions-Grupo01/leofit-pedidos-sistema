# Diagramas de Arquitectura — Leofit Pedidos

## Propósito
Este directorio contiene 7 diagramas que responden preguntas
específicas del comité evaluador sobre el funcionamiento del
sistema. Cada diagrama tiene su fuente Mermaid editable y su
render SVG.

## Índice

| ID | Pregunta que responde | Ubicación | Formato |
| --- | --- | --- | --- |
| D1 | Flujo de comunicación end-to-end | `./D1-end-to-end-http/` | sequenceDiagram |
| D2 | Flujo entre áreas/módulos | `./D2-modulos/` | flowchart |
| D3 | Contratos de API | `./D3-contratos-api/` | classDiagram + tabla |
| D4 | Formato de retorno JSON | `./D4-formato-retorno/` | classDiagram |
| D5 | Flujo de un pedido típico | `./D5-crear-pedido/` | sequence + flowchart |
| D6 | Evaluación de rendimiento | `./D6-rendimiento/` | flowchart |
| D7 | Topología de despliegue | `./D7-despliegue/` | flowchart |

## GAPs consolidados
Lista única de todos los GAPs marcados en los 7 diagramas:
- PedidoForm.tsx no consume el endpoint POST /api/orders (D1, D5).
- Auth flow: verificar si el frontend usa sessionStorage o cookies (D4).
- No hay OpenTelemetry / Prometheus / APM (D6).
- No hay SLIs/SLOs definidos (D6).
- No hay tests de carga en CI/CD (D6).
- Backend no desplegado en producción (D7).
- No hay Dockerfile de producción (D7).
- No hay IaC / K8s (D7).

## Cómo regenerar todos los SVG
```bash
cd docs/diagramas
for d in D*/; do
  cd "$d"
  for f in *.mmd; do
    mmdc -i "$f" -o "${f%.mmd}.svg"
  done
  cd ..
done
```

## Nota sobre el peso
Cada SVG pesa ~200 KB por tipografía embebida.
Para versiones optimizadas: mmdc --no-svg-fonts (verificar
visualmente antes de commitear).

## Versión
- Fecha: 2026-10-07
- Commits: D1-D7 (ver `git log --oneline docs/diagramas/`)
