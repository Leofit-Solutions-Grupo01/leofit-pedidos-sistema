# D4 — Formato de Retorno (Respuestas JSON)

## Pregunta que responde
¿En qué formato retorna la información el servidor backend a los clientes web y móviles?

## Patrón de Diseño: JSON Envelope y REST Puro
El sistema sigue un enfoque mixto de REST maduro:
1. **Respuestas Singulares**: Retornan el objeto JSON directamente en la raíz sin envoltorios extraños (ej. al pedir una orden específica).
2. **Respuestas Paginadas (Colecciones)**: Utilizan un "Envelope" (Envoltorio) que incluye la data en un array y los metadatos de paginación o totales de la consulta para poder armar la grilla en React.
3. **Paginación por Headers**: Para compatibilidad con clientes REST estrictos, los totales y límites también se exponen de forma redundante en las cabeceras HTTP (`X-Total-Count`).

### 1. Respuesta Exitosa Simple (Ej. GET /api/orders/123)
Retorna la entidad cruda directamente.
```json
{
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
```

### 2. Respuesta Paginada (Colección) (Ej. GET /api/orders?page=1&limit=10)
Usa una estructura de sobre (`envelope`) para adjuntar la cuenta total de registros.
```json
{
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
  ],
  "total": 54
}
```
*Adicionalmente, el servidor inyecta el Header:* `X-Total-Count: 54`.

### 3. Respuesta de Error Estandarizada (4xx / 5xx)
Cualquier fallo de validación de `Zod` (como el intento de vector DoS que reparamos en la cabecera `x-isolation-level`) o error de negocio retorna una estructura unificada para que el Frontend pueda mapearlo a alertas visuales uniformes.
```json
{
  "error": "Bad Request",
  "message": "Falló la validación de entrada",
  "details": [
    {
      "path": ["items", 0, "quantity"],
      "message": "Number must be greater than 0"
    }
  ]
}
```

## Fuentes
- Controladores: `backend/src/controllers/order.controller.ts`
- Rutas y Middlewares.

## Cómo regenerar
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i diagram.mmd -o diagram.svg
```

## Versión
- Fecha: 2026-10-07
