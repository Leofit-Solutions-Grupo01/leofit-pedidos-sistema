# D3 — Contratos de cada llamada (API)

## Pregunta que responde
¿Qué endpoint recibe qué, qué devuelve, con qué códigos de error y bajo qué schemas de datos?

## Tabla de Endpoints y Contratos

| Endpoint | Método | Auth | Request Payload (Body / Query) | Response Payload | Códigos HTTP |
| -------- | ------ | ---- | ------------------------------ | ---------------- | ------------ |
| `/api/auth/login` | `POST` | No | `{ email, password }` | `{ success, data: { token, user } }` | `200`, `400`, `401`, `429` |
| `/api/auth/register` | `POST` | No | `{ name, email, password, role }` | `{ success, data: User }` | `201`, `400`, `409` |
| `/api/auth/profile` | `GET` | Sí | (Ninguno) | `{ success, data: User }` | `200`, `401` |
| `/api/orders` | `GET` | Sí | `?page, limit, status, dateFrom...` | `{ success, data: Order[] }` | `200`, `401` |
| `/api/orders` | `POST` | Sí | `CreateOrderDTO` | `{ success, data: Order }` | `201`, `400`, `401`, `409` |
| `/api/orders/:id` | `GET` | Sí | (URL Param: `id`) | `{ success, data: Order }` | `200`, `401`, `404` |
| `/api/orders/:id/status` | `PATCH`| Sí | `{ status, comments? }` | `{ success, data: Order }` | `200`, `400`, `401`, `404` |
| `/api/orders/:id/cancel` | `POST` | Sí | (URL Param: `id`) | `{ success, data: Order }` | `200`, `400`, `401`, `404` |
| `/api/orders/track/:orderNumber` | `GET` | No | (URL Param: `orderNumber`) | `{ success, data: Order }` | `200`, `404` |
| `/api/products` | `GET` | No | `?page, limit, search, category` | `{ success, data: Product[] }` | `200` |
| `/api/products/:id` | `GET` | No | (URL Param: `id`) | `{ success, data: Product }` | `200`, `404` |
| `/api/products` | `POST` | Sí (Admin) | `CreateProductDTO` | `{ success, data: Product }` | `201`, `400`, `401`, `403` |
| `/api/products/:id` | `PUT` | Sí (Admin) | `UpdateProductDTO` | `{ success, data: Product }` | `200`, `400`, `401`, `403`, `404` |
| `/api/products/variant/:variantId/stock` | `PATCH`| Sí | `{ quantityDelta }` | `{ success, data: ProductVariant }` | `200`, `400`, `401`, `404` |
| `/api/products/:id` | `DELETE`| Sí (Admin) | (URL Param: `id`) | `{ success, message }` | `200`, `401`, `403`, `404`, `409` |
| `/api/products/alerts/low-stock` | `GET` | Sí | (Ninguno) | `{ success, data: ProductVariant[] }` | `200`, `401` |
| `/api/clients` | `GET` | No | `?page, limit, search` | `{ success, data: Client[] }` | `200` |
| `/api/clients/:id` | `GET` | No | (URL Param: `id`) | `{ success, data: Client }` | `200`, `404` |
| `/api/clients` | `POST` | No | `CreateClientDTO` | `{ success, data: Client }` | `201`, `400`, `409` |
| `/api/clients/:id` | `PUT` | No | `UpdateClientDTO` | `{ success, data: Client }` | `200`, `400`, `404` |
| `/api/external/whatsapp/notify` | `POST` | No | `WhatsAppNotifyPayload` | `{ success, data: Receipt }` | `200`, `400`, `500` |
| `/api/external/identity/lookup` | `POST` | No | `{ type: DNI|RUC, number }` | `{ success, data: Identity }` | `200`, `400`, `500` |
| `/api/external/payments/webhook` | `POST` | HMAC | `PaymentWebhookPayload` | `{ success, data: Reconciled }` | `200`, `400`, `401`, `500` |
| `/api/dashboard/stats` | `GET` | Sí | (Ninguno) | `{ success, data: DashboardMetrics }` | `200`, `401` |
| `/api/health` | `GET` | No | (Ninguno) | `{ status: "ok", timestamp }` | `200` |

## Fuentes por endpoint

- Rutas de Producto (`backend/src/routes/product.routes.ts`)
- Rutas de Cliente (`backend/src/routes/client.routes.ts`)
- Rutas de Orden (`backend/src/routes/order.routes.ts`)
- Rutas de Auth (`backend/src/routes/auth.routes.ts`)
- Rutas Externas (`backend/src/routes/external.routes.ts`)
- Controlador Health (`backend/src/controllers/health.controller.ts:21`)
- Schemas de validación (`backend/src/infrastructure/validators/schemas.ts`)

## Autenticación
La autenticación se implementa a través de `auth.middleware.ts`. 
- **`authenticateToken`**: Valida el JWT Bearer Token. Se aplica a todas las rutas protegidas (`/orders`, `/dashboard`, escritura de `/products`).
- **`requireRole('ADMIN')`**: Valida que el rol del usuario sea administrador (creación/edición/borrado de productos).
- **Rutas Públicas**: `/auth/login`, `/auth/register`, `/products` (lectura), `/clients` (lectura y escritura), endpoints en `/external` (poseen sus propias firmas), y `/health`.

## Errores por Endpoint
- `400 Bad Request`: Error de validación de Zod en el Payload o inconsistencia de la solicitud.
- `401 Unauthorized`: Token faltante, expirado, inválido o falta de firma HMAC (webhook).
- `403 Forbidden`: El usuario está autenticado pero no tiene el rol necesario (ej. no es Admin).
- `404 Not Found`: Recurso no encontrado.
- `409 Conflict`: Conflicto de estado (ej. cambiar status a una orden cancelada, email de usuario ya existe).
- `500 Internal Server Error`: Errores no controlados, base de datos caída o fallos en servicios externos.

## Servicios Externos (`external.controller.ts:36`)
- **WhatsApp Cloud API**:
  - URL (Local): `/api/external/whatsapp/notify`
  - Auth: Pública
  - Payload: `{ phone, orderCode, customerName, total, status }`
  - Errores: 400 (Zod), 500 (Falla envío).
- **Consultas de Identidad (SUNAT/RENIEC simulado)**:
  - URL (Local): `/api/external/identity/lookup`
  - Auth: Pública
  - Payload: `{ type: 'DNI' | 'RUC', number: string }`
  - Errores: 400 (formato incorrecto), 500.
- **Webhook de Pagos**:
  - URL (Local): `/api/external/payments/webhook`
  - Auth: `x-signature` (HMAC SHA256 usando `WEBHOOK_SECRET`)
  - Payload: `{ provider, transactionId, orderCode, amount, status }`
  - Validación de Firma: Compara el buffer del body firmado con HMAC frente al header `x-signature`.
  - Errores: 401 (Missing/Invalid signature), 400 (Zod), 500.

## Diagrama de Clases
El archivo `diagram.svg` anexo a este documento ilustra las entidades core que viajan en estos contratos, incorporando `Product`, `Client`, y payloads externos.

## Nota sobre el tamaño
El SVG se compila con mmdc. Para versiones optimizadas, regenerar con mmdc --no-svg-fonts.

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```
