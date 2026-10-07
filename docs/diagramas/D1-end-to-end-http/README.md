# D1 — Flujo de comunicación end-to-end HTTP

## Pregunta que responde
¿Cómo viaja un request desde el usuario hasta la BD y vuelve?

## Decisiones de diseño y convivencia de dos flujos
El sistema actual (HEAD en la rama de reparación) presenta una asimetría estructural:
- **Flujo A (Autenticación)**: Está integrado end-to-end. El frontend consume el API REST a través de `fetch`, gestionando la sesión real con JWT.
- **Flujo B (Negocio / Pedidos)**: El backend está listo y soporta transacciones ACID, pero el frontend (React) está desconectado y gestiona los datos de negocio en memoria (`mockData.ts`).

Por lo tanto, este diagrama se ha dividido en dos secuencias (`Flujo A` y `Flujo B`) para no inventar una integración que no existe en el código, mostrando tanto la capacidad real E2E como el estado actual del negocio.

## Fuentes
| Nodo | Descripción | Fuente |
| --- | --- | --- |
| `UI` | Componente de Login | `frontend/src/pages/Login.tsx` |
| `Ctx` | Contexto global de la App | `frontend/src/context/AppContext.tsx:115` (fetch a `/api/auth/login`) |
| `Rate` | Middleware de Rate Limiting | `backend/src/app.ts:38` |
| `Zod` | Validación de body | `backend/src/routes/auth.routes.ts:14` y `backend/src/middlewares/validate.middleware.ts:24` |
| `Ctrl` | Lógica de controlador (Auth) | `backend/src/controllers/auth.controller.ts:29` |
| `Bcrypt` | Utilidades de seguridad / hash | `backend/src/infrastructure/security/jwt.utils.ts` y `auth.controller.ts` |
| `UI_GAP` | Componente desconectado | `frontend/src/pages/PedidoForm.tsx` (Usa `mockData.ts`) |
| `Mid` | Middleware de autenticación | `backend/src/middlewares/auth.middleware.ts` |
| `OrderCtrl` | Controlador de órdenes | `backend/src/controllers/order.controller.ts:126` |
| `Repo` | Persistencia en BD | `backend/src/infrastructure/repositories/pg.repositories.ts:445` (`create()`) |
| `DB` | Postgres (Transacción) | `backend/src/infrastructure/repositories/pg.repositories.ts:453` (`BEGIN`) y `:478` (`FOR UPDATE`) |

## Límites explícitos
- El **Flujo A** no muestra las interacciones con la base de datos (PostgreSQL/Memoria) en el login, se centra en la emisión del JWT y mitigación de timing attacks.
- El **Flujo B** muestra la transacción de BD (`FOR UPDATE`, `COMMIT`) pero asume un request válido desde Postman/cURL, evidenciando el `GAP` con la UI.
- No se detallan latencias (no existen SLA / timeouts predefinidos hardcodeados).

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
