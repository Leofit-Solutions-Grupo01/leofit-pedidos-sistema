# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# ESPECIFICACIÓN TÉCNICA DE LA PROGRESSIVE WEB APP (PWA) Y ARQUITECTURA DE INTERFAZ
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. INTRODUCCIÓN Y CONTEXTO TÉCNICO
El presente documento describe la especificación técnica de la **Progressive Web App (PWA)** desarrollada para la empresa **LeoFit**. La arquitectura está concebida bajo principios de modularidad, diseño responsive *Mobile-First*, gestión reactiva del estado y optimización de rendimiento web (WPO), garantizando una experiencia de usuario fluida tanto en dispositivos móviles inteligentes como en estaciones de escritorio.

---

## 2. CONFIGURACIÓN DEL MANIFIESTO WEB (WEB APP MANIFEST)

El archivo `manifest.json` define los metadatos necesarios para permitir la instalación de la aplicación en la pantalla de inicio del usuario:

```json
{
  "short_name": "LeoFit",
  "name": "LeoFit - Sistema de Gestión y Pedidos",
  "icons": [
    {
      "src": "pwa-192x192.png",
      "type": "image/png",
      "sizes": "192x192"
    },
    {
      "src": "pwa-512x512.png",
      "type": "image/png",
      "sizes": "512x512",
      "purpose": "any maskable"
    }
  ],
  "start_url": "./index.html",
  "background_color": "#090D16",
  "theme_color": "#F97316",
  "display": "standalone",
  "orientation": "portrait"
}
```

---

## 3. ESTRATEGIAS DE SERVICE WORKER Y ALMACENAMIENTO EN CACHÉ

1. **Estrategia Cache-First (Recursos Estáticos):** Tipografías, hojas de estilo CSS minificadas y componentes gráficos estáticos se sirven directamente desde la memoria caché del Service Worker para garantizar renderizado instantáneo en $< 300$ ms.
2. **Estrategia Network-First con Fallback (Datos Dinámicos):** Las transacciones de pedidos e inventario consultan primero la capa de red; en caso de interrupción de conectividad, se utiliza el almacenamiento local inmutable (*LocalStorage*) para evitar pérdidas de información.

---

## 4. SISTEMA DE DISEÑO (DESIGN SYSTEM) Y ERGONOMÍA VISUAL

### 4.1. Tokens de Color Corporativos:
* **Color Primario (Acento / Energía):** Naranja Fitness `#F97316` (RGB: 249, 115, 22).
* **Color Secundario (Fondo Principal):** Slate Oscuro `#0F172A` y Carbon `#090D16`.
* **Superficies y Tarjetas:** Slate `#1E293B` con bordes sutiles en `#334155`.
* **Estados Operativos:**
  - `Recibido`: Azul Cielo `#0284C7`.
  - `En Preparación`: Ámbar `#D97706`.
  - `En Camino`: Violeta `#7C3AED`.
  - `Entregado`: Verde Esmeralda `#059669`.
  - `Cancelado`: Rojo Carmesí `#DC2626`.

### 4.2. Tipografía y Jerarquía:
* **Familia Tipográfica:** *Inter / System UI Sans* con carga asíncrona optimizada (`font-display: swap`).
* **Escala Modular:** Titulares h1 (24px bold), subtítulos h2 (18px semi-bold), cuerpo de texto (14px regular), metadatos y badges (12px medium).

---

## 5. CONTRATO DE INTERFACES Y MODELOS DE DATOS TYPESCRIPT

```typescript
// frontend/src/data/mockData.ts (Extracto de Interfaces Formales)

export interface Producto {
  id: string;
  nombre: string;
  categoria: string;
  precio: number;
  stock: number;
  talla: string;
  color: string;
  imagen: string;
}

export interface ItemPedido {
  productoId: string;
  nombre: string;
  talla: string;
  color: string;
  cantidad: number;
  precioUnitario: number;
  subtotal: number;
}

export type EstadoPedido = 'Recibido' | 'En Preparación' | 'En Camino' | 'Entregado' | 'Cancelado';

export interface Pedido {
  id: string;
  clienteNombre: string;
  clienteTelefono: string;
  clienteDireccion: string;
  items: ItemPedido[];
  subtotal: number;
  costoEnvio: number;
  total: number;
  metodoPago: 'Yape' | 'Plin' | 'Transferencia' | 'Efectivo';
  estado: EstadoPedido;
  fechaCreacion: string;
  fechaActualizacion: string;
}
```

---

## 6. ALINEACIÓN CON EL ESTADO DEL ARTE Y CONCURRENCIA OPTIMISTA (INTEGRACIÓN TEÓRICA)

Para dotar a la Progressive Web App de un valor operativo significativo y un rigor académico alineado con el marco teórico del proyecto, la experiencia de usuario y el diseño del flujo de compra (Checkout Flow) están diseñados utilizando los principios de **Control de Concurrencia Optimista (Optimistic Concurrency Control)**, tal como fue formalizado por **Kung y Robinson (1981)** y contrastado en arquitecturas modernas por **Menascé (1982)** y **Yu et al. (2014)**.

### 6.1. ¿Cómo se refleja el marco teórico en la PWA?
A nivel de frontend, la PWA asume una postura *Optimista*:
1. **Fase de Lectura (Read Phase):** El cliente navega por el catálogo y agrega productos al carrito asumiendo que el stock mostrado en la caché (vía Service Worker) es válido. **No se imponen bloqueos (locks)** ni se congela la interfaz del usuario. Esto maximiza la fluidez (WPO) y evita tiempos de espera innecesarios.
2. **Fase de Validación y Escritura (Validation & Write Phase):** Cuando el usuario confirma el pedido, la PWA lanza la solicitud al backend. Si en ese microsegundo otro usuario concurrentemente agotó el stock (generando un error de asilamiento bajo SSI), la PWA captura el rechazo del backend de forma limpia.
3. **Manejo Resiliente del Conflicto:** En lugar de lanzar errores técnicos crípticos (típicos de bloqueos pesimistas donde la petición entra en un timeout de *deadlock*), la PWA notifica al cliente elegante y reactivamente: *"Lo sentimos, el producto acaba de agotarse. Su carrito ha sido actualizado."*

Este diseño demuestra que las decisiones tomadas en el backend (Niveles de Aislamiento) no son entes aislados, sino que **potencian la agilidad y escalabilidad del Frontend PWA**, alineando el comportamiento empírico del sistema de LeoFit con la literatura científica de la carpeta `vu`.
