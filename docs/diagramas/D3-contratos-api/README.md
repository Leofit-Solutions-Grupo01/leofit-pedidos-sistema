# D3 — Contratos de cada llamada (API)

## Pregunta que responde
¿Qué endpoint recibe qué, qué devuelve, con qué códigos de error y bajo qué schemas de datos?

## Tabla de Endpoints y Contratos

| Endpoint | Método | Request Payload (Body / Query) | Response Payload | Códigos HTTP |
| -------- | ------ | ------------------------------ | ---------------- | ------------ |
| `/api/auth/login` | `POST` | `{ email: string, password: string }` | `{ token: string, user: { id, name, role } }` | `200 OK`, `400 Bad Request`, `401 Unauthorized`, `429 Too Many Requests` |
| `/api/orders` | `GET` | `?page, limit, status, dateFrom, dateTo, search` | `{ data: Order[], total: number }` | `200 OK`, `401 Unauthorized` |
| `/api/orders` | `POST` | `CreateOrderDTO` (ver diagrama de clases) | `Order` (Creada) | `201 Created`, `400 Bad Request`, `401 Unauthorized` |
| `/api/orders/:id` | `GET` | (URL Param: `id`) | `Order` | `200 OK`, `401 Unauthorized`, `404 Not Found` |
| `/api/orders/:id/status` | `PATCH` | `{ status: OrderStatus, comments?: string }` | `Order` (Actualizada) | `200 OK`, `400 Bad Request`, `404 Not Found` |
| `/api/dashboard/metrics` | `GET` | (Ninguno) | `DashboardMetrics` | `200 OK`, `401 Unauthorized` |

*Nota: Todas las llamadas a rutas protegidas (excepto `/api/auth/login`) exigen el Header HTTP `Authorization: Bearer <jwt_token>`.*

## Fuentes
- Payload Schemas (`Zod`): `backend/src/controllers/*.ts`
- Contratos TypeScript (`Interfaces / DTOs`): `backend/src/domain/repositories/interfaces.ts` y `models.ts`

## Diagrama de Clases
El archivo `diagram.svg` anexo a este documento ilustra las entidades core que viajan en estos contratos, particularmente la compleja estructura de `CreateOrderDTO` y el `Order Aggregate`.

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
