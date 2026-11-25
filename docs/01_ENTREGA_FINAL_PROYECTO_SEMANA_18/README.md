# CARPETA OFICIAL DE ENTREGA FINAL Y SUSTENTACIÓN (SEMANA 18)
## Curso Integrador II: Software (100000S12F) — Ciclo 2026-I
**Docente Asesor:** **Ing. Enrique Lee Huamani Uriarte**  
**Equipo de Ingeniería:** Grupo 01 (LeoFit Solutions)  

---

Bienvenido a la carpeta oficial de **Entrega Final y Sustentación del Proyecto (Semana 18)**.  
Todos los entregables oficiales exigidos por las rúbricas de la Universidad Tecnológica del Perú (UTP) y las instrucciones del docente se encuentran consolidados y actualizados en esta ubicación.

---

## 1. Mapa de Entregables Oficiales para el Docente

| Archivo | Formato | Rol en la Evaluación | Enlaces Directos |
| :--- | :---: | :--- | :--- |
| **`00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE`** | DOCX / PDF / MD | **Carátula Oficial y Hoja de Enlaces Cloud** con credenciales, URLs de producción y checklist de entregables. | [Descargar DOCX](00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx) · [Ver PDF](00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf) · [Ver MD](00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.md) |
| **`01_INFORME_FINAL_LEOFIT`** | DOCX / PDF | **Informe General Final del Proyecto** (Memoria técnica integral de 19 capítulos, 703 párrafos, 35 tablas en formato APA 7ma Edición). Incluye la evaluación de calidad ISO 25010 / ISO 9126 de semanas 10-11, arquitectura, base de datos y DevOps. | [Descargar DOCX](01_INFORME_FINAL_LEOFIT.docx) · [Ver PDF](01_INFORME_FINAL_LEOFIT.pdf) |
| **`02_INFORME_CONTINUACION_S14_S15_LEOFIT`** | DOCX / PDF / MD | **Informe Acumulativo de Calidad y Continuación (Semanas 14 y 15)** según plantilla oficial UTP en formato APA 7ma Edición. Evalúa Rendimiento (p95, k6), Flexibilidad (Adaptabilidad y Escalabilidad) y Mantenibilidad (Modularidad, Reusabilidad, Modificabilidad, Testabilidad). | [Descargar DOCX](02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx) · [Ver PDF](02_INFORME_CONTINUACION_S14_S15_LEOFIT.pdf) · [Ver MD](02_INFORME_CONTINUACION_S14_S15_LEOFIT.md) |
| **`03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT`** | PPTX / PDF / HTML | **Presentación Oficial de Sustentación** (25 diapositivas, formato 16:9 widescreen, diseño corporativo sin emojis, gráficos 300 DPI y notas de orador completas en cada lámina). | [Descargar PPTX](03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx) · [Ver PDF](03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pdf) · [Abrir Visor HTML](03_VISOR_WEB_PRESENTACION_SUSTENTACION.html) |
| **`04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx`** | XLSX | **Libro de Auditoría y Trazabilidad** con 7 hojas de trabajo: Dashboard, Trazabilidad Jurado, Inventario Cloud, Auditoría ISO 25010, Gap SUNAT CPE, Dimensionamiento y Estándares. | [Descargar XLSX](04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx) |
| **`04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md`** | MD | Compendio integral de las Sesiones 21 a 29 (ISO 9126, ISO 25000, ISO 29119) y Criptografía SSL/TLS (Polanía Tovar, 2024). | [Ver Compendio](04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md) |

---

## 2. Galería de Gráficos Científicos de Calidad (`graficos/`)

1. [`graficos/fig01_radar_iso25010_2023.png`](graficos/fig01_radar_iso25010_2023.png): Gráfico radial de las 9 características del estándar ISO/IEC 25010:2023.
2. [`graficos/fig02_percentiles_latencia_k6.png`](graficos/fig02_percentiles_latencia_k6.png): Barras horizontales de percentiles k6 ($p50$, $p90$, $p95$, $p99$, $p99.9$).
3. [`graficos/fig03_bandas_latencia_tiempo_soak.png`](graficos/fig03_bandas_latencia_tiempo_soak.png): Bandas de latencia temporal en prueba soak de 30 minutos.
4. [`graficos/fig04_saturacion_capacidad_throughput_cpu.png`](graficos/fig04_saturacion_capacidad_throughput_cpu.png): Curva de saturación throughput (TPS) vs. uso de CPU.
5. [`graficos/fig05_treemap_complejidad_ciclomatica.png`](graficos/fig05_treemap_complejidad_ciclomatica.png): Treemap de complejidad ciclomática de McCabe por módulo.
6. [`graficos/fig06_cobertura_por_capa.png`](graficos/fig06_cobertura_por_capa.png): Cobertura de pruebas unitarias e integración por capa arquitectónica.

---

## 3. Anexos Técnicos de Sustentación (`anexos_tecnicos/`)

Respuestas de nivel ingeniería a las preguntas fundamentales del jurado evaluador:

- [`01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md`](anexos_tecnicos/01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md): Justificación económica y técnica de la elección Cloud.
- [`02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md`](anexos_tecnicos/02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md): Maquetación AWS objetivo y servicios complementarios.
- [`03_CUMPLIMIENTO_SUNAT_CPE.md`](anexos_tecnicos/03_CUMPLIMIENTO_SUNAT_CPE.md): Facturación electrónica SUNAT UBL 2.1 y OSE.
- [`04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md`](anexos_tecnicos/04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md): Pasarela de pagos, webhooks HMAC y PCI-DSS.
- [`05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md`](anexos_tecnicos/05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md): Estructura Clean Architecture y estándares de ingeniería.
- [`06_MATRIZ_TRAZABILIDAD_JURADO.md`](anexos_tecnicos/06_MATRIZ_TRAZABILIDAD_JURADO.md): Matriz de trazabilidad integral código vs. preguntas del jurado.
