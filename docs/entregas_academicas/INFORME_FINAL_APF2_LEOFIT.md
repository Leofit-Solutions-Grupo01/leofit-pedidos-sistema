# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F) - CICLO 2026A

---

# INFORME DE AVANCE DE PROYECTO FINAL 2 (APF2)
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT INDUMENTARIA
### Integración de Base de Datos, Controles de Seguridad OWASP, Patrón Repositorio y Despliegue en la Nube

---

### DATOS DEL EQUIPO DE TRABAJO (GRUPO 01)
* **Loayza Rodriguez, Lady Luz** (Scrum Master / Lead Dev)
* **Cárdenas Fernández, Víctor Leandro** (Product Owner / Data Architect)
* **Roman Delgado, Harley Anthony** (Front-End Lead / UX Specialist)
* **Dávila Morales, Jim Alessandro** (QA Automation / DevOps)
* **Rojas Sanchez, Daniel Enrique** (Analista de Negocio)

**Docente:** Mg. Ing. de Sistemas - UTP Sede Lima Centro  
**Repositorio GitHub:** [https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)  

---

## 1. INTEGRACIÓN CON BASE DE DATOS (CRITERIO 1 - 4 PTS)
1. **Informe de Administración y Replicación:** Motor PostgreSQL 16 con replicación física mediante streaming WAL (`wal_level=replica`), failover y connection pooler transaccional PgBouncer en puerto 6432 (`database/ADMINISTRATION_AND_REPLICATION.md`).
2. **Diseño Físico de Base de Datos:** Modelo relacional normalizado en 3NF con constraints de integridad referencial, índices B-Tree en campos de búsqueda y triggers de auditoría (`database/schema.sql`).
3. **Implementación del Patrón de Acceso a Datos:** Clean Architecture con el Patrón Repositorio (`IOrderRepository`, `IProductRepository`, `IClientRepository`) desacoplando la lógica de negocio de PostgreSQL (`backend/src/infrastructure/repositories/pg.repositories.ts`).
4. **Consistencia:** 100% de coherencia entre los diagramas entidad-relación y los scripts DDL/DML.

---

## 2. APLICACIÓN DE CONTROLES DE SEGURIDAD (CRITERIO 2 - 4 PTS)
1. **Módulo de Autenticación y Autorización:** Tokens JWT firmados con HMAC-SHA256, contraseñas protegidas con salt hashing mediante `bcryptjs` (10 rounds) y middleware de autorización por roles RBAC (`requireRole`).
2. **Informe Técnico de Seguridad y Cifrado de Datos:** Cifrado en tránsito con TLS 1.3 / HTTPS obligatorio y cifrado en reposo con AES-256 en almacenamiento.
3. **Pruebas de Seguridad Web:** Auditoría SAST con `npm audit` (0 vulnerabilidades) y pruebas DAST con inyección simulada de SQLi y XSS neutralizadas al 100% por Zod y Helmet (`backend/tests/security.test.ts`).
4. **Catálogo de Controles OWASP:** Matriz de mitigación detallada contra el OWASP Top 10.

---

## 3. DESPLIEGUE DE LA APLICACIÓN (CRITERIO 3 - 4 PTS)
1. **Plan de Pruebas del Sistema:** Cobertura de pruebas unitarias, de integración y de seguridad.
2. **Manual de Despliegue:** Guía paso a paso para contenedores Docker (`Dockerfile`, `docker-compose.yml`) y servicios cloud en Render, Supabase y Vercel.
3. **Evidencia de Pruebas de Despliegue:** Verificación de salud `/api/health` con latencia menor a 50 ms.
4. **Evidencias de Monitoreo de Base de Datos:** Supervisión de conexiones activas con `pg_stat_activity` y cache hit ratio > 99%.

---

## 4. VALIDACIÓN Y VERIFICACIÓN EN PLATAFORMA CLOUD (CRITERIO 4 - 2 PTS)
Validación en vivo de endpoints cloud demostrando conectividad transaccional con la base de datos y respuesta segura bajo HTTPS.

---

## 5. SUSTENTACIÓN (CRITERIO 5 - 2 PTS)
Diapositivas académicas oficiales preparadas en `docs/academic/diapositivas/` y guión de sustentación con 16 preguntas críticas respondidas ante el jurado calificador.

---

## 6. LEVANTAMIENTO DE OBSERVACIONES DEL APF1 (CRITERIO 6 - 4 PTS)
Subsanación al 100% de los comentarios de la entrega previa:
* Incorporación de justificación cuantitativa WPO (Lighthouse 96/100).
* Matriz completa de trazabilidad de requerimientos.
* Evidencia documental de configuración de herramientas y repositorios.
