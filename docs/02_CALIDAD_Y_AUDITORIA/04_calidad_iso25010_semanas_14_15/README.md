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

Esta carpeta contiene la documentación técnica acumulativa y formal de evaluación de calidad de software bajo la norma internacional vigente **ISO/IEC 25010:2023**, desarrollada según las directivas, guía didáctica y plantilla oficial del docente Ing. Enrique Lee Huamani:

| Entregable / Archivo | Formato | Páginas / Contenido | Audiencia y Propósito |
| :--- | :--- | :--- | :--- |
| [**`INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx`**](./INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.docx) | Word Formal Editable | 522 líneas compiladas, 14 tablas completas | **Entregable Oficial de Calificación UTP.** Informe acumulativo completo (APF1 + APF2 + APF3 + Unidad 4: Semanas 14 y 15) con estilos institucionales, tabla de contenidos dinámica y formato A4. |
| [**`INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md`**](./INFORME_CONTINUACION_S14_S15_PROYECTO_FINAL_LEOFIT.md) | Markdown Canónico | Memoria técnica auditable (49.9 KB) | Especificación técnica auditable en texto plano con logs de k6, señales doradas SRE, tablas de percentiles, fragmentos de código, consultas SQL y justificaciones arquitectónicas. |

---

## 2. Marco Normativo: De ISO/IEC 25010:2011 a ISO/IEC 25010:2023

El proyecto fundamenta su calidad en la versión vigente **ISO/IEC 25010:2023**, incorporando sus cambios clave:
1. **De 8 a 9 características:** Incorporación de **Safety (Seguridad Funcional)** como característica de primer nivel independiente de Security. Security aborda confidencialidad e integridad criptográfica (JWT/Bcrypt/HMAC); Safety garantiza ausencia de daños económicos u operativos (cero sobreventas mediante concurrencia ACID y bloqueos `FOR UPDATE`).
2. **Interaction Capability:** Evolución del concepto clásico de *Usability* hacia la capacidad integral de interacción persona-sistema, inclusión y accesibilidad (WCAG 2.1 AA/AAA y puntaje SUS 88.5/100).
3. **Flexibility:** Absorbe formalmente la antigua *Portability*, consolidando Adaptabilidad, Escalabilidad, Instalabilidad y Reemplazabilidad bajo la denominación estándar: **“ISO/IEC 25010:2023 — Flexibility — Adaptability / Scalability”**.

---

## 3. Resumen Técnico de los Criterios Evaluados

### 3.1. Eficiencia de Desempeño / Rendimiento (Semana 14)
* **Medición por Percentiles (no solo promedios):** El promedio oculta la cola larga de latencias producidas por pausas de Garbage Collection en el motor V8 de Node.js o contención de locks en PostgreSQL. Se auditan $p50$, $p95$ y $p99$.
* **Cuatro Señales Doradas de Google SRE:**
  - **Latencia:** Mediana $p50 = 120\text{ ms}$, **$p95 = 280\text{ ms}$** (1 VU) y **$480\text{ ms}$** (10 VU) $\to$ **Cumple holgadamente el SLO ($< 700\text{ ms}$)**.
  - **Tráfico:** 19.0 req/s nominales; capacidad máxima demostrada de 45.2 req/s en tier base de Render.
  - **Errores:** **0.00% fallos** en 34,200 solicitudes procesadas (meta SRE $< 0.10\%$).
  - **Saturación:** CPU $< 25\%$ y RAM en $185\text{ MB}$, respetando el umbral de seguridad SRE ($< 70\%$).
* **Cuatro Tipos de Ensayos k6:** Línea Base (1 VU), Steady-State (10 VU por 30 min), Spike Test (35 VU súbitos) y Soak Test (8 VU continuos por 4 horas para descartar fugas de memoria).
* **Diagnóstico de Cuello de Botella y Optimización B-Tree:** En 35 VU ($p99 = 1,820\text{ ms}$ por RTT transfronterizo hacia Neon en EE. UU.), se implementaron los índices compuestos `idx_orders_customer_created` y `idx_variants_stock`, reduciendo el costo `EXPLAIN ANALYZE` en **64.2%** (de 14.8 ms a 5.3 ms).

### 3.2. Flexibilidad y Patrones de Resiliencia Cloud (Semana 14)
* **Adaptabilidad:** Clean Architecture desacoplada en 4 capas y Factor III de The Twelve-Factor App (inyección de `.env`). Comprobada portabilidad idéntica en 3 entornos: Local Docker Compose, Render Staging y AWS ECS Fargate con **cero líneas de código modificadas**.
* **Escalabilidad y Resiliencia Avanzada:**
  - **Circuit Breaker (Cortacircuito / 熔断器):** Fail-fast ante 5 fallos consecutivos en pasarelas externas (SUNAT/WhatsApp) para proteger el Event Loop de Node.js.
  - **Bulkhead (Aislamiento):** Separación de pools de conexiones (`orders_pool` vs `read_pool`).
  - **Retry con Exponential Backoff y Jitter:** Reintentos con dispersión aleatoria ($\pm 20\%$) para neutralizar el fenómeno de *thundering herd*.
  - **Rate Limiting y Load Shedding:** Ventana deslizante de 100 req/min por IP y descarte selectivo de búsquedas pesadas al superar 75% CPU.
  - **Auto-Scaling y Observabilidad:** Disparo a 70% CPU, tiempo de aprovisionamiento de 42s en ECS Fargate, enfriamiento de 300s y trazabilidad distribuida con `X-Request-ID`.

### 3.3. Mantenibilidad: Modularidad, Reusabilidad, Modificabilidad y Testabilidad (Semana 15)
* **Modularidad y Dirección de Dependencias:** Clean Architecture donde las dependencias apuntan estrictamente hacia el Dominio Puro (`Dominio <- Aplicación <- Infraestructura`). Erradicación del anti-patrón monolítico (`app.py`).
* **Reusabilidad (DRY):** Componentes transversales reutilizados: RBAC `requireRole` (14 endpoints), Idempotencia RFC 8785, Generador PDF vectorial y validadores Zod.
* **Modificabilidad y Análisis de Blast Radius:** Cambio real de regla comercial CHG-01 (10% descuento textil $\ge 6$ unidades) confinado a **únicamente 2 archivos** (`order.service.ts` y test unitario), con 0 cambios en controladores y 0 en BD.
* **Testabilidad y Métricas Objetivas (TDD):**
  - **Pirámide de Pruebas:** 194 pruebas automatizadas (140 unitarias, 44 de integración, 10 e2e) con 100% de éxito en CI/CD.
  - **Complejidad Ciclomática (McCabe):** Valores de **1 a 3** en métodos core (umbral óptimo $\le 4$).
  - **Cobertura de Pruebas:** 84.6% en servicios y 92.1% en utilitarios monetarios con `Decimal.js`.

### 3.4. Confiabilidad y Disponibilidad (Semana 16)
* **Alta Disponibilidad (HA 24/7) vs HPC:** Selección justificada de arquitectura HA 24/7 orientada a disponibilidad continua y redundancia Multi-AZ (SLA $99.9\%$) en lugar de computación de alto rendimiento científico (HPC).
* **Tolerancia a Fallos:** PWA con Service Worker para operación desconectada en galerías de Gamarra.
* **Recuperación ante Desastres (DRP / PITR):** RTO medido de **3.2 segundos** y RPO de **0 segundos** en Neon PostgreSQL.

---

## 4. Instrucciones de Regeneración de Entregables

```bash
# Regenerar Informe Markdown y Word DOCX
python scripts/proyecto_final/build_informe_s14_s15.py

# Validar integridad y ausencia de emojis
python scripts/proyecto_final/validate_deliverables.py
```
