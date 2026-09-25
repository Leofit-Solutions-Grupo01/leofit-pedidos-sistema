# Manual de Despliegue en la Nube y Evidencias de Operatividad (Versión 1)
## Sistema de Gestión de Pedidos - Leofit Solutions

---

### 1. Arquitectura de Despliegue en la Nube (Cloud Topology)

```mermaid
graph TD
  User([Usuario / Smartphone PWA]) -->|HTTPS / CDN Global| Vercel[Vercel Edge Network / Frontend PWA]
  Vercel -->|REST API HTTPS / CORS| Render[Render.com / Containerized Node.js API]
  Render -->|SSL Connection Pool (5432)| Supabase[(Supabase Cloud / Managed PostgreSQL 16)]
  Supabase -->|Automated Backups| S3[(Amazon S3 Cold Storage)]
```

---

### 2. Parámetros y Variables de Entorno de Producción

| Variable | Descripción | Valor / Formato |
| :--- | :--- | :--- |
| `NODE_ENV` | Entorno de ejecución | `production` |
| `PORT` | Puerto de escucha | `4000` (asignado por el PaaS) |
| `DATABASE_URL` | Cadena de conexión PostgreSQL | `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres?sslmode=require` |
| `JWT_SECRET` | Clave criptográfica para firma JWT | Cadena secreta de 64 caracteres alfanuméricos |
| `CORS_ORIGIN` | Dominios autorizados para invocar la API | `https://leofit-pedidos.vercel.app` |

---

### 3. Procedimiento de Despliegue Paso a Paso

#### A. Aprovisionamiento de la Base de Datos (Supabase / Neon / AWS)
1. Iniciar sesión en la consola de **Supabase** y crear un nuevo proyecto denominado `leofit-production-db`.
2. Acceder al **SQL Editor** y ejecutar en orden:
   - `database/schema.sql` (creación de tablas, llaves foráneas e índices).
   - `database/seeds.sql` (poblado de categorías, catálogo y credenciales iniciales).
3. Obtener la cadena de conexión con SSL obligatorio (`Transaction Pooler URL - Port 6543`).

#### B. Despliegue del Backend API (Render / Railway / Docker)
1. Conectar el repositorio de GitHub con **Render.com**.
2. Configurar el servicio web con:
   - **Environment:** `Docker` (usando `backend/Dockerfile`) o `Node.js` (`npm run build` y `npm start`).
   - **Environment Variables:** Añadir `DATABASE_URL`, `JWT_SECRET`, `CORS_ORIGIN`.
3. Iniciar despliegue automático con cada commit a la rama `main`.

#### C. Despliegue del Frontend PWA (Vercel / GitHub Pages)
1. Importar el repositorio en **Vercel**.
2. Establecer el directorio raíz en `frontend`.
3. Configurar la variable `VITE_API_URL` apuntando a la URL del backend en producción.
4. Desplegar y verificar la asignación del certificado SSL gratuito Let's Encrypt.

---

### 4. Evidencias de Pruebas de Despliegue y Health Check
- **Endpoint de Diagnóstico:** `GET https://[BACKEND_URL]/api/health`
- **Respuesta esperada (HTTP 200 OK):**
```json
{
  "status": "UP",
  "service": "leofit-backend-api",
  "version": "2.0.0",
  "database": {
    "engine": "PostgreSQL Cluster",
    "status": "CONNECTED"
  },
  "slo": {
    "targetAvailability": "99.9%",
    "targetLatencyMs": "< 200ms"
  }
}
```
