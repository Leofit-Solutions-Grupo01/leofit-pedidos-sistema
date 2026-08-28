# Leofit Solutions - Sistema de Gestión de Pedidos & Inventario

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE)
[![Deploy to GitHub Pages](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/actions/workflows/deploy.yml/badge.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/deploy.yml)
[![Curso](https://img.shields.io/badge/Curso-Integrador%20II%3A%20Software-orange.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/docs/01_Ficha_Identificacion.md)
[![Demo Live](https://img.shields.io/badge/Demo-GitHub%20Pages%20Live-brightgreen.svg)](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)

---

## 📌 1. Descripción del Proyecto

**Leofit** es una PYME familiar peruana dedicada a la confección y venta de ropa deportiva de alto rendimiento (camisetas oversized, shorts de compresión, joggers, bividis y accesorios). 

Este repositorio contiene:
1. **Documentación Formal:** Fichas de identificación, requerimientos RF/RNF, actas de reunión y glosario en formatos **Markdown (.md)**, **Word (.docx)** y **PDF (.pdf)**.
2. **Diagramas Técnicos:** Diagramas BPMN AS-IS, flujo de proceso TO-BE, arquitectura en capas, matriz de riesgos y matriz de requerimientos.
3. **Aplicación Web PWA:** Código fuente en React 19 + TypeScript + TailwindCSS v4 listo para operar y desplegado en GitHub Pages.

---

## 👥 2. Integrantes del Equipo (Grupo 01 - UTP)

| N° | Integrante | Rol Principal |
|:---|:---|:---|
| 1 | **Cárdenas Fernández Víctor Leandro** | Back-End / Base de Datos |
| 2 | **Dávila Morales Jim Alessandro** | Calidad / DevOps / Despliegue |
| 3 | **Roman Delgado Harley Anthony** | UX / Front-End |
| 4 | **Loayza Rodriguez Lady Luz** | UX / Front-End / Coordinación |
| 5 | **Rojas Sanchez Daniel Enrique** | Gestión / Análisis Funcional |

---

## 📁 3. Estructura del Repositorio y Documentación

```text
Leofit-Solutions-Grupo01/
├── .github/
│   └── workflows/
│       ├── deploy.yml                 # Despliegue automático a GitHub Pages
│       └── security-scan.yml          # Auditoría de dependencias y escaneo de secretos
├── .env.example                       # Plantilla de variables de entorno
├── .gitignore                         # Exclusiones de Git
├── LICENSE                            # Licencia MIT
├── README.md                          # Documentación principal
├── SECURITY.md                        # Directrices y políticas de seguridad
│
├── 📁 docs/                           # Documentación en MD, Word (.docx) y PDF (.pdf)
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
│   │   ├── components/                # Componentes (Navbar, Modal, Badge, MontoPrivado)
│   │   ├── context/                   # AppContext (sesión, estado de pedidos e inventario)
│   │   ├── data/                      # mockData inicial de pedidos y productos
│   │   ├── pages/                     # Login, Dashboard, PedidosLista, PedidoForm, ProductosGestion
│   │   ├── App.tsx                    # Enrutador principal de vistas
│   │   └── main.tsx                   # Punto de entrada de React
│   ├── 📁 mockups/                    # Diseños UI de referencia
│   │   ├── 01_Login.png
│   │   ├── 02_Dashboard.png
│   │   ├── 03_Listado_Pedidos.png
│   │   ├── 04_Formulario_Pedido.png
│   │   └── 05_Gestion_Productos.png
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

## 📊 4. Diagramas del Proyecto

* **BPMN Proceso Actual (AS-IS):** [`diagrams/01_BPMN_AS-IS.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/01_BPMN_AS-IS.png)
* **Mapa de Riesgos:** [`diagrams/02_Mapa_Riesgos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/02_Mapa_Riesgos.png)
* **Arquitectura del Sistema:** [`diagrams/03_Arquitectura_Inicial.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/03_Arquitectura_Inicial.png)
* **Flujo del Proceso Digital (TO-BE):** [`diagrams/04_Flujo_Proceso_Pedidos.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/04_Flujo_Proceso_Pedidos.png)
* **Matriz de Requerimientos (RF y RNF):** [`diagrams/05_Matriz_RF_RNF.png`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/diagrams/05_Matriz_RF_RNF.png)

---

## 🚀 5. Ejecución Local del Frontend

```bash
# 1. Entrar a la carpeta frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev

# 4. Compilar para producción
npm run build
```

* **Credenciales Demo:**
  * **Usuario:** `victor@leofit.com`
  * **Contraseña:** `leofit2026`

---

## 🌐 6. Despliegue en GitHub Pages
La aplicación web se encuentra desplegada y disponible en:
👉 **[https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/](https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/)**
