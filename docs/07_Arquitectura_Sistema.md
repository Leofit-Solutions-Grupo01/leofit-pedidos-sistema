# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# DOCUMENTO DE ARQUITECTURA DE SOFTWARE (SAD)
## MODELO DE VISTAS 4+1 DE KRUCHTEN Y ESTÁNDAR C4
### PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. CONTROL DEL DOCUMENTO Y EQUIPO DE ARQUITECTURA

* **Institución:** Universidad Tecnológica del Perú (UTP)
* **Curso:** Curso Integrador II: Software (100000S12F)
* **Proyecto:** Progressive Web App (PWA) de Gestión de Pedidos & Inventario LeoFit
* **Equipo de Desarrollo (Grupo 01):**
  1. **Loayza Rodriguez, Lady Luz** - Scrum Master / UX-UI Lead
  2. **Cárdenas Fernández, Víctor Leandro** - Product Owner / Arquitecto Back-End y Base de Datos
  3. **Roman Delgado, Harley Anthony** - Front-End Lead / Especialista PWA y WPO
  4. **Dávila Morales, Jim Alessandro** - QA Engineer / Automatización de Pruebas
  5. **Rojas Sanchez, Daniel Enrique** - Analista Funcional / Modelado de Procesos
* **Versión del Documento:** 1.0.0

---

## 2. REPRESENTACIÓN ARQUITECTÓNICA (VISTA LÓGICA Y DESACOPLAMIENTO)

El sistema implementa una **Arquitectura Limpia (Clean Architecture)** organizada en capas concéntricas con flujo de dependencias unidireccional:

```text
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                     │
│    (React 18 + TypeScript + Tailwind CSS + Lucide Icons)    │
│  [Vistas: Login, Dashboard, PedidoForm, PedidosLista, etc.] │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAPA DE ESTADO Y NEGOCIO                   │
│   (React Context API: AppContext + Custom Hooks + Reducers) │
│ [Lógica: Validación Stock, Cálculo Totales, Filtros Reactivos]│
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE ACCESO A DATOS                      │
│ (Mock Data Engine / REST API Client / LocalStorage Cache)   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. VISTA DE DESARROLLO (ESTRUCTURA MODULAR)

```text
frontend/src/
├── __tests__/            # Suite de pruebas unitarias automatizadas (Vitest)
├── components/           # Componentes modulares reutilizables
│   ├── common/           # Componentes atómicos (Badge, Modal, MontoPrivado)
│   └── layout/           # Elementos estructurales (Navbar)
├── context/              # Capa de estado global inmutable (AppContext.tsx)
├── data/                 # Modelos de datos TypeScript y catálogo (mockData.ts)
└── pages/                # Vistas de la aplicación (Dashboard, Pedidos, Productos, Login)
```

---

## 4. VISTA DE PROCESOS (FLUJO TRANSACCIONAL DE PEDIDOS)

```text
[Cliente: Confirmar Pedido]
           │
           ▼
[AppContext: Validar Existencias de Ítems]
           │
     ┌─────┴─────┐
[Hay Stock]   [Sin Stock] ──► [Notificar Error y Bloquear Envío]
     │
     ▼
[Generar ID Único: PED-2026-XXXX]
     │
     ▼
[Deducir Stock de Productos en Memoria/BD]
     │
     ▼
[Agregar Pedido a Lista Global con Estado: 'Recibido']
     │
     ▼
[Actualizar Tarjetas de Métricas en Dashboard]
```

---

## 5. VISTA FÍSICA Y DE DESPLIEGUE (EDGE SERVERLESS CDN)

* **Proveedor de Infraestructura:** GitHub Pages / Vercel Serverless Edge Network.
* **Seguridad y Transporte:** Certificado SSL/TLS nativo (HTTPS forzado).
* **Distribución de Contenidos:** Red de Entrega de Contenidos (CDN) global con puntos de presencia de baja latencia.
* **Integración Continua:** GitHub Actions ejecutando pipelines automáticos de auditoría de seguridad y despliegue continuo ante cada confirmación a la rama `main`.
