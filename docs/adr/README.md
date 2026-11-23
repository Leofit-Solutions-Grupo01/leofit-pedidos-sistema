# Architectural Decision Records (ADR) — Registro de Decisiones de Arquitectura
## LeoFit Solutions — Curso Integrador II: Software (UTP)
**Estándar Documental:** Markdown Architectural Decision Records ([MADR](https://adr.github.io/madr/))  

---

Este directorio contiene el registro canónico de las decisiones de arquitectura de software más trascendentes tomadas durante el ciclo de vida del proyecto **LeoFit Solutions**, justificando el balance entre costo, esfuerzo, time-to-market, escalabilidad y seguridad.

---

## Índice de Decisiones Arquitectónicas

| Código | Decisión de Arquitectura | Estado | Fecha de Decisión | Pregunta del Jurado que Resuelve |
| :---: | :--- | :---: | :---: | :--- |
| **[ADR-001](ADR-001_ELECCION_RENDER_NEON_VS_AWS.md)** | **Elección de Render + Neon PostgreSQL en lugar de AWS en Etapa MVP** | **Aprobada** | 06/11/2026 | ¿Por qué Render+Neon en lugar de AWS para la etapa MVP? Análisis financiero ($0 vs $95.80/mes), time-to-market, matriz de dimensionamiento SRE y cálculo de almacenamiento SUNAT CPE a 5 años. |
| **[ADR-002](ADR-002_ARQUITECTURA_OBJETIVO_AWS.md)** | **Diseño de Arquitectura Objetivo en AWS y Servicios Complementarios** | **Aprobada** | 06/11/2026 | ¿Cómo sería la maquetación 100% nativa en AWS? Diseño bajo Well-Architected Framework: VPC Multi-AZ, ECS Fargate, Aurora Serverless, WAF, S3 Lifecycle a Glacier, y justificación de servicios SaaS especializados (Culqi y Nubefact OSE). |

---

> [!NOTE]
> Las versiones ampliadas con anexos y trazabilidad al código se encuentran en [**`docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18/anexos_tecnicos/`**](../01_ENTREGA_FINAL_PROYECTO_SEMANA_18/anexos_tecnicos/).
