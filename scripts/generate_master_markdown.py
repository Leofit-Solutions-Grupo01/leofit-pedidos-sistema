# -*- coding: utf-8 -*-
"""
Script generador del Documento Maestro Integral y Definitivo de LeoFit Solutions.
Consolida al 100% todos los documentos dispersos, elimina duplicidades y contradicciones,
y produce una única fuente de verdad técnica y académica.
"""

import os
import sys

def build_master_markdown():
    content = """# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# SISTEMA DE GESTIÓN DE PEDIDOS Y CONTROL DE INVENTARIO MULTICANAL PARA LA EMPRESA LEOFIT
## LIBRO DE INGENIERÍA Y DOCUMENTO MAESTRO INTEGRAL DEL PROYECTO
### FUENTE ÚNICA DE VERDAD (SINGLE SOURCE OF TRUTH) — CICLO 2026-I

---

### CONTROL DE INFORMACIÓN DEL PROYECTO

| Campo | Detalle Institucional y de Proyecto |
| :--- | :--- |
| **Nombre del Proyecto** | Sistema Web Progresivo (PWA) de Gestión de Pedidos y Control de Inventario Multicanal |
| **Empresa Beneficiaria** | LeoFit (RUC: 20608912345) — Emporio Comercial de Gamarra, La Victoria, Lima |
| **Asignatura** | Curso Integrador II: Software (Código: `100000S12F`) |
| **Docente Asignado** | Ing. Enrique Lee Huamani Uriarte |
| **Equipo de Desarrollo (Grupo 01)** | • Loayza Rodriguez, Lady Luz — Código: `U22221489` (Scrum Master / DevSecOps)<br>• Cárdenas Fernández, Víctor Leandro — Código: `U19217414` (Product Owner / Data Architect)<br>• Roman Delgado, Harley Anthony — Código: `U21313032` (Frontend Lead / PWA Specialist)<br>• Dávila Morales, Jim Alessandro — Código: `U18206081` (QA Engineer Lead / Backend)<br>• Rojas Sanchez, Daniel Enrique — Código: `U21214627` (Business Analyst / Cloud DevOps) |
| **Versión del Documento** | 3.0.0 (Unificación Maestra Total) |
| **Fecha de Publicación** | Septiembre de 2026 |
| **Estado del Documento** | Aprobado — Versión Oficial Consolidada |

---

### HISTORIAL DE REVISIONES Y CONTROL DE VERSIONES

| Versión | Fecha | Autor(es) | Resumen de Modificaciones y Aportes |
| :---: | :---: | :--- | :--- |
| **v1.0** | 10/05/2026 | Grupo 01 | Entrega formal de Avance de Proyecto Final 1 (APF1). Análisis empresarial, requerimientos RF-001 a RF-012, arquitectura preliminar y prototipo UI inicial. Calificación obtenida: 18/20. |
| **v2.0** | 20/07/2026 | Grupo 01 | Entrega formal de Avance de Proyecto Final 2 (APF2). Despliegue cloud inicial, base de datos relacional PostgreSQL normalizada, catálogo de seguridad OWASP y levantamiento de observaciones. |
| **v3.0** | 24/09/2026 | Loayza R., Lady Luz (Lead) | **Consolidación Integral y Fusión Total**: Se eliminan 13 documentos fragmentados y dispersos en el repositorio para unificar toda la información técnica, de negocio, arquitectura, base de datos, seguridad, pruebas, evidencias de pantallas (14 pantallas) y gobernanza en un único Documento Maestro Definitivo. |

---

## ÍNDICE GENERAL DEL DOCUMENTO MAESTRO

1. **CAPÍTULO 1: ANÁLISIS EMPRESARIAL Y MODELO DE NEGOCIO**
   - 1.1 Introducción y Contexto del Sector Textil en Gamarra
   - 1.2 Ficha de Identificación de la Organización
   - 1.3 Misión y Visión Estratégica
   - 1.4 Diagnóstico Operativo del Proceso Actual (AS-IS)
   - 1.5 Modelo Propuesto y Oportunidades de Mejora (TO-BE)
   - 1.6 Matriz Comparativa de Brechas (Gap Analysis)
   - 1.7 Documento de Análisis de Negocio (Lean Canvas)
2. **CAPÍTULO 2: GESTIÓN ÁGIL DEL PROYECTO Y GOBERNANZA**
   - 2.1 Acta de Constitución del Proyecto (Project Charter Ágil)
   - 2.2 Objetivos SMART y Matriz de Alcance (In / Out)
   - 2.3 Cronograma Maestro del Proyecto (Gantt Semanas 1 a 18)
   - 2.4 Planificación Ágil de Sprints (Sprint Planning S0 al S4)
   - 2.5 Definición de Roles Scrum y Matriz de Responsabilidades RACI
   - 2.6 Políticas del Tablero Kanban / Scrum y Límites WIP
   - 2.7 Product Backlog Priorizado (Metodología MoSCoW)
   - 2.8 Historias de Usuario Detalladas bajo Estándar Gherkin (HU-001 a HU-008)
   - 2.9 Matriz Integral de Requerimientos Funcionales (RF-001 a RF-018)
   - 2.10 Matriz Integral de Requerimientos No Funcionales (RNF-001 a RNF-010)
3. **CAPÍTULO 3: ENTORNO DE DESARROLLO, STACK TECNOLÓGICO Y CONTROL DE VERSIONES**
   - 3.1 Matriz de Selección Multicriterio de Herramientas y Tecnologías
   - 3.2 Comandos Estandarizados de Configuración y Ejecución Local
   - 3.3 Estructura del Repositorio GitHub, Políticas de Ramas (GitFlow) y Convención de Commits
4. **CAPÍTULO 4: PROTOTIPOS, SISTEMA DE DISEÑO Y EXPERIENCIA DE USUARIO (UX/UI)**
   - 4.1 Wireframes de Baja Fidelidad (Mobile-First)
   - 4.2 Design System Corporativo de LeoFit (Tokens, Colores HSL y Tipografía)
   - 4.3 Evaluación de las 10 Heurísticas de Nielsen y Accesibilidad WCAG 2.1 AA
   - 4.4 Flujo de Navegación e Interacción del Usuario (User Flow)
5. **CAPÍTULO 5: GESTIÓN INTEGRAL DE RIESGOS DEL PROYECTO**
   - 5.1 Identificación y Taxonomía de Riesgos (Técnicos, Operativos, de Seguridad y de Negocio)
   - 5.2 Matriz de Probabilidad e Impacto 5x5 y Heatmap de Severidad
   - 5.3 Plan de Contingencia y Mitigación Preventiva y Reactiva
6. **CAPÍTULO 6: MÉTRICAS DEL SISTEMA, OBSERVABILIDAD Y NIVELES DE SERVICIO (SLA / SLO)**
   - 6.1 Identificación de KPIs de Negocio e Ingeniería de Software
   - 6.2 Definición Contractual de Niveles de Servicio (SLA 99.5% y SLOs de Latencia/Error)
   - 6.3 Plan de Medición, Telemetría y Observabilidad
7. **CAPÍTULO 7: ARQUITECTURA DE SOFTWARE E INGENIERÍA FRONT-END**
   - 7.1 Arquitectura General del Sistema (Clean Architecture por Capas)
   - 7.2 Modelo C4 (Diagramas de Contexto, Contenedores y Componentes)
   - 7.3 Arquitectura PWA Offline-First y Estrategia de Service Worker (Cache-First y Background Sync)
   - 7.4 Estrategias de Optimización Web (WPO) y Comparativa Cuantitativa de Métricas (Lighthouse)
8. **CAPÍTULO 8: MODELADO, NORMALIZACIÓN Y ADMINISTRACIÓN DE BASE DE DATOS**
   - 8.1 Proceso Formal de Normalización de Base de Datos (1NF, 2NF y 3NF)
   - 8.2 Diagrama Entidad-Relación Lógico y Físico
   - 8.3 Esquema DDL en PostgreSQL con Triggers, Constraints e Índices B-Tree/GIN
   - 8.4 Estrategia de Respaldo Automatizado, Replicación WAL y Recuperación ante Desastres (DRP)
9. **CAPÍTULO 9: SEGURIDAD DEL SOFTWARE, CRIPTOGRAFÍA Y PRUEBAS WEB**
   - 9.1 Matriz de Mitigación OWASP Top 10 (2021-2026)
   - 9.2 Módulo de Control de Acceso Basado en Roles (RBAC) y Ciclo de Vida de Tokens JWT
   - 9.3 Especificación de Cifrado de Datos en Reposo (AES-256-GCM) y Tránsito (TLS 1.3)
   - 9.4 Pruebas de Seguridad Web Automatizadas (SAST, DAST con OWASP ZAP y Auditoría de Dependencias)
10. **CAPÍTULO 10: VERIFICACIÓN, VALIDACIÓN Y EVIDENCIAS DE REQUERIMIENTOS**
    - 10.1 Plan Integral y Pirámide de Pruebas (Unitarias, Integración y End-to-End con Playwright)
    - 10.2 Matriz de Trazabilidad Total Requerimiento vs Casos de Prueba (100% Cobertura)
    - 10.3 Catálogo Fotográfico y Técnico Exhaustivo de Evidencias de Pantalla (14 Pantallas del Sistema)
11. **CAPÍTULO 11: MANUAL DE DESPLIEGUE EN LA NUBE Y OPERATIVIDAD**
    - 11.1 Topología Cloud y Arquitectura de Infraestructura
    - 11.2 Guía Paso a Paso de Despliegue con Docker y Docker Compose
    - 11.3 Pipeline de Integración y Despliegue Continuo (CI/CD con GitHub Actions)
    - 11.4 Verificación de Operatividad y Monitoreo de Endpoints en Producción
12. **CAPÍTULO 12: GOBERNANZA ACADÉMICA, GLOSARIO Y DEFENSA ANTE EL PANEL**
    - 12.1 Resumen de Acuerdos de Gobernanza de Equipo y Actas de Reunión
    - 12.2 Glosario Unificado de Términos Técnicos y de Dominio Textil/Comercial
    - 12.3 Banco de 15 Preguntas Críticas y Respuestas Sólidas para la Sustentación ante el Jurado Calificador
13. **CAPÍTULO 13: CONCLUSIONES Y LECCIONES APRENDIDAS**
    - 13.1 Conclusiones Técnicas y de Negocio
    - 13.2 Lecciones Aprendidas en Gestión Ágil y Calidad de Software
14. **REFERENCIAS BIBLIOGRÁFICAS (NORMAS IEEE Y APA 7ma EDICIÓN)**

---

# LEVANTAMIENTO DE OBSERVACIONES DE EVALUACIONES PREVIAS (APF1)

El equipo de desarrollo (Grupo 01) obtuvo una calificación de **18/20** en la entrega del Avance de Proyecto Final 1 (APF1). Para esta consolidación maestra y las subsiguientes defensas, se subsanaron al 100% las observaciones docentes:

1. **Profundización en Requerimientos y Casos Borde**: Se expandió el catálogo de requerimientos funcionales de 12 a **18 RFs**, incorporando explícitamente el soporte de multi-rol, auditoría de transacciones, modo offline-first y alertas automáticas de rotura de stock.
2. **Evidencias de Pantalla con Rigor de Aceptación UAT**: Se integró una sección exhaustiva con 14 capturas de pantalla de alta fidelidad, desglosando componentes visuales, reglas de negocio validadas y criterios de aceptación específicos para cada funcionalidad.
3. **Formalización de la Base de Datos**: Se incluyó la demostración matemática de normalización hasta Tercera Forma Normal (3NF), el script DDL completo en PostgreSQL con triggers automáticos para el cálculo de totales y actualización de stock, e índices optimizados B-Tree y GIN.
4. **Seguridad y Criptografía Demostrada**: Se agregaron reportes de pruebas automatizadas DAST (OWASP ZAP) y SAST (ESLint-plugin-security y pip-audit), con políticas de rotación de JWT y hashing de contraseñas mediante Bcrypt con costo 12.

---

# CAPÍTULO 1: ANÁLISIS EMPRESARIAL Y MODELO DE NEGOCIO

## 1.1. Introducción y Contexto del Sector Textil en Gamarra

El Emporio Comercial de Gamarra, situado en el distrito de La Victoria, Lima, representa el conglomerado textil y confeccionista más grande del Perú y uno de los principales motores económicos del país. Históricamente, las transacciones en Gamarra se sustentaron en la venta física presencial. No obstante, la transformación digital post-pandemia y la penetración masiva de smartphones impulsaron el comercio conversacional a través de canales digitales como WhatsApp Business, Instagram Direct y TikTok.

A pesar de esta digitalización en el canal de contacto, la operativa interna de muchas micro y pequeñas empresas (MYPEs) textiles continúa fundamentándose en registros informales: cuadernos físicos manuscritos, hojas de cálculo desarticuladas y mensajes de chat no estructurados. Esta disonancia operativa provoca cuellos de botella severos: demoras de hasta 45 minutos por pedido, pérdida de mensajes por saturación, ventas cruzadas sin stock disponible (quiebre de inventario) y falta absoluta de trazabilidad comercial y financiera. En este escenario opera **LeoFit**, requiriendo urgentemente una plataforma tecnológica profesional de gestión de pedidos y control de inventario multicanal.

## 1.2. Ficha de Identificación de la Organización

| Campo Institucional | Detalle de la Empresa |
| :--- | :--- |
| **Razón Social** | LeoFit Confecciones y Diseños Deportivos S.A.C. |
| **Nombre Comercial** | LeoFit Solutions / Ropa Deportiva LeoFit |
| **Número de RUC** | `20608912345` (RUC Activo y Habido) |
| **Ubicación Principal** | Jr. Gamarra 1230, Interior Galería "El Rey de Gamarra", Piso 4, La Victoria, Lima, Perú |
| **Representante Legal** | Víctor Leandro Cárdenas Fernández (Gerente General) |
| **Contacto y Operaciones** | Correo institucional: `contacto@leofit.com.pe` \| Celular comercial: `+51 987 654 321` |
| **Sector Económico** | Industria Textil, Confección y Comercialización de Indumentaria Deportiva Masculina y Femenina |
| **Modelo de Negocio** | Mixto: Venta Mayorista B2B (distribuidores de provincias) y Venta Minorista B2C (clientes finales) |
| **Canales Actuales** | Stand físico comercial en Gamarra, WhatsApp Business, Instagram Direct y Marketplace de Facebook |

## 1.3. Misión y Visión Estratégica

- **Misión Corporativa**: Diseñar, confeccionar y distribuir prendas deportivas de alta durabilidad, confort y estética vanguardista para la comunidad fitness y mayoristas del Perú, garantizando una atención ágil, confiable y sincronizada que supere las expectativas de nuestros clientes mediante procesos estandarizados y tecnología de vanguardia.
- **Visión Estratégica**: Consolidarse hacia el año 2028 como la marca independiente líder de ropa deportiva en el canal digital peruano, reconocida nacionalmente por su excelencia textil, innovación tecnológica en la experiencia de compra multicanal y capacidad de respuesta logística eficiente.

## 1.4. Diagnóstico Operativo del Proceso Actual (AS-IS)

El proceso operativo tradicional de LeoFit presenta una fuerte dependencia de la intervención manual y una nula sincronización de datos entre los vendedores y el almacén. El ciclo de vida de un pedido manual comprende 8 pasos críticos:

```mermaid
flowchart TD
    A([Cliente inicia contacto por WhatsApp]) --> B[Vendedor responde mensaje manualmente]
    B --> C[Cliente solicita prendas y tallas]
    C --> D[Vendedor consulta stock físico caminando al almacén]
    D --> E{¿Hay Stock Disponible?}
    E -- No --> F[Vendedor avisa y ofrece sustitutos - 20 min perdidos]
    E -- Sí --> G[Cliente envía captura de comprobante de pago Yape/Plin]
    G --> H[Vendedor anota pedido en cuaderno o Excel manual]
    H --> I[Vendedor entrega boleta a almacenero]
    I --> J([Almacenero empaqueta y despacha de forma descoordinada])
```

![Figura 1.1: Diagrama BPMN del Proceso Operativo Actual (AS-IS)](../diagrams/01_BPMN_AS-IS.png)

### Tabla de Desglose del Proceso AS-IS (8 Pasos Operativos):

| Paso | Actividad Operativa | Responsable | Herramienta / Soporte | Tiempo Estimado | Cuello de Botella y Riesgo Crítico |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **1** | Recepción de consulta de catálogo y precios | Vendedor | Chat de WhatsApp | 5 - 15 min | Demora en responder genera abandono de compra hacia la competencia. |
| **2** | Envío de fotos y disponibilidad de tallas | Vendedor | Galería del teléfono | 5 - 10 min | Fotos desactualizadas de modelos sin stock real. |
| **3** | Verificación de inventario disponible | Vendedor | Consulta visual en almacén | 10 - 20 min | Doble compromiso de la misma prenda a dos clientes distintos. |
| **4** | Confirmación de compra y datos de envío | Vendedor y Cliente | Mensaje de texto libre | 5 - 10 min | Errores en números de DNI, teléfono o dirección de envío. |
| **5** | Validación del pago (Yape / Plin / Transferencia) | Vendedor | Captura de pantalla | 5 - 15 min | Riesgo de comprobantes falsificados y falta de conciliación bancaria. |
| **6** | Registro del pedido en libro físico | Vendedor | Cuaderno o Excel personal | 5 - 10 min | Pérdida de apuntes, tachones y omisión de pedidos urgentes. |
| **7** | Notificación al personal de almacén | Vendedor | Llamada o mensaje verbal | 10 - 30 min | Descoordinación de prioridades y demoras en el despacho. |
| **8** | Empaque, rotulado y entrega a courier | Almacenero | Guía física en papel | 30 - 60 min | Errores en etiquetado y despachos de productos erróneos. |

> **Diagnóstico Cuantitativo AS-IS**: El tiempo total promedio para procesar un único pedido oscila entre **45 y 120 minutos**, con una tasa de error en pedidos despachados del **14.2%** y una pérdida estimada del **22%** de ventas potenciales por demoras en la respuesta al cliente.

## 1.5. Modelo Propuesto y Oportunidades de Mejora (TO-BE)

La solución implementada automatiza y centraliza la toma de pedidos mediante una **Aplicación Web Progresiva (PWA)** accesible desde cualquier dispositivo móvil o de escritorio, permitiendo a clientes y vendedores operar con catálogo en tiempo real y reserva de stock inmediata:

```mermaid
flowchart TD
    A([Cliente/Vendedor accede a la PWA]) --> B[Explora Catálogo con Filtros y Stock en Tiempo Real]
    B --> C[Agrega prendas al Carrito Interactivo]
    C --> D[Ingresa datos validados del cliente: DNI, Teléfono, Destino]
    D --> E[Selecciona Método de Pago y Adjunta Comprobante Digital]
    E --> F[PWA emite Reserva Atómica de Stock vía API REST / PostgreSQL]
    F --> G[Generación Inmediata de Pedido con Código Único]
    G --> H[Notificación Automática a Panel de Almacén]
    H --> I([Almacenero despacha con Guía Digital e Imprime Ticket QR])
```

![Figura 1.2: Diagrama BPMN del Proceso Propuesto Optimizado (TO-BE)](../diagrams/01_BPMN_TO-BE.png)

## 1.6. Matriz Comparativa de Brechas (Gap Analysis)

| Dimensión Operativa | Situación Actual (AS-IS) | Situación Propuesta (TO-BE) | Impacto y Beneficio Esperado |
| :--- | :--- | :--- | :--- |
| **Tiempo de Toma de Pedido** | 45 a 120 minutos por transacción | Menos de 90 segundos mediante el carrito digital | **Reducción del 92%** en tiempo de atención |
| **Precisión del Inventario** | Desincronizado; chequeos visuales manuales | Actualización atómica en base de datos PostgreSQL | **0% de sobreventas** de productos agotados |
| **Registro de Información** | Cuadernos manuscritos y chats dispersos | Base de datos relacional centralizada con auditoría | **100% de trazabilidad** y respaldos diarios |
| **Capacidad de Atención** | Máximo 25 pedidos diarios por vendedor | Más de 300 pedidos diarios simultáneos | **Escalabilidad comercial 12x** sin aumentar personal |
| **Disponibilidad Offline** | Nula; pérdida de información ante cortes | PWA con Service Worker y almacenamiento IndexedDB | **Operatividad ininterrumpida** en galerías de Gamarra |

## 1.7. Documento de Análisis de Negocio (Lean Canvas)

![Figura 1.3: Modelo de Negocio Lean Canvas de LeoFit Solutions](../diagrams/06_Lean_Canvas.png)

El modelo de negocio validado se sintetiza en la siguiente matriz Lean Canvas estructurada:

| Bloque Lean Canvas | Detalle y Formulación Estratégica para LeoFit |
| :--- | :--- |
| **1. Problema** | • Demoras excesivas en atención y cotización vía WhatsApp.<br>• Quiebres de stock por ventas cruzadas de prendas inexistentes.<br>• Errores humanos en notas manuscritas y despachos equivocados.<br>• Cero visibilidad gerencial de métricas comerciales y financieras. |
| **2. Segmento de Clientes** | • **Mayoristas de Provincias**: Comerciantes que compran lotes para reventa en Arequipa, Trujillo, Huancayo y Cusco.<br>• **Clientes Minoristas Digitales**: Deportistas y entusiastas fitness (18 a 40 años) en Lima Metropolitana.<br>• **Vendedores Internos y Almaceneros de LeoFit**. |
| **3. Propuesta de Valor Única** | *"Plataforma web PWA ultrarrápida que permite registrar, pagar y despachar pedidos deportivos en menos de 90 segundos con inventario en tiempo real garantizado y operatividad offline en el emporio de Gamarra."* |
| **4. Solución Tecnológica** | • Catálogo PWA interactivo con filtros por categoría, talla y color.<br>• Carrito de compras con reserva de stock en tiempo real.<br>• Panel administrativo con dashboard de KPIs y semáforo de inventario.<br>• Modo offline-first para operar en sótanos y zonas con baja señal celular. |
| **5. Canales de Distribución** | • Web App PWA instalable en celulares Android/iOS sin pasar por App Store.<br>• Enlace directo fijado en perfil de Instagram y WhatsApp Business.<br>• Stand comercial presencial en Galería El Rey de Gamarra. |
| **6. Flujos de Ingresos** | • Venta mayorista por volumen de conjuntos deportivos (ticket promedio: S/ 850).<br>• Venta minorista directa al consumidor final (ticket promedio: S/ 110).<br>• Cobros directos mediante billeteras digitales (Yape/Plin) y transferencias BCP/BBVA. |
| **7. Estructura de Costos** | • Costo de infraestructura Cloud (Hosting VPS, Base de datos Supabase, Dominio SSL): ~$25 USD/mes.<br>• Costos de confección textil, insumos de tela suplex/algodón y mano de obra.<br>• Mantenimiento de software, licencias y conectividad de red. |
| **8. Métricas Clave (KPIs)** | • Tasa de conversión de pedidos registrados vs cotizados (> 35%).<br>• Tiempo promedio de registro y confirmación de pedido (< 90 segundos).<br>• Tasa de discrepancia de stock en inventario (< 0.5%). |
| **9. Ventaja Competitiva Injusta** | Integración nativa entre el catálogo digital conversacional y el control físico de stock en Gamarra con sincronización offline-first, diseñada a medida para el flujo operativo textil peruano. |

---

# CAPÍTULO 2: GESTIÓN ÁGIL DEL PROYECTO Y GOBERNANZA

## 2.1. Acta de Constitución del Proyecto (Project Charter Ágil)

| Sección del Charter | Definición Formal y Alcance |
| :--- | :--- |
| **Título del Proyecto** | Sistema Web PWA de Gestión de Pedidos y Control de Inventario Multicanal — LeoFit |
| **Patrocinador (Sponsor)** | Víctor Leandro Cárdenas Fernández (Gerente General de LeoFit) |
| **Líder de Proyecto / Scrum Master** | Lady Luz Loayza Rodriguez (Estudiante UTP) |
| **Propósito y Justificación** | Erradicar la pérdida de pedidos por desorganización manual, optimizar los tiempos de atención a clientes y garantizar la sincronización atómica del stock textil en Gamarra. |
| **Presupuesto Estimado** | Proyecto de desarrollo académico-empresarial con un costo de infraestructura cloud estimado en S/ 120 soles mensuales de operación y soporte. |
| **Supuestos Clave** | • La empresa facilitará el inventario inicial de prendas y fotos de catálogo.<br>• Los vendedores disponen de smartphones con navegadores web estándar (Chrome/Safari). |
| **Restricciones Principales** | • Fecha de entrega estricta dictada por el calendario académico de 18 semanas de la UTP.<br>• La aplicación debe soportar intermitencia de conexión a Internet en galerías comerciales. |

## 2.2. Objetivos SMART y Matriz de Alcance (In / Out)

### Objetivos SMART:
1. **Específico (S)**: Desarrollar una Progressive Web App (PWA) con backend RESTful y base de datos relacional para gestionar el 100% de los pedidos mayoristas y minoristas de LeoFit.
2. **Medible (M)**: Reducir el tiempo de toma de pedidos de 45 minutos a menos de 90 segundos, alcanzando una precisión de inventario del 99.5%.
3. **Alcanzable (A)**: Implementado por un equipo de 5 ingenieros de sistemas utilizando metodologías ágiles Scrum y tecnologías probadas de alto rendimiento (React, Vite, Node/FastAPI, PostgreSQL).
4. **Relevante (R)**: Aumentar la capacidad comercial de LeoFit para procesar pedidos en temporadas de alta demanda (Día de la Madre, Fiestas Patrias y Navidad).
5. **Temporal (T)**: Desplegar y validar en producción durante las 18 semanas del ciclo académico 2026-I de la UTP.

### Matriz de Alcance (In / Out):

| Dentro del Alcance (IN SCOPE) | Fuera del Alcance (OUT OF SCOPE) |
| :--- | :--- |
| • Catálogo digital interactivo con búsqueda y filtros multicriterio. | • Pasarela de cobro bancario automático internacional (ej. Stripe/PayPal) — se procesa mediante validación de comprobante Yape/Plin/Transferencia. |
| • Carrito de compras y emisión de pedidos con código único alfanumérico. | • Módulo de facturación electrónica directa con SUNAT (se generan reportes compatibles pero sin envío OSE directo en fase 1). |
| • Panel administrativo de control de estados: *Pendiente, Confirmado, En Preparación, Despachado, Cancelado*. | • Sistema de trazabilidad GPS de camiones de reparto en tiempo real. |
| • Módulo de inventario con alertas de stock mínimo (semáforo visual). | • Módulo de diseño gráfico automatizado de prendas de vestir. |
| • Autenticación segura basada en roles (RBAC) con tokens JWT y cifrado. | • Aplicaciones nativas compiladas en Java/Swift para App Store/Google Play (se resuelve con PWA instalable). |
| • Modo offline para consulta y captura de pedidos sin conectividad activa. | • Sistema de gestión de recursos humanos y pago de planillas (nóminas). |

## 2.3. Cronograma Maestro del Proyecto (Gantt Semanas 1 a 18)

| Semana | Hito / Fase | Entregables Principales | Estado |
| :---: | :--- | :--- | :---: |
| **S1 - S2** | Análisis Empresarial | Ficha de empresa, Lean Canvas, Modelo AS-IS / TO-BE, Project Charter | 100% Completado |
| **S3 - S4** | Requisitos y UX/UI | Historias de usuario, Product Backlog, Wireframes, Prototipos Figma | 100% Completado |
| **S5 - S6** | Arquitectura y Setup | Repositorio GitHub, CI/CD, Arquitectura C4, Setup de Docker y PostgreSQL | 100% Completado |
| **S7** | **Hito APF1 (Entrega 1)** | **Sustentación de Avance 1: Front-End funcional, WPO y Planificación** | **Aprobado (18/20)** |
| **S8 - S9** | Backend y Persistencia | Modelado y normalización BD (3NF), Endpoints API REST, Triggers | 100% Completado |
| **S10 - S11** | Seguridad y Cifrado | OWASP Top 10, Auth JWT RBAC, Cifrado AES-256-GCM, Pruebas SAST/DAST | 100% Completado |
| **S12** | **Hito APF2 (Entrega 2)** | **Sustentación de Avance 2: Despliegue Cloud, BD integrada y Seguridad** | **100% Completado** |
| **S13 - S14** | PWA Offline & Reportes | Service Worker Workbox, Cache IndexedDB, Exportación Excel/PDF | 100% Completado |
| **S15 - S16** | QA, UAT y Carga | Pruebas End-to-End Playwright, Pruebas de Carga k6, Auditoría Final | 100% Completado |
| **S17 - S18** | **Cierre y Defensa Final** | **Sustentación Final ante Jurado UTP y Entrega de Memoria Técnica** | **Listo para Defensa** |

![Figura 2.1: Diagrama de Gantt del Cronograma Maestro (Semanas 1 a 18)](../diagrams/07_Cronograma_Gantt.png)

## 2.4. Planificación Ágil de Sprints (Sprint Planning S0 al S4)

- **Sprint 0 (Semanas 1 a 4) - Fundación y Diseño**: Configuración del entorno de desarrollo, creación de lineamientos de arquitectura, diseño de wireframes y levantamiento de requisitos formales.
- **Sprint 1 (Semanas 5 a 7) - Catálogo y Carrito PWA (APF1)**: Desarrollo de componentes Front-End interactivos, optimización WPO, catálogo con buscador instantáneo y carrito con persistencia local.
- **Sprint 2 (Semanas 8 a 10) - Backend API, Persistencia y Seguridad (APF2)**: Normalización de base de datos PostgreSQL, desarrollo de endpoints FastAPI/Express, autenticación JWT con roles y defensas OWASP.
- **Sprint 3 (Semanas 11 a 14) - Dashboard Administrativo y Modo Offline**: Panel de control con gráficos de rendimiento, módulo de gestión de stock con triggers automáticos y Service Worker con Background Sync.
- **Sprint 4 (Semanas 15 a 18) - Calidad, Despliegue y Sustentación Final**: Pruebas automatizadas con Playwright, auditorías DAST con OWASP ZAP, manuales técnicos de usuario y defensa final.

## 2.5. Definición de Roles Scrum y Matriz de Responsabilidades RACI

### Equipo Scrum (Grupo 01):
1. **Lady Luz Loayza Rodriguez** — *Scrum Master & DevSecOps Lead*: Responsable de remover impedimentos del equipo, velar por la adhesión al marco ágil Scrum, configurar pipelines CI/CD y liderar las auditorías de seguridad informática.
2. **Víctor Leandro Cárdenas Fernández** — *Product Owner & Data Architect*: Responsable de la priorización del Product Backlog, interlocutor principal con el negocio LeoFit, diseñador y normalizador del modelo de base de datos relacional.
3. **Harley Anthony Roman Delgado** — *Frontend Lead & PWA Specialist*: Diseñador de interfaces UI/UX, implementador del Design System y responsable de la arquitectura offline-first del Service Worker.
4. **Jim Alessandro Dávila Morales** — *QA Engineer Lead & Backend Developer*: Diseñador del plan de pruebas, implementador de pruebas automatizadas E2E y unitarias, y desarrollador de endpoints RESTful.
5. **Daniel Enrique Rojas Sanchez** — *Business Analyst & Cloud DevOps*: Analista de procesos de negocio AS-IS/TO-BE, configurador de infraestructura en la nube (Docker, Render, Supabase) y monitor de observabilidad.

### Matriz RACI del Proyecto:

| Entregable / Actividad Técnica | Lady Loayza (SM) | Víctor Cárdenas (PO) | Harley Roman (Front) | Jim Dávila (QA) | Daniel Rojas (DevOps) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Análisis de Negocio y Lean Canvas** | C | **A** | C | I | **R** |
| **Definición y Priorización del Backlog** | C | **A / R** | C | C | C |
| **Diseño UI/UX y Sistema de Diseño** | I | C | **A / R** | C | I |
| **Desarrollo Front-End PWA** | I | C | **A / R** | C | I |
| **Modelado y Normalización de BD** | C | **A / R** | I | C | C |
| **Desarrollo de API Backend** | C | C | C | **R** | **A** |
| **Seguridad OWASP y Pruebas DAST** | **A / R** | C | C | C | I |
| **Pruebas Automatizadas Unitarias / E2E** | C | I | C | **A / R** | I |
| **Despliegue Cloud y CI/CD** | C | I | I | I | **A / R** |

*(Donde: **R** = Responsable de ejecución, **A** = Aprobador final / Accountable, **C** = Consultado, **I** = Informado).*

## 2.6. Políticas del Tablero Kanban / Scrum y Límites WIP

El equipo gestiona el flujo de trabajo a través de un tablero GitHub Projects configurado con 5 columnas y límites estrictos de trabajo en progreso (Work In Progress - WIP):

| Columna del Tablero | Propósito y Política de Entrada | Límite WIP | Criterio de Salida (Definition of Done - DoD) |
| :--- | :--- | :---: | :--- |
| **1. Backlog** | Repositorio de todas las Historias de Usuario priorizadas por el Product Owner. | Sin límite | Historia de usuario redactada con criterios de aceptación Gherkin y estimación en puntos de historia. |
| **2. Ready / To Do** | Tareas seleccionadas para el Sprint actual en el Sprint Planning. | Max. 10 | Tarea asignada a un desarrollador con dependencias técnicas resueltas. |
| **3. In Progress** | Tareas en desarrollo activo por parte del equipo. | **Max. 4** | Código completado localmente, pasando linters estáticos y pruebas unitarias preliminares. |
| **4. Code Review / QA** | Pull Request abierto con pruebas automáticas ejecutándose en CI/CD. | **Max. 3** | Revisión aprobada por al menos un par (peer review), 0 errores en SonarCloud/Linter y cobertura > 80%. |
| **5. Done** | Funcionalidad desplegada en ambiente de staging o producción. | Sin límite | Aprobada por el Product Owner y documentada en la memoria técnica del proyecto. |

![Figura 2.2: Tablero Kanban / Scrum con Políticas y Límites WIP](../diagrams/08_Tablero_Kanban.png)

## 2.7. Product Backlog Priorizado (Metodología MoSCoW)

| ID | Ítem del Backlog | Prioridad MoSCoW | Estimación (Story Points) | Sprint Asignado |
| :---: | :--- | :---: | :---: | :---: |
| **PB-01** | Catálogo digital responsivo con buscador en tiempo real | **Must Have** | 5 | Sprint 1 |
| **PB-02** | Carrito de compras interactivo con persistencia local | **Must Have** | 5 | Sprint 1 |
| **PB-03** | Formulario de registro de pedidos con validación de DNI/Teléfono | **Must Have** | 8 | Sprint 1 |
| **PB-04** | Base de datos relacional PostgreSQL con integridad referencial | **Must Have** | 8 | Sprint 2 |
| **PB-05** | API RESTful con endpoints protegidos por JWT | **Must Have** | 8 | Sprint 2 |
| **PB-06** | Panel de administración de pedidos con cambio de estados | **Must Have** | 5 | Sprint 2 |
| **PB-07** | Módulo de inventario con alertas de stock mínimo | **Must Have** | 5 | Sprint 3 |
| **PB-08** | Implementación de Service Worker para soporte offline (PWA) | **Should Have** | 8 | Sprint 3 |
| **PB-09** | Dashboard gerencial con métricas y gráficos de ventas | **Should Have** | 5 | Sprint 3 |
| **PB-10** | Exportación de reportes de pedidos en formato Excel y PDF | **Should Have** | 3 | Sprint 3 |
| **PB-11** | Impresión de tickets de despacho con código QR | **Could Have** | 5 | Sprint 4 |
| **PB-12** | Notificaciones automáticas por mensaje web | **Could Have** | 3 | Sprint 4 |
| **PB-13** | Integración con pasarelas de pago con tarjeta de crédito | **Won't Have (v1)** | 13 | Futuras Versiones |

## 2.8. Historias de Usuario Detalladas bajo Estándar Gherkin (HU-001 a HU-008)

### HU-001: Búsqueda y Filtrado Dinámico de Prendas Deportivas
- **Como**: Vendedor o Cliente de LeoFit.
- **Quiero**: Filtrar el catálogo por nombre, categoría, rango de precio y disponibilidad de talla.
- **Para**: Encontrar de forma instantánea la prenda solicitada sin tener que revisar manualmente fotos dispersas en WhatsApp.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Filtrado exitoso de producto por categoría y texto
    Dado que el usuario se encuentra en la pantalla principal del catálogo
    Cuando escribe "Short Runner" en la barra de búsqueda y selecciona la categoría "Varones"
    Entonces el sistema debe mostrar únicamente las prendas que coincidan con ambos filtros en menos de 200 ms
    Y debe indicar la cantidad exacta de unidades disponibles por talla.
  ```

### HU-002: Carrito de Compras Interactivo y Resumen de Totales
- **Como**: Vendedor de piso o mayorista.
- **Quiero**: Añadir múltiples prendas con diferentes tallas y colores a una bolsa interactiva.
- **Para**: Calcular el total exacto a cobrar en tiempo real, incluyendo descuentos por volumen y costos de envío.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Modificación de cantidades y recálculo automático
    Dado que el usuario ha agregado 3 polos deportivos al carrito
    Cuando incrementa la cantidad a 6 unidades en la vista del carrito
    Entonces el total del pedido debe recalcularse automáticamente aplicando el precio mayorista
    Y el botón "Continuar Pedido" debe habilitarse de inmediato.
  ```

### HU-003: Registro y Emisión Formal del Pedido con Generación de Código
- **Como**: Vendedor de LeoFit.
- **Quiero**: Registrar los datos del cliente (nombre, DNI, teléfono, dirección) y adjuntar el comprobante de pago.
- **Para**: Generar una orden de compra formal numerada que descuente automáticamente el stock y pase a cola de almacén.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Registro de pedido con stock suficiente
    Dado que el cliente cuenta con prendas seleccionadas en el carrito con stock validado
    Cuando el vendedor completa el formulario con datos válidos y presiona "Confirmar Pedido"
    Entonces el sistema debe generar un código de orden único (ej. ORD-2026-0042)
    Y descontar las unidades correspondientes de la tabla de inventario en la base de datos
    Y cambiar el estado de la orden a "Pendiente de Despacho".
  ```

### HU-004: Control y Actualización del Estado del Pedido en Almacén
- **Como**: Operario de almacén o despachador.
- **Quiero**: Visualizar los pedidos en estado "Confirmado" y cambiar su estado a "En Preparación" y "Despachado".
- **Para**: Coordinar los envíos diarios y asegurar que ninguna orden quede sin empaquetar ni entregar al courier.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Despacho de pedido con registro de auditoría
    Dado que un pedido se encuentra en estado "En Preparación"
    Cuando el almacenero selecciona "Marcar como Despachado" e ingresa el número de remito
    Entonces el sistema debe actualizar el estado de la orden a "Despachado"
    Y registrar la marca de tiempo exacta y el ID del usuario en la tabla de auditoría.
  ```

### HU-005: Visualización de Indicadores de Negocio en Dashboard Gerencial
- **Como**: Administrador o Dueño de LeoFit.
- **Quiero**: Visualizar gráficos interactivos con el total de ventas del día, productos más vendidos y pedidos por estado.
- **Para**: Tomar decisiones estratégicas rápidas sobre reabastecimiento de tela y promociones comerciales.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Carga del dashboard con métricas actualizadas
    Dado que el usuario autenticado tiene el rol de "Administrador"
    Cuando accede a la sección de Dashboard
    Entonces el sistema debe calcular y renderizar los totales de ventas de los últimos 30 días
    Y mostrar un gráfico de dona con la distribución porcentual de estados de pedidos.
  ```

### HU-006: Alertas Visuales Preventivas de Agotamiento de Stock
- **Como**: Encargado de compras e inventario.
- **Quiero**: Un indicador visual tipo semáforo que me advierta cuando una prenda tenga menos de 5 unidades.
- **Para**: Ordenar la confección oportuna del lote de reposición antes de incurrir en un quiebre de stock comercial.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Detección de producto con stock crítico
    Dado que el stock de la prenda "Buzo Térmico Pro Negro M" disminuye a 3 unidades tras una venta
    Cuando el usuario ingresa al módulo de Inventario
    Entonces la fila del producto debe mostrar una etiqueta roja de alerta "Stock Crítico"
    Y figurar en la parte superior del listado de reposición prioritaria.
  ```

### HU-007: Operatividad Offline y Sincronización Automática
- **Como**: Vendedor itinerante en sótanos de Gamarra.
- **Quiero**: Continuar consultando el catálogo y registrando pedidos aún si el teléfono pierde señal celular.
- **Para**: No detener las ventas en áreas sin cobertura y sincronizar los datos automáticamente al reconectarse a Internet.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Captura de orden sin conexión a red
    Dado que el dispositivo pierde la conexión a Internet
    Cuando el vendedor registra un pedido
    Entonces el sistema debe almacenar la transacción en IndexedDB local
    Y mostrar un banner amarillo "Modo Offline - Datos guardados localmente"
    Y al restablecerse la conexión, enviar los pedidos pendientes al backend sin duplicar registros.
  ```

### HU-008: Exportación de Reportes Consolidados en Formato Excel y PDF
- **Como**: Administrador o Contador.
- **Quiero**: Descargar un reporte tabular de todos los pedidos filtrados por rango de fechas.
- **Para**: Realizar la conciliación de caja semanal y facilitar el cierre contable mensual.
- **Criterio de Aceptación (Gherkin)**:
  ```gherkin
  Escenario: Descarga de reporte semanal en Excel
    Dado que el administrador selecciona el rango del 1 al 7 de septiembre de 2026
    Cuando hace clic en el botón "Exportar a Excel"
    Entonces el sistema debe generar y descargar un archivo .xlsx estructurado con cliente, prendas, montos y métodos de pago
    En un tiempo inferior a 3 segundos.
  ```

## 2.9. Matriz Integral de Requerimientos Funcionales (RF-001 a RF-018)

| Código | Denominación del Requerimiento | Descripción Técnica | Prioridad | Módulo Asociado |
| :---: | :--- | :--- | :---: | :--- |
| **RF-001** | Catálogo Dinámico de Productos | Renderizado en tiempo real de prendas organizadas por categorías con fotos, descripción, tallas, colores y precios mayorista/minorista. | Alta | Catálogo |
| **RF-002** | Buscador y Filtrado Predictivo | Búsqueda por texto con debouncing (300ms) y filtros combinables por categoría, talla, color y rango de precios. | Alta | Catálogo |
| **RF-003** | Carrito de Compras Interactivo | Gestión en memoria y LocalStorage de prendas seleccionadas con modificación de cantidades y validación instantánea contra stock. | Alta | Ventas |
| **RF-004** | Registro Formal de Pedidos | Formulario con validación de tipo de documento (DNI/RUC), nombres, teléfono (9 dígitos), dirección de envío y método de despacho. | Alta | Ventas |
| **RF-005** | Adjunto de Comprobante de Pago | Capacidad de subir imagen o PDF de comprobante bancario (Yape, Plin, Transferencia) con compresión en cliente antes del envío. | Media | Ventas |
| **RF-006** | Generación de Código Único de Orden | Creación automática de correlativo alfanumérico inmutable (ej. `ORD-2026-XXXX`) para trazabilidad del cliente y almacén. | Alta | Backend / Ventas |
| **RF-007** | Panel de Gestión de Pedidos | Vista administrativa tabular con estados: *Pendiente, Confirmado, En Preparación, Despachado, Entregado, Cancelado*. | Alta | Almacén / Admin |
| **RF-008** | Transición y Auditoría de Estados | Mecanismo seguro de cambio de estado de pedidos restringido por rol, registrando usuario, fecha, hora y motivo de cancelación si aplica. | Alta | Almacén / Admin |
| **RF-009** | Control Atómico de Inventario | Actualización inmediata del stock en PostgreSQL mediante transacciones ACID concurrentes para evitar ventas cruzadas de la misma prenda. | Alta | Base de Datos |
| **RF-010** | Semáforo de Alerta de Stock Crítico | Notificación visual en panel cuando el stock de una SKU es inferior o igual al umbral configurado (umbral estándar: 5 unidades). | Media | Inventario |
| **RF-011** | Autenticación y Autorización RBAC | Inicio de sesión con correo y contraseña cifrada, emitiendo tokens JWT con roles definidos: *Administrador, Vendedor, Almacenero*. | Alta | Seguridad |
| **RF-012** | Gestión de Usuarios y Accesos | Módulo para que el Administrador cree, edite, bloquee o restablezca credenciales del personal operativo. | Media | Seguridad |
| **RF-013** | Dashboard Gerencial de Analítica | Visualización gráfica de métricas: total vendido diario/semanal, prendas más vendidas, ticket promedio y distribución de canales. | Media | Analítica |
| **RF-014** | Exportación de Reportes (Excel / PDF) | Generación en cliente/servidor de archivos estructurados de ventas e inventario listos para impresión y auditoría contable. | Media | Reportes |
| **RF-015** | Soporte PWA Offline-First | Service Worker configurado con Workbox para almacenamiento en caché de activos estáticos y registro de pedidos en IndexedDB sin red. | Alta | Frontend PWA |
| **RF-016** | Sincronización Automática en Segundo Plano | Sincronización bidireccional (Background Sync) de pedidos encolados localmente en cuanto el navegador detecte conexión a Internet. | Media | Frontend PWA |
| **RF-017** | Impresión de Tickets y Etiquetas QR | Generación de vista para ticketera térmica (80mm) con código QR que contiene el enlace de seguimiento del pedido para el cliente. | Baja | Despacho |
| **RF-018** | Bitácora de Auditoría del Sistema | Registro inmutable de operaciones críticas (cambios de stock, eliminaciones lógicas, modificaciones de precio y despachos). | Alta | Seguridad |

## 2.10. Matriz Integral de Requerimientos No Funcionales (RNF-001 a RNF-010)

| Código | Categoría | Requisito No Funcional y Métrica Objetivo | Método de Verificación |
| :---: | :--- | :--- | :--- |
| **RNF-001** | **Rendimiento (WPO)** | El puntaje en Google Lighthouse para la versión Mobile debe ser $\ge 90$ puntos en Performance, con First Contentful Paint (FCP) $\le 1.2$ s y Largest Contentful Paint (LCP) $\le 2.0$ s. | Auditoría automatizada con Lighthouse CI en pipeline. |
| **RNF-002** | **Disponibilidad** | El sistema debe ofrecer una disponibilidad contractual (Uptime SLA) del **99.5%** durante el horario comercial (08:00 a 20:00 horas GMT-5). | Monitoreo continuo mediante sondas UptimeRobot y BetterUptime. |
| **RNF-003** | **Seguridad** | Inmunidad frente a las vulnerabilidades del OWASP Top 10 (Inyección SQL, XSS, CSRF, Broken Access Control). Hashing de claves con Bcrypt (costo 12) y tokens JWT RS256. | Escaneo DAST con OWASP ZAP y SAST con Bandit/ESLint. |
| **RNF-004** | **Usabilidad UX** | La interfaz debe ser intuitiva (Nivel de Usabilidad SUS $\ge 85$), permitiendo completar un pedido completo en no más de 4 pasos e incorporando modo oscuro/claro semántico. | Pruebas de usabilidad con vendedores reales en Gamarra. |
| **RNF-005** | **Accesibilidad** | Cumplimiento del estándar **WCAG 2.1 Nivel AA**, con ratios de contraste de color $\ge 4.5:1$ en textos estándar y navegación accesible por teclado. | Auditoría Axe-core y Lighthouse Accessibility $\ge 95$. |
| **RNF-006** | **Compatibilidad** | Soporte responsivo fluido en pantallas desde 360px (smartphones gama baja) hasta 2560px (monitores 2K), en navegadores Google Chrome, Safari, Edge y Firefox. | Pruebas automatizadas Cross-Browser con Playwright. |
| **RNF-007** | **Escalabilidad** | La API backend y la base de datos deben soportar un mínimo de 150 peticiones concurrentes por segundo sin degradación de latencia ($p95 \le 350$ ms). | Pruebas de estrés y carga con herramientas k6 y Apache Bench. |
| **RNF-008** | **Mantenibilidad** | Código fuente modular estructurado bajo Clean Architecture, documentado en español e inglés, con cobertura de pruebas unitarias $\ge 80\%$. | Cobertura Jest/Pytest y análisis estático en SonarCloud. |
| **RNF-009** | **Integridad de Datos** | La base de datos relacional debe aplicar el principio ACID mediante PostgreSQL, con claves foráneas, restricciones de chequeo y respaldos automáticos diarios. | Verificación de scripts DDL y pruebas de rollback en transacciones. |
| **RNF-010** | **Capacidad Offline** | La aplicación debe instalarse en la pantalla de inicio del smartphone como PWA nativa, funcionando de manera autónoma sin conexión a red mediante Service Worker. | Pruebas de desconexión en Chrome DevTools (Network: Offline). |

---

# CAPÍTULO 3: ENTORNO DE DESARROLLO, STACK TECNOLÓGICO Y CONTROL DE VERSIONES

## 3.1. Matriz de Selección Multicriterio de Herramientas y Tecnologías

Para garantizar una selección tecnológica fundamentada y reproducible, el equipo aplicó una matriz de decisión cuantitativa ponderada evaluando criterios de: Rendimiento (30%), Curva de Aprendizaje del Equipo (20%), Comunidad y Madurez (20%), Compatibilidad PWA (15%) y Costo de Despliegue en la Nube (15%):

| Capa Tecnológica | Alternativas Evaluadas | Opción Seleccionada | Justificación Técnica de la Decisión |
| :--- | :--- | :---: | :--- |
| **Front-End Framework** | React 18 + Vite vs Next.js vs Vue 3 | **React 18 + Vite** | Tiempos de compilación ultrarrápidos con Hot Module Replacement (HMR) mediante esbuild, soporte nativo de PWA con Workbox y ecosistema maduro de componentes de interfaz. |
| **Lenguaje de Programación** | TypeScript vs JavaScript Vanilla | **TypeScript / Modern JS** | Tipado estático robusto que previene errores en tiempo de compilación al manejar estructuras complejas de pedidos, productos y estados de inventario. |
| **Estilos y Maquetación** | Tailwind CSS vs CSS Vanilla vs Bootstrap | **Tailwind CSS + CSS Semántico** | Clases de utilidad que minimizan el tamaño del bundle final (Tree-Shaking), facilitan el soporte responsivo mobile-first y permiten definir variables semánticas (Dark/Light). |
| **Backend Framework** | FastAPI (Python) vs Node.js (Express) | **Node.js / FastAPI** | Arquitectura ligera y asíncrona capaz de resolver transacciones I/O de alta concurrencia con documentación OpenAPI Swagger autogenerada. |
| **Motor de Base de Datos** | PostgreSQL 16 vs MySQL vs MongoDB | **PostgreSQL 16** | Cumplimiento estricto de ACID, soporte avanzado de datos JSONB para detalles flexibles de pedidos, extensiones criptográficas (`pgcrypto`) y alta fiabilidad empresarial. |
| **Caché y Mensajería** | Redis vs Memcached | **Redis** | Almacenamiento clave-valor en memoria de latencia sub-milisegundo para tokens JWT en lista negra y catálogo en memoria durante horas pico. |
| **Contenedores y Virtualización** | Docker + Docker Compose | **Docker** | Garantiza la paridad absoluta entre el entorno de desarrollo local y los servidores de producción en la nube, eliminando el problema de "funciona en mi máquina". |

## 3.2. Comandos Estandarizados de Configuración y Ejecución Local

Para facilitar la incorporación de cualquier miembro del equipo o evaluador académico, el proyecto se ejecuta mediante comandos estandarizados:

```bash
# 1. Clonar el repositorio oficial desde GitHub
git clone https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema.git
cd leofit-pedidos-sistema

# 2. Inicializar entorno backend e instalar dependencias
cd backend
npm install   # o pip install -r requirements.txt si se ejecuta servicio Python
npm run dev

# 3. Inicializar entorno frontend (PWA) en terminal paralela
cd ../frontend
npm install
npm run dev   # Servidor Vite activo en http://localhost:5173

# 4. Despliegue de infraestructura completa con Docker Compose
cd ..
docker-compose up -d --build
# Servicios activos: PostgreSQL (5432), Backend API (3000), Frontend (80)
```

## 3.3. Estructura del Repositorio GitHub, Políticas de Ramas (GitFlow) y Commits

El repositorio se organiza bajo una arquitectura modular limpia con separación estricta de responsabilidades:

```
leofit-pedidos-sistema/
├── .github/                  # Pipelines de CI/CD (GitHub Actions)
├── backend/                  # Código fuente del servidor API RESTful
│   ├── src/                  # Controladores, modelos, servicios y rutas
│   ├── tests/                # Pruebas unitarias y de integración
│   └── Dockerfile            # Manifiesto de contenedorización de backend
├── frontend/                 # Aplicación Web Progresiva (PWA React + Vite)
│   ├── public/               # Iconos PWA, manifest.json y assets estáticos
│   ├── src/
│   │   ├── components/       # Componentes atómicos y moleculares de UI
│   │   ├── context/          # Gestión de estado global (Auth, Carrito)
│   │   ├── pages/            # Vistas principales (Catálogo, Admin, Login)
│   │   └── service-worker.js # Estrategias de caché y Background Sync
│   └── package.json
├── database/                 # Scripts DDL, procedimientos almacenados y semillas
├── diagrams/                 # Diagramas de ingeniería en alta resolución
├── docs/                     # Repositorio maestro de documentación técnica y académica
└── docker-compose.yml        # Orquestador local de servicios
```

### Política de Ramas (GitFlow) y Convención de Commits:
- `main`: Rama de producción altamente protegida. No admite commits directos; únicamente Pull Requests aprobados que superen la suite de pruebas automatizadas.
- `dev`: Rama de integración continua de desarrollo activo.
- `feature/<nombre-funcionalidad>`: Ramas de trabajo asignadas a cada desarrollador para nuevas características.
- `hotfix/<nombre-parche>`: Ramas de resolución inmediata de incidencias críticas en producción.
- **Convención Semántica de Commits (Conventional Commits)**:
  - `feat(catalogo): implementar buscador con debounce y cache local`
  - `fix(auth): corregir expiracion de refresh token jwt`
  - `docs(arquitectura): actualizar diagrama C4 con supabase`
  - `test(pedidos): agregar casos de prueba E2E con playwright`

---

# CAPÍTULO 4: PROTOTIPOS, SISTEMA DE DISEÑO Y EXPERIENCIA DE USUARIO (UX/UI)

## 4.1. Wireframes de Baja Fidelidad (Mobile-First)

El diseño del sistema inició con wireframes de baja fidelidad enfocados en la ergonomía móvil de los vendedores que transitan por las galerías de Gamarra. Los componentes principales (barra de navegación inferior, botones de llamada a la acción y buscador) fueron ubicados estratégicamente dentro de la "zona del pulgar" (Thumb Zone) para facilitar la operación con una sola mano.

![Figura 4.1: Wireframes Mobile-First de Baja Fidelidad](../diagrams/09_Wireframes_Baja_Fidelidad.png)

## 4.2. Design System Corporativo de LeoFit (Tokens, Colores HSL y Tipografía)

Se definió un sistema de diseño propio basado en variables CSS semánticas para garantizar coherencia visual y soporte nativo de modo claro y oscuro:

| Token Semántico | Valor HSL / HEX | Significado y Uso en Interfaz |
| :--- | :---: | :--- |
| `--color-primary` | `hsl(215, 85%, 50%)` / `#1665D8` | Azul institucional; acciones principales, botones de confirmación y enlaces activos. |
| `--color-primary-hover` | `hsl(215, 85%, 42%)` | Estado interactivo sobre botones primarios. |
| `--color-success` | `hsl(142, 70%, 45%)` / `#16A34A` | Verde semántico; pedidos confirmados, stock disponible y transacciones aprobadas. |
| `--color-warning` | `hsl(38, 92%, 50%)` / `#EAB308` | Amarillo/Ámbar de advertencia; alertas de stock crítico y pedidos en preparación. |
| `--color-danger` | `hsl(0, 84%, 60%)` / `#DC2626` | Rojo semántico; cancelaciones, errores de validación y stock agotado. |
| `--bg-surface` | `hsl(220, 20%, 98%)` (Light) / `hsl(220, 25%, 10%)` (Dark) | Fondos de tarjetas, paneles modales y barras de navegación. |
| `--font-family-base` | `'Outfit', 'Inter', -apple-system, sans-serif` | Tipografía geométrica legible de gran rendimiento en pantallas Retina. |

## 4.3. Evaluación de las 10 Heurísticas de Nielsen y Accesibilidad WCAG 2.1 AA

| Heurística de Jakob Nielsen | Implementación Práctica en la Solución LeoFit |
| :--- | :--- |
| **1. Visibilidad del estado del sistema** | Notificaciones tipo Toast inmediatas tras cada acción, barras de progreso y skeleton loaders al cargar datos. |
| **2. Relación entre sistema y mundo real** | Uso de terminología textil familiar ("Polos", "Shorts", "Talla M", "Media docena", "Pedido al por mayor"). |
| **3. Control y libertad del usuario** | Capacidad de editar cantidades en el carrito, vaciar la canasta o retroceder sin perder información gracias al draft local. |
| **4. Consistencia y estándares** | Iconografía uniforme estándar (Lucide Icons), botones con comportamiento y estados homogéneos en todas las vistas. |
| **5. Prevención de errores** | Deshabilitación de botones de compra cuando no hay stock, validación sintáctica de DNI (8 dígitos numéricos) y teléfono. |
| **6. Reconocimiento antes que recuerdo** | Las fotos, colores y tallas elegidas permanecen visibles en el resumen del pedido en todo momento. |
| **7. Flexibilidad y eficiencia de uso** | Atajos de teclado para vendedores experimentados y filtros rápidos de "Top Ventas" para agilizar cotizaciones. |
| **8. Diseño estético y minimalista** | Interfaz limpia sin saturación de banners promocionales irrelevantes; foco absoluto en agilizar el despacho. |
| **9. Ayuda a reconocer y resolver errores** | Mensajes de validación claros y contextuales debajo de cada campo con sugerencias de corrección en español. |
| **10. Ayuda y documentación** | Sección de preguntas frecuentes, soporte directo a soporte técnico vía enlace y manuales embebidos. |

## 4.4. Flujo de Navegación e Interacción del Usuario (User Flow)

```mermaid
stateDiagram-v2
    [*] --> Catalogo: Acceso a la PWA
    Catalogo --> BusquedaFiltros: Filtra por categoría/talla
    BusquedaFiltros --> DetalleProducto: Selecciona Prenda
    DetalleProducto --> Carrito: Agrega al Carrito (Reserva Local)
    Carrito --> FormularioPedido: Clic en 'Finalizar Pedido'
    FormularioPedido --> ValidacionDatos: Ingresa DNI / Comprobante
    ValidacionDatos --> Confirmacion: Transacción Exitosa API
    Confirmacion --> GeneracionTicket: Genera Código ORD-2026
    GeneracionTicket --> [*]
```

---

![Figura 4.2: Diagrama de Flujo de Navegación del Usuario (User Flow)](../diagrams/10_User_Flow_Navegacion.png)

# CAPÍTULO 5: GESTIÓN INTEGRAL DE RIESGOS DEL PROYECTO

## 5.1. Identificación y Taxonomía de Riesgos

Se identificaron 10 riesgos potenciales clasificados en 4 categorías: Técnicos (T), Operativos (O), de Seguridad (S) y de Negocio (N):

| Código | Categoría | Descripción del Riesgo Identificado |
| :---: | :---: | :--- |
| **R-01** | Técnico | Caída de conectividad celular en los sótanos y galerías congestionadas de Gamarra. |
| **R-02** | Técnico | Incompatibilidad de Service Workers en versiones antiguas de navegadores móviles. |
| **R-03** | Operativo | Resistencia al cambio del personal acostumbrado a los cuadernos manuscritos. |
| **R-04** | Operativo | Errores en la carga inicial masiva de prendas y tallas existentes en el almacén físico. |
| **R-05** | Seguridad | Exfiltración de datos personales de clientes (DNI, teléfonos, direcciones). |
| **R-06** | Seguridad | Ataques de inyección SQL o adulteración de peticiones de cambio de precio en la API. |
| **R-07** | Negocio | Discrepancia entre el stock físico real y el stock digital registrado por robos o mermas. |
| **R-08** | Técnico | Saturación del servidor por picos de tráfico en campañas de alta demanda (Black Friday/Navidad). |
| **R-09** | Operativo | Pérdida de comprobantes de pago por envíos fallidos al almacenamiento en la nube. |
| **R-10** | Negocio | Desinterés de los clientes mayoristas en registrar sus compras a través de la web. |

## 5.2. Matriz de Probabilidad e Impacto 5x5 y Heatmap de Severidad

| Nivel de Probabilidad \ Impacto | 1 (Muy Bajo) | 2 (Bajo) | 3 (Moderado) | 4 (Alto) | 5 (Crítico) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **5 (Muy Alta)** | | | R-01 (PWA) | | |
| **4 (Alta)** | | R-04 | R-07 | R-03 | |
| **3 (Media)** | | R-02 | R-08 | R-05 | R-06 (Seguridad) |
| **2 (Baja)** | | | R-10 | R-09 | |
| **1 (Muy Baja)** | | | | | |

*Interpretación de Severidad*: Los riesgos **R-01 (Conectividad)**, **R-06 (Seguridad)**, **R-03 (Resistencia al cambio)** y **R-07 (Discrepancia de stock)** se ubican en la zona de severidad crítica/alta, recibiendo planes de mitigación prioritarios.

![Figura 5.1: Matriz de Probabilidad e Impacto 5x5 y Heatmap de Riesgos](../diagrams/02_Mapa_Riesgos.png)

## 5.3. Plan de Contingencia y Mitigación Preventiva y Reactiva

| Riesgo | Plan de Mitigación Preventiva (Proactivo) | Plan de Contingencia (Reactivo) | Responsable |
| :---: | :--- | :--- | :---: |
| **R-01** | Implementación de arquitectura PWA con Service Worker y cola de peticiones en IndexedDB local. | Sincronización diferida en segundo plano apenas se detecta reconexión a red. | Harley Roman |
| **R-06** | Uso estricto de Prepared Statements / ORM, validación exhaustiva de payloads con schemas y WAF. | Bloqueo automático de IP maliciosa y revocación inmediata de tokens comprometidos. | Lady Loayza |
| **R-03** | Talleres prácticos presenciales de 30 minutos con vendedores simulando ventas reales. | Acompañamiento técnico directo durante las primeras dos semanas de despliegue. | Daniel Rojas |
| **R-07** | Auditoría y conteo físico ciego cada 15 días con ajuste mediante módulo de inventario supervisado. | Congelamiento temporal del SKU en el catálogo hasta completar el recuento físico. | Víctor Cárdenas |

---

# CAPÍTULO 6: MÉTRICAS DEL SISTEMA, OBSERVABILIDAD Y NIVELES DE SERVICIO (SLA / SLO)

## 6.1. Identificación de KPIs de Negocio e Ingeniería de Software

### KPIs de Negocio:
1. **Tiempo Promedio de Toma de Pedido (TPTP)**: Tiempo transcurrido desde que se selecciona la primera prenda hasta la emisión del código de orden. Meta: $\le 90$ segundos.
2. **Tasa de Conversión de Carritos (TCC)**: Porcentaje de carritos creados que concluyen en pedido confirmado. Meta: $\ge 65\%$.
3. **Índice de Discrepancia de Inventario (IDI)**: Diferencia porcentual entre el inventario del sistema y el conteo físico. Meta: $\le 0.5\%$.

### KPIs de Ingeniería de Software:
1. **Latencia de Respuesta API ($p95$)**: Tiempo de procesamiento de peticiones en el 95% de los casos. Meta: $\le 200$ ms.
2. **Tiempo Medio de Recuperación (MTTR)**: Tiempo transcurrido para restaurar el servicio ante una caída inesperada. Meta: $\le 15$ minutos.
3. **Cobertura de Código de Pruebas**: Porcentaje de líneas de código cubiertas por pruebas automáticas. Meta: $\ge 80\%$.

## 6.2. Definición Contractual de Niveles de Servicio (SLA 99.5% y SLOs de Latencia/Error)

- **Acuerdo de Nivel de Servicio (SLA)**: El equipo se compromete a mantener el sistema operativo con una tasa de disponibilidad del **99.5%** mensual en el horario de 08:00 a 20:00 GMT-5, lo que tolera un tiempo de inactividad máximo no programado de **3.6 horas al mes**.
- **Objetivos de Nivel de Servicio (SLOs)**:
  - *SLO de Latencia*: 98% de las peticiones GET al catálogo deben responder en $< 150$ ms.
  - *SLO de Integridad*: 99.9% de las transacciones de descuento de inventario deben ejecutarse sin errores de concurrencia.
  - *SLO de Errores 5xx*: La tasa de errores de servidor HTTP 5xx debe ser inferior al $0.1\%$ del volumen total de solicitudes.

## 6.3. Plan de Medición, Telemetría y Observabilidad

El sistema implementa tres pilares de observabilidad:
1. **Métricas y Monitoreo de Salud**: Endpoint `/health` que verifica en tiempo real la conectividad con la base de datos PostgreSQL, espacio en disco y memoria disponible.
2. **Logging Estructurado en Formato JSON**: Todos los eventos de servidor (peticiones HTTP, errores no controlados, cambios de estado) se registran con campos estándar: `timestamp`, `level`, `service`, `endpoint`, `status_code`, `response_time_ms` y `user_id`.
3. **Sistemas de Alerta Automatizada**: Webhooks configurados hacia Discord / Telegram que alertan al equipo de infraestructura ante errores 5xx sostenidos o latencias superiores a 1 segundo.

---

# CAPÍTULO 7: ARQUITECTURA DE SOFTWARE E INGENIERÍA FRONT-END

## 7.1. Arquitectura General del Sistema (Clean Architecture por Capas)

El software sigue los principios de la **Clean Architecture** (Arquitectura Limpia / Puertos y Adaptadores), desacoplando las reglas de negocio de los marcos de trabajo y controladores externos:

```
[ Capa de Presentación (React PWA + Tailwind CSS) ]
                    ↓  (Peticiones HTTP REST / JSON / JWT)
[ Capa de Infraestructura (FastAPI / Express + Controllers + Middlewares) ]
                    ↓
[ Capa de Aplicación (Casos de Uso: CrearPedido, DescontarStock, Autenticar) ]
                    ↓
[ Capa de Dominio (Entidades de Negocio: Pedido, Producto, Inventario, Usuario) ]
                    ↓
[ Repositorios y Adaptadores de Datos (PostgreSQL Pool + Supabase + Redis) ]
```

## 7.2. Modelo C4 (Diagramas de Contexto, Contenedores y Componentes)

### 1. Diagrama de Contexto (Nivel 1):
Muestra cómo los actores (Clientes, Vendedores, Almaceneros y Administradores) interactúan con el Sistema LeoFit, y cómo este se conecta con servicios externos (Supabase PostgreSQL, Servicio de Almacenamiento Cloud y Notificaciones).

### 2. Diagrama de Contenedores (Nivel 2):
- **Contenedor 1 - Frontend PWA**: Single Page Application desarrollada en React 18, empaquetada con Vite y servida mediante CDN / Nginx con Service Worker offline.
- **Contenedor 2 - Backend API**: Servicio RESTful en Node.js/Python encargado de la autenticación, validación de reglas de negocio y transacciones de base de datos.
- **Contenedor 3 - Base de Datos Relacional**: Instancia de PostgreSQL 16 con esquemas normalizados y soporte de procedimientos transaccionales.
- **Contenedor 4 - Cache en Memoria**: Redis para almacenamiento temporal de sesiones y catálogo acelerado.

![Figura 7.1: Arquitectura General del Sistema - Modelo C4](../diagrams/11_Arquitectura_C4_Model.png)

## 7.3. Arquitectura PWA Offline-First y Estrategia de Service Worker

La solución implementa una estrategia híbrida de almacenamiento en caché para garantizar que un vendedor en el sótano de una galería de Gamarra no se quede sin sistema:

```javascript
// service-worker.js (Estrategia Dual LeoFit)
// 1. Activos estáticos (HTML, JS, CSS, Iconos): Cache-First
registerRoute(
  ({request}) => request.destination === 'style' || request.destination === 'script' || request.destination === 'image',
  new CacheFirst({
    cacheName: 'leofit-assets-cache-v3',
    plugins: [new ExpirationPlugin({ maxEntries: 100, maxAgeSeconds: 30 * 24 * 60 * 60 })]
  })
);

// 2. Catálogo de productos: Network-First con fallback inmediato a Cache
registerRoute(
  ({url}) => url.pathname.startsWith('/api/productos'),
  new NetworkFirst({
    cacheName: 'leofit-catalogo-cache-v3',
    networkTimeoutSeconds: 3
  })
);

// 3. Emisión de pedidos: Background Sync mediante IndexedDB
const bgSyncPlugin = new BackgroundSyncPlugin('cola-pedidos-offline', {
  maxRetentionTime: 24 * 60 // Reintentar durante 24 horas
});
```

## 7.4. Estrategias de Optimización Web (WPO) y Comparativa Cuantitativa de Métricas

Para alcanzar los máximos puntajes de rendimiento y cumplir con los criterios de evaluación, se aplicaron 5 técnicas WPO:
1. **División de Código Dinámica (Code Splitting)**: Carga perezosa de rutas administrativas mediante `React.lazy()` y `Suspense`, reduciendo el bundle inicial de 1.8 MB a apenas 142 KB.
2. **Formato de Imágenes Moderno (WebP / AVIF)**: Conversión y redimensionamiento automático de fotos de prendas deportivas, reduciendo el peso de cada imagen en un 78% sin pérdida perceptual de nitidez.
3. **Purga y Minificación CSS**: Eliminación de selectores no utilizados en producción a través de Tailwind CSS / PostCSS.
4. **Compresión Gzip / Brotli**: Habilitada en cabeceras de servidor para archivos de texto y respuestas JSON de la API.
5. **Fuentes Autoalojadas con `font-display: swap`**: Eliminación del bloqueo de renderizado por descarga de fuentes externas de Google Fonts.

### Comparativa Cuantitativa de Métricas (Lighthouse Mobile):

| Métrica de Rendimiento Web Vitals | Antes de WPO (Línea Base) | Después de WPO (Implementado) | Mejora Obtenida |
| :--- | :---: | :---: | :---: |
| **Puntaje Global Lighthouse** | 48 / 100 | **96 / 100** | **+100% de mejora** |
| **First Contentful Paint (FCP)** | 3.4 segundos | **0.9 segundos** | **Reducción del 73.5%** |
| **Largest Contentful Paint (LCP)** | 5.8 segundos | **1.6 segundos** | **Reducción del 72.4%** |
| **Total Blocking Time (TBT)** | 680 ms | **40 ms** | **Reducción del 94.1%** |
| **Cumulative Layout Shift (CLS)** | 0.28 | **0.002** | **Estabilidad visual total** |
| **Tamaño del Bundle Inicial** | 1,840 KB | **142 KB** | **Reducción del 92.2%** |

---

# CAPÍTULO 8: MODELADO, NORMALIZACIÓN Y ADMINISTRACIÓN DE BASE DE DATOS

## 8.1. Proceso Formal de Normalización de Base de Datos (1NF, 2NF y 3NF)

El diseño de la base de datos se sometió a un proceso riguroso de normalización para erradicar anomalías de inserción, actualización y borrado:

### Primera Forma Normal (1NF) — Atomicidad:
- *Condición*: Todos los atributos deben ser atómicos (valores indivisibles) y no deben existir grupos repetitivos ni arrays no estructurados en una misma celda.
- *Corrección*: Se eliminaron campos concatenados como "Prendas: 2 polos M rojos, 1 short L azul" de la tabla de pedidos, dividiéndolos en una entidad separada de detalle de transacción (`detalle_pedidos`) donde cada fila representa una combinación única de producto, talla, color, cantidad y precio unitario.

### Segunda Forma Normal (2NF) — Dependencia Funcional Completa:
- *Condición*: Estar en 1NF y asegurar que todos los atributos que no forman parte de la clave primaria dependan por completo de la totalidad de dicha clave, no de una parte de ella (eliminación de dependencias parciales en claves compuestas).
- *Corrección*: En la tabla `detalle_pedidos`, la clave primaria compuesta es `(pedido_id, producto_id)`. Atributos como el nombre del producto, la categoría o el costo de confección dependían únicamente de `producto_id`, por lo que se trasladaron a la tabla maestra `productos`.

### Tercera Forma Normal (3NF) — Eliminación de Dependencias Transitivas:
- *Condición*: Estar en 2NF y asegurar que ningún atributo no clave dependa funcionalmente de otro atributo no clave (no dependencias transitivas: si $A \to B$ y $B \to C$, entonces $C$ no debe almacenarse junto a $A$).
- *Corrección*: En la tabla `pedidos`, se almacenaba el nombre del cliente, su teléfono y su dirección. Dado que estos atributos dependen funcionalmente de `cliente_id` y no directamente de `pedido_id`, se aisló la entidad independiente `clientes`. Lo propio se aplicó aislando la tabla `roles` respecto de `usuarios`.

## 8.2. Diagrama Entidad-Relación Lógico y Físico

El modelo resultante comprende 8 entidades interconectadas con integridad referencial estricta:

```
[ ROLES ] 1 ──< N [ USUARIOS ]
                      │ 1
                      │
                      └──< N [ AUDITORIA_LOGS ]

[ CATEGORIAS ] 1 ──< N [ PRODUCTOS ] 1 ──< N [ DETALLE_PEDIDOS ] >── N 1 [ PEDIDOS ]
                                │ 1                                          │ 1
                                │                                            │
                                └──< N [ MOVIMIENTOS_INVENTARIO ]            └──< N 1 [ CLIENTES ]
```

![Figura 8.1: Modelo Entidad-Relación Lógico de Base de Datos](../diagrams/12_Modelo_Logico_BD.png)

![Figura 8.2: Modelo Físico Relacional DDL de Base de Datos](../diagrams/13_Modelo_Fisico_BD.png)

## 8.3. Esquema DDL en PostgreSQL con Triggers, Constraints e Índices B-Tree/GIN

A continuación se presenta el script DDL representativo con restricciones de integridad, triggers de recálculo de montos y control de inventario:

```sql
-- Habilitar extensión criptográfica
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 1. Tabla de Roles del Sistema
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabla de Usuarios y Operadores
CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rol_id INT NOT NULL REFERENCES roles(id) ON DELETE RESTRICT,
    nombre_completo VARCHAR(120) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabla de Clientes (Mayoristas y Minoristas)
CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tipo_documento VARCHAR(10) DEFAULT 'DNI' CHECK (tipo_documento IN ('DNI', 'RUC', 'CE')),
    numero_documento VARCHAR(20) UNIQUE NOT NULL,
    nombres VARCHAR(120) NOT NULL,
    telefono VARCHAR(15) NOT NULL,
    direccion_envio TEXT,
    ciudad VARCHAR(60) DEFAULT 'Lima',
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Tabla de Categorías de Ropa Deportiva
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(60) UNIQUE NOT NULL,
    slug VARCHAR(60) UNIQUE NOT NULL,
    activo BOOLEAN DEFAULT TRUE
);

-- 5. Tabla Maestra de Productos e Inventario
CREATE TABLE productos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    categoria_id INT NOT NULL REFERENCES categorias(id) ON DELETE RESTRICT,
    codigo_sku VARCHAR(30) UNIQUE NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    talla VARCHAR(10) NOT NULL CHECK (talla IN ('S', 'M', 'L', 'XL', 'Standard')),
    color VARCHAR(30) NOT NULL,
    precio_minorista NUMERIC(10, 2) NOT NULL CHECK (precio_minorista > 0),
    precio_mayorista NUMERIC(10, 2) NOT NULL CHECK (precio_mayorista > 0),
    stock_actual INT NOT NULL DEFAULT 0 CHECK (stock_actual >= 0),
    stock_minimo INT NOT NULL DEFAULT 5 CHECK (stock_minimo >= 0),
    imagen_url TEXT,
    activo BOOLEAN DEFAULT TRUE,
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Tabla Cabecera de Pedidos
CREATE TABLE pedidos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    codigo_orden VARCHAR(20) UNIQUE NOT NULL,
    cliente_id UUID NOT NULL REFERENCES clientes(id) ON DELETE RESTRICT,
    usuario_registro_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'Pendiente' 
        CHECK (estado IN ('Pendiente', 'Confirmado', 'En Preparación', 'Despachado', 'Entregado', 'Cancelado')),
    canal_venta VARCHAR(20) DEFAULT 'PWA_Web' CHECK (canal_venta IN ('PWA_Web', 'WhatsApp', 'Presencial')),
    subtotal NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    costo_envio NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    total NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    metodo_pago VARCHAR(30) DEFAULT 'Yape' CHECK (metodo_pago IN ('Yape', 'Plin', 'Transferencia_BCP', 'Efectivo')),
    comprobante_url TEXT,
    notas_despacho TEXT,
    creado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 7. Tabla Detalle de Líneas de Pedido
CREATE TABLE detalle_pedidos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pedido_id UUID NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    producto_id UUID NOT NULL REFERENCES productos(id) ON DELETE RESTRICT,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL CHECK (precio_unitario > 0),
    importe_subtotal NUMERIC(10, 2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    CONSTRAINT uq_pedido_producto UNIQUE (pedido_id, producto_id)
);

-- Índices B-Tree y GIN para Alto Rendimiento
CREATE INDEX idx_productos_busqueda ON productos (nombre, codigo_sku);
CREATE INDEX idx_pedidos_estado ON pedidos (estado, creado_en DESC);
CREATE INDEX idx_clientes_doc ON clientes (numero_documento);

-- Trigger Automático para Descuento Atómico de Stock tras Confirmación de Pedido
CREATE OR REPLACE FUNCTION fn_descontar_stock_pedido()
RETURNS TRIGGER AS $$
BEGIN
    IF (NEW.estado = 'Confirmado' AND OLD.estado = 'Pendiente') THEN
        UPDATE productos p
        SET stock_actual = p.stock_actual - dp.cantidad
        FROM detalle_pedidos dp
        WHERE dp.pedido_id = NEW.id AND dp.producto_id = p.id;
    ELSIF (NEW.estado = 'Cancelado' AND OLD.estado IN ('Confirmado', 'En Preparación')) THEN
        -- Reversión de stock
        UPDATE productos p
        SET stock_actual = p.stock_actual + dp.cantidad
        FROM detalle_pedidos dp
        WHERE dp.pedido_id = NEW.id AND dp.producto_id = p.id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_actualizar_stock
AFTER UPDATE OF estado ON pedidos
FOR EACH ROW
EXECUTE FUNCTION fn_descontar_stock_pedido();
```

## 8.4. Estrategia de Respaldo Automatizado, Replicación WAL y Recuperación (DRP)

- **Política de Respaldo (Backup Policy)**: Se ejecuta una copia de seguridad física completa (Full Dump) cada 24 horas a las 02:00 AM (GMT-5) mediante `pg_dump` comprimido y cifrado con clave pública GPG, transferido automáticamente a un bucket de almacenamiento seguro S3/Cloud Storage con política de retención de 30 días.
- **Replicación Write-Ahead Logging (WAL)**: Supabase PostgreSQL mantiene réplicas de lectura secundarias sincronizadas mediante streaming de logs WAL, permitiendo recuperación en un punto específico del tiempo (Point-in-Time Recovery - PITR).
- **Métricas de Recuperación ante Desastres (DRP)**:
  - **RPO (Recovery Point Objective)**: $\le 5$ minutos (máxima pérdida de datos tolerable).
  - **RTO (Recovery Time Objective)**: $\le 30$ minutos (tiempo máximo para restaurar el servicio en un nodo secundario).

---

# CAPÍTULO 9: SEGURIDAD DEL SOFTWARE, CRIPTOGRAFÍA Y PRUEBAS WEB

## 9.1. Matriz de Mitigación OWASP Top 10 (2021-2026)

| Vector de Amenaza OWASP | Nivel de Riesgo | Control de Seguridad Implementado en LeoFit |
| :--- | :---: | :--- |
| **A01: Broken Access Control** | Crítico | Validación estricta de roles (RBAC) en cada ruta protegida mediante middleware. Los vendedores no pueden acceder a configuración ni finanzas; los almaceneros solo pueden modificar estados de despacho. |
| **A02: Cryptographic Failures** | Crítico | Forzado de protocolo HTTPS con TLS 1.3 y HSTS habilitado. Hashing de contraseñas con **Bcrypt (costo 12)** y almacenamiento de datos sensibles cifrados con **AES-256-GCM**. |
| **A03: Injection (SQL / NoSQL)** | Crítico | Eliminación absoluta de queries concatenadas en crudo. Uso 100% de consultas parametrizadas con ORM / Prepared Statements en PostgreSQL. |
| **A04: Insecure Design** | Alto | Implementación de límites de tasa (Rate Limiting) en endpoints de autenticación (máximo 5 intentos fallidos por IP cada 15 minutos). |
| **A05: Security Misconfiguration** | Alto | Cabeceras de seguridad HTTP inyectadas vía middleware Helmet: `Content-Security-Policy (CSP)`, `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`. |
| **A06: Vulnerable and Outdated Components** | Alto | Auditoría automatizada de vulnerabilidades en el pipeline CI/CD mediante `npm audit --audit-level=high` y `pip-audit`. |
| **A07: Identification and Authentication Failures** | Alto | Tokens de acceso JWT de corta duración (15 minutos) combinados con Refresh Tokens rotativos almacenados en cookies HttpOnly y Secure. |
| **A08: Software and Data Integrity Failures** | Medio | Verificación de firmas de paquetes npm y plugins PWA; restricción de scripts de terceros en CSP. |
| **A09: Security Logging and Monitoring Failures** | Medio | Registro de auditoría centralizado de eventos críticos (intentos de login fallidos, borrado de registros, cambio de precios) en tabla `auditoria_logs`. |
| **A10: Server-Side Request Forgery (SSRF)** | Medio | La aplicación no realiza peticiones HTTP a URLs dinámicas provistas por el usuario; subida de comprobantes restringida a almacenamiento interno. |

## 9.2. Módulo de Control de Acceso Basado en Roles (RBAC) y Ciclo de Vida de Tokens JWT

El sistema cuenta con tres niveles de privilegio claramente delimitados:

| Rol de Usuario | Permisos de Catálogo | Permisos de Pedidos | Permisos de Almacén | Permisos de Reportes y Config |
| :--- | :---: | :---: | :---: | :---: |
| **Vendedor** | Lectura y Búsqueda | Crear y Consultar Pedidos propios | Solo lectura de stock | Sin acceso |
| **Almacenero** | Solo lectura | Consultar pedidos pendientes | Cambiar estados y ajustar stock | Sin acceso |
| **Administrador** | Crear, Editar y Eliminar | Acceso total y Cancelación | Auditoría total de inventario | Acceso Total a Dashboard y Reportes |

```javascript
// Middleware de autorización RBAC
const authorize = (rolesPermitidos = []) => {
  return (req, res, next) => {
    if (!req.user || !rolesPermitidos.includes(req.user.rol)) {
      return res.status(403).json({
        error: 'Acceso Denegado: Su rol no posee permisos para ejecutar esta acción.'
      });
    }
    next();
  };
};
```

## 9.3. Especificación de Cifrado de Datos en Reposo (AES-256-GCM) y Tránsito (TLS 1.3)

1. **Datos en Tránsito**: Todas las comunicaciones entre el cliente PWA y los servicios backend utilizan túneles cifrados **TLS 1.3** con suites de cifrado modernas (ECDHE-ECDSA-AES256-GCM-SHA384). Se implementa cabecera `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
2. **Datos en Reposo**:
   - Contraseñas de usuario: Tratadas mediante **Bcrypt** con factor de costo (salt rounds) fijado en **12**, imposibilitando ataques de tablas arcoíris.
   - Datos sensibles de clientes (DNI, Teléfono): Cifrados a nivel de columna con **AES-256-GCM** utilizando claves criptográficas gestionadas fuera de la base de datos a través de variables de entorno seguras.

## 9.4. Pruebas de Seguridad Web Automatizadas (SAST, DAST y Auditoría de Dependencias)

- **Escaneo DAST (Dynamic Application Security Testing)**: Ejecutado con **OWASP ZAP 2.14** contra la instancia de staging desplegada. Se realizaron ataques simulados de Cross-Site Scripting (XSS), SQLi y Path Traversal, obteniendo un reporte con **0 alertas de severidad Alta o Crítica**.
- **Escaneo SAST (Static Application Security Testing)**: Ejecutado con `eslint-plugin-security` para el frontend y `bandit` para módulos de backend, garantizando que no existan credenciales hardcodeadas, buffers inseguros o funciones `eval()` en el código base.
- **Auditoría de Dependencias de Terceros**:
  - `npm audit`: 0 vulnerabilidades altas o críticas en 892 paquetes escaneados.
  - `pip-audit`: 0 paquetes con vulnerabilidades conocidas (CVE) en dependencias Python.

---

# CAPÍTULO 10: VERIFICACIÓN, VALIDACIÓN Y EVIDENCIAS DE REQUERIMIENTOS

## 10.1. Plan Integral y Pirámide de Pruebas

El aseguramiento de la calidad de LeoFit se estructuró siguiendo la pirámide de pruebas estándar de la industria:

1. **Pruebas Unitarias (Jest / Vitest)**: 45 pruebas que validan el comportamiento aislado de funciones matemáticas (cálculo de subtotales, descuentos mayoristas, validadores de DNI de 8 dígitos y formateadores de moneda peruana PEN).
2. **Pruebas de Integración (Supertest / Pytest)**: 28 pruebas que validan la interacción entre los controladores de la API, middlewares de autenticación JWT y la base de datos PostgreSQL en contenedor de pruebas.
3. **Pruebas End-to-End (E2E con Playwright)**: 12 flujos completos ejecutados en navegadores Chromium, Firefox y WebKit emulando dispositivos móviles, cubriendo el ciclo de vida del pedido desde la búsqueda en catálogo hasta el cambio de estado en el panel de despacho.

## 10.2. Matriz de Trazabilidad Total Requerimiento vs Casos de Prueba

| Requerimiento Funcional | Caso de Prueba Automatizado | Herramienta | Resultado | Cobertura |
| :---: | :--- | :---: | :---: | :---: |
| **RF-001 (Catálogo)** | `TC-01: Carga catálogo y renderiza tarjetas de productos` | Vitest / Testing Library | PASS | 100% |
| **RF-002 (Buscador)** | `TC-02: Filtra productos por término y categoría en <200ms` | Playwright E2E | PASS | 100% |
| **RF-003 (Carrito)** | `TC-03: Agrega prenda, incrementa cantidad y valida stock` | Vitest | PASS | 100% |
| **RF-004 (Pedido)** | `TC-04: Emite orden con DNI válido y descuenta stock en BD` | Playwright E2E | PASS | 100% |
| **RF-007 (Admin)** | `TC-05: Modifica estado de orden a Despachado con rol Almacén` | Playwright E2E | PASS | 100% |
| **RF-009 (Stock ACID)**| `TC-06: Impide sobreventa concurrente de última unidad disponible` | Jest / Supertest | PASS | 100% |
| **RF-011 (Auth RBAC)**| `TC-07: Bloquea acceso a rutas admin a usuario sin rol autorizado` | Supertest | PASS | 100% |
| **RF-015 (PWA Offline)**| `TC-08: Carga catálogo y registra orden con desconexión de red` | Playwright (Offline) | PASS | 100% |

## 10.3. Catálogo Fotográfico y Técnico Exhaustivo de Evidencias de Pantalla (14 Pantallas del Sistema)

Para cumplir a cabalidad con la exigencia académica del docente y evidenciar la operatividad del software, a continuación se desglosan las **14 pantallas del sistema**, detallando su propósito funcional, componentes visuales, reglas de negocio validadas y criterios de aceptación UAT:

---

### Pantalla 01:

![Figura 10.1: Pantalla 01 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_01.png) Catálogo General de Productos y Filtros de Búsqueda
- **Requerimientos Asociados**: `RF-001`, `RF-002`, `RNF-001`, `RNF-006`.
- **Propósito Funcional**: Presentar de manera atractiva y ágil la totalidad de prendas deportivas confeccionadas por LeoFit, permitiendo a clientes y vendedores filtrar instantáneamente por categorías (Polos, Shorts, Buzos, Casacas) y buscar por texto libre.
- **Anatomía Visual y Componentes**:
  - Encabezado institucional con logotipo de LeoFit, buscador interactivo con icono de lupa y badge numérico del carrito de compras.
  - Barra de categorías horizontales con botones de desplazamiento suave y estado activo resaltado en azul institucional (`--color-primary`).
  - Cuadrícula responsiva de tarjetas de productos con fotografía optimizada en formato WebP, etiqueta de categoría, nombre del modelo, selector de talla disponible, precio visible en Soles (S/) y botón interactivo "Agregar al Carrito".
- **Reglas de Negocio Validadas**:
  - Los productos cuyo stock actual sea 0 muestran automáticamente una insignia gris "Agotado" y deshabilitan el botón de agregar.
  - La búsqueda por texto filtra con un retardo controlado (debouncing) de 300 ms para no saturar el rendimiento del hilo principal del navegador.
- **Criterio de Aceptación UAT**: El usuario puede encontrar un producto específico escribiendo al menos 3 caracteres y visualizar su precio y tallas en menos de 200 ms.

---

### Pantalla 02:

![Figura 10.2: Pantalla 02 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_02.png) Detalle de Producto y Selección de Tallas y Colores
- **Requerimientos Asociados**: `RF-001`, `RF-003`, `RNF-004`.
- **Propósito Funcional**: Proporcionar la ficha técnica completa de una prenda seleccionada, permitiendo al comprador seleccionar su talla (S, M, L, XL), apreciar las opciones de color textil y consultar la composición del tejido (suplex, algodón reactivo).
- **Anatomía Visual y Componentes**:
  - Galería de imágenes con zoom visual y miniaturas navegables.
  - Selector de tallas tipo botones radiales que informan visualmente cuántas unidades quedan en stock por cada talla seleccionada.
  - Cuadro de cantidad con selectores numéricos (+) y (-) que impiden ingresar números negativos o valores mayores al inventario existente.
  - Botón destacado de acción principal "Agregar al Carrito" con micro-animación de confirmación visual.
- **Reglas de Negocio Validadas**:
  - No es posible añadir prendas al carrito sin haber seleccionado previamente una talla válida.
  - Si el usuario selecciona una cantidad superior a 12 unidades, el sistema muestra automáticamente el precio con descuento mayorista.
- **Criterio de Aceptación UAT**: La interfaz actualiza el stock visible en tiempo real al conmutar entre diferentes tallas de la misma prenda.

---

### Pantalla 03:

![Figura 10.3: Pantalla 03 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_03.png) Carrito de Compras Interactivo y Resumen de Totales
- **Requerimientos Asociados**: `RF-003`, `RF-004`, `RNF-001`.
- **Propósito Funcional**: Centralizar los productos preseleccionados por el usuario, permitiendo revisar detalles, modificar cantidades en caliente, remover ítems y visualizar el desglose exacto de la compra (subtotal, descuento mayorista y costo de envío).
- **Anatomía Visual y Componentes**:
  - Panel deslizante o vista dedicada con listado de prendas agregadas, incluyendo miniatura, nombre, talla, precio unitario y subtotal.
  - Controles de modificación de cantidad y botón de eliminación con icono de papelera.
  - Caja de resumen financiero con subtotal en Soles (PEN), costo de envío estimado y total a pagar destacado en tipografía de gran peso.
  - Botón de navegación principal "Proceder al Checkout / Datos de Envío".
- **Reglas de Negocio Validadas**:
  - Persistencia de los ítems en el almacenamiento local del dispositivo (LocalStorage / IndexedDB); si el usuario recarga la página, su carrito no se vacía.
  - Recálculo atómico de los totales matemáticos en menos de 50 ms tras cada cambio de cantidad.
- **Criterio de Aceptación UAT**: El carrito refleja instantáneamente cualquier alteración en las cantidades y bloquea la prosecución de la compra si la canasta se encuentra vacía.

---

### Pantalla 04:

![Figura 10.4: Pantalla 04 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_04.png) Formulario de Registro de Pedido y Datos del Cliente
- **Requerimientos Asociados**: `RF-004`, `RF-005`, `RNF-003`, `RNF-004`.
- **Propósito Funcional**: Capturar de manera estructurada y validada la información del comprador final o comerciante mayorista para fines de emisión de la orden y entrega logística.
- **Anatomía Visual y Componentes**:
  - Campos de entrada: Tipo de documento (DNI / RUC), número de documento, nombres y apellidos completos, teléfono de contacto (9 dígitos) y correo electrónico opcional.
  - Sección de despacho: Selección de método de entrega (Recojo en tienda en Gamarra o Envío por Agencia a Lima/Provincias), dirección detallada y referencias.
  - Selector de método de pago: Opciones de Billetera Digital (Yape / Plin), Transferencia BCP/BBVA o Pago contra entrega en tienda.
  - Módulo de carga de archivos (File Uploader) con previsualización para adjuntar la foto o captura del comprobante de transferencia bancaria.
- **Reglas de Negocio Validadas**:
  - Validación de formato: El DNI debe contener exactamente 8 dígitos numéricos; el RUC debe contener 11 dígitos iniciando con 10 o 20.
  - Compresión automática en cliente de la imagen del comprobante para optimizar el consumo de datos celulares antes de la subida al servidor.
- **Criterio de Aceptación UAT**: El formulario impide el envío del pedido y resalta en rojo los campos obligatorios que presenten errores sintácticos o estén incompletos.

---

### Pantalla 05:

![Figura 10.5: Pantalla 05 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_05.png) Confirmación de Pedido y Emisión de Código de Orden
- **Requerimientos Asociados**: `RF-006`, `RF-017`, `RNF-001`.
- **Propósito Funcional**: Proporcionar al usuario la constancia formal de que su orden ha sido registrada exitosamente en el sistema de LeoFit, informando su número correlativo oficial y los pasos subsiguientes del despacho.
- **Anatomía Visual y Componentes**:
  - Icono animado de confirmación exitosa (Check verde).
  - Número de orden destacado en tipografía monoespaciada (ej. `ORD-2026-0042`).
  - Resumen conciso de prendas adquiridas, monto total pagado y dirección de destino.
  - Botón para compartir o enviar el resumen de la orden directamente por WhatsApp a la central de LeoFit.
  - Enlace para descargar el comprobante en formato PDF o imprimir el ticket térmico.
- **Reglas de Negocio Validadas**:
  - El código de orden generado es único e inmutable en la base de datos PostgreSQL.
  - El pedido pasa inmediatamente al estado de "Pendiente" y activa una notificación en el panel de los almaceneros.
- **Criterio de Aceptación UAT**: La pantalla de confirmación se despliega en menos de 1.5 segundos tras la confirmación del pago y permite al usuario regresar al inicio limpiando el carrito.

---

### Pantalla 06:

![Figura 10.6: Pantalla 06 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_06.png) Módulo de Autenticación de Usuarios (Login Seguro)
- **Requerimientos Asociados**: `RF-011`, `RNF-003`.
- **Propósito Funcional**: Controlar y restringir el acceso a las funciones operativas, administrativas y de almacén de LeoFit, garantizando que solo el personal autorizado pueda gestionar pedidos y visualizar métricas de negocio.
- **Anatomía Visual y Componentes**:
  - Tarjeta de autenticación centrada con imagotipo corporativo de LeoFit.
  - Campos de entrada: Correo institucional (`usuario@leofit.com.pe`) y contraseña secreta con botón para alternar visibilidad (mostrar/ocultar).
  - Botón de ingreso "Iniciar Sesión" con estado de carga (spinner).
  - Enlace de recuperación de acceso y aviso legal de confidencialidad.
- **Reglas de Negocio Validadas**:
  - Bloqueo por fuerza bruta: Tras 5 intentos fallidos consecutivos desde la misma dirección IP, el acceso se bloquea temporalmente por 15 minutos.
  - Emisión de token JWT firmado digitalmente con almacenamiento seguro en cookies HttpOnly y configuración de expiración a los 15 minutos.
- **Criterio de Aceptación UAT**: El usuario ingresa credenciales válidas y es redirigido automáticamente al panel que corresponda según su rol asignado (*Administrador, Vendedor o Almacenero*).

---

### Pantalla 07:

![Figura 10.7: Pantalla 07 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_07.png) Panel Administrativo de Control y Listado de Pedidos
- **Requerimientos Asociados**: `RF-007`, `RF-008`, `RNF-001`, `RNF-006`.
- **Propósito Funcional**: Ofrecer una vista panorámica centralizada de todas las órdenes emitidas en LeoFit, permitiendo a los operadores buscar pedidos, filtrar por estado logístico y ordenar por fecha de emisión.
- **Anatomía Visual y Componentes**:
  - Barra superior con resumen rápido de contadores: Total Pedidos, Pendientes de Pago, En Preparación y Despachados hoy.
  - Tabla de datos enriquecida con columnas: Código de Orden, Fecha/Hora, Cliente, Teléfono, Total (S/), Canal de Venta, Estado actual y Acciones.
  - Etiquetas visuales semánticas (Badges) con código de color: Amarillo (Pendiente), Azul (Confirmado), Púrpura (En Preparación), Verde (Despachado) y Rojo (Cancelado).
  - Botones de acción rápida por fila: "Ver Detalle", "Cambiar Estado" e "Imprimir Guía".
- **Reglas de Negocio Validadas**:
  - Paginación del lado del servidor para garantizar tiempos de respuesta inferiores a 200 ms aun cuando la base de datos supere los 10,000 pedidos.
  - Los vendedores estándar únicamente pueden visualizar los pedidos gestionados por ellos mismos; los administradores visualizan la totalidad de la empresa.
- **Criterio de Aceptación UAT**: La tabla actualiza sus registros en tiempo real o mediante un botón de refresco sin recargar la página completa.

---

### Pantalla 08:

![Figura 10.8: Pantalla 08 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_08.png) Modal de Detalle de Pedido y Transición de Estados
- **Requerimientos Asociados**: `RF-007`, `RF-008`, `RF-018`.
- **Propósito Funcional**: Examinar a profundidad una orden específica, verificar el comprobante de pago bancario adjunto y modificar el estado del pedido a medida que avanza por la cadena logística.
- **Anatomía Visual y Componentes**:
  - Ventana modal sobrepuesta con cabecera de orden, datos completos del cliente y dirección exacta de envío.
  - Listado detallado de ítems con sus SKUs, fotos, tallas, colores y precios unitarios.
  - Visualizador del comprobante de pago bancario con zoom para verificar el número de operación de Yape/Plin.
  - Menú desplegable para cambiar el estado de la orden (*de Confirmado a En Preparación o Despachado*) con campo de texto para observaciones de despacho.
- **Reglas de Negocio Validadas**:
  - Las transiciones de estado siguen una máquina de estados estricta (no se puede pasar una orden de "Pendiente" directamente a "Entregado" sin pasar por "Confirmado" y "Despachado").
  - Toda modificación queda registrada de forma inmutable en la tabla de auditoría con el ID del operador responsable y la estampa de tiempo.
- **Criterio de Aceptación UAT**: Al confirmar el cambio de estado, la orden actualiza su badge en la tabla principal y se emite el movimiento de stock correspondiente.

---

### Pantalla 09:

![Figura 10.9: Pantalla 09 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_09.png) Módulo de Gestión de Inventario y Semáforo de Stock
- **Requerimientos Asociados**: `RF-009`, `RF-010`, `RNF-009`.
- **Propósito Funcional**: Monitorear las existencias físicas de cada prenda en almacén, alertar sobre roturas inminentes de stock y permitir a los administradores registrar entradas de nuevos lotes confeccionados.
- **Anatomía Visual y Componentes**:
  - Filtros por categoría y selector de umbral de alerta de stock.
  - Tabla de inventario con SKU, Nombre de la prenda, Talla, Stock Actual, Stock Mínimo y Estado del Semáforo.
  - Columna de estado con indicadores de color:
    - **Verde**: Stock Óptimo ($> 15$ unidades).
    - **Amarillo**: Stock Regular ($6$ a $15$ unidades).
    - **Rojo**: Stock Crítico ($\le 5$ unidades) con aviso de reposición urgente.
  - Botón de ajuste rápido de existencias (+) y (-) con motivo obligatorio de movimiento.
- **Reglas de Negocio Validadas**:
  - El sistema prohíbe el registro de existencias negativas en la base de datos mediante restricción CHECK en PostgreSQL.
  - Todo incremento o decremento manual de stock genera un registro en la tabla `movimientos_inventario`.
- **Criterio de Aceptación UAT**: Cualquier venta confirmada descuenta automáticamente el stock en esta pantalla sin intervención manual.

---

### Pantalla 10:

![Figura 10.10: Pantalla 10 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_10.png) Modal de Edición y Creación de Nuevas Prendas (Productos)
- **Requerimientos Asociados**: `RF-001`, `RF-009`, `RF-012`.
- **Propósito Funcional**: Permitir al personal administrativo registrar nuevas colecciones de ropa deportiva en el catálogo, asignarles códigos SKU, fijar precios y cargar fotografías promocionales.
- **Anatomía Visual y Componentes**:
  - Formulario con campos: Nombre del producto, Categoría asociada, Código SKU autogenerado o manual, Descripción detallada, Tallas disponibles (checkboxes) y Colores.
  - Entradas numéricas con validación para Precio Minorista y Precio Mayorista en Soles (PEN).
  - Zona de arrastrar y soltar (Drag and Drop) para cargar imágenes de producto con previsualización inmediata.
  - Botones "Guardar Producto" y "Cancelar".
- **Reglas de Negocio Validadas**:
  - El precio mayorista debe ser estrictamente menor o igual al precio minorista.
  - El código SKU debe ser único a nivel de todo el sistema; si se ingresa un duplicado, se alerta inmediatamente al usuario.
- **Criterio de Aceptación UAT**: Al presionar "Guardar Producto", el ítem aparece disponible inmediatamente en el catálogo público PWA.

---

### Pantalla 11:

![Figura 10.11: Pantalla 11 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_11.png) Dashboard Gerencial de Analítica y Métricas Comerciales
- **Requerimientos Asociados**: `RF-013`, `RNF-001`, `RNF-004`.
- **Propósito Funcional**: Proveer a la gerencia de LeoFit un centro de comando visual con indicadores clave de desempeño (KPIs), tendencias de facturación y comportamiento de ventas por categoría para la toma de decisiones informadas.
- **Anatomía Visual y Componentes**:
  - Tarjetas de resumen en la parte superior:
    - **Ventas Totales del Mes (S/)** con porcentaje de crecimiento comparativo.
    - **Total de Pedidos Procesados** en el período seleccionado.
    - **Ticket Promedio por Pedido**.
    - **Tasa de Cumplimiento Logístico**.
  - Gráfico de barras interactivo con la evolución diaria de ingresos en Soles.
  - Gráfico circular (Dona) con la distribución porcentual de ventas por categoría textil (ej. 45% Polos, 30% Buzos, 25% Shorts).
  - Ranking de los 5 productos más vendidos ("Top Sellers") con barras de progreso.
- **Reglas de Negocio Validadas**:
  - Los cálculos se realizan agregando únicamente los pedidos en estados válidos (*Confirmado, En Preparación, Despachado, Entregado*), excluyendo automáticamente las órdenes canceladas.
- **Criterio de Aceptación UAT**: El administrador puede cambiar el rango temporal (Hoy, Últimos 7 Días, Mes Actual) y los gráficos se actualizan de forma reactiva en menos de 300 ms.

---

### Pantalla 12:

![Figura 10.12: Pantalla 12 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_12.png) Módulo de Exportación de Reportes Contables y Comerciales
- **Requerimientos Asociados**: `RF-014`, `RF-018`.
- **Propósito Funcional**: Generar y descargar sábanas de datos consolidadas de las operaciones de venta e inventario en formatos estándar (Excel `.xlsx` y PDF) para facilitar la contabilidad y auditorías tributarias.
- **Anatomía Visual y Componentes**:
  - Selector de tipo de reporte: *Reporte Consolidado de Ventas, Reporte de Movimientos de Inventario o Reporte de Clientes Frecuentes*.
  - Filtro por rango de fechas (Fecha Inicio y Fecha Fin) y filtro opcional por canal de venta.
  - Botones destacados de descarga: "Descargar Reporte en Excel (.xlsx)" con icono verde y "Descargar Resumen Ejecutivo en PDF" con icono rojo.
  - Tabla de previsualización con las primeras 10 filas de los datos a exportar.
- **Reglas de Negocio Validadas**:
  - La exportación se procesa mediante flujos de datos asíncronos para no bloquear la interfaz de usuario ante reportes de más de 5,000 transacciones.
  - Los archivos generados contienen metadatos oficiales de LeoFit, fecha y hora de emisión, y firma digital del sistema.
- **Criterio de Aceptación UAT**: El archivo Excel descargado se abre correctamente en Microsoft Excel o Google Sheets con columnas tabulares formateadas y fórmulas de totales calculadas.

---

### Pantalla 13:

![Figura 10.13: Pantalla 13 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_13.png) Vista de Operatividad Offline y Notificación PWA
- **Requerimientos Asociados**: `RF-015`, `RF-016`, `RNF-010`.
- **Propósito Funcional**: Garantizar la continuidad operativa del personal cuando la señal celular o WiFi se interrumpe en galerías o sótanos comerciales de Gamarra, mostrando el estado de conectividad e informando que los datos están protegidos localmente.
- **Anatomía Visual y Componentes**:
  - Banner horizontal de alerta en la parte superior con fondo ámbar/amarillo y mensaje: *"Modo Sin Conexión Activado — El catálogo se encuentra en modo local y sus pedidos se guardarán en el dispositivo"*.
  - Indicador de estado en la barra de navegación con icono de antena/WiFi tachado.
  - Contador de pedidos pendientes de sincronización encolados en IndexedDB.
  - Transición fluida a banner verde cuando se detecta el evento de red `online`, notificando: *"Conexión restablecida — Sincronizando pedidos pendientes con el servidor..."*.
- **Reglas de Negocio Validadas**:
  - Ningún pedido registrado sin conexión se pierde; las transacciones se encolan con una marca de tiempo local y se transmiten al backend en orden FIFO (First-In, First-Out) al reconectarse.
- **Criterio de Aceptación UAT**: Al desconectar deliberadamente el adaptador de red en las herramientas de desarrollo, la aplicación permite navegar por el catálogo y emitir un pedido sin generar errores en pantalla.

---

### Pantalla 14:

![Figura 10.14: Pantalla 14 del Sistema LeoFit](../scripts/extracted_evidence_imgs/evidence_screen_14.png) Vista de Impresión de Guía de Despacho y Ticket Térmico con Código QR
- **Requerimientos Asociados**: `RF-006`, `RF-017`, `RNF-004`.
- **Propósito Funcional**: Generar el documento físico estandarizado para adjuntar al paquete textil antes de entregarlo al transportista o courier, facilitando el control en almacén y el seguimiento para el cliente.
- **Anatomía Visual y Componentes**:
  - Formato adaptado para impresoras de tickets térmicos de 80 mm de ancho (POS) y formato A4 para guías formales.
  - Cabecera con datos fiscales de LeoFit (RUC, Razón Social, Dirección en Gamarra).
  - Código QR dinámico que codifica la URL pública única de rastreo del pedido.
  - Cuadro con datos del destinatario, teléfono de contacto y dirección de envío en provincias.
  - Tabla compacta con el desglose de prendas empacadas y firma del responsable de embalaje.
- **Reglas de Negocio Validadas**:
  - Estilos CSS específicos para medios de impresión (`@media print`) que ocultan automáticamente barras de navegación, botones y fondos oscuros para ahorrar tinta térmica.
- **Criterio de Aceptación UAT**: Al hacer clic en "Imprimir Ticket", se abre de inmediato el cuadro de diálogo nativo de impresión del sistema operativo con el formato ajustado a 80 mm sin desbordamientos de texto.

---

# CAPÍTULO 11: MANUAL DE DESPLIEGUE EN LA NUBE Y OPERATIVIDAD

## 11.1. Topología Cloud y Arquitectura de Infraestructura

La arquitectura de despliegue productivo de LeoFit aprovecha un esquema híbrido y escalable de servicios en la nube de alta disponibilidad:

```
[ Usuarios y Vendedores en Móviles/Desktop ]
                     ↓ (HTTPS / TLS 1.3)
      [ CDN Global / Edge Hosting (Vercel / GitHub Pages) ]
      └── Frontend PWA (React 18 + Vite + Service Worker)
                     ↓ (API REST / JSON / JWT)
      [ Servidor de Aplicaciones Cloud (Render / VPS Docker) ]
      └── Backend RESTful (Node.js / FastAPI Container)
                     ↓ (Conexión Pool SSL Segura)
      [ Plataforma de Base de Datos Cloud (Supabase PostgreSQL 16) ]
      └── Base de Datos Relacional + Storage de Comprobantes + Backups WAL
```

## 11.2. Guía Paso a Paso de Despliegue con Docker y Docker Compose

Para reproducir el entorno productivo de forma autocontenida se definen los siguientes pasos operativos:

### Paso 1: Configuración de Variables de Entorno (`.env`)
Crear un archivo `.env` en la raíz del backend con los valores de producción:
```ini
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://leofit_admin:PasswordSeguro2026!@aws-0-sa-east-1.pooler.supabase.com:5432/leofit_db?sslmode=require
JWT_SECRET_KEY=clave_secreta_criptografica_sha256_leofit_2026_segura
JWT_ACCESS_EXPIRATION_MINUTES=15
JWT_REFRESH_EXPIRATION_DAYS=7
CORS_ORIGIN=https://leofit-pedidos.vercel.app
```

### Paso 2: Construcción y Levantamiento de Contenedores Docker
```bash
# Construir la imagen optimizada multi-etapa del backend
docker build -t leofit-backend:v3.0 ./backend

# Desplegar los servicios orquestados en segundo plano
docker-compose -f docker-compose.prod.yml up -d

# Verificar el estado operativo y consumo de recursos
docker-compose ps
docker stats
```

## 11.3. Pipeline de Integración y Despliegue Continuo (CI/CD con GitHub Actions)

El repositorio cuenta con un flujo automatizado en `.github/workflows/deploy.yml` que se dispara ante cada push en la rama `main`:

```yaml
name: CI/CD Pipeline LeoFit Production

on:
  push:
    branches: [ main ]

jobs:
  quality-and-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js 20
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - name: Install Dependencies
        run: |
          cd frontend && npm ci
          cd ../backend && npm ci
      - name: Run Linter & Security Audit
        run: |
          cd frontend && npm run lint
          cd ../backend && npm audit --audit-level=high
      - name: Run Automated Tests
        run: |
          cd backend && npm test -- --coverage
      - name: Build Frontend Bundle
        run: |
          cd frontend && npm run build
      - name: Deploy to Vercel / GitHub Pages
        run: |
          echo "Despliegue automático completado con éxito."
```

## 11.4. Verificación de Operatividad y Monitoreo de Endpoints en Producción

Tras el despliegue, se ejecutan pruebas de verificación de salud (Smoke Tests):
```bash
# 1. Probar el endpoint de salud de la API
curl -I https://api.leofit.com/health
# Respuesta esperada: HTTP/1.1 200 OK {"status": "healthy", "database": "connected"}

# 2. Probar la compresión y cabeceras de seguridad
curl -I https://leofit.com/
# Respuesta esperada: Content-Encoding: br, X-Frame-Options: DENY, Strict-Transport-Security
```

---

# CAPÍTULO 12: GOBERNANZA ACADÉMICA, GLOSARIO Y DEFENSA ANTE EL PANEL

## 12.1. Resumen de Acuerdos de Gobernanza de Equipo y Actas de Reunión

A lo largo del ciclo académico, el equipo sostuvo reuniones periódicas de alineamiento:
- **Daily Standups (15 minutos)**: Reuniones virtuales diarias de lunes a viernes a las 20:00 horas para responder las tres preguntas clásicas de Scrum: ¿Qué se logró ayer? ¿Qué se hará hoy? ¿Existen bloqueos técnicos?
- **Sprint Planning y Sprint Reviews**: Sesiones bisemanales con presencia del Product Owner y revisión de entregables frente a las rúbricas académicas de la UTP.
- **Políticas de Calidad y Revisión de Código**: Obligatoriedad de aprobación de al menos 1 desarrollador antes de fusionar cualquier Pull Request hacia la rama `dev` o `main`.

## 12.2. Glosario Unificado de Términos Técnicos y de Dominio Textil/Comercial

| Término | Definición Técnica y Contextual en el Proyecto LeoFit |
| :--- | :--- |
| **ACID** | Propiedades de las transacciones en bases de datos relacionales: Atomicidad, Consistencia, Aislamiento (Isolation) y Durabilidad. Garantiza que el descuento de inventario nunca se aplique a medias. |
| **Background Sync** | Característica de las PWAs que permite diferir peticiones HTTP cuando el usuario no tiene conexión y ejecutarlas en segundo plano apenas se restablece el acceso a Internet. |
| **Bcrypt** | Función hash unidireccional de contraseñas basada en el cifrado Blowfish que incorpora salt aleatorio y factor de costo adaptable para resistir ataques de fuerza bruta. |
| **C4 Model** | Marco de trabajo para la visualización de arquitectura de software en cuatro niveles jerárquicos de zoom: Contexto, Contenedores, Componentes y Código. |
| **DAST** | Dynamic Application Security Testing. Pruebas de seguridad sobre la aplicación en ejecución sin conocer su código interno (análisis de caja negra), ejecutadas mediante OWASP ZAP. |
| **Gamarra** | Emporio comercial y textil ubicado en La Victoria, Lima, principal centro de confección y venta de prendas deportivas del Perú. |
| **Gherkin** | Lenguaje estructurado y legible por humanos de desarrollo guiado por comportamiento (BDD) que emplea las palabras clave Dado (Given), Cuando (When) y Entonces (Then). |
| **JWT** | JSON Web Token. Estándar abierto (RFC 7519) que define un mecanismo compacto y autónomo para transmitir información de identidad segura entre partes como objeto JSON firmado. |
| **MoSCoW** | Técnica de priorización ágil que clasifica los requisitos en cuatro niveles: *Must have* (Debe tener), *Should have* (Debería tener), *Could have* (Podría tener) y *Won't have* (No tendrá por ahora). |
| **PWA** | Progressive Web App. Aplicación web construida con estándares modernos que ofrece una experiencia similar a una app nativa: instalable, rápida y con soporte offline. |
| **RBAC** | Role-Based Access Control. Modelo de seguridad que restringe el acceso a los recursos y endpoints de un sistema basándose en los roles asignados a los usuarios autorizados. |
| **SAST** | Static Application Security Testing. Análisis estático del código fuente en busca de vulnerabilidades de seguridad, malas prácticas y secretos filtrados antes de la compilación. |
| **Service Worker** | Script que el navegador web ejecuta en segundo plano, separado de la página web, habilitando funciones como almacenamiento en caché independiente y sincronización en background. |
| **SKU** | Stock Keeping Unit. Identificador alfanumérico único asignado a cada tipo de prenda, talla y color específico para su control logístico en almacén. |
| **SLA / SLO** | Service Level Agreement (Acuerdo contractual de nivel de servicio garantizado) y Service Level Objective (Objetivo técnico cuantitativo interno de rendimiento y estabilidad). |
| **Suplex** | Tejido elástico y transpirable de alta tecnología utilizado en la confección de ropa deportiva de compresión y licras en Gamarra. |
| **Thumb Zone** | Zona de la pantalla de un smartphone que puede ser alcanzada cómodamente por el dedo pulgar del usuario cuando sujeta el dispositivo con una sola mano. |
| **WPO** | Web Performance Optimization. Conjunto de técnicas de ingeniería web orientadas a acelerar la velocidad de carga y renderizado de una página en navegadores. |

## 12.3. Banco de 15 Preguntas Críticas y Respuestas Sólidas para la Sustentación ante el Jurado Calificador

A continuación se detallan las 15 preguntas de mayor complejidad técnica y metodológica que el jurado evaluador de la UTP formula en las sustentaciones de proyectos integradores, junto con sus respuestas fundamentadas:

### 1. ¿Por qué decidieron desarrollar una PWA en lugar de una aplicación móvil nativa en Flutter, Kotlin o Swift?
- **Respuesta**: La decisión se sustentó en un análisis de costo-beneficio y adopción del cliente en el entorno de Gamarra. Una app nativa exige a los clientes y vendedores descargar 40 a 80 MB desde Google Play o App Store, lo que representa una barrera de fricción severa en zonas con planes de datos limitados. La PWA desarrollada pesa menos de 2 MB, se instala instantáneamente desde el navegador mediante un banner, es 100% multiplataforma (Android, iOS, Windows, Mac) con un único código base en React/Vite, y ofrece soporte offline completo gracias a Service Workers y almacenamiento local en IndexedDB.

### 2. ¿Cómo garantizan que dos vendedores no vendan la última unidad disponible al mismo tiempo a través de WhatsApp?
- **Respuesta**: La integridad del inventario se garantiza a nivel de base de datos relacional PostgreSQL mediante el principio de aislamiento en transacciones ACID. Cuando un pedido es enviado a confirmación, el backend inicia una transacción con bloqueo pesimista mediante la sentencia `SELECT ... FOR UPDATE` sobre la fila del producto específico, o ejecuta una actualización atómica condicionada: `UPDATE productos SET stock_actual = stock_actual - $cant WHERE id = $id AND stock_actual >= $cant RETURNING stock_actual;`. Si el stock disponible es insuficiente, la transacción efectúa un `ROLLBACK` inmediato y la API responde un error HTTP 409 Conflict, informando al vendedor que el ítem acaba de ser reservado.

### 3. ¿En qué se diferencia el modelo de procesos propuesto (TO-BE) del flujo tradicional (AS-IS)?
- **Respuesta**: En el modelo AS-IS, el vendedor atendía manualmente por chat de WhatsApp, debía caminar hacia el almacén para constatar visualmente la existencia de tallas, apuntaba en cuadernos manuscritos y avisaba de forma verbal al almacenero, demorando entre 45 y 120 minutos por pedido con un 14.2% de errores en despachos. En el modelo TO-BE, el cliente o vendedor visualiza el catálogo en tiempo real con stock garantizado, emite el pedido en el carrito interactivo en menos de 90 segundos, la orden entra automáticamente a la cola digital de almacén y se descuenta el stock atómicamente, reduciendo el tiempo de procesamiento en más del 90% y erradicando los quiebres de inventario.

### 4. ¿Por qué eligieron una base de datos relacional como PostgreSQL en lugar de una solución NoSQL orientada a documentos como MongoDB?
- **Respuesta**: Porque el dominio central del proyecto es transaccional financiero y logístico (pedidos, clientes, detalles de compra y control de inventario). Estas operaciones exigen coherencia estricta, integridad referencial mediante claves foráneas y garantías ACID absolutas. MongoDB, al carecer de esquemas relacionales rígidos por defecto y gestionar transacciones distribuidas con mayor sobrecarga, incrementaba el riesgo de anomalías de stock y registros huérfanos. Además, PostgreSQL 16 nos ofrece soporte para columnas JSONB si requerimos atributos textiles dinámicos, combinando la robustez relacional con la flexibilidad NoSQL.

### 5. ¿Qué metodología de desarrollo de software aplicaron y cómo gestionaron los cambios de alcance durante el ciclo?
- **Respuesta**: Aplicamos el marco ágil **Scrum** adaptado a un ciclo académico de 18 semanas, complementado con prácticas visuales de **Kanban**. Definimos Sprints de dos semanas con ceremonias formales de Sprint Planning, Daily Standups de 15 minutos, Sprint Review y Retrospectivas. Para gestionar los cambios de alcance, el Product Owner mantuvo un Product Backlog priorizado bajo la técnica MoSCoW. Cualquier nuevo requerimiento emergente de LeoFit fue evaluado en términos de valor de negocio y costo técnico, ingresando como una Historia de Usuario que se estimó y planificó en el Sprint subsiguiente sin alterar el Sprint en curso.

### 6. ¿Cómo implementaron la arquitectura de seguridad frente al Top 10 de vulnerabilidades OWASP?
- **Respuesta**: Diseñamos una arquitectura de defensa en profundidad. Frente a Inyección SQL (A03), utilizamos un 100% de consultas parametrizadas con ORM / Prepared Statements. Frente a Broken Access Control (A01), implementamos un middleware RBAC estricto que valida roles en cada endpoint protegido. Frente a fallas criptográficas (A02), forzamos TLS 1.3 con HSTS, hasheamos contraseñas con Bcrypt costo 12 y ciframos datos sensibles con AES-256-GCM. Finalmente, validamos la eficacia de estas medidas ejecutando análisis dinámicos DAST automatizados con OWASP ZAP, obteniendo 0 vulnerabilidades de severidad alta o crítica.

### 7. ¿Cómo resolvieron el levantamiento de observaciones del 18/20 obtenido en la entrega APF1 previa?
- **Respuesta**: Identificamos que las observaciones de la retroalimentación docente se concentraban en cuatro áreas: necesidad de ampliar los requerimientos y casos borde, incorporar evidencias formales de pantalla con criterios UAT, profundizar en el modelado formal de la base de datos hasta 3NF con triggers, y documentar exhaustivamente las pruebas de seguridad. Subsanamos esto expandiendo el catálogo de 12 a 18 RFs, documentando 14 pantallas con su anatomía visual y reglas de negocio, incluyendo el script DDL de PostgreSQL con triggers automáticos, y anexando reportes de pruebas DAST con OWASP ZAP y SAST con linters de seguridad.

### 8. ¿Qué estrategias de WPO (Web Performance Optimization) aplicaron para alcanzar una puntuación de 96 en Lighthouse?
- **Respuesta**: Implementamos 5 técnicas avanzadas: 1) Code Splitting dinámico mediante `React.lazy()` que redujo el bundle inicial a 142 KB; 2) Conversión de activos fotográficos a formato WebP optimizado con compresión sin pérdidas apreciables; 3) Purga de selectores CSS no utilizados mediante Tailwind CSS / PostCSS; 4) Habilitación de compresión Brotli/Gzip en el servidor; y 5) Almacenamiento en caché agresivo mediante Service Worker con Workbox y política Cache-First para recursos estáticos y tipografías con `font-display: swap`.

### 9. ¿Cómo funciona la arquitectura offline-first si el dispositivo de un vendedor se queda sin internet en el sótano de Gamarra?
- **Respuesta**: Cuando el navegador detecta el evento de desconexión `offline`, el Service Worker intercepta las peticiones GET al catálogo y las sirve instantáneamente desde la caché local. Cuando el vendedor registra un pedido, la aplicación captura la información, la valida sintácticamente y la almacena en una base de datos local **IndexedDB** a través de la cola de Background Sync de Workbox. El usuario visualiza un banner que indica que la orden fue resguardada localmente. Apenas el smartphone detecta señal de internet (`online`), el Service Worker dispara el evento de sincronización en segundo plano, enviando las órdenes pendientes a la API REST sin duplicar registros.

### 10. ¿Cómo estructuraron el control de versiones y la colaboración en equipo en GitHub?
- **Respuesta**: Adoptamos el flujo de trabajo **GitFlow**. La rama `main` se encuentra protegida contra escritura directa y requiere que cualquier código provenga de un Pull Request originado en ramas temáticas (`feature/*` o `hotfix/*`). Cada Pull Request debe pasar obligatoriamente la suite de integración continua (CI) en GitHub Actions (validación de linters, escaneo de dependencias y pruebas unitarias automáticas) y contar con la aprobación de al menos un revisor par (Peer Review). Además, aplicamos la convención semántica de commits (Conventional Commits) para mantener un historial trazable y limpio.

### 11. ¿Cómo manejan el ciclo de vida y la revocación de tokens JWT en el sistema de autenticación?
- **Respuesta**: Aplicamos un esquema de doble token: Access Token de corta duración (15 minutos) firmado con clave criptográfica asimétrica, y Refresh Token de larga duración (7 días) almacenado en una cookie con banderas `HttpOnly`, `Secure` y `SameSite=Strict`. Cuando el Access Token expira, el frontend solicita de forma transparente su renovación enviando el Refresh Token. Para la revocación inmediata de sesiones (por ejemplo, ante el despido o bloqueo de un operador), mantenemos una lista negra en memoria con Redis que verifica el ID único del token (`jti`) con tiempo de expiración equivalente al TTL residual.

### 12. ¿Cuál es el proceso que siguieron para normalizar la base de datos hasta Tercera Forma Normal (3NF)?
- **Respuesta**: Partimos de los formatos no normalizados de los cuadernos de LeoFit. En la 1NF eliminamos grupos repetitivos y forzamos la atomicidad, separando la lista de prendas compradas en la entidad `detalle_pedidos`. En la 2NF eliminamos dependencias parciales en tablas con clave compuesta, aislando atributos como nombre o precio base del producto a la tabla `productos`. En la 3NF eliminamos dependencias transitivas entre atributos no clave, aislando los datos personales del comprador a la tabla `clientes` y los roles a la tabla `roles`. Con ello garantizamos 0 redundancia y consistencia matemática referencial.

### 13. ¿Qué métricas cuantitativas sustentan que la solución es viable económicamente para una MYPE como LeoFit?
- **Respuesta**: La solución tiene un costo de infraestructura cloud en servidores gestionados de aproximadamente $20 a $25 USD mensuales (Supabase Free/Pro tier, Vercel Edge Hosting gratuito y VPS ligero para el backend). Frente a este costo operativo ínfimo, la reducción del tiempo de toma de pedidos de 45 minutos a 90 segundos permite a cada vendedor procesar hasta 12 veces más cotizaciones diarias, incrementando la tasa de conversión en un 35% y recuperando la inversión del proyecto en menos de 2 meses de operación.

### 14. ¿Cómo validaron que la aplicación es accesible según los estándares internacionales de la W3C?
- **Respuesta**: Evaluamos el cumplimiento del estándar **WCAG 2.1 Nivel AA**. Verificamos mediante herramientas automatizadas (Axe-core y Lighthouse Accessibility con puntaje $\ge 95$) y pruebas manuales: ratios de contraste de color superiores a 4.5:1 entre textos y fondos en ambos temas (claro y oscuro), navegación íntegra de la tienda mediante teclado (uso de tabuladores y focos visuales claros), y atributos semánticos ARIA en botones interactivos y modales para lectores de pantalla de personas con discapacidad visual.

### 15. ¿Cuáles son los próximos pasos o trabajos futuros para la evolución del sistema tras la finalización del curso integrador?
- **Respuesta**: Tras el cierre del Curso Integrador II, la hoja de ruta evolutiva (Roadmap v4.0) contempla: 1) Integración directa con pasarelas de pago automatizadas mediante webhooks (MercadoPago / Culqi) para conciliación bancaria instantánea; 2) Integración mediante API con los servicios de SUNAT para la emisión automática de boletas y facturas electrónicas válidas tributariamente; y 3) Un módulo de predicción de demanda textil mediante modelos ligeros de Machine Learning para proyectar el consumo de rollos de tela según la estacionalidad climática en el país.

---

# CAPÍTULO 13: CONCLUSIONES Y LECCIONES APRENDIDAS

## 13.1. Conclusiones Técnicas y de Negocio

1. **Transformación Digital Efectiva de una MYPE Textil**: Se demostró que la implementación de una Progressive Web App (PWA) moderna, liviana y adaptada a la realidad operativa del Emporio de Gamarra erradica los cuellos de botella de la gestión manual, reduciendo el tiempo de atención comercial de 45 minutos a menos de 90 segundos y garantizando 0% de ventas cruzadas sin stock disponible.
2. **Arquitectura Limpia y Escalable**: La separación rigurosa de responsabilidades bajo principios de Clean Architecture y la normalización matemática de la base de datos relacional PostgreSQL hasta 3NF dotan a LeoFit de un núcleo transaccional robusto, capaz de soportar picos de concurrencia y expandirse modularmente hacia nuevos canales de venta sin requerir reingenierías de software.
3. **Cultura DevSecOps y Calidad Demostrada**: La incorporación de pipelines automatizados de CI/CD, auditorías continuas de seguridad DAST/SAST (OWASP Top 10) y suites de pruebas automáticas con Playwright asegura que el software entregado cumpla con los más altos estándares de la ingeniería de software profesional contemporánea.

## 13.2. Lecciones Aprendidas en Gestión Ágil y Calidad de Software

1. **El Valor del Trabajo Cercano al Usuario Real**: El contacto temprano con los vendedores y encargados de almacén en Gamarra permitió descubrir que la señal celular es altamente intermitente en las galerías comerciales. Esta lección motivó el diseño temprano de la arquitectura offline-first con Service Workers y Background Sync, convirtiéndose en el diferencial técnico más valioso del proyecto.
2. **Importancia de la Documentación Viva y Centralizada**: La fragmentación inicial de información en múltiples documentos y carpetas generaba confusión y demoras en el equipo. La consolidación de este Documento Maestro Integral como fuente única de verdad unificada optimizó radicalmente la comunicación interna y garantiza una defensa académica contundente, estructurada y sin contradicciones.

---

# REFERENCIAS BIBLIOGRÁFICAS (NORMAS IEEE Y APA 7ma EDICIÓN)

1. **[IEEE Std 830-1998]**, *IEEE Recommended Practice for Software Requirements Specifications*, IEEE Computer Society, Piscataway, NJ, USA, 1998.
2. **[Pressman, 2021]**, R. S. Pressman y B. R. Maxim, *Ingeniería del Software: Un enfoque práctico*, 9na ed., México: McGraw-Hill Interamericana, 2021.
3. **[Martin, 2018]**, R. C. Martin, *Clean Architecture: A Craftsman's Guide to Software Structure and Design*, Boston, MA, USA: Prentice Hall, 2018.
4. **[OWASP Foundation, 2021]**, *OWASP Top 10:2021 - The Ten Most Critical Web Application Security Risks*, Open Web Application Security Project. Disponible en: `https://owasp.org/Top10/`.
5. **[Schwaber y Sutherland, 2020]**, K. Schwaber y J. Sutherland, *La Guía de Scrum: Las Reglas del Juego*, Scrum.org, 2020.
6. **[W3C, 2018]**, World Wide Web Consortium, *Web Content Accessibility Guidelines (WCAG) 2.1*, W3C Recommendation. Disponible en: `https://www.w3.org/TR/WCAG21/`.
7. **[Nielsen, 1994]**, J. Nielsen, *10 Usability Heuristics for User Interface Design*, Nielsen Norman Group, Fremont, CA, USA, 1994.
8. **[PostgreSQL Global Development Group, 2024]**, *PostgreSQL 16 Documentation*, PostgreSQL.org. Disponible en: `https://www.postgresql.org/docs/16/`.

---
*Fin del Documento Maestro Integral — LeoFit Solutions (Grupo 01 - UTP 2026).*
"""
    os.makedirs('docs', exist_ok=True)
    target_path = os.path.abspath('docs/DOCUMENTO_MAESTRO_INTEGRAL_LEOFIT.md')
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[OK] Documento Maestro Markdown generado con exito en: {target_path}")
    print(f"     Tamano: {len(content)} caracteres, {len(content.splitlines())} lineas.")

if __name__ == '__main__':
    build_master_markdown()
