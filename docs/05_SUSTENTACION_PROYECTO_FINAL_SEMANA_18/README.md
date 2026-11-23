# Presentación Oficial de Sustentación Final (Semana 18)
## Sistema Web PWA de Gestión de Pedidos Multicanal — LeoFit Solutions
**Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (100000S12F)**  
**Docente Asesor Evaluador:** Ing. Enrique Lee Huamani Uriarte  
**Sección:** 35374 | **Ciclo:** 2026-I  

**Equipo de Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

## 1. Entregables de la Presentación Final

| Recurso / Archivo | Formato | Especificaciones Técnicas | Propósito |
| :--- | :--- | :--- | :--- |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx) | PowerPoint (`.pptx`) | Widescreen 16:9, **25 diapositivas ejecutivas**, gráficos científicos integrados (Radar ISO 25010, Percentiles k6, Saturación CPU vs TPS, Complejidad McCabe y Cobertura Clean Arch). | **Entregable Oficial de Sustentación.** Presentación ejecutiva para evaluación académica. |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html) | HTML5 Responsivo | Visor web interactivo standalone compatible con cualquier navegador moderno. | Consulta rápida en línea sin requerir software ofimático. |

---

## 2. Estructura Temática (25 Diapositivas)

```text
BLOQUE I: CONTEXTO, PROBLEMÁTICA Y ARQUITECTURA ACTUAL (Slides 1 - 6)
  ├─ Slide 01: Carátula Oficial Institucional UTP
  ├─ Slide 02: Contexto Comercial, Problemática y Solución LeoFit Solutions
  ├─ Slide 03: Arquitectura Implementada Hoy (GitHub Pages + Render + Neon PostgreSQL)
  ├─ Slide 04: Justificación Técnica y Económica: Render + Neon vs. AWS (ADR-001)
  ├─ Slide 05: Análisis Financiero Comparativo Cloud (Tier Base vs. Producción)
  └─ Slide 06: Riesgos Operativos de Free Tiers y Mitigaciones Implementadas

BLOQUE II: ARQUITECTURA OBJETIVO AWS Y COMPLEMENTOS (Slides 7 - 9)
  ├─ Slide 07: Arquitectura Objetivo en AWS (Route 53, CloudFront, ECS Fargate, Aurora)
  ├─ Slide 08: Diseño de Red VPC Multi-AZ y Subredes Privadas de Datos (BCNF)
  └─ Slide 09: Ecosistema de Complementos: Lo que AWS NO Conviene Construir

BLOQUE III: INTEGRACIÓN TRIBUTARIA SUNAT, PAGOS Y SEGURIDAD SSL/TLS (Slides 10 - 13)
  ├─ Slide 10: Cumplimiento Normativo SUNAT para Comprobantes Electrónicos (UBL 2.1)
  ├─ Slide 11: Flujo Asíncrono de Facturación Electrónica con OSE Nubefact
  ├─ Slide 12: Integración de Pagos: Estado Actual Sandbox vs. Producción Live
  └─ Slide 13: Seguridad Criptográfica: Blindaje SSL/TLS 1.3, Webhooks HMAC y PCI-DSS

BLOQUE IV: CALIDAD DE SOFTWARE ISO 9126 E ISO/IEC 25010:2023 (Slides 14 - 19)
  ├─ Slide 14: Marco de Calidad: Fundamentos ISO 9126 y Transición a ISO/IEC 25010:2023
  ├─ Slide 15: Calidad de Rendimiento (Semana 14): Latencia p50/p95/p99 y SRE
  ├─ Slide 16: Rendimiento: Serie Temporal (Soak Test) y Curva de Saturación CPU/TPS
  ├─ Slide 17: Calidad de Flexibilidad (Semana 14): Adaptabilidad y Escalabilidad
  ├─ Slide 18: Calidad de Mantenibilidad (Semana 15): Clean Architecture y McCabe 1-3
  └─ Slide 19: Calidad de Confiabilidad (Semana 16): Arquitectura HA 24/7 vs. HPC

BLOQUE V: TESTING ISO 29119, DESPLIEGUE Y CONCLUSIONES (Slides 20 - 25)
  ├─ Slide 20: Testing ISO/IEC/IEEE 29119: Caja Negra, Ruta Básica y 194 Pruebas
  ├─ Slide 21: Evaluación Integral ISO/IEC 25010:2023 y Calidad en Uso (ISO 9126-4)
  ├─ Slide 22: Validación y Despliegue en Vivo en la Nube (Cloud Staging)
  ├─ Slide 23: Gobernanza del Repositorio, Estándares IEEE/ISO y CI/CD
  ├─ Slide 24: Matriz de Trazabilidad y Evidencias Verificables
  └─ Slide 25: Conclusiones de Ingeniería y Defensa Técnica
```
