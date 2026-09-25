# Leofit Solutions — Sistema de Gestión de Pedidos & Control de Inventario Multicanal
## Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (`100000S12F`)
**Docente:** Ing. Enrique Lee Huamani Uriarte | **Sección:** 35374 | **Grupo:** 01  
**Organización GitHub:** [`Leofit-Solutions-Grupo01`](https://github.com/Leofit-Solutions-Grupo01) | **Repositorio:** [`leofit-pedidos-sistema`](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)

---

[![Estado APF1](https://img.shields.io/badge/APF1%20(Semana%2005)-18%2F20%20Aprobado-brightgreen.svg)](docs/entregas_academicas/INFORME_FINAL_APF1_LEOFIT.pdf)
[![Estado APF2](https://img.shields.io/badge/APF2%20(Semana%2009)-100%25%20Completado-blue.svg)](docs/entregas_academicas/INFORME_FINAL_APF2_LEOFIT.pdf)
[![Pruebas Backend](https://img.shields.io/badge/Backend%20Tests-18%20Passing-brightgreen.svg)](backend/README.md)
[![Pruebas Frontend](https://img.shields.io/badge/Frontend%20Tests-17%20Passing-brightgreen.svg)](frontend/README.md)
[![Arquitectura](https://img.shields.io/badge/Architecture-Clean%20Architecture%20%2B%20BCNF-purple.svg)](docs/modulos_tecnicos/07_Arquitectura_Sistema.md)
[![Seguridad](https://img.shields.io/badge/Security-OWASP%20Top%2010%20%7C%20JWT%20%7C%20bcrypt-red.svg)](docs/modulos_tecnicos/10_Catalogo_Controles_Seguridad_OWASP.md)
[![Demo PWA](https://img.shields.io/badge/Demo%20Live-PWA%20Online-orange.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 1. Descripción del Proyecto

**LeoFit Solutions** es una plataforma web progresiva (PWA) de alto rendimiento conectada a un backend de Arquitectura Limpia con persistencia en PostgreSQL 16. La solución digitaliza el flujo integral de ventas, toma de pedidos y control de existencias en tiempo real para la empresa textil deportiva **LeoFit** (Gamarra, La Victoria, Lima).

### Problemática Resuelta:
- **Sobreventa y descontrol de stock:** Desincronización entre canales físicos y virtuales (WhatsApp / Instagram).
- **Registro manual en papel:** Retrasos de hasta 48 horas en la preparación de paquetes y pérdida de comprobantes.
- **Falta de métricas:** Ausencia de indicadores en tiempo real de facturación, prendas más vendidas y alertas de stock bajo.

---

## 2. Integrantes del Equipo y Asignación de Roles

| Integrante | Código UTP | Usuario GitHub | Rol Primario Scrum | Rol Técnico Especializado |
| :--- | :--- | :--- | :--- | :--- |
| **Lady Luz Loayza Rodriguez** | `U22221489` | `@LadyyLuz` / `luzylay` | **Scrum Master** | DevSecOps, Coordinadora de Seguridad JWT & Gobernanza |
| **Víctor Leandro Cárdenas F.** | `U19217414` | `@VictorCardenazFernandez` | **Product Owner** | Arquitecto de Base de Datos (DBA), BCNF & Replicación WAL |
| **Harley Anthony Roman D.** | `U21313032` | `@hroman2004` | **Frontend Lead** | Especialista PWA, Diseñador UI/UX & Optimización WPO |
| **Jim Alessandro Dávila M.** | `U18206081` | `@Jim4279` | **QA Engineer Lead** | Desarrollador Backend Node.js/TS & Pruebas Automatizadas |
| **Daniel Enrique Rojas S.** | `U21214627` | `@Daniel102608` | **Business Analyst** | Cloud DevOps, SLA/SLO, Render/Vercel & Supabase |

---

## 3. Entregables Oficiales e Informes Académicos UTP

| Hito | Calificación / Estado | Entregable Oficial en Word (.docx) | Entregable Oficial en PDF (.pdf) |
| :--- | :---: | :---: | :---: |
| **APF1 (Avance 1 - Sem. 05)** | **18 / 20 (Aprobado)** | [`INFORME_FINAL_APF1_LEOFIT.docx`](docs/entregas_academicas/INFORME_FINAL_APF1_LEOFIT.docx) | [`INFORME_FINAL_APF1_LEOFIT.pdf`](docs/entregas_academicas/INFORME_FINAL_APF1_LEOFIT.pdf) |
| **APF2 (Avance 2 - Sem. 09)** | **100% Completado** | [`INFORME_FINAL_APF2_LEOFIT.docx`](docs/entregas_academicas/INFORME_FINAL_APF2_LEOFIT.docx) | [`INFORME_FINAL_APF2_LEOFIT.pdf`](docs/entregas_academicas/INFORME_FINAL_APF2_LEOFIT.pdf) |
| **APF3 (Avance 3 - Sem. 13)** | *Planificado (Sprint 4)* | *En desarrollo según cronograma* | *En desarrollo según cronograma* |
| **PROY (Proyecto Final - Sem. 18)** | *Planificado (Sprint 5)* | *En desarrollo según cronograma* | *En desarrollo según cronograma* |

> Para consultar la colección completa de los 13 módulos de especificación técnica y material de clase, revise el [`Directorio Maestro de Documentación (docs/README.md)`](docs/README.md).

---

## 4. Arquitectura de Software y Persistencia de Datos

### Diagrama de Contenedores C4 (Nivel 2)
```text
+-------------------------------------------------------------------------+
|                         USUARIO / OPERADOR LEOFIT                       |
|               (Dispositivo Móvil / Laptop / Navegador Web)             |
+-------------------------------------------------------------------------+
                                    |
                            [HTTPS / TLS 1.3]
                                    v
+-------------------------------------------------------------------------+
|                    FRONTEND PWA (Vercel Edge Network)                   |
|           React 19 + TypeScript + Vite + TailwindCSS + Offline SW        |
+-------------------------------------------------------------------------+
                                    |
                    [REST API / JSON / Bearer JWT / CORS]
                                    v
+-------------------------------------------------------------------------+
|                  BACKEND API REST (Render.com / Docker)                 |
|         Node.js 20 + TypeScript + Express + Zod + Helmet + RateLimit    |
|      - Capa Dominio: Entidades & Interfaces de Repositorio             |
|      - Capa Infraestructura: PgOrderRepository (Consultas $1, ACID)     |
|      - Capa Fallback: MemoryOrderRepository (In-Memory Fallback)        |
+-------------------------------------------------------------------------+
                                    |
                    [TCP/IP / Port 5432 / SSL Encrypted]
                                    v
+-------------------------------------------------------------------------+
|             BASE DE DATOS RELACIONAL (Supabase / PostgreSQL 16)         |
|      - Normalización BCNF (12 tablas/vistas con integridad referencial) |
|      - Physical Streaming Replication (Primary -> Standby WAL slot)     |
|      - Backups Diarios PITR con verificación de hash SHA-256            |
+-------------------------------------------------------------------------+
```

---

## 5. Pruebas Automatizadas y Cobertura de Calidad (35 Tests Totales)

El proyecto cuenta con **35 pruebas automatizadas (100% aprobadas)** distribuidas en Frontend y Backend:

### A. Backend (18 tests con Jest & Supertest)
```bash
cd backend && npm test
```
- `tests/orders.test.ts`: Creación, cálculo atómico y rechazo por ruptura de stock.
- `tests/auth.test.ts`: Registro, login JWT, protección RBAC y manejo de contraseñas erróneas.
- `tests/security.test.ts`: Cabeceras Helmet, mitigación de inyección SQL y saneamiento Zod.
- `tests/products.test.ts`: Catálogo de indumentaria y detalle de variantes.
- `tests/clients_dashboard.test.ts`: Registro de clientes y cálculo de KPIs.

### B. Frontend (17 tests con Vitest)
```bash
cd frontend && npm test
```
- `src/__tests__/mockData.test.ts`: Integridad de datos y validaciones de inventario.
- `src/__tests__/allTabsFunctional.test.ts`: Navegación, cambio de estados y renderizado de módulos.
- `src/__tests__/pdfGenerator.test.ts`: Generación vectorial de comprobantes oficiales y rótulos.

---

## 6. Guía de Ejecución Local y Despliegue con Docker

### Opción A: Despliegue Rápido con Docker Compose (Recomendado)
```bash
# Inicia PostgreSQL 16, Backend API y Adminer con un solo comando
docker-compose up -d

# Acceso al Backend API: http://localhost:4000/api/health
# Acceso a Adminer (Gestor BD): http://localhost:8080
```

### Opción B: Ejecución Manual en Entorno de Desarrollo
```bash
# 1. Iniciar el Backend API
cd backend
npm install
npm run dev

# 2. Iniciar el Frontend PWA (en otra terminal)
cd frontend
npm install
npm run dev
```

---

## 7. Seguridad de la Información y Manejo de Secretos

- **Sin credenciales expuestas:** Todos los parámetros confidenciales se configuran mediante variables de entorno en el servidor (`process.env.DATABASE_URL`, `process.env.JWT_SECRET`).
- **Plantilla de referencia:** Ver [`backend/.env.example`](backend/.env.example) para configurar un entorno local seguro.
- **Protección de contraseñas:** Cifrado con algoritmo **bcrypt** (10 rondas de salt).
- **Protección perimetral:** Cabeceras HTTP seguras configuradas con **Helmet**, mitigación de ataques DoS con **Rate-Limiting** y sanitización de consultas preparadas `$1` contra inyecciones SQL.

---

## 8. Licencia y Gobernanza

- **Licencia:** MIT License. Ver archivo [`LICENSE`](LICENSE).
- **Gobernanza de Código:** Ver [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) y [`CONTRIBUTING.md`](CONTRIBUTING.md).
- **Políticas de Seguridad:** Ver [`SECURITY.md`](SECURITY.md).
