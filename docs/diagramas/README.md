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

## GAPs Consolidados y Estado de Resolución (Cierre APF3)

| GAP Técnico Original (2026-10-07) | Estado Actual (APF3 / Producción v2.0.0) | Evidencia y Resolución |
| :--- | :---: | :--- |
| `PedidoForm.tsx` no consume `POST /api/orders` | **RESUELTO** | `frontend/src/pages/PedidoForm.tsx` consume activamente `createOrder()` contra la API REST. |
| Backend no desplegado en producción | **RESUELTO** | Desplegado y verificado en Render (`https://leofit-backend-api.onrender.com/api/health`). |
| No hay Dockerfile de producción | **RESUELTO** | Configurado en `docker-compose.yml` y `render.yaml` con build nativo de Node.js 20. |
| SLIs / SLOs y Pruebas de Carga | **RESUELTO** | SLI de latencia < 300 ms verificado con K6 y coexistencia ISO 25010 (latencia media 2.85 ms, P95 5.8 ms). |
| Línea de Actividad Reciente | **RESUELTO** | Endpoint `/api/dashboard/activity` y componente `RecentActivity.tsx` implementados. |
| Separación modular de mocks | **MITIGADO** | Tipos aislados en interfaces de TypeScript en frontend/backend. |

## Cómo regenerar todos los SVG

### Bash (Linux/Mac/WSL)
```bash
for d in D*/; do (cd "$d" && for f in *.mmd; do mmdc -i "$f" -o "${f%.mmd}.svg"; done); done
```

### PowerShell (Windows)
```powershell
Get-ChildItem -Directory | ForEach-Object {
  Push-Location $_.FullName
  Get-ChildItem *.mmd | ForEach-Object {
    mmdc -i $_.Name -o ($_.Name -replace '\.mmd$', '.svg')
  }
  Pop-Location
}
```

## Nota sobre el peso
Cada SVG pesa ~200 KB por tipografía embebida.
Para versiones optimizadas: mmdc --no-svg-fonts (verificar
visualmente antes de commitear).

## Versión
- Fecha: 2026-10-07
- Commits: D1-D7 (ver `git log --oneline docs/diagramas/`)
