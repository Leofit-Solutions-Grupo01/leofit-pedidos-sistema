# Leofit Solutions - Sistema de Gestión de Pedidos & Inventario

[![Status: In Development](https://img.shields.io/badge/Status-In%20Development%20(v1.0.0--beta)-yellow.svg)](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema)
[![Tests: Passing](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/src/__tests__/mockData.test.ts)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE)
[![Deploy to GitHub Pages](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/actions/workflows/deploy.yml/badge.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/deploy.yml)
[![Curso](https://img.shields.io/badge/Curso-Integrador%20II%3A%20Software-orange.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/docs/01_Ficha_Identificacion.md)
[![Demo Live](https://img.shields.io/badge/Demo-GitHub%20Pages%20Live-brightgreen.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 📌 1. ¿Qué es el proyecto?

**Leofit Solutions** es una plataforma web progresiva (PWA) para la gestión centralizada de pedidos multicanal y control de inventario en tiempo real, diseñada a medida para la PYME textil deportiva **Leofit**.

---

## 🎯 2. ¿Para quién es y qué problema resuelve?

* **Público Objetivo:** Dueño y equipo operativo de **Leofit**, PYME familiar peruana confeccionista y comercializadora de ropa deportiva (oversized, compresión, joggers, accesorios).
* **Problema que resuelve:** 
  * Eliminación del desorden operativo causado por la toma manual de pedidos en cuadernos y chats dispersos de WhatsApp.
  * Prevención de quiebres de stock y sobreventas gracias a alertas visuales de inventario crítico (< 5 unidades).
  * Reducción de retrasos en entregas mediante el cálculo automático de pedidos **"En Riesgo"** y seguimiento en tiempo real de estados de preparación y despacho.

---

## 👥 3. Integrantes del Equipo (Grupo 01 - UTP)

| N° | Integrante | Rol Principal |
|:---|:---|:---|
| 1 | **Cárdenas Fernández Víctor Leandro** | Back-End / Base de Datos |
| 2 | **Dávila Morales Jim Alessandro** | Calidad / DevOps / Despliegue |
| 3 | **Roman Delgado Harley Anthony** | UX / Front-End |
| 4 | **Loayza Rodriguez Lady Luz** | UX / Front-End / Coordinación |
| 5 | **Rojas Sanchez Daniel Enrique** | Gestión / Análisis Funcional |

---

## 📁 4. Estructura del Repositorio y Documentación

```text
Leofit-Solutions-Grupo01/
├── .github/
│   └── workflows/
│       ├── deploy.yml                 # Despliegue automático a GitHub Pages
│       └── security-scan.yml          # Auditoría, escaneo de secretos y CI tests
├── .env.example                       # Plantilla de variables de entorno
├── .gitignore                         # Exclusiones de Git
├── CHANGELOG.md                       # Historial de cambios y versiones (SemVer)
├── CODE_OF_CONDUCT.md                 # Código de conducta para la comunidad
├── CONTRIBUTING.md                    # Guía de contribución y flujo Git
├── LICENSE                            # Licencia MIT
├── README.md                          # Documentación principal
├── SECURITY.md                        # Políticas de seguridad y reporte responsable
│
├── 📁 docs/                           # Documentación formal en MD, Word (.docx) y PDF (.pdf)
│   ├── 01_Ficha_Identificacion (.md | .docx | .pdf)   # Ficha de mapeo oficial UTP
│   ├── 02_Requerimientos (.md | .docx | .pdf)         # Requerimientos RF y RNF
│   ├── 03_Acta_Reunion_1 (.md | .docx | .pdf)         # Minuta de primera reunión con Víctor
│   ├── 04_Glosario (.md | .docx | .pdf)               # Glosario técnico y del negocio
│   ├── 05_Preguntas_Criticas_Panel (.md | .docx | .pdf) # Análisis de KPIs operativos
│   └── 06_Especificacion_PWA_Prompt (.md | .docx | .pdf)# Especificación técnica PWA
│
├── 📁 diagrams/                       # Diagramas de procesos y arquitectura (PNG Alta Res)
│   ├── 01_BPMN_AS-IS.png              # Diagrama BPMN del flujo manual actual
│   ├── 02_Mapa_Riesgos.png            # Matriz de evaluación de riesgos y mitigación
│   ├── 03_Arquitectura_Inicial.png    # Arquitectura del sistema web multicapa
│   ├── 04_Flujo_Proceso_Pedidos.png   # Flujo digital del proceso de pedidos (TO-BE)
│   └── 05_Matriz_RF_RNF.png           # Matriz visual de requerimientos RF y RNF
│
├── 📁 frontend/                       # Aplicación Web React 19 + TypeScript + TailwindCSS
│   ├── public/
│   │   ├── 404.html                   # Manejador SPA para GitHub Pages
│   │   └── manifest.json              # Configuración PWA (instalable en móvil)
│   ├── src/
│   │   ├── __tests__/                 # Pruebas unitarias con Vitest
│   │   ├── components/                # Componentes (Navbar, Modal, Badge, MontoPrivado)
│   │   ├── context/                   # AppContext (sesión, pedidos e inventario)
│   │   ├── data/                      # mockData inicial de pedidos y productos
│   │   ├── pages/                     # Login, Dashboard, PedidosLista, PedidoForm, ProductosGestion
│   │   ├── App.tsx                    # Enrutador principal de vistas
│   │   └── main.tsx                   # Punto de entrada de React
│   ├── 📁 mockups/                    # Diseños UI de referencia
│   ├── index.html                     # HTML principal con Google Fonts y Material Icons
│   └── vite.config.ts                 # Configuración Vite adaptada a GitHub Pages
│
├── 📁 backend/                        # Arquitectura y servicios de API REST
│   └── README.md
│
├── 📁 evidence/                       # Evidencias de la empresa y entrevistas
│   ├── 📁 semana_1/
│   │   ├── Evidencia_Contacto.png     # Captura de WhatsApp con el dueño
│   │   └── Ficha_Mapeo_Original.pdf   # PDF oficial completado Semana 1
│   └── 📁 semana_2/
│       └── .gitkeep
│
└── 📁 database/                       # Persistencia relacional
    └── README.md                      # Modelo Entidad-Relación y diccionario SQL
```

---

## 📊 5. Diagramas del Proyecto

* **BPMN Proceso Actual (AS-IS):** [`diagrams/01_BPMN_AS-IS.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/01_BPMN_AS-IS.png)
* **Mapa de Riesgos:** [`diagrams/02_Mapa_Riesgos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/02_Mapa_Riesgos.png)
* **Arquitectura del Sistema:** [`diagrams/03_Arquitectura_Inicial.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/03_Arquitectura_Inicial.png)
* **Flujo del Proceso Digital (TO-BE):** [`diagrams/04_Flujo_Proceso_Pedidos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/04_Flujo_Proceso_Pedidos.png)
* **Matriz de Requerimientos (RF y RNF):** [`diagrams/05_Matriz_RF_RNF.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/05_Matriz_RF_RNF.png)

---

## 🚀 6. Instalación y Ejecución Local

### Comandos Rápidos

Puedes ejecutar los comandos directamente desde la raíz del proyecto o dentro de la carpeta `frontend/`:

```bash
# 1. Clonar el repositorio
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema

# 2. Instalar dependencias
npm --prefix frontend install
# o simplemente: cd frontend && npm install

# 3. Iniciar servidor de desarrollo en vivo
npm run dev

# 4. Ejecutar pruebas unitarias automatizadas
npm test

# 5. Compilar para producción
npm run build
```

* **Credenciales de Acceso Demo:**
  * **Usuario:** `victor@leofit.com`
  * **Contraseña:** `leofit2026`

---

## 🧪 7. Pruebas y Calidad de Código

El proyecto cuenta con validación de modelos y lógica de negocio mediante **Vitest**:

```bash
cd frontend
npm test
```

Los flujos de integración continua en [`.github/workflows/security-scan.yml`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/security-scan.yml) ejecutan automáticamente las pruebas y la auditoría de dependencias ante cada push y pull request a la rama `main`.

---

## 🌐 8. Despliegue en Vivo

La aplicación web está desplegada y lista para ser utilizada en:
👉 **[https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)**

---

## 🤝 9. Comunidad y Gobernanza

* **¿Cómo contribuir?** Consulta nuestra [Guía de Contribución](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CONTRIBUTING.md).
* **Código de Conducta:** Revisa nuestro [Código de Conducta](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CODE_OF_CONDUCT.md).
* **Historial de Cambios:** Consulta el [CHANGELOG](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/CHANGELOG.md).
* **Seguridad:** Revisa las políticas y reporte responsable en [SECURITY.md](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/SECURITY.md).

---

## 📄 10. Licencia

Este proyecto está bajo la Licencia **MIT**. Consulta el archivo [`LICENSE`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE) para más detalles.
