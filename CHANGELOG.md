# Historial de Cambios (Changelog)

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [No publicado / Unreleased]

### Añadido
- Suite de pruebas unitarias con Vitest para validación de datos y modelos del frontend.
- Guías de contribución (`CONTRIBUTING.md`), código de conducta (`CODE_OF_CONDUCT.md`) y política de divulgación responsable en `SECURITY.md`.
- Paso de ejecución de pruebas automatizadas en el flujo de CI de GitHub Actions.

---

## [1.0.0-beta] - 2026-08-30

### Añadido
- **Aplicación Web Progresiva (PWA):**
  - Módulo de autenticación con control de acceso por roles (Dueño/Admin y Operador).
  - Dashboard interactivo con indicadores clave (ventas de hoy, pedidos pendientes, alertas de stock y pedidos en riesgo).
  - Módulo de gestión y seguimiento de pedidos en tiempo real con filtrado por canal (WhatsApp, Llamada, Sistema) y estado operativo.
  - Formulario ágil de registro de pedidos con autocalculado de subtotales, delivery y descuentos.
  - Catálogo y control de inventario de productos deportivos con alerta visual de stock crítico (< 5 unidades).
  - Soporte offline y manifest PWA para instalación móvil en Android e iOS.
- **Documentación Técnica y Académica (/docs):**
  - `01_Ficha_Identificacion`: Ficha oficial del proyecto y mapeo organizacional.
  - `02_Requerimientos`: Especificación formal de requerimientos funcionales (RF) y no funcionales (RNF).
  - `03_Acta_Reunion_1`: Minuta de alineamiento con el dueño del negocio (Víctor Cárdenas).
  - `04_Glosario`: Definiciones de negocio y terminología técnica.
  - `05_Preguntas_Criticas_Panel`: Análisis de contingencias, KPIs y decisiones de diseño.
  - `06_Especificacion_PWA_Prompt`: Especificación completa del frontend PWA.
  - `07_Arquitectura_Sistema`: Documento formal de Arquitectura de Software (SAD) basado en el modelo de vistas 4+1 y registros ADR.
- **Diagramas de Arquitectura y Procesos (/diagrams):**
  - BPMN AS-IS (proceso manual actual).
  - Flujo de Proceso TO-BE (digitalizado).
  - Diagrama de Arquitectura Multicapa del Sistema.
  - Matriz de Riesgos y Matriz RF/RNF.
- **DevOps & CI/CD:**
  - Pipeline de despliegue automático a GitHub Pages (`.github/workflows/deploy.yml`).
  - Pipeline de escaneo de secretos y auditoría de seguridad (`.github/workflows/security-scan.yml`).
