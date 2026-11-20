# Calidad de Software ISO/IEC 25010:2023 — Semanas 14 y 15 (Unidad 4)
## Sistema Web PWA de Gestión de Pedidos Multicanal — LeoFit Solutions
**Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (100000S12F)**  
**Docente Asesor Evaluador:** Ing. Enrique Lee Huamani Uriarte  
**Sección:** 35374 | **Ciclo:** 2026-I | **Estado:** APROBADO Y EJECUTADO  

**Equipo de Desarrollo e Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

## 1. Catálogo Oficial de Entregables de la Unidad 4

Esta carpeta contiene la documentación técnica acumulativa y formal de evaluación de calidad de software bajo la norma internacional **ISO/IEC 25010:2023**, desarrollada según las directivas, guía didáctica y plantilla oficial del docente Ing. Enrique Lee Huamani:

| Entregable / Archivo | Formato | Páginas / Contenido | Audiencia y Propósito |
| :--- | :--- | :--- | :--- |
| [**`INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx`**](./INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx) | Word Formal Editable | 156 párrafos, 14 tablas completas | **Entregable Oficial de Calificación UTP.** Informe acumulativo completo (APF1 + APF2 + APF3 + Unidad 4: Semanas 14 y 15) con estilos institucionales, tabla de contenidos dinámica y formato A4. |
| [**`INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md`**](./INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md) | Markdown Canónico | Memoria técnica auditable | Especificación técnica auditable en texto plano con logs de k6, tablas de métricas, fragmentos de código, consultas SQL y justificaciones arquitectónicas. |

---

## 2. Resumen Técnico de los Criterios Evaluados (ISO/IEC 25010:2023)

### 2.1. Eficiencia de Desempeño / Rendimiento (Semana 14)
Pruebas escalonadas de carga automatizadas ejecutadas con **Grafana k6** sobre el endpoint transaccional crítico `POST /api/orders` (creación de pedido, validación de stock y emisión de comprobante preliminar):
* **1 Usuario Virtual (Línea Base):** Mediana $p50 = 120\text{ ms}$, **Percentil $p95 = 280\text{ ms}$**, $0.0\%$ errores, CPU $< 10\%$, RAM $145\text{ MB}$. Cumple SLA contractual ($< 700\text{ ms}$).
* **10 Usuarios Virtuales (Carga Nominal Concurrente):** Mediana $p50 = 240\text{ ms}$, **Percentil $p95 = 480\text{ ms}$**, $0.0\%$ errores, CPU $24\%$, RAM $185\text{ MB}$. Cumple SLA contractual.
* **30 Usuarios Virtuales (Carga Pico / Estrés):** Mediana $p50 = 620\text{ ms}$, **Percentil $p95 = 1,400\text{ ms}$**, $0.0\%$ errores, CPU $58\%$, RAM $230\text{ MB}$.
* **Optimización de Base de Datos:** Se identificó contención de I/O en la consulta de historial de pedidos. La creación del índice compuesto B-Tree `idx_orders_customer_created (customer_id, created_at DESC)` redujo el costo del plan de ejecución `EXPLAIN ANALYZE` de $145.20$ a $52.00$ (**reducción del 64.2%**).

### 2.2. Flexibilidad: Adaptabilidad y Escalabilidad (Semana 14)
* **Adaptabilidad de Entornos:** Arquitectura basada en principios de *Clean Architecture* con separación estricta en 4 capas (Rutas $\leftrightarrow$ Controladores $\leftrightarrow$ Servicios $\leftrightarrow$ Repositorios). Configuración externalizada mediante Twelve-Factor App vía variables de entorno (`.env`), permitiendo portabilidad inmediata entre Local Docker, Render Cloud Staging y AWS Production sin modificar una sola línea de código fuente.
* **Escalabilidad Elástica:** Estrategia en dos niveles:
  1. *Optimización previa a nivel de código y base de datos:* Consultas paginadas, índices selectivos y pool transaccional PgBouncer.
  2. *Escalabilidad elástica de infraestructura:* Configuración de contenedores con escalado horizontal (Render Web Service auto-scale y AWS ECS Fargate con Target Tracking al 70% CPU).

### 2.3. Mantenibilidad: Modularidad, Reusabilidad, Modificabilidad y Testabilidad (Semana 15)
* **Modularidad:** Inyección de dependencias y desacoplamiento estricto de responsabilidades.
* **Reusabilidad:** Componentes transversales reutilizados en toda la solución (`authMiddleware` RBAC, `idempotencyMiddleware` con Redis/caché en memoria, y generador de PDF vectorial `pdfKit`).
* **Modificabilidad Aislada:** Modificación real de regla de negocio documentada en el historial de Git (cambio en el cálculo de comisión para pedidos mayoristas de Lima Metropolitana vs. Provincias), impactando únicamente la clase `OrderPricingService` sin alterar contratos de API ni capas de persistencia.
* **Testabilidad (TDD / Shift-Left):** 194 pruebas automatizadas ejecutadas en CI/CD (125 pruebas backend en Jest/Supertest y 69 pruebas frontend en Vitest/RTL) con 100% de aprobación y cero defectos bloqueantes.

### 2.4. Confiabilidad y Disponibilidad (Semana 16)
* **Alta Disponibilidad (HA) vs HPC:** Selección fundamentada de arquitectura de Alta Disponibilidad 24/7 orientada a transacciones comerciales concurrentes (SLA $99.9\%$, uptime continuo con redundancia geográfica Multi-AZ) en lugar de Computación de Alto Rendimiento (HPC).
* **Tolerancia a Fallos:** PWA con Service Worker para modo offline y cola transaccional local en IndexedDB.
* **Recuperación ante Desastres (DRP / PITR):** RTO medido de $3.2\text{ segundos}$ (umbral SLA: 15 minutos) y RPO de $0\text{ segundos}$ (cero pérdida de datos confirmados).

---

## 3. Instrucciones de Regeneración de Entregables

Para recompilar los documentos a partir del generador oficial:

```bash
# Regenerar Informe Markdown y Word DOCX
python scripts/proyecto_final/build_informe_s14_s15.py

# Validar integridad y ausencia de emojis
python scripts/proyecto_final/validate_deliverables.py
```
