# Evidencias de Calidad, Auditoría de Software y Planes de Prueba
## Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (`100000S12F`)
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería (Grupo 01):** LeoFit Solutions  

---

Este directorio centraliza las evidencias técnicas, planes de prueba formales, auditorías de código y protocolos de continuidad de negocio desarrollados a lo largo del ciclo 2026-I para **LeoFit Confecciones y Diseños Deportivos S.A.C.**

---

## 1. Índice de Carpetas y Módulos de Calidad

| Carpeta / Módulo | Estándar Internacional | Descripción Técnica y Entregables Clave |
| :--- | :---: | :--- |
| [`01_plan_de_pruebas_iso29119/`](01_plan_de_pruebas_iso29119/) | **ISO/IEC/IEEE 29119** (Partes 1-4) | Plan Maestro de Pruebas: 3 documentos de gestión (Plan, Estado, Finalización) y 7 dinámicos (Diseño, Casos, Procedimiento, Requisitos de Datos, Preparación, Resultados, Incidentes). |
| [`02_calidad_iso25010_semanas_10_11/`](02_calidad_iso25010_semanas_10_11/) | **ISO/IEC 25010** | Evaluación intermedia de calidad del producto: Adecuación Funcional, Eficiencia de Desempeño y pruebas empíricas de Coexistencia de servicios. |
| [`03_auditoria_y_cierre_proyecto/`](03_auditoria_y_cierre_proyecto/) | **ISO 9000-3 / IEEE 1028** | Auditoría de código, inventario de activos, trazabilidad a requisitos y actas formales de cierre de sprint. |
| [`04_calidad_iso25010_semanas_14_15/`](04_calidad_iso25010_semanas_14_15/) | **ISO/IEC 25010:2023** | Evidencias del hito de Unidad 4: Evaluación de Rendimiento con percentiles k6 ($p50$, $p95$, $p99$), Flexibilidad (Circuit Breaker, escalabilidad) y Mantenibilidad (McCabe, testabilidad). *(Consolidado en el Informe Final de Semana 18)*. |
| [`05_operaciones_respaldo_drp/`](05_operaciones_respaldo_drp/) | **ISO 22301 / NIST SP 800-34** | Protocolo de Continuidad Operativa y simulación de Desastre (DRP): Procedimientos de respaldo automatizado (`pg_dump`), restauración en frío y validación de RPO (5 min) y RTO (15 min). |
| [`METRICAS_SESION_28_UTP/`](METRICAS_SESION_28_UTP/) | **ISO/IEC 9126-2/3/4** | Formalización matemática de las fórmulas enseñadas en clase: Adecuación Funcional $X = 1 - (A/B)$, Suficiencia de Pruebas y Productividad en Uso. |

---

## 2. Compendio Técnico Maestro

* **[COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA_SSL_TLS.md](COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA_SSL_TLS.md):**  
  Documento de síntesis integral que formaliza las **Sesiones 21 a 29 de clase** (ISO 9126 partes 1 a 4, ISO 25000, ISO 9000-3, ISO 9001, ISO 29119, métricas de Lafuente) y los fundamentos matemáticos y normativos de la política criptográfica **SSL/TLS 1.3 / AES-256-GCM** (Polanía Tovar, 2024).

---

> [!NOTE]
> Para la entrega oficial y definitiva de fin de ciclo para el docente evaluador, consulte el paquete consolidado en [**`docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/`**](../01_ENTREGA_FINAL_PROYECTO_SEMANA_18/).
