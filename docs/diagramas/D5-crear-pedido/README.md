# D5 — Flujo de un pedido típico

## Pregunta que responde
¿Cómo se crea, valida, persiste y responde un pedido en el sistema?

## Decisiones de diseño
El diagrama se ha dividido en dos vistas para no sobrecargar cognitivamente al lector:
1. **Flujo HTTP (Secuencia):** Muestra el recorrido end-to-end de la petición desde Postman, atravesando la capa de middlewares, validación Zod, controlador y la respuesta JSON (Envelope).
2. **Transacción SQL (Flowchart):** Enfoca la vista exclusivamente en la capa de persistencia (`pg.repositories`), demostrando el uso explícito de `BEGIN ISOLATION LEVEL READ COMMITTED`, concurrencia pesimista (`FOR UPDATE`), y la atomicidad del proceso.

## Límites explícitos
- El diagrama asume que la petición viene de un cliente REST como Postman/cURL, evidenciando el `GAP` de que el frontend (`PedidoForm.tsx`) aún no está conectado.
- No se detallan las operaciones internas del Hash de autenticación, asumiendo un token válido.
- Los **reintentos con backoff exponencial** presentes en la implementación de base de datos no se dibujan como ciclos iterativos en el diagrama de secuencia para evitar ruido visual, pero se señalan mediante una Nota.

## Fuentes

| Nodo / Acción | Fuente (archivo:línea) |
| --- | --- |
| `POST /api/orders` (Endpoint) | `backend/src/routes/order.routes.ts:19` |
| `CreateOrderSchema` (Zod) | `backend/src/infrastructure/validators/schemas.ts:52` |
| `order.controller.createOrder` | `backend/src/controllers/order.controller.ts:136` |
| `pg.repositories.create` (Firma) | `backend/src/infrastructure/repositories/pg.repositories.ts:439` |
| `BEGIN ISOLATION LEVEL...` | `backend/src/infrastructure/repositories/pg.repositories.ts:453` |
| `SELECT ... FOR UPDATE` | `backend/src/infrastructure/repositories/pg.repositories.ts:478` |
| Tabla `orders` (Schema DB) | `database/schema.sql:148` |

## Nota sobre el tamaño
Los archivos SVG pesan ~200 KB porque `mmdc` embebe una tipografía completa (`Fira Code` / `SIL Open Font License`).
Para versiones optimizadas, se puede regenerar con `mmdc --no-svg-fonts` (verificando visualmente antes de commitear).

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i sequence.mmd -o sequence.svg
mmdc -i flowchart.mmd -o flowchart.svg
```

## Versión
- Fecha: 2026-10-07
