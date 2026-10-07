# D4 — Formato de Retorno (Respuestas JSON)

## Pregunta que responde
¿En qué formato retorna la información el servidor backend a los clientes web y móviles?

## Patrón de Diseño: JSON Envelope y REST Puro
El sistema sigue un enfoque mixto de REST maduro:
1. **Respuestas Singulares**: Retornan el objeto JSON envuelto siempre en un objeto con el estado de la operación (`success`) y la información solicitada en `data`.
2. **Respuestas Paginadas (Colecciones)**: Utilizan un "Envelope" (Envoltorio) que incluye la data en un array y los metadatos de paginación (`count`, `total`).
3. **Paginación por Headers**: Para compatibilidad con clientes REST estrictos, los totales y límites también se exponen de forma redundante en las cabeceras HTTP (`X-Total-Count`).

### 1. Respuesta Exitosa Simple (Ej. GET /api/orders/123)
Retorna la entidad envuelta con `success: true`.
```json
{
  "success": true,
  "data": {
    "id": 123,
    "order_number": "LEO-20260302-001",
    "client_id": 45,
    "status": "PREPARACION",
    "subtotal": 120.00,
    "shipping_cost": 15.00,
    "total_amount": 135.00,
    "payment_method": "YAPE",
    "created_at": "2026-10-07T10:00:00Z"
  }
}
```

### 2. Respuesta Paginada (Colección) (Ej. GET /api/orders?page=1&limit=10)
Usa una estructura de sobre (`envelope`) para adjuntar la cuenta total y de la página actual.
```json
{
  "success": true,
  "count": 2,
  "total": 54,
  "data": [
    {
      "id": 123,
      "order_number": "LEO-20260302-001",
      "status": "PREPARACION"
    },
    {
      "id": 124,
      "order_number": "LEO-20260302-002",
      "status": "RECIBIDO"
    }
  ]
}
```
*Adicionalmente, el servidor inyecta el Header:* `X-Total-Count: 54`.

### 3. Respuesta de Error Estandarizada (4xx / 5xx)
Cualquier fallo retorna una estructura unificada para que el Frontend pueda mapearlo a alertas visuales uniformes. Existen dos formatos:

**Formato A — Error de Validación Zod (400):**
```json
{
  "success": false,
  "error": [
    {
      "path": ["items", 0, "quantity"],
      "message": "Number must be greater than 0"
    }
  ]
}
```

**Formato B — Error genérico (negocio o excepción):**
```json
{
  "success": false,
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Pedido con ID 123 no encontrado."
  }
}
```
*Nota: En entornos de desarrollo (`NODE_ENV !== 'production'`), el Formato B incluye el campo opcional `stack` con la traza completa.*

## Fuentes

| Aspecto | Fuente |
| --- | --- |
| Envelope exitoso (paginado) | `backend/src/controllers/order.controller.ts:48` |
| Envelope exitoso (singular) | `backend/src/controllers/order.controller.ts:81` |
| Envelope exitoso (creación) | `backend/src/controllers/order.controller.ts:136` |
| Error Zod | `backend/src/middlewares/error.middleware.ts:24` |
| Error genérico | `backend/src/middlewares/error.middleware.ts:38` |

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
