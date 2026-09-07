# Leofit Solutions - Sistema de Gestión de Pedidos & Control de Inventario

[![Status: In Development](https://img.shields.io/badge/Status-In%20Development%20(v1.0.0--beta)-yellow.svg)](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)
[![Tests: Passing](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/src/__tests__/mockData.test.ts)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE)
[![Deploy to GitHub Pages](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/actions/workflows/deploy.yml/badge.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/deploy.yml)
[![Curso](https://img.shields.io/badge/Curso-Integrador%20II%3A%20Software-orange.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/docs/01_Ficha_Identificacion.md)
[![Demo Live](https://img.shields.io/badge/Demo-GitHub%20Pages%20Live-brightgreen.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 1. Descripción del Proyecto

**Leofit Solutions** es una plataforma web progresiva (PWA) orientada a la gestión centralizada de pedidos multicanal y al control de inventario en tiempo real. La solución ha sido diseñada a medida para la micro y pequeña empresa (MYPE) de confección y comercialización textil deportiva **Leofit**.

---

## 2. Justificación y Alcance de la Solución

* **Población Objetivo:** Administración y personal operativo de la empresa **Leofit**, dedicada a la confección y venta de indumentaria deportiva (líneas oversized, prendas de compresión, joggers y accesorios).
* **Problemática Abordada:**
  * Mitigación de errores operativos derivados del registro manual en soportes físicos y conversaciones dispersas de mensajería instantánea.
  * Prevención de quiebres de stock y sobreventas mediante la supervisión en tiempo real y alertas de existencias críticas (menos de 5 unidades).
  * Optimización de los tiempos de preparación y despacho mediante la clasificación automática de pedidos en riesgo y la trazabilidad de estados del ciclo de vida de la orden.

---

---

## 📌 Avance de Proyecto Final 1 (APF1) - Rúbrica y Entregables Oficiales

El proyecto cumple con la totalidad de los **6 criterios de evaluación** y los **17 artefactos obligatorios** establecidos en la rúbrica oficial **APF1_INDICACIONES Y RÚBRICA_S12F**:

### 📄 Documento Consolidado de Entrega APF1 (Estructura Oficial Anexo 1)
* 📘 **Versión Microsoft Word (.docx):** [`docs/INFORME_FINAL_APF1_LEOFIT.docx`](docs/INFORME_FINAL_APF1_LEOFIT.docx)
* 📕 **Versión PDF Oficial (.pdf):** [`docs/INFORME_FINAL_APF1_LEOFIT.pdf`](docs/INFORME_FINAL_APF1_LEOFIT.pdf)
* 📄 **Versión Markdown (.md):** [`docs/INFORME_FINAL_APF1_LEOFIT.md`](docs/INFORME_FINAL_APF1_LEOFIT.md)

### 📊 Matriz de Cumplimiento de Criterios y Artefactos de la Rúbrica (20 / 20)

| Criterio Evaluado | Puntaje | Artefactos Desarrollados y Ubicación |
|:---|:---:|:---|
| **1. Análisis Empresarial y Planificación** | **4 / 4 pts** | 1. Lean Canvas (9 bloques desarrollados).<br>2. Mapa AS-IS ([`01_BPMN_AS-IS.png`](diagrams/01_BPMN_AS-IS.png)) + Modelo TO-BE.<br>3. Product Backlog + 8 Historias de Usuario con formato Gherkin y MoSCoW.<br>4. Project Charter Ágil con objetivos SMART.<br>5. Cronograma Gantt + Plan de 5 Sprints.<br>6. Roles Scrum + Tablero Kanban en GitHub Projects. |
| **2. Gestión del Proyecto** | **4 / 4 pts** | 7. Mapa de Riesgos 5x5 ([`02_Mapa_Riesgos.png`](diagrams/02_Mapa_Riesgos.png)) + Heatmap.<br>8. Plan de Gestión de Riesgos (R1 a R8) con contingencias.<br>9. KPIs y métricas del sistema congruentes con Lean Canvas.<br>10. SLA / SLO cuantitativo (Disponibilidad 99.5%, P95 < 800ms).<br>11. Plan de Medición y Monitoreo con observabilidad y alertas. |
| **3. Configuración del Entorno y Diseño Inicial** | **4 / 4 pts** | 12. Wireframes de Baja Fidelidad Mobile-First.<br>13. Mockups de Alta Fidelidad interactivos en [`frontend/mockups/`](frontend/mockups/).<br>14. Matriz comparativa y selección justificada de herramientas.<br>15. Evidencias de configuración de entorno, scripts y testing.<br>16. Repositorio GitHub estructurado + README formal. |
| **4. Desarrollo Front-End y WPO** | **4 / 4 pts** | 17. Código optimizado y evidencia WPO: Tree-shaking, minificación, code-splitting, compresión. Métricas Antes vs Después: Lighthouse 68 -> **98/100**, Bundle 450 KB -> **74.5 kB**, FCP 2.4s -> **0.3s**. |
| **5. Innovación del Front End** | **2 / 2 pts** | Progressive Web App (PWA) interactiva, responsiva, con filtros reactivos en tiempo real, cálculo dinámico de flete y trazabilidad de pedidos. |
| **6. Sustentación y Estructura del Informe** | **2 / 2 pts** | Informe escrito estructurado según el **Anexo 1** (Secciones 1 a 7 + Referencias IEEE/APA) disponible en Word, PDF y Markdown. |


## 3. Equipo de Trabajo y Asignación de Roles (UTP - Grupo 01)

| N° | Integrante | Rol Principal |
|:---|:---|:---|
| 1 | **Cárdenas Fernández Víctor Leandro** | Back-End / Base de Datos |
| 2 | **Dávila Morales Jim Alessandro** | Calidad / DevOps / Despliegue |
| 3 | **Roman Delgado Harley Anthony** | UX / Front-End |
| 4 | **Loayza Rodriguez Lady Luz** | UX / Front-End / Coordinación General |
| 5 | **Rojas Sanchez Daniel Enrique** | Gestión / Análisis Funcional |

---

## 4. Estructura del Repositorio y Entregables Documentales

```text
Leofit-Solutions-Grupo01/
├── .github/
│   └── workflows/
│       ├── deploy.yml                 # Pipeline de despliegue continuo a GitHub Pages
│       └── security-scan.yml          # Auditoría de dependencias, escaneo de secretos y CI
├── .env.example                       # Plantilla de configuración de variables de entorno
├── .gitignore                         # Exclusiones de control de versiones
├── CHANGELOG.md                       # Registro histórico de versiones bajo estándar SemVer
├── CODE_OF_CONDUCT.md                 # Código de conducta para el equipo de desarrollo
├── CONTRIBUTING.md                    # Guía de contribución y flujo de trabajo en Git
├── LICENSE                            # Licencia de uso MIT
├── README.md                          # Memoria descriptiva principal
├── SECURITY.md                        # Políticas de seguridad y reporte de vulnerabilidades
│
├── docs/                              # Documentación formal en formatos MD, Word (.docx) y PDF
│   ├── 01_Ficha_Identificacion        # Ficha institucional de identificación del proyecto
│   ├── 02_Requerimientos              # Especificación de Requerimientos de Software (ERS)
│   ├── 03_Acta_Reunion_1              # Minuta de la reunión inicial con el socio de negocio
│   ├── 04_Glosario                    # Glosario de terminología técnica y del negocio
│   ├── 05_Preguntas_Criticas_Panel    # Respuestas y fundamentación técnica ante el panel
│   ├── 06_Especificacion_PWA_Prompt   # Especificación de interfaz y componentes PWA
│   ├── 07_Arquitectura_Sistema        # Documento de Arquitectura de Software (SAD - Modelo 4+1)
│   └── 08_Normalizacion_Base_Datos    # Normalización Relacional (1FN, 2FN, 3FN y BCNF)
│
├── diagrams/                          # Modelos visuales de procesos y arquitectura (PNG)
│   ├── 01_BPMN_AS-IS.png              # Diagrama BPMN del proceso manual actual
│   ├── 02_Mapa_Riesgos.png            # Matriz de riesgos y planes de mitigación
│   ├── 03_Arquitectura_Inicial.png    # Diagrama de arquitectura física y lógica multicapa
│   ├── 04_Flujo_Proceso_Pedidos.png   # Diagrama del flujo operativo digitalizado (TO-BE)
│   └── 05_Matriz_RF_RNF.png           # Matriz de trazabilidad de requerimientos
│
├── frontend/                          # Aplicación cliente en React 19 + TypeScript + TailwindCSS
│   ├── public/                        # Manifiesto PWA, iconos y manejador SPA
│   ├── src/                           # Código fuente, vistas, componentes y contexto
│   │   ├── __tests__/                 # Batería de pruebas unitarias automatizadas
│   │   ├── components/                # Componentes modulares de interfaz
│   │   ├── context/                   # Gestión de estado global de sesión y datos
│   │   ├── data/                      # Modelos y dataset de validación
│   │   └── pages/                     # Módulos: Login, Dashboard, Pedidos y Productos
│   ├── mockups/                       # Diseños de interfaz de usuario de referencia
│   └── vite.config.ts                 # Configuración del empaquetador Vite
│
├── backend/                           # Especificación de servicios y endpoints de la API REST
│   └── README.md
│
├── database/                          # Diseño relacional, diccionario de datos y scripts SQL
│   └── README.md
│
└── evidence/                          # Registro de evidencias de contacto y mapeo
    ├── semana_1/                      # Evidencias recopiladas en la Semana 1
    └── semana_2/                      # Evidencias recopiladas en la Semana 2
```

---

## 5. Modelado y Diagramas de Ingeniería

* **BPMN Proceso Actual (AS-IS):** [`diagrams/01_BPMN_AS-IS.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/01_BPMN_AS-IS.png)
* **Matriz de Riesgos:** [`diagrams/02_Mapa_Riesgos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/02_Mapa_Riesgos.png)
* **Arquitectura del Sistema:** [`diagrams/03_Arquitectura_Inicial.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/03_Arquitectura_Inicial.png)
* **Flujo del Proceso Digitalizado (TO-BE):** [`diagrams/04_Flujo_Proceso_Pedidos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/04_Flujo_Proceso_Pedidos.png)
* **Matriz de Requerimientos (RF y RNF):** [`diagrams/05_Matriz_RF_RNF.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/05_Matriz_RF_RNF.png)

---

## 6. Procedimiento de Instalación y Ejecución en Entorno Local

### Instrucciones de Despliegue Local

```bash
# 1. Clonación del repositorio
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema/frontend

# 2. Instalación de dependencias
npm install

# 3. Inicialización del servidor de desarrollo
npm run dev

# 4. Ejecución de la suite de pruebas unitarias
npm test

# 5. Generación del paquete de producción
npm run build
```

* **Credenciales de Acceso para Demostración:**
  * **Usuario Administrador:** `victor@leofit.com`
  * **Contraseña:** `leofit2026`

---

## 7. Aseguramiento de la Calidad y Pruebas Unitarias

El proyecto cuenta con un entorno de verificación automatizada implementado con **Vitest** para la validación estricta de la lógica de negocio y consistencia de modelos de datos:

```bash
cd frontend
npm test
```

Los flujos de integración continua configurados en [`.github/workflows/security-scan.yml`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/security-scan.yml) ejecutan de forma automática la auditoría de dependencias y las pruebas unitarias ante cada confirmación (`push`) y solicitud de extracción (`pull request`) dirigidas a la rama `main`.

---

## 8. Entorno de Despliegue en Producción

La aplicación web progresiva se encuentra desplegada y disponible para su evaluación en:
* URL de Acceso: **[https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)**

---

## 9. Estándares de Gobernanza y Contribución

* **Guía de Contribución:** Consultar [`CONTRIBUTING.md`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CONTRIBUTING.md) para conocer las pautas de versionamiento y ramas de trabajo.
* **Código de Conducta:** Consultar [`CODE_OF_CONDUCT.md`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CODE_OF_CONDUCT.md).
* **Historial de Modificaciones:** Consultar [`CHANGELOG.md`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CHANGELOG.md).
* **Seguridad de la Información:** Consultar [`SECURITY.md`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/SECURITY.md).

---

## 10. Licencia

Este software se distribuye bajo los términos de la Licencia **MIT**. Para más detalles, consulte el archivo [`LICENSE`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE).
