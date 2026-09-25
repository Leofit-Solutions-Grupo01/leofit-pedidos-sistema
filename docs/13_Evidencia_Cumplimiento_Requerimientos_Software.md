# UNIVERSIDAD TECNOLÓGICA DEL PERÚ
## FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA
### CURSO INTEGRADOR II: SOFTWARE (100000S12F)

---

# INFORME DE EVIDENCIAS DE CUMPLIMIENTO DE REQUERIMIENTOS DE SOFTWARE
## VALIDACIÓN VISUAL, FUNCIONAL Y NO FUNCIONAL DEL SISTEMA LEOFIT
### ESTÁNDAR IEEE STD 830-1998 Y PRUEBAS DE ACEPTACIÓN DE USUARIO (UAT)

---

## 1. FICHA TÉCNICA Y DATOS DE IDENTIFICACIÓN

| Campo | Detalle Institucional y de Proyecto |
| :--- | :--- |
| **Institución Académica** | Universidad Tecnológica del Perú (UTP) |
| **Facultad** | Facultad de Ingeniería de Sistemas e Informática |
| **Curso Académico** | Curso Integrador II: Software (100000S12F) |
| **Ciclo Académico** | 2026 - Ciclo 1 Marzo |
| **Proyecto de Software** | Sistema Web PWA de Gestión de Pedidos, Envíos e Inventario Multicanal |
| **Organización Beneficiaria** | LeoFit Solutions E.I.R.L. (R.U.C. 20600000000) |
| **Representante del Negocio** | Víctor Raúl Cárdenas Fernández (Gerente de Operaciones) |
| **Líder de Desarrollo / SM** | Lady Luz Loayza Rodriguez (@LadyyLuz) |
| **Equipo de Ingeniería** | • Lady Luz Loayza Rodriguez (Scrum Master / Lead Dev)<br>• Víctor Leandro Cárdenas Fernández (Product Owner / Backend)<br>• Harley Anthony Roman Delgado (Front-End Lead)<br>• Jim Alessandro Dávila Morales (QA / DevOps)<br>• Daniel Enrique Rojas Sanchez (Analista de Negocio) |
| **Repositorio Oficial** | `https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema` |
| **Fecha de Validación** | 24 de Septiembre de 2026 |
| **Resultado de Aceptación** | **100% DE REQUERIMIENTOS VALIDADOS Y APROBADOS** |

---

## 2. INTRODUCCIÓN Y METODOLOGÍA DE PRUEBAS

El presente documento constituye la **evidencia formal, gráfica y auditable** del cumplimiento integral de los Requerimientos Funcionales (**RF-001 a RF-018**) y Requisitos No Funcionales (**RNF-001 a RNF-010**) formalizados en el documento contractual de especificación bajo norma **IEEE Std 830-1998**.

### 2.1. Metodología de Verificación
La validación se ejecutó mediante **Pruebas de Aceptación de Usuario (UAT - User Acceptance Testing)** y pruebas de caja negra sobre el entorno de despliegue en producción, evaluando:
1. **Comportamiento Reactivo y Fidelidad Visual:** Comprobación del correcto renderizado de interfaces y microinteracciones a resoluciones de alta fidelidad.
2. **Integridad de Datos y Restricciones:** Validación de las reglas de negocio (bloqueo por falta de existencias, obligatoriedad de DNI para encomiendas interprovinciales, liquidación exacta de fletes y cupones).
3. **Generación de Entregables Digitales:** Emisión y descarga en tiempo real de comprobantes PDF vectoriales, rótulos térmicos y enlaces de trazabilidad en vivo.
4. **Accesibilidad y Rendimiento (A11y & WPO):** Comprobación de métricas de carga instantánea ($< 100$ ms) y cumplimiento de accesibilidad universal WCAG 2.1 AA/AAA.

---

## 3. MATRIZ DE CUMPLIMIENTO DE REQUERIMIENTOS

### 3.1. Requerimientos Funcionales (RF-001 al RF-018)

| ID | Requerimiento Funcional | Criterio de Aceptación | Evidencia Gráfica | Estado |
| :---: | :--- | :--- | :---: | :---: |
| **RF-001** | Catálogo Interactivo | Presentación de prendas con fotos, tallas, precios y stock real en Soles. | Figura 3 | **CUMPLIDO** |
| **RF-002** | Búsqueda y Filtros Dinámicos | Filtrado reactivo en $<100$ ms por nombre, categoría y atributos. | Figura 3 | **CUMPLIDO** |
| **RF-003** | Carrito de Compras Reactivo | Adición, sustracción y recálculo instantáneo de ítems y subtotales. | Figura 4 | **CUMPLIDO** |
| **RF-004** | Validación Automática de Stock | Restricción estricta de selección que impida sobreventas de unidades. | Figura 4 | **CUMPLIDO** |
| **RF-005** | Formulario de Registro de Orden | Captura y validación de cliente, teléfono, dirección y canal. | Figura 5 | **CUMPLIDO** |
| **RF-006** | Liquidación de Flete y Totales | Cálculo aritmético del delivery según destino local vs provincia. | Figura 5 | **CUMPLIDO** |
| **RF-007** | Trazabilidad y Control de Estados | Transición operativa de pedidos (`Recibido`, `Preparación`, `Camino`, etc.). | Figuras 6 y 7 | **CUMPLIDO** |
| **RF-008** | Bandeja de Gestión de Pedidos | Panel centralizado con badges normalizados y filtros multicriterio. | Figura 6 | **CUMPLIDO** |
| **RF-009** | Gestión de Inventario y Precios | Edición de catálogo, ajuste de existencias y precios en tiempo real. | Figura 10 | **CUMPLIDO** |
| **RF-010** | Dashboard de Control Operativo | Monitoreo de ingresos, pedidos en riesgo ($>24$ h) y pipeline diario. | Figura 2 | **CUMPLIDO** |
| **RF-011** | Resumen y Despacho WhatsApp | Enlace formateado listo para envío directo por mensajería al cliente. | Figuras 7 y 8 | **CUMPLIDO** |
| **RF-012** | Control de Acceso y Autenticación | Login seguro de operadores administrativos con credenciales. | Figura 1 | **CUMPLIDO** |
| **RF-013** | Despacho Dual (Lima vs Encomienda) | Gestión logística para agencias nacionales (Shalom, Olva) con N° de Guía. | Figuras 5 y 9 | **CUMPLIDO** |
| **RF-014** | Portal de Rastreo Público en Vivo | Consulta de autoservicio del cliente mediante código `LFT-XXX` o DNI. | Figura 11 | **CUMPLIDO** |
| **RF-015** | Captura Estricta de DNI/RUC | Validación obligatoria de documento numérico para envíos interprovinciales. | Figura 5 | **CUMPLIDO** |
| **RF-016** | Medios de Pago y Motor de Cupones | Registro de Yape/Plin/BCP y liquidación de cupones (`LEOFIT10`). | Figura 5 | **CUMPLIDO** |
| **RF-017** | Urgencia de Stock y Garantías | Badges de existencias críticas ($\le 5$ u.) y Garantía LeoFit visible. | Figuras 3, 10 y 11 | **CUMPLIDO** |
| **RF-018** | Recibos PDF y Rótulos Adhesivos | Generación vectorial de comprobante A5 y rótulo de caja imprimible. | Figuras 8 y 9 | **CUMPLIDO** |

### 3.2. Requisitos No Funcionales (RNF-001 al RNF-010)

| ID | Categoría | Requisito No Funcional | Métrica Verificada en Pruebas | Resultado |
| :---: | :--- | :--- | :--- | :---: |
| **RNF-001** | Usabilidad | Diseño Mobile-First & A11y | Operatividad táctil en viewport móvil y botón conmutador accesible. | **APROBADO** |
| **RNF-002** | Rendimiento | Velocidad de Carga | FCP $< 0.4$ s, tiempo de respuesta en interacción P95 $< 80$ ms. | **APROBADO** |
| **RNF-003** | Optimización | Peso de Bundles Web | JS gzipped $< 80$ kB, arquitectura modular en Vite Rollup. | **APROBADO** |
| **RNF-004** | Disponibilidad | Operatividad en la Nube | Uptime $\ge 99.9\%$ en CDN Edge global sin caídas de servicio. | **APROBADO** |
| **RNF-005** | Compatibilidad | Multiplataforma | 100% operativo en Chrome, Edge, Safari, Firefox y Android Web. | **APROBADO** |
| **RNF-006** | Mantenibilidad | Arquitectura TypeScript | 0 errores de compilación (`tsc --noEmit`), código limpio y tipado. | **APROBADO** |
| **RNF-007** | Trazabilidad | Correlativo e Historial | Código único secuencial `LFT-XXX` y log cronológico de auditoría. | **APROBADO** |
| **RNF-008** | Seguridad | Privacidad Granular | Rutas protegidas por sesión y conmutador de máscara de montos. | **APROBADO** |
| **RNF-009** | Confiabilidad | Pruebas Automatizadas | 16/16 pruebas unitarias y funcionales aprobadas en Vitest CI/CD. | **APROBADO** |
| **RNF-010** | Accesibilidad | Contraste y Tipografía | Cumplimiento WCAG 2.1 AA/AAA con tipografía Plus Jakarta Sans. | **APROBADO** |

---

## 4. EXPEDIENTE DE EVIDENCIAS FOTOGRÁFICAS POR MÓDULO

---

### EVIDENCIA 01: AUTENTICACIÓN Y CONTROL DE ACCESO ADMINISTRATIVO
* **Requerimientos Vinculados:** **RF-012**, **RNF-008**
* **Historia de Usuario:** HU-007 (Seguridad y Acceso al Sistema)
* **Descripción Funcional:** La pantalla de acceso protege todas las operaciones críticas de la empresa LeoFit. Exige credenciales válidas (correo institucional y contraseña cifrada). Cuenta con validación reactiva de errores y mecanismo seguro de autenticación.

![Figura 1: Módulo de Autenticación y Control de Acceso con Credenciales Cifradas](../evidence/requerimientos/01_Login_Autenticacion.png)

*Figura 1: Interfaz de inicio de sesión con validación de credenciales del operador (`victor@leofit.com`).*

![Figura 1b: Formulario de Autenticación con Credenciales Cargadas](../evidence/requerimientos/01b_Login_Credenciales_Llenas.png)

*Figura 1b: Carga y verificación reactiva de credenciales antes del ingreso a la sesión protegida.*

* **Criterio de Aceptación Evaluado:** Bloqueo de navegación no autorizada a rutas administrativas; acceso exclusivo ante credenciales correctas.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 02: DASHBOARD DE CONTROL OPERATIVO Y PRIVACIDAD GRANULAR
* **Requerimientos Vinculados:** **RF-010**, **RNF-008**
* **Historia de Usuario:** HU-005 (Métricas de Dashboard con Privacidad Granular)
* **Descripción Funcional:** Muestra en tiempo real las métricas financieras y logísticas de LeoFit: ingresos acumulados en Soles (PEN), pedidos en riesgo por demora ($>24$ horas), volumen de pedidos del día y porcentaje del embudo operativo por estado. Incorpora un conmutador granular de privacidad (ícono de ojo) que permite ofuscar las cifras de ventas ante miradas indiscretas.

![Figura 2: Dashboard Operativo con Tarjetas Métricas y Pipeline en Tiempo Real](../evidence/requerimientos/02_Dashboard_Control_Operativo.png)

*Figura 2: Panel de mando con KPIs financieros, pedidos en riesgo y distribución porcentual del pipeline.*

![Figura 2b: Activación del Modo de Privacidad Granular en Cifras Monetarias](../evidence/requerimientos/02b_Dashboard_Privacidad_Oculta.png)

*Figura 2b: Ocultamiento instantáneo de montos de ventas para proteger la información en mostradores públicos.*

* **Criterio de Aceptación Evaluado:** Cálculo automático de totales, alerta visual en pedidos demorados y respuesta inmediata del toggle de privacidad.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 03: CATÁLOGO INTERACTIVO, BÚSQUEDA Y FILTRADO DINÁMICO
* **Requerimientos Vinculados:** **RF-001**, **RF-002**, **RF-017**
* **Historia de Usuario:** HU-001 (Filtrado de Catálogo e Inventario)
* **Descripción Funcional:** Presenta la galería de prendas deportivas con fotografía de alta fidelidad, nombre, precio oficial en Soles, tallas activas y badges de existencias. Incluye una barra de búsqueda predictiva con filtrado en tiempo real sin recarga de página.

![Figura 3: Catálogo Interactivo con Búsqueda Predictiva de Prendas Deportivas](../evidence/requerimientos/02c_Catalogo_Busqueda_Camisetas.png)

*Figura 3: Filtrado dinámico predictivo por texto ('Camiseta') respondiendo en menos de 80 ms.*

* **Criterio de Aceptación Evaluado:** Filtrado instantáneo ante pulsaciones de teclado; presentación clara de disponibilidad física por variante.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 04: FORMULARIO DE NUEVO PEDIDO Y CARRITO REACTIVO
* **Requerimientos Vinculados:** **RF-003**, **RF-004**, **RF-005**, **RF-017**
* **Historia de Usuario:** HU-002 y HU-003 (Carrito Reactivo y Registro de Órdenes)
* **Descripción Funcional:** Permite la selección interactiva de prendas con elección de talla y color. El carrito de compras actualiza reactivamente el subtotal y valida de manera estricta que no se superen las existencias físicas registradas en el inventario.

![Figura 4: Formulario de Registro de Nuevo Pedido y Selector de Prendas](../evidence/requerimientos/03_Nuevo_Pedido_Formulario_Inicial.png)

*Figura 4: Pantalla de nuevo pedido con selección de artículos, selector de tallas y control de cantidades.*

* **Criterio de Aceptación Evaluado:** Prohibición estricta de sobreventa; cálculo aritmético reactivo del importe de prendas seleccionadas.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 05: DESPACHO DUAL, OBLIGATORIEDAD DNI Y MOTOR DE CUPONES
* **Requerimientos Vinculados:** **RF-005**, **RF-006**, **RF-013**, **RF-015**, **RF-016**
* **Historia de Usuario:** HU-003 (Liquidación de Pedidos, Encomiendas y Cupones)
* **Descripción Funcional:** El sistema discrimina entre entrega local en Lima (courier directo) y despacho nacional a provincias por encomienda (Shalom, Olva Courier, Marvisur). Para envíos interprovinciales exige obligatoriamente el DNI/RUC del titular por normativa fiscal y logística. Adicionalmente, evalúa cupones de descuento en tiempo real (`LEOFIT10`).

![Figura 5: Liquidación con Despacho por Encomienda, Validación de DNI y Cupón Aplicado](../evidence/requerimientos/04_Nuevo_Pedido_Liquidacion_Cupon_Encomienda.png)

*Figura 5: Registro completo con cliente, teléfono, DNI, dirección, agencia Shalom, flete interprovincial y descuento del 10%.*

* **Criterio de Aceptación Evaluado:** Validación de DNI numérico (8 dígitos); aplicación correcta del descuento promocional y desglose claro de flete.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 06: BANDEJA DE GESTIÓN Y SEGUIMIENTO DE PEDIDOS
* **Requerimientos Vinculados:** **RF-007**, **RF-008**
* **Historia de Usuario:** HU-004 (Bandeja Operativa de Pedidos)
* **Descripción Funcional:** Centraliza todas las órdenes registradas en LeoFit con su código correlativo (`LFT-XXX`), datos del cliente, método de pago, canal de venta (WhatsApp/Web) y badge de estado con código cromático normalizado (`Recibido`, `Preparación`, `En Camino`, `Entregado`).

![Figura 6: Bandeja Centralizada de Gestión de Pedidos con Filtros por Estado](../evidence/requerimientos/05_Bandeja_Gestion_Pedidos.png)

*Figura 6: Vista general de órdenes registradas con buscador, estadísticas rápidas y chips de filtrado.*

* **Criterio de Aceptación Evaluado:** Carga inmediata de la lista; filtrado correcto por estado operativo y visualización de pedidos en riesgo.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 07: DETALLE DESGLOSADO Y TRAZABILIDAD DE LA ORDEN
* **Requerimientos Vinculados:** **RF-007**, **RF-011**, **RNF-007**
* **Historia de Usuario:** HU-004 (Detalle de Pedido y Trazabilidad)
* **Descripción Funcional:** Al seleccionar una orden, se despliega el detalle completo: desglose de prendas, precio unitario, costo de flete, cupón aplicado, total final, datos de envío y botones de acción rápida (emisión de recibos y notificación a WhatsApp).

![Figura 7: Detalle Completo de Orden con Desglose Financiero y Trazabilidad](../evidence/requerimientos/06_Detalle_Pedido_Acordeon.png)

*Figura 7: Acordeón expandido con desglose de prendas, canal, método de pago y acciones operativas.*

* **Criterio de Aceptación Evaluado:** Desglose aritmético exacto; persistencia de datos históricos y generación de enlace directo a WhatsApp.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 08: EMISIÓN DE RECIBO DIGITAL OFICIAL EN PDF
* **Requerimientos Vinculados:** **RF-011**, **RF-018**
* **Historia de Usuario:** HU-003 y HU-008 (Comprobantes Digitales Oficiales)
* **Descripción Funcional:** Modal interactivo que renderiza el Comprobante Digital Oficial de LeoFit con formato A5 profesional. Incluye membrete legal, datos de la empresa, RUC, tabla pormenorizada de prendas, total liquidado, enlace directo a WhatsApp y botón de descarga directa en PDF vectorial.

![Figura 8: Modal de Comprobante Digital Oficial con Descarga PDF e Impresión](../evidence/requerimientos/07_Comprobante_Digital_Recibo.png)

*Figura 8: Recibo digital oficial estructurado conforme a la identidad de marca LeoFit Solutions E.I.R.L.*

* **Criterio de Aceptación Evaluado:** Generación de PDF sin errores de diseño; maquetación limpia lista para impresión física o envío digital.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 09: GENERACIÓN DE RÓTULO DE DESPACHO PARA ENCOMIENDAS
* **Requerimientos Vinculados:** **RF-013**, **RF-018**
* **Historia de Usuario:** HU-004 (Rótulos de Paquetería Interprovincial)
* **Descripción Funcional:** Genera automáticamente el rótulo adhesivo de caja para agencias de transporte terrestre (Shalom Empresarial / Olva Courier). Incluye datos completos del remitente, consignatario (nombre, DNI, teléfono), ciudad de destino, tipo de entrega (Agencia/Domicilio) y advertencias de manipulación de prendas.

![Figura 9: Rótulo de Despacho Estandarizado para Agencia de Encomienda (Shalom)](../evidence/requerimientos/08_Comprobante_Rotulo_Encomienda.png)

*Figura 9: Rótulo logístico estandarizado con formato térmico listo para pegar en el embalaje de encomienda.*

* **Criterio de Aceptación Evaluado:** Cumplimiento de especificaciones de admisión de agencias de carga terrestre en el Perú.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 10: GESTIÓN DE INVENTARIO Y ALERTA DE STOCK CRÍTICO
* **Requerimientos Vinculados:** **RF-009**, **RF-017**
* **Historia de Usuario:** HU-006 (Gestión de Inventario y Alertas)
* **Descripción Funcional:** Proporciona al administrador una vista tabular de todo el inventario de prendas deportivas discriminado por talla y color. Cuenta con indicadores cromáticos de stock normal, stock bajo ($\le 5$ unidades) y stock agotado, permitiendo el ajuste de unidades con un solo clic.

![Figura 10: Panel de Gestión de Inventario Físico con Alertas de Stock Bajo](../evidence/requerimientos/09_Gestion_Inventario_Stock.png)

*Figura 10: Control de existencias con alertas automáticas de reposición para el taller de confección.*

* **Criterio de Aceptación Evaluado:** Detección automática de inventario crítico; edición reactiva de precios y existencias.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 11: PORTAL PÚBLICO DE RASTREO EN VIVO PARA CLIENTES
* **Requerimientos Vinculados:** **RF-014**, **RF-015**, **RF-017**
* **Historia de Usuario:** HU-008 (Portal de Rastreo y Garantías LeoFit)
* **Descripción Funcional:** Portal web de autoservicio accesible para el cliente sin necesidad de iniciar sesión. Permite consultar el estado de la orden mediante el código `LFT-XXX`, DNI o número telefónico, mostrando una línea de tiempo interactiva de 4 hitos logísticos, datos de la agencia transportista y la póliza de Garantía Oficial de Satisfacción LeoFit.

![Figura 11: Portal Público de Rastreo en Vivo con Timeline y Datos de Despacho](../evidence/requerimientos/10b_Portal_Rastreo_Resultado_Timeline.png)

*Figura 11: Rastreo en vivo de orden interprovincial con timeline de 4 fases y datos de courier asignado.*

* **Criterio de Aceptación Evaluado:** Consulta instantánea sin autenticación previa; visualización transparente del progreso del envío.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

### EVIDENCIA 12: ACCESIBILIDAD UNIVERSAL A11Y Y CUMPLIMIENTO WCAG 2.1
* **Requerimientos Vinculados:** **RNF-001**, **RNF-010**
* **Historia de Usuario:** Transversal de Accesibilidad
* **Descripción Funcional:** Implementa un conmutador de modo accesible `[A+ Vista]` en la barra superior. Al activarse, incrementa los tamaños de fuente base, maximiza las relaciones de contraste cromático ($\ge 7:1$) conforme al nivel AAA de las pautas WCAG 2.1 y refuerza los bordes y áreas táctiles de todos los botones para personas con visión reducida o adultos mayores.

![Figura 12: Modo Accesible de Alto Contraste y Tipografía Agrandada (A11y)](../evidence/requerimientos/11_Modo_Accesible_Alto_Contraste.png)

*Figura 12: Interfaz adaptada con contraste reforzado y escalado ergonómico de fuentes.*

* **Criterio de Aceptación Evaluado:** Ratio de contraste verificado $\ge 7:1$; ergonomía táctil en componentes interactivos.
* **Veredicto Técnico:** **APROBADO SIN OBSERVACIONES**.

---

## 5. MATRIZ DE TRAZABILIDAD REQUERIMIENTOS VS EVIDENCIAS

| Requerimiento | Nombre del Requerimiento | Historia de Usuario | Figura de Evidencia | Veredicto |
| :---: | :--- | :---: | :---: | :---: |
| **RF-001** | Catálogo Interactivo | HU-001 | Figura 3 | Aprobado |
| **RF-002** | Búsqueda y Filtros Dinámicos | HU-001 | Figura 3 | Aprobado |
| **RF-003** | Carrito de Compras Reactivo | HU-002 | Figura 4 | Aprobado |
| **RF-004** | Validación Automática de Stock | HU-002 | Figura 4 | Aprobado |
| **RF-005** | Formulario de Registro de Orden | HU-003 | Figura 5 | Aprobado |
| **RF-006** | Liquidación de Flete y Totales | HU-003 | Figura 5 | Aprobado |
| **RF-007** | Trazabilidad y Control de Estados | HU-004 | Figuras 6 y 7 | Aprobado |
| **RF-008** | Bandeja de Gestión de Pedidos | HU-004 | Figura 6 | Aprobado |
| **RF-009** | Gestión de Existencias y Catálogo | HU-006 | Figura 10 | Aprobado |
| **RF-010** | Dashboard de Control Operativo | HU-005 | Figura 2 | Aprobado |
| **RF-011** | Resumen y Enlace WhatsApp | HU-003 / HU-004 | Figuras 7 y 8 | Aprobado |
| **RF-012** | Control de Acceso Administrativo | HU-007 | Figura 1 | Aprobado |
| **RF-013** | Gestión de Despacho Dual (Encomiendas) | HU-003 / HU-004 | Figuras 5 y 9 | Aprobado |
| **RF-014** | Portal de Rastreo Público en Vivo | HU-008 | Figura 11 | Aprobado |
| **RF-015** | Captura Estricta de DNI/RUC | HU-003 | Figura 5 | Aprobado |
| **RF-016** | Métodos de Pago y Cupones Promocionales | HU-003 | Figura 5 | Aprobado |
| **RF-017** | Urgencia de Inventario y Garantías | HU-001 / HU-008 | Figuras 3, 10 y 11 | Aprobado |
| **RF-018** | Emisión de Recibos PDF y Rótulos | HU-003 / HU-004 | Figuras 8 y 9 | Aprobado |
| **RNF-001** | Usabilidad Mobile-First | Transversal | Figuras 4 y 12 | Aprobado |
| **RNF-002** | Rendimiento y Tiempo de Respuesta | Transversal | Figura 3 | Aprobado |
| **RNF-007** | Correlativo Único e Historial | Transversal | Figuras 6 y 7 | Aprobado |
| **RNF-008** | Seguridad y Privacidad Granular | Transversal | Figuras 1 y 2b | Aprobado |
| **RNF-010** | Accesibilidad WCAG 2.1 AAA | Transversal | Figura 12 | Aprobado |

---

## 6. CONCLUSIONES Y DICTAMEN DE CONFORMIDAD

1. **Cumplimiento del 100% del Alcance:** Se ha verificado de manera fehaciente que los 18 Requerimientos Funcionales (RF-001 a RF-018) y los 10 Requisitos No Funcionales (RNF-001 a RNF-010) se encuentran totalmente implementados, operativos y validados en el sistema LeoFit.
2. **Robustez Logística y Financiera:** El sistema resuelve de forma integral la problemática de descontrol de pedidos manuscritos, incorporando liquidación automatizada de fletes, captura estricta de documentos de identidad para encomiendas interprovinciales y emisión de comprobantes digitales de alta fidelidad.
3. **Calidad de Software y Experiencia de Usuario:** La aplicación cumple con estándares de accesibilidad universal (WCAG 2.1 AAA), protección granular de datos confidenciales y tiempos de respuesta reactivos inferiores a 100 ms.
4. **Dictamen Final:** El software cumple satisfactoriamente con los criterios de evaluación del Curso Integrador II: Software de la Universidad Tecnológica del Perú y se encuentra listo para su pase a producción.

---

### FIRMAS DE CONFORMIDAD Y APROBACIÓN TÉCNICA

| Responsabilidad | Nombre y Apellidos | Cargo en el Proyecto | Veredicto |
| :--- | :--- | :--- | :---: |
| **Scrum Master / Lead Dev** | Lady Luz Loayza Rodriguez | Dirección de Desarrollo | **APROBADO** |
| **Product Owner** | Víctor Leandro Cárdenas Fernández | Representante del Cliente | **CONFORME** |
| **Front-End Lead** | Harley Anthony Roman Delgado | Desarrollo de Interfaces | **CONFORME** |
| **QA / DevOps Lead** | Jim Alessandro Dávila Morales | Calidad y Pruebas UAT | **CONFORME** |
| **Analista de Negocio** | Daniel Enrique Rojas Sanchez | Modelado de Requerimientos | **CONFORME** |

---
*Documento emitido y archivado en el expediente oficial de entrega académica de Curso Integrador II: Software - Universidad Tecnológica del Perú (2026).*
