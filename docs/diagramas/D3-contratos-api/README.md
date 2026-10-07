# D3 — Contratos de cada llamada (API)

## Pregunta que responde
¿Qué endpoint recibe qué, qué devuelve, con qué códigos de error y bajo qué schemas de datos?

## Tabla de Endpoints y Contratos

| Endpoint | Método | Request Payload (Body / Query) | Response Payload | Códigos HTTP |
| -------- | ------ | ------------------------------ | ---------------- | ------------ |
| `/api/auth/login` | `POST` | `{ email: string, password: string }` | `{ success: true, message: string, data: { token: string, user: { id, name, role } } }` | `200 OK`, `400 Bad Request`, `401 Unauthorized`, `429 Too Many Requests` |
| `/api/orders` | `GET` | `?page, limit, status, dateFrom, dateTo, search` | `{ success: true, count: number, total: number, data: Order[] }` | `200 OK`, `401 Unauthorized` |
| `/api/orders` | `POST` | `CreateOrderDTO` (ver diagrama de clases) | `{ success: true, message: string, data: Order }` | `201 Created`, `400 Bad Request`, `401 Unauthorized`, `409 Conflict` |
| `/api/orders/:id` | `GET` | (URL Param: `id`) | `{ success: true, data: Order }` | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `/api/orders/:id/status` | `PATCH` | `{ status: OrderStatus, comments?: string }` | `{ success: true, message: string, data: Order }` | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `/api/dashboard/stats` | `GET` | (Ninguno) | `{ success: true, data: DashboardMetrics }` | `200 OK`, `401 Unauthorized` |

*Nota: Todas las llamadas a rutas protegidas exigen el Header HTTP `Authorization: Bearer <jwt_token>`.*

## Fuentes por endpoint

| Endpoint | Definición de ruta | Validación Zod | Controlador |
| --- | --- | --- | --- |
| POST /api/auth/login | `backend/src/routes/auth.routes.ts:14` | `LoginSchema` en validateBody | `auth.controller.ts` |
| GET /api/orders | `backend/src/routes/order.routes.ts:17` | N/A | `order.controller.ts:48` |
| POST /api/orders | `backend/src/routes/order.routes.ts:19` | `CreateOrderSchema` | `order.controller.ts:136` |
| GET /api/orders/:id | `backend/src/routes/order.routes.ts:18` | N/A | `order.controller.ts:81` |
| PATCH /api/orders/:id/status | `backend/src/routes/order.routes.ts:20` | `UpdateOrderStatusSchema` | `order.controller.ts:178` |
| GET /api/dashboard/stats | `backend/src/routes/dashboard.routes.ts:11` | N/A | `dashboard.controller.ts` |

## Diagrama de Clases
El archivo `diagram.svg` anexo a este documento ilustra las entidades core que viajan en estos contratos, particularmente la compleja estructura de `CreateOrderDTO` y el `Order Aggregate`.

## Nota sobre el tamaño
El SVG pesa ~200 KB porque mmdc embebe una tipografía completa.
Para versiones optimizadas, regenerar con mmdc --no-svg-fonts (verificar visualmente antes de commitear).

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
