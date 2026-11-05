# LeoFit Solutions v2.0.0 — Manual de Código, Arquitectura y Reproducibilidad

## Información de Identificación (Anexo A del Manual)
* **Proyecto:** LeoFit Solutions — Plataforma Web PWA Multicanal y Control de Existencias
* **Organización:** LeoFit Confecciones y Diseños Deportivos S.A.C. (RUC 20601234567, Jr. Gamarra 1230 Stand 304, Lima)
* **Curso:** Curso Integrador II: Software (100000S12F) — Ciclo 2026-I — UTP
* **Docente Asesor:** Ing. Enrique Lee Huamani Uriarte
* **Equipo de Desarrollo (Grupo 01):**
  * Lady Luz Loayza Rodríguez (U22221489) — Scrum Master / DevSecOps
  * Víctor Leandro Cárdenas Fernández (U19217414) — Product Owner / DBA
  * Harley Anthony Roman Delgado (U21313032) — Frontend Lead / UI-UX
  * Jim Alessandro Dávila Morales (U18206081) — QA Engineer Lead / Backend
  * Daniel Enrique Rojas Sánchez (U21214627) — Business Analyst / Cloud DevOps

---

## Repositorio y Versión Oficial
* **Repositorio GitHub:** https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema
* **Versión Oficial:** `v2.0.0`
* **Release Tag:** `v2.0.0-apf3`
* **Commit Trazable:** `e35e32b8f877d9c12a0f8812c3b5d`

---

## Instrucciones Paso a Paso para la Reproducción de Pruebas

### 1. Clonar el Repositorio Oficial
```bash
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema
```

### 2. Ejecutar la Suite de Pruebas Backend (125 pruebas Jest / Supertest)
```bash
cd backend
npm install
npm test
```
*Valida: Integración de autenticación JWT, creación atómica de pedidos (ACID), firma criptográfica HMAC en webhooks, control de acceso RBAC y deduplicación canónica RFC 8785.*

### 3. Ejecutar la Suite de Pruebas Frontend (69 pruebas Vitest / React Testing Library)
```bash
cd ../frontend
npm install
npm test
```
*Valida: Renderizado reactivo del catálogo textil, lógica del carrito, validación sintáctica de DNI y teléfono, prevención proactiva de errores y accesibilidad WCAG 2.1.*

---

## Variables de Entorno de Producción (Render Secrets Store)
```env
NODE_ENV=production
PORT=5000
DATABASE_URL=postgresql://leofit_user:***@ep-dry-pond-***.neon.tech/leofit_db?sslmode=require
JWT_SECRET=64_bytes_cryptographic_random_secret_hs256
CORS_ORIGIN=https://leofit-solutions-grupo01.github.io
```
