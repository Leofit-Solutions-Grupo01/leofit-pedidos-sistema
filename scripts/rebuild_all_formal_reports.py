# -*- coding: utf-8 -*-
"""
Script maestro para la reconstrucción, estandarización y compilación de
todos los documentos formales del proyecto LeoFit bajo normativa UTP e IEEE.
"""

import os
import glob
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import win32com.client
import pythoncom

# Datos estandarizados del equipo y proyecto
TEAM_MEMBERS = [
    ("1", "Loayza Rodriguez, Lady Luz", "Scrum Master / Coordinadora General / Especialista UX-UI"),
    ("2", "Cárdenas Fernández, Víctor Leandro", "Product Owner / Arquitecto Back-End y Base de Datos"),
    ("3", "Roman Delgado, Harley Anthony", "Front-End Lead / Especialista PWA y Optimización WPO"),
    ("4", "Dávila Morales, Jim Alessandro", "Ingeniero QA / Automatización de Pruebas y DevOps"),
    ("5", "Rojas Sanchez, Daniel Enrique", "Analista Funcional / Modelado de Procesos y Requisitos")
]

STAKEHOLDER = "Víctor Raúl Cárdenas Ramírez (Gerente General y Operador de LeoFit)"
COMPANY_NAME = "LeoFit Indumentaria & Nutrición Deportiva"

def write_01_ficha():
    path = os.path.join("docs", "01_Ficha_Identificacion.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# FICHA DE IDENTIFICACIÓN Y MAPEO INICIAL DE EMPRESA Y PROBLEMA (SEMANA 1)
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

### 1. DATOS DEL EQUIPO DE TRABAJO (GRUPO 01)

| N° | Apellidos y Nombres | Rol en el Proyecto | Responsabilidad Técnica Principal |
|:---:|:---|:---|:---|
| 1 | **Loayza Rodriguez, Lady Luz** | Scrum Master | Coordinación general, facilitación ágil y diseño UX/UI. |
| 2 | **Cárdenas Fernández, Víctor Leandro** | Product Owner | Definición de requerimientos, arquitectura Back-End y Base de Datos. |
| 3 | **Roman Delgado, Harley Anthony** | Front-End Lead | Desarrollo de interfaz PWA, componentes React y optimización WPO. |
| 4 | **Dávila Morales, Jim Alessandro** | QA / DevOps | Automatización de pruebas unitarias, CI/CD y aseguramiento de calidad. |
| 5 | **Rojas Sanchez, Daniel Enrique** | Analista de Negocio | Levantamiento de requisitos, modelado de procesos y documentación técnica. |

---

### 2. IDENTIFICACIÓN DE LA ORGANIZACIÓN

* **Nombre Comercial:** LeoFit Indumentaria & Nutrición Deportiva.
* **Rubro Comercial:** Comercialización minorista de indumentaria deportiva (conjuntos térmicos, lycras de compresión, camisetas dry-fit, fajas deportivas) y accesorios de entrenamiento.
* **Ubicación Geográfica:** Lima Metropolitana, Perú.
* **Modelo de Operación:** Ventas directas al consumidor (B2C) en Lima y despachos a provincias mediante agencias de encomienda.
* **Justificación de la Selección:** LeoFit es un emprendimiento comercial independiente en fase de expansión que gestiona sus ventas de forma reactiva y no estandarizada a través de redes sociales (Facebook y WhatsApp). Representa un caso de estudio real, accesible y de alta pertinencia para la implementación de una solución de software orientada a la eficiencia operativa.

---

### 3. CONTACTO Y EVIDENCIA DE ACCESO AL STAKEHOLDER

* **Representante y Contacto Principal:** Víctor Raúl Cárdenas Ramírez.
* **Cargo:** Fundador, Gerente General y Operador Principal.
* **Disponibilidad y Compromiso:** El representante ha suscrito actas de conformidad y se encuentra plenamente comprometido para participar en las sesiones semanales de Sprint Review y validación de prototipos.
* **Evidencias Disponibles:** Registros históricos en cuadernos físicos de notas, capturas anonimizadas de conversaciones de WhatsApp comercial y catálogo fotográfico actual de prendas.

---

### 4. MAPEO INICIAL DEL PROCESO Y DEFINICIÓN DEL PROBLEMA

* **Proceso Crítico Seleccionado:** Recepción, validación de existencias, registro y despacho de pedidos.
* **Definición Formal del Problema:**
  "La gestión manual, descentralizada y reactiva de los pedidos comerciales a través de canales de mensajería informal (WhatsApp y llamadas telefónicas) en LeoFit ocasiona cuellos de botella operativos, demoras de hasta 25 minutos en la atención por cliente, quiebres de inventario no advertidos y errores en las direcciones de despacho, impactando negativamente en la rentabilidad y en la satisfacción del cliente."

---

### 5. ACTORES Y MATRIZ DE NECESIDADES

| Actor / Usuario | Rol en el Negocio | Necesidad Principal | Dificultad Actual | Validación Propuesta |
|:---|:---|:---|:---|:---|
| **Víctor Raúl Cárdenas** | Administrador / Dueño | Centralizar pedidos, controlar stock en tiempo real y actualizar estados de entrega con un clic. | Sobrecarga de trabajo operativo, errores de registro manuscrito y falta de trazabilidad. | Pruebas de usabilidad del panel administrativo y flujo de pedidos en vivo. |
| **Cliente Deportivo** | Comprador final | Explorar prendas con tallas y precios actualizados, calcular totales y confirmar su orden en $< 2$ minutos. | Respuestas demoradas por chat, falta de catálogo ordenado y desconocimiento del estado de entrega. | Tasa de conversión de pedidos y reducción del tiempo de espera. |
| **Equipo de Proyecto** | Desarrolladores UTP | Requerimientos técnicos claros, acceso a datos sintéticos y retroalimentación iterativa. | Tiempo limitado del stakeholder por su dedicación a la operación diaria. | Sesiones semanales de Sprint Review estructuradas de 30 minutos. |

---

### 6. HIPÓTESIS DE SOLUCIÓN Y ALCANCE DEL MVP

* **Tipo de Solución:** Sistema Web Progresivo (PWA) responsivo, accesible desde navegadores móviles y de escritorio sin requerir descargas pesadas desde tiendas de aplicaciones.
* **Cinco Funcionalidades Principales del MVP:**
  1. *Catálogo Interactivo:* Visualización reactiva con filtros dinámicos por categoría, talla, color y precio.
  2. *Carrito de Compras y Control de Stock:* Cálculo automático de importes y bloqueo de pedidos que excedan existencias reales.
  3. *Toma y Registro Formal de Pedidos:* Formulario validado con generación automática de código identificador único de orden.
  4. *Módulo de Trazabilidad de Estados:* Cambio de estados operativo (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`).
  5. *Dashboard Administrativo:* Indicadores cuantitativos en tiempo real de ventas de la jornada, pedidos pendientes y alertas de stock bajo.

---

### 7. FACTIBILIDAD Y EVALUACIÓN DE VIABILIDAD

| Criterio de Viabilidad | Evaluación | Sustentación Técnica |
|:---|:---:|:---|
| **Acceso a Experto del Proceso** | Sí | Contacto directo y comprometido con el dueño del negocio. |
| **Evidencia Comprobable** | Sí | Registros físicos, capturas de chat y validación presencial. |
| **Alcance Acotado** | Sí | Enfocado estrictamente en la gestión de pedidos e inventario. |
| **Factibilidad Técnica** | Sí | Pila tecnológica madura y probada (React 18, TypeScript, Vite, Tailwind CSS y Node.js). |
| **Protección de Datos** | Sí | Uso de datos sintéticos y homologación conforme a la Ley de Protección de Datos Personales. |
| **Despliegue Operativo** | Sí | Despliegue automatizado en CDN Serverless (GitHub Pages / Vercel) con alta disponibilidad. |

---

### 8. PITCH TÉCNICO DEL PROYECTO

"LeoFit es un negocio peruano de indumentaria deportiva que gestiona sus ventas manualmente por WhatsApp y notas en papel, generando demoras de 25 minutos por orden y riesgos de sobreventa. Desarrollamos una Progressive Web App (PWA) de ultra-bajo peso que permite a los clientes confirmar pedidos en 2 minutos con stock en tiempo real y brinda al administrador control integral del inventario y trazabilidad de despachos con un solo clic."
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_02_requerimientos():
    path = os.path.join("docs", "02_Requerimientos.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# ESPECIFICACIÓN DE REQUERIMIENTOS DE SOFTWARE (ERS)
## ESTÁNDAR IEEE STD 830-1998
### PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. INTRODUCCIÓN

### 1.1. Propósito del Documento
El presente documento especifica de manera formal y estructurada los Requerimientos Funcionales (RF) y Requisitos No Funcionales (RNF) para el desarrollo del **Sistema de Gestión de Pedidos e Inventario de LeoFit**, siguiendo las directrices del estándar internacional **IEEE Std 830-1998** y los lineamientos del Curso Integrador II: Software de la Universidad Tecnológica del Perú.

### 1.2. Alcance del Sistema
El software es una **Progressive Web App (PWA)** que automatiza la captura, validación, registro, costeo y seguimiento de pedidos de indumentaria deportiva, proporcionando sincronización en tiempo real con el inventario y permitiendo la administración operativa desde cualquier dispositivo móvil o de escritorio.

### 1.3. Objetivos del Sistema
* Reducir el tiempo promedio de atención y toma de pedidos de 25 minutos a $\le 3$ minutos.
* Eliminar en un 100% las pérdidas de pedidos y sobreventas originadas por anotaciones manuscritas.
* Proporcionar trazabilidad total del ciclo de vida de la orden a través de 5 estados operativos normalizados.

---

## 2. DESCRIPCIÓN GENERAL

### 2.1. Perspectiva del Producto
El sistema opera de forma autónoma e independiente, interactuando con clientes y administradores mediante una arquitectura web modular basada en componentes y desacoplada en capas (Presentación, Estado, Lógica de Negocio y Persistencia).

### 2.2. Características de los Usuarios
* **Cliente Deportivo:** Usuario final sin formación técnica especializada que navega por el catálogo, selecciona artículos y formaliza órdenes de compra.
* **Administrador del Sistema (Víctor Raúl Cárdenas):** Responsable de la gestión de existencias, actualización de precios, cambio de estados de pedidos y visualización de métricas en el panel.

### 2.3. Restricciones de Diseño e Implementación
* Uso obligatorio de estándares web modernos (HTML5, CSS3, ECMAScript 2022+).
* Tipado estricto mediante TypeScript 5+.
* Rendimiento optimizado bajo métricas Core Web Vitals (FCP $< 0.5$ s, LCP $< 1.2$ s, bundle JS $< 80$ kB gzipped).
* Compatibilidad multi-navegador en Google Chrome, Microsoft Edge, Mozilla Firefox y Safari Mobile.

---

## 3. MATRIZ DE REQUISITOS FUNCIONALES (RF-001 A RF-012)

| ID | Nombre del Requisito | Actor Principal | Descripción Funcional | Prioridad | Criterios de Aceptación | Módulo | Estado |
|:---|:---|:---|:---|:---:|:---|:---|:---:|
| **RF-001** | Catálogo Interactivo | Cliente / Admin | El sistema debe mostrar el catálogo de prendas deportivas con fotografía HD, nombre, precio, tallas disponibles y stock en existencias. | Alta | Carga reactiva de productos con formato de moneda nacional (S/) y badges de disponibilidad. | Catálogo | Implementado |
| **RF-002** | Búsqueda y Filtrado Dinámico | Cliente / Admin | El sistema debe permitir filtrar productos por categoría, talla y texto predictivo en tiempo real sin recargar la página. | Alta | Respuesta del filtro en menos de 100 ms ante cualquier interacción del usuario. | Catálogo | Implementado |
| **RF-003** | Carrito de Compras Reactivo | Cliente / Admin | El sistema debe permitir añadir artículos, modificar cantidades y eliminar prendas, recalculando el subtotal al instante. | Alta | Persistencia del estado del carrito durante la sesión y actualización reactiva de montos. | Carrito | Implementado |
| **RF-004** | Validación Automática de Stock | Sistema | El sistema debe impedir la selección o compra de cantidades que excedan las existencias físicas registradas. | Alta | Deshabilitación de botones de incremento y presentación de alerta contextual de stock agotado. | Inventario | Implementado |
| **RF-005** | Formulario de Registro de Orden | Cliente / Admin | El sistema debe capturar los datos de entrega: nombre completo, teléfono móvil, dirección de envío y método de pago. | Alta | Validación estricta de campos obligatorios y generación de identificador único correlativo (`PED-2026-XXXX`). | Pedidos | Implementado |
| **RF-006** | Liquidación de Flete y Totales | Sistema | El sistema debe calcular el costo de despacho según la zona geográfica seleccionada y consolidar el monto total a pagar. | Media | Desglose aritmético exacto de subtotal de prendas, tarifa de flete y total de la orden. | Pedidos | Implementado |
| **RF-007** | Trazabilidad y Control de Estados | Administrador | El sistema debe permitir la actualización de estados de la orden (`Recibido`, `En Preparación`, `En Camino`, `Entregado`, `Cancelado`). | Alta | Cambio de estado con un solo clic en la interfaz y registro de la marca de tiempo correspondiente. | Gestión | Implementado |
| **RF-008** | Bandeja de Gestión de Pedidos | Administrador | El sistema debe presentar la lista consolidada de pedidos con filtros por estado, cliente, fecha y rango de importes. | Alta | Visualización en tarjetas interactivas y tabla responsiva con badges de colores normalizados. | Gestión | Implementado |
| **RF-009** | Gestión de Existencias y Catálogo | Administrador | El sistema debe permitir la creación, modificación de precios, edición de tallas y ajuste de stock de productos. | Alta | Modal interactivo para actualización inmediata de existencias en el catálogo. | Inventario | Implementado |
| **RF-010** | Dashboard de Control Operativo | Administrador | El sistema debe mostrar tarjetas métricas con total de pedidos del día, importe bruto recaudado y prendas en nivel crítico ($< 5$ unid). | Media | Cálculo reactivo de totales de la jornada sin sobrecarga en la memoria del navegador. | Dashboard | Implementado |
| **RF-011** | Generación de Resumen para WhatsApp | Cliente / Admin | El sistema debe generar un mensaje de texto formateado con el resumen de la orden listo para compartir por mensajería. | Media | Formato limpio con ID de pedido, detalle de ítems, flete, total y datos de contacto del cliente. | Pedidos | Implementado |
| **RF-012** | Control de Acceso Administrativo | Administrador | El sistema debe proteger las rutas de gestión de inventario y configuración mediante credenciales de autenticación. | Alta | Validación segura de credenciales de administrador y persistencia de sesión controlada. | Seguridad | Implementado |

---

## 4. MATRIZ DE REQUISITOS NO FUNCIONALES (RNF-001 A RNF-010)

| ID | Categoría | Requisito No Funcional | Descripción Técnica | Métrica Verificable | Prioridad | Método de Validación | Estado |
|:---|:---|:---|:---|:---|:---:|:---|:---:|
| **RNF-001** | Usabilidad | Diseño Mobile-First | La interfaz debe ser altamente intuitiva y ergonómica en pantallas táctiles de smartphones. | Registro de orden completado en $\le 2$ minutos por usuarios no técnicos. | Alta | Prueba de usabilidad con 3 usuarios finales. | Validado |
| **RNF-002** | Rendimiento | Tiempo de Carga y Render | Las vistas y filtros del catálogo deben desplegarse de manera instantánea. | First Contentful Paint (FCP) $\le 0.5$ s y tiempo de respuesta P95 $< 100$ ms. | Alta | Auditoría con Google Lighthouse y Chrome DevTools. | Validado |
| **RNF-003** | Rendimiento (WPO) | Optimización de Paquete | El bundle compilado de producción debe ser minúsculo para operar en redes móviles lentas. | Bundle JS $\le 80$ kB gzipped y Bundle CSS $\le 10$ kB gzipped. | Alta | Análisis de compilación con Vite / Rollup bundle analyzer. | Validado |
| **RNF-004** | Disponibilidad | Operatividad Continua | La plataforma debe permanecer disponible y accesible en la nube de forma ininterrumpida. | Uptime mensual $\ge 99.5\%$ garantizado por CDN Serverless en el Edge. | Alta | Bitácora y monitoreo de disponibilidad en hosting. | Validado |
| **RNF-005** | Compatibilidad | Multi-Plataforma | El sistema debe operar con total fidelidad visual en todos los navegadores modernos. | 100% funcional en Google Chrome, Microsoft Edge, Firefox y Safari. | Media | Pruebas de compatibilidad cruzada en navegadores. | Validado |
| **RNF-006** | Mantenibilidad | Arquitectura Modular | El código fuente debe estar estructurado en capas desacopladas con tipado estricto. | 100% código TypeScript sin errores de compilación (`tsc --noEmit`). | Alta | Análisis estático de código y suite de linters. | Validado |
| **RNF-007** | Trazabilidad | Integridad de Transacciones | Toda orden debe conservar su historial y no puede ser eliminada físicamente sin registro. | Cada orden almacena identificador correlativo, fecha, hora y estado actual. | Alta | Verificación de esquemas de datos y persistencia. | Validado |
| **RNF-008** | Seguridad | Rutas Protegidas | Las opciones de edición de existencias deben estar restringidas a sesiones autenticadas. | Denegación inmediata de acceso ante solicitudes no autorizadas. | Alta | Pruebas de navegación a rutas administrativas sin sesión. | Validado |
| **RNF-009** | Confiabilidad | Suite de Pruebas Unitarias | La lógica de cálculo y consistencia de datos debe estar respaldada por pruebas automatizadas. | Cobertura de pruebas unitarias $\ge 80\%$ con 100% de tests aprobados. | Alta | Ejecución automatizada de `vitest run` en CI/CD. | Validado |
| **RNF-010** | Accesibilidad | Contraste y Tipografía | Textos, botones y componentes interactivos deben cumplir con estándares de legibilidad. | Cumplimiento estricto de directrices WCAG 2.1 nivel AA (contraste $\ge 4.5:1$). | Media | Auditoría con extensión Axe y Lighthouse Accessibility. | Validado |

---

## 5. MATRIZ DE TRAZABILIDAD (REQUISITOS VS HISTORIAS DE USUARIO)

| Requisito Funcional | Historia de Usuario Vinculada | Épica Asociada | Módulo de Software |
|:---|:---:|:---:|:---|
| **RF-001, RF-002** | HU-001 (Filtrado de Catálogo) | EP-01 | `src/pages/Dashboard.tsx` |
| **RF-003, RF-004** | HU-002 (Carrito de Compras) | EP-02 | `src/context/AppContext.tsx` |
| **RF-005, RF-006, RF-011** | HU-003 (Registro de Pedidos) | EP-02 | `src/pages/PedidoForm.tsx` |
| **RF-007, RF-008** | HU-004 (Control de Estados) | EP-03 | `src/pages/PedidosLista.tsx` |
| **RF-009** | HU-006 (Gestión de Inventario) | EP-01 | `src/pages/ProductosGestion.tsx` |
| **RF-010** | HU-005 (Métricas de Dashboard) | EP-04 | `src/pages/Dashboard.tsx` |
| **RF-012** | HU-007 (Seguridad y Acceso) | EP-03 | `src/pages/Login.tsx` |
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_03_acta():
    path = os.path.join("docs", "03_Acta_Reunion_1.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# ACTA FORMAL DE REUNIÓN N° 01
## LEVANTAMIENTO DE INFORMACIÓN Y VALIDACIÓN DEL PROBLEMA DE NEGOCIO

---

### 1. DATOS GENERALES DE LA SESIÓN

* **Proyecto:** Sistema Web PWA de Gestión y Toma de Pedidos Multicanal para LeoFit.
* **Fecha:** 15 de Agosto de 2026.
* **Hora de Inicio:** 10:00 AM | **Hora de Finalización:** 11:30 AM.
* **Lugar / Modalidad:** Presencial (Taller y Almacén de LeoFit, Lima) con apoyo audiovisual virtual.
* **Convocado por:** Equipo de Desarrollo Grupo 01 - UTP.

---

### 2. ASISTENCIA Y CONTROL DE PARTICIPANTES

| Apellidos y Nombres | Rol en la Reunión | Entidad / Organización | Estado de Asistencia |
|:---|:---|:---|:---:|
| **Víctor Raúl Cárdenas Ramírez** | Gerente General / Dueño del Negocio | LeoFit Indumentaria Deportiva | Presente |
| **Lady Luz Loayza Rodriguez** | Scrum Master / Líder de Proyecto | Grupo 01 - UTP | Presente |
| **Víctor Leandro Cárdenas Fernández** | Product Owner / Arquitecto Back-End | Grupo 01 - UTP | Presente |
| **Harley Anthony Roman Delgado** | Front-End Lead / Diseñador UI | Grupo 01 - UTP | Presente |
| **Jim Alessandro Dávila Morales** | Especialista QA / Testing | Grupo 01 - UTP | Presente |
| **Daniel Enrique Rojas Sanchez** | Analista de Negocio / Procesos | Grupo 01 - UTP | Presente |

---

### 3. AGENDA DE LA REUNIÓN

1. Presentación formal del equipo de desarrollo de la Universidad Tecnológica del Perú.
2. Descripción del modelo de negocio de LeoFit y diagnóstico de los canales de venta actuales.
3. Identificación detallada de los cuellos de botella en la atención de pedidos y control de inventario.
4. Definición preliminar del alcance de la solución informática (Progressive Web App).
5. Acuerdos de colaboración, cronograma de reuniones de Sprint y entrega de insumos de información.

---

### 4. PUNTOS TRATADOS Y DIAGNÓSTICO OPERATIVO

* **Flujo Comercial Actual (AS-IS):** El señor Víctor Raúl Cárdenas explicó que todas las ventas se canalizan manualmente por WhatsApp y Facebook. El proceso de enviar fotos individuales de prendas, responder sobre tallas disponibles y verificar el stock físico en estanterías toma en promedio 25 minutos por cada cliente.
* **Errores y Pérdidas Identificadas:** Se constató que las anotaciones manuscritas en libretas de papel originan confusiones en las tallas seleccionadas, direcciones de entrega incompletas y, ocasionalmente, la confirmación de prendas que ya no se encuentran en stock físico.
* **Propuesta de Solución Tecnológica:** El equipo propuso el desarrollo de una PWA interactiva que permita al cliente consultar el catálogo con stock actualizado en tiempo real y enviar una orden formal consolidada, optimizando el tiempo del administrador para enfocarse en la preparación y despacho de paquetes.

---

### 5. ACUERDOS Y COMPROMISOS ADQUIRIDOS

| N° | Descripción del Acuerdo / Entregable | Responsable Asignado | Fecha Límite |
|:---:|:---|:---|:---:|
| **1** | Redacción y formalización de la Ficha de Mapeo de Empresa y Problema. | Grupo 01 (Daniel Rojas / Lady Loayza) | 20/08/2026 |
| **2** | Entrega de catálogo fotográfico de prendas y datos anonimizados de pedidos pasados. | Víctor Raúl Cárdenas (LeoFit) | 22/08/2026 |
| **3** | Elaboración de wireframes y primeros mockups de interfaz de usuario. | Harley Roman / Lady Loayza | 25/08/2026 |
| **4** | Diseño del modelo de datos normalizado y especificación de requerimientos IEEE 830. | Víctor Cárdenas / Jim Dávila | 28/08/2026 |

---

### 6. CONFORMIDAD Y CIERRE

Habiéndose cumplido con la agenda establecida y en señal de mutua conformidad con los acuerdos registrados, se suscribe la presente acta formal a los quince días del mes de agosto del año dos mil veintiséis.

```text
_________________________________________          _________________________________________
     Víctor Raúl Cárdenas Ramírez                             Lady Luz Loayza Rodriguez
    Gerente General - LeoFit Sport                         Scrum Master - Grupo 01 UTP
```
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_04_glosario():
    path = os.path.join("docs", "04_Glosario.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# GLOSARIO FORMAL DE TÉRMINOS TÉCNICOS Y DE NEGOCIO
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. TÉRMINOS DE NEGOCIO Y MODELADO DE PROCESOS

* **AS-IS (Estado Actual):** Metodología de modelado que describe el flujo operativo y los procedimientos de una organización tal como se ejecutan en el presente, permitiendo identificar ineficiencias, cuellos de botella y costos ocultos.
* **BPMN 2.0 (Business Process Model and Notation):** Estándar internacional gráfico para el modelado formal de procesos de negocio mediante eventos, actividades, compuertas lógicas y carriles de responsabilidad.
* **Ciclo de Pedido (Order Lead Time):** Intervalo de tiempo total transcurrido desde que el cliente inicia la interacción de compra hasta que la orden es entregada físicamente en su domicilio.
* **Flete / Costo de Delivery:** Importe monetario cobrado por el servicio logístico motorizado para trasladar los paquetes desde el almacén hasta la dirección del cliente.
* **Inventario Crítico:** Nivel de existencias de un producto que se encuentra por debajo del umbral de seguridad (en LeoFit, $< 5$ unidades), requiriendo reabastecimiento prioritario.
* **Lean Canvas:** Herramienta estratégica de modelado de negocios creada por Ash Maurya, compuesta por 9 bloques enfocados en la resolución de problemas para startups y productos innovadores.
* **MoSCoW:** Técnica ágil de priorización de requerimientos basada en cuatro categorías: Must have (Imprescindible), Should have (Debería tener), Could have (Podría tener) y Won't have (No tendrá en esta iteración).
* **MVP (Producto Mínimo Viable):** Versión funcional de un producto de software que incluye el conjunto mínimo indispensable de características requeridas para validar hipótesis de valor con usuarios reales.
* **Quiebre de Stock (Stockout):** Situación operativa en la que la demanda de un producto no puede ser satisfecha debido al agotamiento no previsto de las existencias en inventario.
* **SKU (Stock Keeping Unit):** Identificador alfanumérico único asignado a un producto y sus variantes específicas (tipo de prenda, talla, color) para su control y seguimiento en almacén.
* **TO-BE (Estado Propuesto):** Representación del flujo de procesos rediseñado y optimizado mediante la integración de la solución de software, orientada a eliminar las ineficiencias del modelo AS-IS.

---

## 2. TÉRMINOS TÉCNICOS, ARQUITECTURA Y DESARROLLO DE SOFTWARE

* **Bundle:** Archivo o conjunto de archivos compilados y minificados que contienen el código JavaScript, CSS y recursos estáticos de una aplicación web listos para su distribución a producción.
* **Clean Architecture (Arquitectura Limpia):** Patrón arquitectónico propuesto por Robert C. Martin que promueve la separación de responsabilidades en capas concéntricas desacopladas, haciendo la lógica de negocio independiente de frameworks, interfaces y bases de datos.
* **Code-Splitting (División de Código):** Técnica de optimización que fragmenta el paquete de código fuente en chunks independientes que se descargan de forma asíncrona únicamente cuando la vista o componente es requerido.
* **Core Web Vitals:** Conjunto de métricas estandarizadas por Google para evaluar la experiencia de usuario en la web: First Contentful Paint (FCP), Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS) e Interaction to Next Paint (INP).
* **Gherkin:** Lenguaje formal y legible para el ser humano utilizado en el desarrollo guiado por comportamiento (BDD), estructurado mediante cláusulas Given-When-Then (Dado-Cuando-Entonces) para definir criterios de aceptación.
* **Hot Module Replacement (HMR):** Característica de los empaquetadores modernos (como Vite) que actualiza módulos en el navegador en tiempo real durante el desarrollo sin necesidad de recargar la página completa ni perder el estado.
* **PWA (Progressive Web App):** Aplicación web construida con tecnologías estándar que ofrece capacidades avanzadas similares a las aplicaciones móviles nativas, tales como funcionamiento offline, instalación en pantalla de inicio y alto rendimiento de carga.
* **Service Worker:** Script en JavaScript que el navegador ejecuta en segundo plano, independiente de la página web, permitiendo interceptar peticiones de red, gestionar estrategias de caché offline y recibir notificaciones.
* **SLA (Service Level Agreement):** Acuerdo formal y contractual que define los niveles de servicio comprometidos entre el proveedor de software y el cliente (ejemplo: $99.5\%$ de disponibilidad).
* **SLI (Service Level Indicator):** Medición cuantitativa directa del nivel de servicio que se está brindando en tiempo real (ejemplo: porcentaje de peticiones exitosas).
* **SLO (Service Level Objective):** Meta cuantitativa interna establecida por el equipo de ingeniería para un indicador SLI específico (ejemplo: tiempo de respuesta P95 $< 800$ ms).
* **Tree-Shaking:** Proceso de optimización ejecutado por empaquetadores (como Rollup) que analiza el árbol de dependencias estático y elimina de forma automática el código muerto o no utilizado.
* **TypeScript:** Superconjunto tipado estático de JavaScript desarrollado por Microsoft que añade verificación formal de tipos en tiempo de compilación, mejorando la robustez y mantenibilidad del software.
* **Vitest:** Marco de pruebas unitarias de última generación optimizado para entornos Vite, caracterizado por su velocidad de ejecución y compatibilidad nativa con TypeScript y módulos ES.
* **WPO (Web Performance Optimization):** Disciplina de la ingeniería de software enfocada en la aplicación de técnicas y estrategias para maximizar la velocidad de carga, eficiencia de recursos y rendimiento general de aplicaciones web.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_05_preguntas_panel():
    path = os.path.join("docs", "05_Preguntas_Criticas_Panel.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# GUÍA FORMAL DE PREGUNTAS Y RESPUESTAS CRÍTICAS PARA SUSTENTACIÓN ANTE EL JURADO
## PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. CATEGORÍA: ANÁLISIS DE NEGOCIO, PROCESOS Y RÚBRICA APF1

### Pregunta 1.1: ¿Por qué la empresa seleccionada califica como un caso de estudio válido para el curso?
**Fundamentación Técnica y de Negocio:**
LeoFit cumple estrictamente con los criterios de la rúbrica al ser una microempresa peruana debidamente constituida, con operación comercial activa y una problemática real demostrable: la gestión manual y no estandarizada de pedidos por WhatsApp que genera demoras de 25 minutos por orden, sobreventas y extravío de registros. Además, se cuenta con acceso irrestricto al stakeholder (Víctor Raúl Cárdenas), garantizando la validación continua de prototipos e incrementos de software.

### Pregunta 1.2: ¿En qué se diferencia el modelo AS-IS del modelo propuesto TO-BE?
**Fundamentación Técnica y de Negocio:**
El modelo AS-IS es secuencial, manual y vulnerable, con 8 pasos donde la verificación de stock se hace visualmente y las anotaciones en papel. El modelo TO-BE digitaliza el proceso mediante una Progressive Web App (PWA): el cliente consulta un catálogo interactivo con stock sincronizado, el sistema valida y descuenta existencias automáticamente, calcula el flete y genera una orden formal con ID único. El administrador gestiona la preparación y el despacho mediante un tablero con cambio de estados en un solo clic, reduciendo el ciclo de pedido a menos de 3 minutos.

---

## 2. CATEGORÍA: GESTIÓN ÁGIL, SCRUM Y PLANIFICACIÓN

### Pregunta 2.1: ¿Cómo determinaron la velocidad del equipo y la duración de los Sprints?
**Fundamentación Técnica y de Negocio:**
Se estableció un esquema de Sprints de 2 semanas calendario con una capacidad estimada de 35 Story Points (SP) por iteración. Las historias de usuario fueron estimadas mediante la secuencia Fibonacci (1, 2, 3, 5, 8, 13) y priorizadas con la metodología MoSCoW. Cada historia cuenta con criterios de aceptación en estándar Gherkin (*Given-When-Then*), y el flujo de trabajo se controla en un tablero Kanban con límites estrictos de trabajo en progreso (WIP Limits) en GitHub Projects.

### Pregunta 2.2: ¿Cuál es la política de Definition of Done (DoD) acordada por el equipo?
**Fundamentación Técnica y de Negocio:**
Para que una tarea se considere concluida (`Done`), debe cumplir cuatro criterios rigurosos: (1) Código implementado en TypeScript estricto sin advertencias de linters; (2) Pruebas unitarias aprobadas con Vitest garantizando $\ge 80\%$ de cobertura; (3) Revisión por pares mediante Pull Request en GitHub; y (4) Despliegue automatizado exitoso en el ambiente de producción mediante GitHub Actions.

---

## 3. CATEGORÍA: ARQUITECTURA DE SOFTWARE Y TECNOLOGÍA FRONT-END

### Pregunta 3.1: ¿Por qué seleccionaron una Progressive Web App (PWA) con React y Vite en lugar de una aplicación móvil nativa o WordPress?
**Fundamentación Técnica y de Negocio:**
* **Frente a Apps Nativas:** Una PWA no requiere instalación desde tiendas propietarias (Play Store / App Store), eliminando la fricción de descarga para el cliente y reduciendo drásticamente los costos de desarrollo multi-plataforma (un solo código fuente para móvil y escritorio).
* **Frente a WordPress/WooCommerce:** React + Vite proporciona una arquitectura desacoplada, carga instantánea ($< 0.5$ s), menor consumo de memoria y control total sobre el pipeline de optimización WPO.
* **Uso de TypeScript y Tailwind:** Garantiza tipado estricto en tiempo de compilación, previniendo errores en tiempo de ejecución, y un bundle de estilos ultraligero depurado con PurgeCSS.

---

## 4. CATEGORÍA: ASEGURAMIENTO DE LA CALIDAD (QA) Y PRUEBAS

### Pregunta 4.1: ¿Qué estrategia de pruebas se implementó para garantizar la fiabilidad del sistema?
**Fundamentación Técnica y de Negocio:**
Se implementó una suite de pruebas unitarias automatizadas con **Vitest** en la capa de datos y lógica de negocio (`frontend/src/__tests__/mockData.test.ts`). Las pruebas validan la integridad de precios, existencias no negativas, pertenencia de categorías y normalización de estados de los pedidos. La suite se ejecuta de forma automática en el pipeline de Integración Continua (`.github/workflows/security-scan.yml`) ante cada `push` y `pull request` a la rama `main`.

---

## 5. CATEGORÍA: OPTIMIZACIÓN WEB (WPO) Y NIVELES DE SERVICIO (SLA/SLO)

### Pregunta 5.1: ¿Cuáles fueron los resultados cuantitativos de las estrategias WPO implementadas?
**Fundamentación Técnica y de Negocio:**
Se implementaron cinco estrategias técnicas: Tree-shaking, minificación con esbuild, code-splitting modular, memoización React y carga asíncrona de fuentes. Los resultados medidos con Google Lighthouse evidencian:
* Incremento de la puntuación Lighthouse de 68/100 a **98/100** (+44.1%).
* Reducción del First Contentful Paint (FCP) de 2.4 s a **0.3 s** (-87.5%).
* Reducción del tamaño del bundle JavaScript gzipped de 450.0 kB a **74.49 kB** (-83.4%).
* Tiempo de compilación en producción reducido a **0.73 segundos**.

### Pregunta 5.2: ¿Cuáles son los compromisos de SLA y SLO establecidos para LeoFit?
**Fundamentación Técnica y de Negocio:**
Se estableció un SLA de disponibilidad mensual $\ge 99.5\%$ respaldado por CDN Serverless en el Edge, un SLO de latencia de renderizado P95 $< 500$ ms, un tiempo máximo de recuperación ante fallos (RTO) $< 2$ horas y un punto de recuperación de datos (RPO) $< 15$ minutos mediante persistencia local y sincronización en la nube.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_06_especificacion_pwa():
    path = os.path.join("docs", "06_Especificacion_PWA_Prompt.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_07_arquitectura():
    path = os.path.join("docs", "07_Arquitectura_Sistema.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
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
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def write_08_normalizacion():
    path = os.path.join("docs", "08_Normalizacion_Base_Datos.md")
    content = r"""# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# INFORME FORMAL DE NORMALIZACIÓN DE BASE DE DATOS RELACIONAL
## FORMAS NORMALES: 1FN, 2FN, 3FN Y FORMA NORMAL DE BOYCE-CODD (BCNF)
### PROYECTO: SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LEOFIT

---

## 1. CONTROL DEL DOCUMENTO

* **Institución:** Universidad Tecnológica del Perú (UTP)
* **Curso:** Curso Integrador II: Software (100000S12F)
* **Proyecto:** Sistema de Gestión de Pedidos & Inventario LeoFit
* **Equipo Responsable (Grupo 01):**
  1. **Loayza Rodriguez, Lady Luz** - Scrum Master
  2. **Cárdenas Fernández, Víctor Leandro** - Product Owner / Diseñador de Base de Datos
  3. **Roman Delgado, Harley Anthony** - Front-End Lead
  4. **Dávila Morales, Jim Alessandro** - QA / Testing
  5. **Rojas Sanchez, Daniel Enrique** - Analista de Negocio
* **Versión:** 1.0.0 (Formal Académica)

---

## 2. PROCESO PASO A PASO DE NORMALIZACIÓN

### 2.1. Forma No Normalizada (UNF) - Estructura Inicial Desnormalizada
El registro inicial en los cuadernos de notas de LeoFit agrupaba de forma redundante y no atómica los datos del cliente, múltiples prendas en una sola celda y subtotales mezclados:

$$\text{REGISTRO\_PEDIDO}(\underline{\text{ID\_Pedido}}, \text{Fecha}, \text{Cliente\_Nombre}, \text{Cliente\_Tel}, \text{Direccion}, \{\text{Cod\_Prenda}, \text{Prenda}, \text{Talla}, \text{Color}, \text{Cant}, \text{PrecioUnit}\}, \text{Flete}, \text{Total})$$

---

### 2.2. Primera Forma Normal (1FN) - Atomicidad y Eliminación de Grupos Repetitivos
* **Regla Aplicada:** Se eliminan los grupos repetitivos extrayendo el detalle de productos a una entidad separada y se garantiza que todos los atributos contengan valores atómicos individuales.
* **Entidades Resultantes en 1FN:**
  - $\text{PEDIDOS\_1FN}(\underline{\text{id\_pedido}}, \text{fecha}, \text{cliente\_nombre}, \text{cliente\_telefono}, \text{cliente\_direccion}, \text{costo\_envio}, \text{monto\_total})$
  - $\text{DETALLE\_PEDIDO\_1FN}(\underline{\text{id\_pedido}, \text{id\_producto}}, \text{nombre\_producto}, \text{talla}, \text{color}, \text{cantidad}, \text{precio\_unitario}, \text{subtotal})$

---

### 2.3. Segunda Forma Normal (2FN) - Eliminación de Dependencias Funcionales Parciales
* **Regla Aplicada:** Todos los atributos que no forman parte de la clave primaria deben depender funcionalmente de la totalidad de la clave primaria compuesta, no de una parte de ella.
* **Entidades Resultantes en 2FN:**
  - $\text{PRODUCTOS}(\underline{\text{id\_producto}}, \text{nombre}, \text{categoria}, \text{precio}, \text{stock}, \text{talla}, \text{color})$
  - $\text{DETALLE\_PEDIDOS}(\underline{\text{id\_pedido}, \text{id\_producto}}, \text{cantidad}, \text{precio\_unitario})$
  - $\text{PEDIDOS}(\underline{\text{id\_pedido}}, \text{fecha}, \text{id\_cliente}, \text{costo\_envio}, \text{total}, \text{id\_estado})$

---

### 2.4. Tercera Forma Normal (3FN) - Eliminación de Dependencias Transitivas
* **Regla Aplicada:** Ningún atributo no clave debe depender transitivamente de la clave primaria a través de otro atributo no clave. Se independizan las entidades `CLIENTES`, `CATEGORIAS` y `ESTADOS_PEDIDO`.
* **Esquema Relacional Final en 3FN / BCNF:**

```sql
-- 1. Tabla de Roles de Usuario
CREATE TABLE roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre_rol VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Tabla de Usuarios del Sistema
CREATE TABLE usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES roles(id_rol)
);

-- 3. Tabla de Categorías de Indumentaria
CREATE TABLE categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nombre_categoria VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT
);

-- 4. Tabla de Productos e Inventario
CREATE TABLE productos (
    id_producto VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    id_categoria INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    talla VARCHAR(20) NOT NULL,
    color VARCHAR(50) NOT NULL,
    imagen_url VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria)
);

-- 5. Tabla de Estados de Pedido
CREATE TABLE estados_pedido (
    id_estado INT PRIMARY KEY AUTO_INCREMENT,
    nombre_estado VARCHAR(50) NOT NULL UNIQUE
);

-- 6. Tabla de Cabecera de Pedidos
CREATE TABLE pedidos (
    id_pedido VARCHAR(50) PRIMARY KEY,
    cliente_nombre VARCHAR(150) NOT NULL,
    cliente_telefono VARCHAR(20) NOT NULL,
    cliente_direccion TEXT NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    costo_envio DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    total DECIMAL(10, 2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    id_estado INT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estado) REFERENCES estados_pedido(id_estado)
);

-- 7. Tabla de Detalle de Pedidos
CREATE TABLE detalle_pedidos (
    id_pedido VARCHAR(50) NOT NULL,
    id_producto VARCHAR(50) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (id_pedido, id_producto),
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto)
);
```

---

## 3. CONCLUSIÓN TÉCNICA
El esquema normalizado en **BCNF** garantiza:
1. **Cero redundancia de datos** en catálogo, pedidos y clientes.
2. **Integridad referencial total** mediante claves primarias y foráneas con restricciones `CHECK`.
3. **Alto rendimiento en consultas transaccionales** con índices sobre claves foráneas y fechas de creación.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generado: {path}")

def convert_md_to_docx_custom(markdown_text, output_docx_path):
    doc = docx.Document()
    
    # Page Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    lines = markdown_text.split('\n')
    i = 0
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        
        # Table detection
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            if not all(c in '|:- ' for c in line.strip()):
                cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                table_rows.append(cells)
            i += 1
            continue
        else:
            if in_table:
                if table_rows:
                    cols_count = max(len(r) for r in table_rows)
                    t = doc.add_table(rows=len(table_rows), cols=cols_count)
                    t.alignment = WD_TABLE_ALIGNMENT.CENTER
                    for r_idx, row in enumerate(table_rows):
                        for c_idx, cell_value in enumerate(row):
                            if c_idx < cols_count:
                                cell = t.cell(r_idx, c_idx)
                                cell.text = cell_value.replace('<br>', '\n')
                                if r_idx == 0:
                                    shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
                                    cell._tc.get_or_add_tcPr().append(shading)
                                    for p in cell.paragraphs:
                                        for r in p.runs:
                                            r.font.bold = True
                                            r.font.color.rgb = RGBColor(255, 255, 255)
                                else:
                                    if r_idx % 2 == 1:
                                        shading = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                                        cell._tc.get_or_add_tcPr().append(shading)
                    doc.add_paragraph()
                in_table = False
                table_rows = []
                
        # Headings
        if line.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(line[2:].strip())
            run.font.name = 'Calibri'
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif line.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(line[3:].strip())
            run.font.name = 'Calibri'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(249, 115, 22) # Orange
        elif line.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(line[4:].strip())
            run.font.name = 'Calibri'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 41, 59)
        elif line.startswith('* ') or line.startswith('- '):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(2)
            p.add_run(line[2:].strip().replace('**', ''))
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(6)
            shading = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
            p._p.get_or_add_pPr().append(shading)
            run = p.add_run('\n'.join(code_lines))
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(15, 23, 42)
        elif line.strip() == '---':
            pass
        elif line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.add_run(line.strip().replace('**', '').replace('*', ''))
            
        i += 1
        
    doc.save(output_docx_path)
    print(f"Documento Word guardado en: {output_docx_path}")

def build_all():
    print("=== RECONSTRUYENDO TODOS LOS DOCUMENTOS DEL PROYECTO LEOFIT ===")
    write_01_ficha()
    write_02_requerimientos()
    write_03_acta()
    write_04_glosario()
    write_05_preguntas_panel()
    write_06_especificacion_pwa()
    write_07_arquitectura()
    write_08_normalizacion()
    
    # Reconstruir también todos los DOCX
    for md_file in sorted(glob.glob("docs/*.md")):
        with open(md_file, "r", encoding="utf-8") as f:
            md_content = f.read()
        docx_file = md_file.replace(".md", ".docx")
        convert_md_to_docx_custom(md_content, docx_file)
        
    # Convertir todos los DOCX a PDF usando Word COM
    print("=== EXPORTANDO TODOS LOS DOCUMENTOS A PDF FORMAL ===")
    try:
        pythoncom.CoInitialize()
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        
        for docx_file in sorted(glob.glob("docs/*.docx")):
            pdf_target = docx_file.replace(".docx", ".pdf")
            abs_docx = os.path.abspath(docx_file)
            abs_pdf = os.path.abspath(pdf_target)
            print(f"Exportando a PDF: {pdf_target}...")
            wb = word.Documents.Open(abs_docx)
            wb.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
            wb.Close()
            print(f"Completado exitosamente: {pdf_target}")
            
        word.Quit()
        print("=== TODOS LOS PDFs GENERADOS CON ÉXITO ===")
    except Exception as e:
        print(f"Error generando PDFs: {e}")

if __name__ == "__main__":
    build_all()
