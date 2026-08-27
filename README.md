# Leofit Solutions - Sistema de Gestión de Pedidos & Inventario

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/LICENSE)
[![Deploy to GitHub Pages](https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema/actions/workflows/deploy.yml/badge.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/deploy.yml)
[![Curso](https://img.shields.io/badge/Curso-Integrador%20II%3A%20Software-orange.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/docs/01_Ficha_Identificacion.md)
[![Estado](https://img.shields.io/badge/Estado-PWA%20Frontend%20Funcional-green.svg)](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/frontend/)

---

## 📌 1. Descripción del Proyecto

**Leofit** es una PYME familiar peruana orientada a la venta de ropa deportiva de alta calidad (camisetas oversized, pantalones jogger, shorts de compresión, zapatillas y accesorios). 

Este repositorio contiene la aplicación completa **Progressive Web App (PWA)** en React 19 + TypeScript + TailwindCSS v4, su diseño UI/UX, arquitectura backend y la documentación de análisis del proyecto.

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

## 🚀 3. Ejecución Local del Frontend

Para ejecutar la aplicación en tu entorno local:

```bash
# 1. Entrar a la carpeta frontend
cd frontend

# 2. Instalar dependencias
npm install

# 3. Iniciar servidor de desarrollo
npm run dev

# 4. Compilar para producción (Build)
npm run build
```

* **Credenciales de Acceso Demo:**
  * **Usuario:** `victor@leofit.com`
  * **Contraseña:** `leofit2026`

---

## 🌐 4. Despliegue en GitHub Pages

El repositorio cuenta con integración continua (**GitHub Actions CI/CD**) lista en [`.github/workflows/deploy.yml`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/.github/workflows/deploy.yml).

### Para habilitar GitHub Pages en el repositorio:
1. Ir a **Settings** en el repositorio de GitHub.
2. Navegar a **Pages** (en el menú lateral izquierdo).
3. En **Build and deployment > Source**, seleccionar: **GitHub Actions**.
4. ¡Listo! En cada `push` a la rama `main`, la app se compilará y desplegará automáticamente con soporte de rutas relativas y SPA redirect.

---

## 📁 5. Estructura del Repositorio

```text
Leofit-Solutions-Grupo01/
├── .github/
│   └── workflows/
│       ├── deploy.yml                 # Despliegue automático a GitHub Pages
│       └── security-scan.yml          # Auditoría de dependencias y secretos
├── .env.example                       # Plantilla de variables de entorno seguras
├── .gitignore                         # Exclusiones de Git (logs, dist, node_modules, envs)
├── LICENSE                            # Licencia MIT
├── README.md                          # Documentación principal del proyecto
├── SECURITY.md                        # Directrices y políticas de seguridad
│
├── 📁 docs/                           # Documentación de análisis y negocio
│   ├── 01_Ficha_Identificacion.md     # Ficha oficial de mapeo inicial UTP
│   ├── 02_Requerimientos.md           # Requerimientos Funcionales y No Funcionales
│   ├── 03_Acta_Reunion_1.md           # Minuta de primera reunión con Víctor
│   ├── 04_Glosario.md                 # Glosario de términos del negocio y técnicos
│   ├── 05_Preguntas_Criticas_Panel.md # Análisis de KPIs y preguntas de negocio
│   └── 06_Especificacion_PWA_Prompt.md# Especificación detallada de requerimientos PWA
│
├── 📁 diagrams/                       # Diagramas de procesos y arquitectura
│   ├── 01_BPMN_AS-IS.png              # Flujo manual actual
│   ├── 02_Mapa_Riesgos.png            # Matriz de riesgos y mitigación
│   └── 03_Arquitectura_Inicial.png    # Arquitectura de capas del sistema
│
├── 📁 frontend/                       # Aplicación Web React 19 + TypeScript + TailwindCSS
│   ├── public/
│   │   ├── 404.html                   # Manejador SPA para GitHub Pages
│   │   └── manifest.json              # Configuración PWA (instalable en móvil)
│   ├── src/
│   │   ├── components/                # Componentes modulares (Navbar, Modal, Badge, etc.)
│   │   ├── context/                   # AppContext (sesión, estado de pedidos e inventario)
│   │   ├── data/                      # mockData inicial de pedidos y productos
│   │   ├── pages/                     # Login, Dashboard, PedidosLista, PedidoForm, ProductosGestion
│   │   ├── App.tsx                    # Orquestador principal de vistas
│   │   ├── main.tsx                   # Punto de entrada de React
│   │   └── index.css                  # Estilos y tokens con Tailwind v4 y Google Fonts
│   ├── 📁 mockups/                    # Mockups de referencia de diseño UI
│   │   ├── 01_Login.png
│   │   ├── 02_Dashboard.png
│   │   ├── 03_Listado_Pedidos.png
│   │   ├── 04_Formulario_Pedido.png
│   │   └── 05_Gestion_Productos.png
│   ├── index.html                     # Documento HTML principal con Material Icons
│   ├── package.json                   # Dependencias y scripts de construcción
│   ├── tsconfig.json                  # Configuración TypeScript
│   ├── vite.config.ts                 # Configuración de Vite adaptada a GitHub Pages
│   └── README.md                      # Documentación del módulo frontend
│
├── 📁 backend/                        # Arquitectura y servicios de API REST
│   ├── .env.example
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
    └── README.md                      # Modelo Entidad-Relación y diccionario
```

---

## 🔒 6. Seguridad y Buenas Prácticas
Consulta el archivo [`SECURITY.md`](file:///c:/Users/Loayza/Downloads/leofit-pedidos-sistema/SECURITY.md) para conocer las políticas de no exposición de secretos en el frontend público, hashing de contraseñas y validación de entradas.
