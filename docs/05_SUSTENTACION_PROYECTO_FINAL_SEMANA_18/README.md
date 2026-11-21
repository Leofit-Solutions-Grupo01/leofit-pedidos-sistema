# Material Oficial de Sustentación Final de Ingeniería (Semana 18)
## Sistema Web PWA de Gestión de Pedidos Multicanal — LeoFit Solutions
**Universidad Tecnológica del Perú (UTP) — Curso Integrador II: Software (100000S12F)**  
**Docente Asesor Evaluador:** Ing. Enrique Lee Huamani Uriarte  
**Sección:** 35374 | **Ciclo:** 2026-I | **Estado:** APROBADO Y LISTO PARA DEFENSA DE GRADO  

**Equipo de Desarrollo e Ingeniería (Grupo 01):**
* **Lady Luz Loayza Rodríguez** (`U22221489`) — Scrum Master / DevSecOps Lead
* **Víctor Leandro Cárdenas Fernández** (`U19217414`) — Product Owner / DBA
* **Harley Anthony Roman Delgado** (`U21313032`) — Frontend Lead / UI-UX
* **Jim Alessandro Dávila Morales** (`U18206081`) — QA Engineer Lead / Backend
* **Daniel Enrique Rojas Sánchez** (`U21214627`) — Business Analyst / Cloud DevOps

---

## 1. Catálogo de Recursos de la Presentación Final

Esta carpeta consolida la presentación oficial de defensa del proyecto final ante el jurado evaluador y el docente asesor:

| Recurso / Archivo | Formato | Especificaciones Técnicas | Propósito y Audiencia |
| :--- | :--- | :--- | :--- |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx) | PowerPoint (.pptx) | Widescreen 16:9, **25 diapositivas ejecutivas**, tablas dinámicas nativas, paleta institucional Navy/Cobalt/Terracotta WCAG AAA, notas de orador en el 100% de las láminas | **Entregable Oficial de Sustentación.** Archivo ejecutable de presentación formal para el jurado evaluador con alta densidad técnica y visual. |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html) | HTML5 Responsivo Standalone | Visor web interactivo con atajos de teclado (`<-` / `->`), modo pantalla completa y panel lateral de notas de orador (tecla `N`) | Visualización interactiva en cualquier navegador sin necesidad de suite ofimática instalada. |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md) | Markdown Canónico | Transcripción estructurada diapositiva por diapositiva con textos, tablas y notas completas | Guion técnico de lectura y ensayo coordinado para los 5 integrantes del equipo. |

---

## 2. Estructura Temática de la Presentación (25 Diapositivas)

La presentación está organizada en 6 bloques metodológicos alineados a la ingeniería de software y a las directivas del docente Ing. Enrique Lee Huamani:

```text
BLOQUE I: CONTEXTO, PROBLEMÁTICA Y ARQUITECTURA BASE (Slides 1 - 3)
  ├─ Slide 01: Portada Oficial Institucional UTP y Equipo de Ingeniería Grupo 01
  ├─ Slide 02: Contexto Operativo Textil y Cuantificación de Pérdidas Comerciales
  └─ Slide 03: Arquitectura Lógica del Sistema (C4 Modelo - Nivel 2 Contenedores)

BLOQUE II: DECISIONES DE ARQUITECTURA CLOUD - ADRs (Slides 4 - 9)
  ├─ Slide 04: ADR-001: Elección de Render Cloud + Neon PostgreSQL vs AWS
  ├─ Slide 05: Comparativa Técnica y Financiera (Ahorro de $153/mes en Staging)
  ├─ Slide 06: Umbrales Cuantitativos de Migración (80 VU, $1,200 MRR, 15 GB)
  ├─ Slide 07: ADR-002: Arquitectura Objetivo en AWS (ECS Fargate + RDS Multi-AZ)
  ├─ Slide 08: Topología de Red VPC, Seguridad en Capas y Resiliencia
  └─ Slide 09: Lo que AWS NO Conviene Construir (Evitar Sobre-Ingeniería)

BLOQUE III: FACTURACIÓN SUNAT, PAGOS Y SEGURIDAD (Slides 10 - 14)
  ├─ Slide 10: Cumplimiento SUNAT CPE (Esquema XML UBL 2.1 y Firma Criptográfica)
  ├─ Slide 11: Flujo Técnico de Emisión y Contingencias Tributarias
  ├─ Slide 12: Pasarela de Pagos Móviles: Modo Sandbox vs Producción
  ├─ Slide 13: Seguridad Criptográfica, PCI-DSS (SAQ A) y HMAC-SHA256
  └─ Slide 14: Modelo de Datos Relacional (BCNF) y Configuración de Zona Horaria Lima

BLOQUE IV: CALIDAD DE SOFTWARE ISO/IEC 25010:2023 (Slides 15 - 18)
  ├─ Slide 15: Rendimiento k6 (Percentiles p50/p95/p99, SRE Golden Signals, B-Tree)
  ├─ Slide 16: Flexibilidad (Adaptabilidad Twelve-Factor y Resiliencia Cloud)
  ├─ Slide 17: Mantenibilidad (Clean Architecture, Inversión de Dependencias y DRY)
  └─ Slide 18: Modificabilidad (Blast Radius mínimo), Complejidad Ciclomática y TDD

BLOQUE V: CONFIABILIDAD, TESTING Y OPERACIÓN CLOUD (Slides 19 - 22)
  ├─ Slide 19: Confiabilidad: Alta Disponibilidad (HA 24/7 vs HPC), PWA y DRP
  ├─ Slide 20: Batería QA de 194 Pruebas Automatizadas (125 Backend + 69 Frontend)
  ├─ Slide 21: Marco Integral ISO/IEC 25010:2023 (9 Características) y SUS 88.5/100
  └─ Slide 22: Demostración y Validación en Vivo en la Nube (Cloud Staging)

BLOQUE VI: TRAZABILIDAD, CONCLUSIONES Y CIERRE (Slides 23 - 25)
  ├─ Slide 23: Matriz de Trazabilidad ante el Jurado Evaluador UTP
  ├─ Slide 24: Conclusiones de Ingeniería y Recomendaciones Operativas
  └─ Slide 25: Cierre, Agradecimientos y Panel de Defensa Técnica Abierto
```

---

## 3. Instrucciones para la Exposición y Regeneración

### Navegación en el Visor Web Interactivo (`.html`)
* **Flecha Derecha (`->`) / Espacio:** Avanzar a la siguiente diapositiva.
* **Flecha Izquierda (`<-`):** Retroceder a la diapositiva anterior.
* **Tecla `N`:** Mostrar u ocultar el panel flotante de **Notas del Orador**.
* **Tecla `F`:** Activar modo de pantalla completa.

### Regeneración de Recursos
```bash
# Compilar archivo PowerPoint (.pptx)
python scripts/proyecto_final/generate_sustentacion_pptx.py

# Generar Visor Web HTML y Guion Markdown
python scripts/proyecto_final/generate_slides_viewer.py

# Validar integridad y cumplimiento de notas
python scripts/proyecto_final/validate_deliverables.py
```
