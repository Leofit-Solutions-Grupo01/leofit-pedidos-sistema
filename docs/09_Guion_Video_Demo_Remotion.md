# Guía y Guion Técnico Audiovisual - Demostración del Sistema LeoFit Solutions

Este documento establece el guion técnico, estructura de escenas (storyboard), especificación de captura audiovisual y plantilla programática (Code-First con **Remotion / Motion Canvas / OBS Studio**) para la sustentación y demostración en video del **Avance de Proyecto Final 1 (APF1)**.

---

## 1. Ficha Técnica de Producción Audiovisual

| Parámetro | Especificación Técnica |
|:---|:---|
| **Duración Total** | 3 minutos y 30 segundos (210 segundos) |
| **Resolución y Formato** | 1920x1080 Full HD (16:9), 60 FPS, Códec H.264 / AAC |
| **Herramientas de Animación Programática** | **Remotion** (React 19 / TypeScript) / **Motion Canvas** |
| **Herramientas de Captura de Pantalla** | **OBS Studio** (Grabación sin pérdidas) / **ScreenStudio** (Zoom dinámico en UI) |
| **Herramientas de Edición y Subtitulado** | **CapCut Pro** / **Descript** (Normalización de audio a -14 LUFS y subtítulos automáticos sincronizados) |
| **Paleta de Identidad Visual** | Azul Marino (`#1D3557`), Rojo Coral (`#E63946`), Blanco Nieve (`#F1FAEE`), Verde Éxito (`#27AE60`) |

---

## 2. Storyboard y Guion Técnico por Escenas

### Escena 1: Presentación Institucional y Problemática de Negocio
* **Tiempo:** `00:00 - 00:35` (35 seg)
* **Visual / Animación:** Renderizado en **Remotion** con logo LeoFit Solutions, títulos con Motion Blur, nombres de los 5 integrantes UTP y transición hacia diagrama BPMN AS-IS ([`01_BPMN_AS-IS.png`](../diagrams/01_BPMN_AS-IS.png)) con resaltado de puntos de dolor (mensajes de WhatsApp perdidos, descontrol de stock).
* **Voz en Off (Lady Loayza / Daniel Rojas):**
  > "Buenas tardes, profesor y miembros del jurado. Somos el Grupo 01 de Curso Integrador II y presentamos LeoFit Solutions, una Plataforma Web Progresiva diseñada para digitalizar la recepción de pedidos multicanal y el control de inventario en tiempo real de la marca textil deportiva LeoFit. Actualmente, LeoFit opera de forma manual mediante libretas y chats dispersos de WhatsApp, generando pérdida de pedidos y retrasos en las entregas. Hoy demostraremos cómo nuestra solución resuelve esta problemática con rigor técnico y eficiencia de software."

---

### Escena 2: Arquitectura del Sistema, C4 Model y Normalización de BD
* **Tiempo:** `00:35 - 01:15` (40 seg)
* **Visual / Animación:** Zoom dinámico en **C4 Model Nivel 2** ([`11_Arquitectura_C4_Model.png`](../diagrams/11_Arquitectura_C4_Model.png)) y Diagrama Entidad-Relación ([`12_Modelo_Entidad_Relacion.png`](../diagrams/12_Modelo_Entidad_Relacion.png)). Resaltado de transacciones ACID y relaciones 3FN/BCNF.
* **Voz en Off (Víctor Cárdenas):**
  > "El núcleo de la solución se basa en una arquitectura desacoplada y robusta. En el frontend contamos con una Single Page Application en React 19 y Vite con capacidades PWA y soporte offline. En la capa de datos, implementamos un modelo relacional normalizado en Tercera Forma Normal y BCNF con 8 tablas vinculadas por llaves foráneas estrictas, garantizando atomicidad transaccional al momento de descontar inventario y persistir el historial de cambios de estado."

---

### Escena 3: Demostración Interactiva en Vivo (Live Demo PWA)
* **Tiempo:** `01:15 - 02:25` (70 seg)
* **Visual / Captura (ScreenStudio / OBS):**
  1. *Dashboard Principal:* Carga instantánea, reloj en vivo, métricas financieras con modo de privacidad activable/desactivable y badges dinámicos.
  2. *Toma de Pedido Rápida:* Registro de cliente, selección de prendas por catálogo (talla/color), cálculo automático de flete distrital y validación de stock en vivo.
  3. *Trazabilidad de Estados:* Cambio reactivo de estado de orden (`Recibido` -> `En Preparación` -> `En Camino` -> `Entregado`) y botón directo de contacto por WhatsApp.
* **Voz en Off (Harley Roman):**
  > "Veamos la aplicación en funcionamiento real. Desde el Dashboard, el administrador visualiza los KPIs diarios y alertas de pedidos en riesgo que superan 24 horas sin despacho. Al registrar un nuevo pedido, la interfaz calcula automáticamente el subtotal, valida la disponibilidad de stock por SKU y computa el flete según el distrito. Toda la interfaz responde con animaciones de microinteracción a 60 cuadros por segundo y persiste el estado localmente incluso ante pérdidas de conexión."

---

### Escena 4: Rendimiento Web (WPO), Pruebas Unitarias y Calidad CI/CD
* **Tiempo:** `02:25 - 03:05` (40 seg)
* **Visual / Animación (Motion Canvas / Remotion):** Gráfico comparativo de métricas Lighthouse (68 -> 98/100), reducción del bundle size de 450 KB a 74.5 kB (83% de ahorro), y ejecución de pruebas unitarias Vitest en consola terminal (4/4 tests aprobados en 5ms).
* **Voz en Off (Jim Dávila):**
  > "El aseguramiento de la calidad y la optimización web (WPO) son pilares fundamentales de nuestro desarrollo. Mediante técnicas de tree-shaking, compresión Gzip y code-splitting, redujimos el bundle inicial a solo 74.5 kilobytes, alcanzando un puntaje de 98 sobre 100 en Google Lighthouse y un First Contentful Paint de solo 0.3 segundos. Asimismo, contamos con suites de pruebas unitarias automatizadas con Vitest integradas en nuestros pipelines de GitHub Actions."

---

### Escena 5: Conclusiones y Cierre Ejecutivo
* **Tiempo:** `03:05 - 03:30` (25 seg)
* **Visual / Animación:** Pantalla final con enlaces al repositorio GitHub, demo online desplegada en GitHub Pages y resumen de los 6 criterios cumplidos de la rúbrica APF1.
* **Voz en Off (Lady Loayza):**
  > "LeoFit Solutions cumple con la totalidad de los 17 artefactos de la rúbrica APF1, demostrando madurez arquitectónica, innovación en el frontend y un impacto directo en la productividad del negocio. Los invitamos a probar la demo interactiva en GitHub Pages. Muchas gracias."

---

## 3. Plantilla Programática Remotion (React + TypeScript)

Para compilar clips de video automatizados con datos en vivo del sistema, se dispone de la siguiente estructura programática en Remotion:

```tsx
import { Composition, Sequence } from 'remotion';
import { TitleCard } from './components/TitleCard';
import { MetricCounter } from './components/MetricCounter';
import { ArchitectureZoom } from './components/ArchitectureZoom';

export const LeoFitVideoComposition = () => {
  return (
    <>
      <Composition
        id="LeoFitAPF1Promo"
        component={MainVideo}
        durationInFrames={30 * 210} // 210 segundos a 30 FPS
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

const MainVideo = () => {
  return (
    <div style={{ flex: 1, backgroundColor: '#0F172A', color: 'white' }}>
      {/* Escena 1: Intro y Problema */}
      <Sequence from={0} durationInFrames={30 * 35}>
        <TitleCard
          title="LeoFit Solutions"
          subtitle="Sistema de Gestión de Pedidos & Control de Inventario PWA"
          team="UTP - Curso Integrador II (Grupo 01)"
        />
      </Sequence>

      {/* Escena 2: Arquitectura y C4 Model */}
      <Sequence from={30 * 35} durationInFrames={30 * 40}>
        <ArchitectureZoom
          imageSrc="diagrams/11_Arquitectura_C4_Model.png"
          title="Arquitectura C4 Nivel 2 y Persistencia Relacional"
        />
      </Sequence>

      {/* Escena 3: Métricas de Rendimiento WPO */}
      <Sequence from={30 * 145} durationInFrames={30 * 40}>
        <MetricCounter
          lighthouseScore={98}
          bundleSizeKB={74.5}
          fcpSeconds={0.3}
        />
      </Sequence>
    </div>
  );
};
```

---

## 4. Checklist de Grabación y Exportación Recomendado

1. **Configuración de OBS Studio:**
   - Canvas: 1920x1080 @ 60 FPS.
   - Bitrate de Video: 12,000 Kbps (CBR).
   - Audio: 48 kHz / 320 Kbps Stereo.
2. **Entorno de Demostración:**
   - Navegador Chrome en modo incógnito (sin extensiones que interfieran).
   - Servidor local en `http://localhost:5173/` o demo online en GitHub Pages.
   - PWA instalada en modo ventana independiente (`standalone`).
3. **Postproducción:**
   - Edición de cortes en CapCut / DaVinci Resolve.
   - Normalización de niveles de audio con compresor y limitador (-1.0 dB True Peak).
   - Exportación final en `.mp4` 1080p 16:9 con subtítulos pegados (Burn-in) o en archivo `.srt`.
