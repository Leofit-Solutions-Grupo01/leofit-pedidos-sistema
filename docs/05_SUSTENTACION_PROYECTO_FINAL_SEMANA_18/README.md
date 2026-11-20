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
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.pptx) | PowerPoint (.pptx) | Widescreen 16:9, **25 diapositivas ejecutivas**, tablas nativas, paleta institucional Navy/Cobalt/Terracotta WCAG AAA, notas de orador en el 100% de las diapositivas | **Entregable Oficial de Sustentación.** Archivo ejecutable de presentación formal para el jurado evaluador con alta densidad técnica y visual. |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.html) | HTML5 Responsivo Standalone | Visor web interactivo con atajos de teclado (`<-` / `->`), modo pantalla completa y panel lateral de notas de orador (tecla `N`) | Visualización interactiva en cualquier navegador sin necesidad de suite ofimática instalada. |
| [**`03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md`**](./03_PRESENTACION_OFICIAL_SUSTENTACION_PROYECTO_FINAL.md) | Markdown Canónico | Transcripción estructurada diapositiva por diapositiva con textos, tablas y notas completas | Guion técnico de lectura y ensayo coordinado para los 5 integrantes del equipo. |

---

## 2. Estructura Temática de la Presentación (25 Diapositivas)

La presentación está organizada en 6 bloques metodológicos alineados a la ingeniería de software y a las directivas del docente Ing. Enrique Lee Huamani:

```text
BLOQUE I: CONTEXTO Y PROBLEMÁTICA (Slides 1 - 5)
  ├─ Slide 01: Carátula Oficial Institucional UTP
  ├─ Slide 02: Agenda Ejecutiva de Sustentación (6 Bloques)
  ├─ Slide 03: Empresa Patrocinadora: LeoFit Confecciones y Diseños Deportivos S.A.C.
  ├─ Slide 04: Problemática Empresarial y Cuantificación de Pérdidas Operativas
  └─ Slide 05: Objetivos del Proyecto y Matriz de Alineamiento Estratégico

BLOQUE II: ARQUITECTURA Y DISEÑO TÉCNICO (Slides 6 - 9)
  ├─ Slide 06: Arquitectura de Software C4 (Nivel 1 Contexto y Nivel 2 Contenedores)
  ├─ Slide 07: Proceso de Negocio BPMN (AS-IS Manual vs TO-BE Automatizado)
  ├─ Slide 08: Modelo de Datos Relacional PostgreSQL 16 en Boyce-Codd (BCNF)
  └─ Slide 09: Decisiones de Arquitectura Cloud (ADR-001 Render/Neon y ADR-002 AWS)

BLOQUE III: DESARROLLO, SEGURIDAD Y DEMO EN VIVO (Slides 10 - 13)
  ├─ Slide 10: Stack Tecnológico de Ingeniería (Frontend, Backend, DB, DevOps)
  ├─ Slide 11: Seguridad Defensiva en Profundidad (OWASP Top 10, JWT, HMAC, RBAC)
  ├─ Slide 12: Demostración en Vivo del Sistema PWA (Flujo de Pedido e Inventario)
  └─ Slide 13: Experiencia de Usuario y Accesibilidad (SUS 88.5/100, WCAG 2.1 AA)

BLOQUE IV: CALIDAD DE SOFTWARE ISO/IEC 25010:2023 (Slides 14 - 17)
  ├─ Slide 14: Marco de Calidad ISO 25010: Eficiencia, Flexibilidad y Mantenibilidad
  ├─ Slide 15: Pruebas de Rendimiento k6 (p50/p95, CPU, RAM y Optimización B-Tree)
  ├─ Slide 16: Flexibilidad Arquitectónica (Clean Architecture y Escalabilidad Elástica)
  └─ Slide 17: Mantenibilidad y Pirámide de Pruebas (TDD, 194 Tests 100% OK)

BLOQUE V: CONTINUIDAD OPERATIVA Y RESILIENCIA (Slides 18 - 20)
  ├─ Slide 18: Alta Disponibilidad (HA 24/7 Uptime 99.9% vs Computación HPC)
  ├─ Slide 19: Plan de Recuperación ante Desastres DRP (Simulacro RTO 3.2s, RPO 0s)
  └─ Slide 20: Estrategia de Respaldo PITR, Snapshots y Monitoreo Proactivo

BLOQUE VI: GESTIÓN, AUDITORÍA Y CONCLUSIONES (Slides 21 - 25)
  ├─ Slide 21: Auditoría de Calidad y Matriz de Deuda Técnica (ISO 29119)
  ├─ Slide 22: Análisis de Retorno de Inversión (ROI 243%, VAN S/ 86,400, Payback 4.8m)
  ├─ Slide 23: Cumplimiento de Rúbrica Institucional UTP y Cronograma
  ├─ Slide 24: Conclusiones de Ingeniería y Recomendaciones Operativas
  └─ Slide 25: Agradecimientos y Panel de Defensa Técnica Abierto
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
