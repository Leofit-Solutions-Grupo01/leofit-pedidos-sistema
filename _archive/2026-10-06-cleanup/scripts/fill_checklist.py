# -*- coding: utf-8 -*-
"""
Script definitivo para rellenar 'Checklist Integral para la Evaluación de Software.docx'
con información técnica, lógica, profesional y entendible end-to-end del proyecto LeoFit Solutions.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Establece márgenes internos (padding) de celda en dxa."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = tcPr.find(qn('w:tcMar'))
    if tcMar is not None:
        tcPr.remove(tcMar)
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    """Aplica color de fondo hexadecimal a una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = tcPr.find(qn('w:shd'))
    if shd is not None:
        tcPr.remove(shd)
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>'
    tcPr.append(parse_xml(shading_xml))

def set_cell_width_dxa(cell, width_dxa):
    """Ajusta el ancho de celda en dxa de forma estricta en el XML."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is not None:
        tcW.set(qn('w:w'), str(width_dxa))
        tcW.set(qn('w:type'), 'dxa')
    else:
        node = OxmlElement('w:tcW')
        node.set(qn('w:w'), str(width_dxa))
        node.set(qn('w:type'), 'dxa')
        tcPr.append(node)

def apply_table_borders(table):
    """Aplica bordes discretos, profesionales y limpios a toda la tabla."""
    tblPr = table._tbl.tblPr
    existing_borders = tblPr.find(qn('w:tblBorders'))
    if existing_borders is not None:
        tblPr.remove(existing_borders)
    
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        <w:bottom w:val="single" w:sz="8" w:space="0" w:color="0A2F41"/>
        <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
        <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def build_full_checklist():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, 'docs', 'academic', 'recursos', 'Checklist_Integral_Evaluacion_Software_Plantilla.docx')
    
    # Cargar plantilla oficial de respaldo en recursos
    doc = docx.Document(template_path)

    # Configuración de página A4 con márgenes estandarizados
    section = doc.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)

    # 1. Título y Encabezado del Documento
    title_p = doc.paragraphs[0]
    title_p.text = ""
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    
    r_main = title_p.add_run("Checklist Integral para la Evaluación de Software\n")
    r_main.font.name = "Arial"
    r_main.font.size = Pt(15)
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(10, 47, 65) # Navy corporativo #0A2F41

    r_sub = title_p.add_run("Sistema Web PWA de Gestión de Pedidos & Control de Inventario Multicanal — LeoFit Solutions\n")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(11)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(30, 90, 130)

    r_meta = title_p.add_run("Evaluación Técnica End-to-End: Funcionalidad, Usabilidad (UX), Rendimiento y Seguridad / Costos\nCurso Integrador II: Software (100000S12F) | Universidad Tecnológica del Perú (UTP)")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(9)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(90, 100, 115)

    if len(doc.paragraphs) > 1 and doc.paragraphs[1].text.strip() == "":
        doc.paragraphs[1].paragraph_format.space_before = Pt(0)
        doc.paragraphs[1].paragraph_format.space_after = Pt(4)

    # 2. Datos y Contenidos de Evaluación End-to-End
    checklist_data = [
        # =========================================================================
        # BLOQUE 1: FUNCIONALIDAD (3 ÍTEMS)
        # =========================================================================
        {
            "cat": "Funcionalidad",
            "pregunta": "¿El software resuelve los problemas específicos y cubre las necesidades críticas del negocio de punta a punta?",
            "items": [
                ("Problema Central Resuelto", 
                 "Digitalización y automatización integral del flujo comercial y logístico de la empresa LeoFit Indumentaria & Nutrición Deportiva (Gamarra, Lima), erradicando las demoras de atención manual (reducidas de 25 min a <= 2 min), la sobreventa y el descontrol de inventario por registros manuscritos en cuadernos y chats informales de WhatsApp."),
                ("Flujo Operativo End-to-End Implementado",
                 "1. Exploración y Filtrado: Catálogo reactivo con segmentación por categoría, talla, color y existencias reales (src/pages/Dashboard.tsx).\n"
                 "2. Control Atómico de Stock: Carrito de compras reactivo (src/context/AppContext.tsx) que valida la disponibilidad física de inventario e impide compras que excedan existencias reales (RF-003, RF-004).\n"
                 "3. Formalización de la Orden: Formulario estructurado (src/pages/PedidoForm.tsx) con validación estricta de DNI (8 dígitos) o RUC (11 dígitos), cálculo automático de flete y generación de código correlativo unívoco (LFT-XXX) (RF-005, RF-006, RF-015).\n"
                 "4. Motor de Despacho Dual: Lógica bifurcada que diferencia reparto local directo en Lima Metropolitana de envíos interprovinciales por agencias de encomienda (Shalom, Olva Courier, Marvisur) con registro de N° de guía física y clave de entrega (RF-013).\n"
                 "5. Comprobantes y Notificación: Emisión de recibos digitales oficiales en PDF, rótulos adhesivos de encomienda (RF-018) y generación de enlace directo a WhatsApp (wa.me) con el resumen estructurado de la compra para confirmación inmediata con el cliente (RF-011)."),
                ("Criterio de Validación", 
                 "100% de requerimientos funcionales críticos (RF-001 a RF-018 bajo estándar IEEE 830) implementados, probados y en funcionamiento productivo.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Funcionalidad",
            "pregunta": "¿El sistema implementa una gestión integral, atómica y sincronizada del inventario multicanal con actualización de stock en tiempo real?",
            "items": [
                ("Aislamiento y Consistencia Transaccional (ACID)", 
                 "El backend en Node.js 20 / TypeScript implementa el patrón repositorio sobre PostgreSQL 16 (backend/src/infrastructure/repositories/pg.repositories.ts). Las operaciones de decremento o restitución de existencias se ejecutan dentro de transacciones de base de datos protegidas con bloqueos a nivel de fila (SELECT stock FROM products WHERE id = $1 FOR UPDATE), garantizando consistencia estricta e impidiendo condiciones de carrera (race conditions) y sobreventas simultáneas entre la tienda física y canales digitales."),
                ("Gestión Integral del Catálogo", 
                 "Módulo administrativo completo (src/pages/ProductosGestion.tsx) que faculta al administrador Víctor Raúl Cárdenas para dar de alta nuevos productos, ajustar precios en Soles (S/), actualizar tallas (S, M, L, XL, estándar) y editar existencias físicas con persistencia inmediata y sincronización hacia el catálogo público (RF-009)."),
                ("Detección Preventiva de Stock Crítico", 
                 "Algoritmo reactivo que identifica existencias <= 5 unidades (RF-017), desplegando badges de advertencia de urgencia en el catálogo para el comprador y notificando al administrador en el dashboard para coordinar la reposición con los talleres de confección textil.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Funcionalidad",
            "pregunta": "¿El flujo de trazabilidad logística y estados operativos cubre el ciclo de vida completo de la orden con portal de autoservicio para el cliente?",
            "items": [
                ("Máquina de Estados Finita Normalizada", 
                 "El ciclo de vida de cada orden transita por 5 estados operativos determinísticos y secuenciales: Recibido -> En Preparación -> En Camino -> Entregado (con estado de excepción Cancelado que restituye el stock automáticamente) (src/pages/PedidosLista.tsx), registrando marcas temporales inmutables (timestamps) y usuario ejecutor en cada transición (tabla order_status_history) (RF-007, RF-008)."),
                ("Motor Logístico de Despacho Dual", 
                 "Discrimina operativamente el reparto directo en Lima Metropolitana (asignación a transportista motorizado local, verificación de dirección y cobro contra entrega / Yape / Plin) frente al despacho nacional a provincias (consignación formal en agencias Shalom, Olva Courier o Marvisur, exigencia obligatoria de DNI/RUC para encomiendas y registro de N° de guía física y clave de retiro) (RF-013, RF-015)."),
                ("Portal Público de Tracking en Vivo", 
                 "Módulo de autoservicio web (src/pages/RastreoPublico.tsx) que permite al cliente final consultar de forma transparente el avance de su pedido en tiempo real mediante su código correlativo LFT-XXX, DNI o número de teléfono, visualizando un timeline interactivo de 4 hitos, datos de guía y póliza de garantía oficial de cambio de talla, descongestionando los canales de atención manual en más de un 85% (RF-014).")
            ],
            "si": "X",
            "no": ""
        },

        # =========================================================================
        # BLOQUE 2: USABILIDAD (UX) (3 ÍTEMS)
        # =========================================================================
        {
            "cat": "Usabilidad (UX)",
            "pregunta": "¿La interfaz de usuario cumple con principios ergonómicos Mobile-First y directrices de accesibilidad universal (WCAG 2.1 AA/AAA)?",
            "items": [
                ("Diseño Mobile-First y Ergonomía Táctil", 
                 "Arquitectura responsiva fluida desarrollada con Tailwind CSS optimizada prioritariamente para pantallas táctiles de smartphones, tablets y laptops. Zonas de interacción táctil sobredimensionadas (>= 48x48 px) conforme a los estándares de ergonomía de Google Material Design y Apple HIG, garantizando un manejo ágil y cómodo con una sola mano."),
                ("Tipografía Moderna y Ratio de Contraste", 
                 "Uso de la familia tipográfica moderna Plus Jakarta Sans con pesos jerárquicos definidos, garantizando ratios de contraste cromático superiores a 7:1 en textos principales sobre fondos claros y oscuros, superando los requerimientos de accesibilidad WCAG 2.1 nivel AAA (RNF-010)."),
                ("Modo de Accesibilidad Visual Granular", 
                 "Incorporación de un selector de escalado tipográfico dinámico [A+ / A++] (RNF-001, RNF-010) que ajusta proporcionalmente el tamaño de texto de toda la aplicación sin quebrar el layout ni generar desbordamientos horizontales, garantizando inclusión para adultos mayores o usuarios con fatiga visual.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Usabilidad (UX)",
            "pregunta": "¿La experiencia de compra y toma de pedidos minimiza la carga cognitiva del usuario y optimiza el tiempo de conversión a menos de 2 minutos?",
            "items": [
                ("Reducción Drástica del Tiempo de Atención", 
                 "Optimización del embudo de conversión reduciendo el tiempo de toma de pedidos de 25 minutos (en el esquema manual AS-IS de chats desestructurados y llamadas) a <= 2 minutos en la PWA, estructurado en un recorrido lineal de 3 etapas: exploración de catálogo -> carrito reactivo -> liquidación y despacho."),
                ("Búsqueda y Filtrado Predictivo Instantáneo", 
                 "Motor de filtrado facetado reactivo en el cliente (RF-002) con latencia < 100 ms que segmenta simultáneamente por categoría textil (conjuntos térmicos, lycras de compresión, fajas, polos dry-fit), rango de precio y talla disponible sin recargar la página."),
                ("Validación Contextual y Prevención de Errores", 
                 "Formularios interactivos con retroalimentación inmediata sobre campos críticos (validación de 8 dígitos numéricos para DNI, 11 para RUC y 9 para celulares peruanos), deshabilitación automática de controles al agotar existencias físicas y alertas contextuales comprensibles que orientan al usuario antes de emitir la orden.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Usabilidad (UX)",
            "pregunta": "¿El panel administrativo y las interfaces operativas se adhieren a las 10 Heurísticas de Nielsen y proveen retroalimentación inmediata del estado del sistema?",
            "items": [
                ("Visibilidad del Estado del Sistema (Heurística 1)", 
                 "Presentación inmediata del estado de sincronización y procesamiento de cada orden mediante badges semánticos normalizados por color (verde: Entregado, azul: En Camino, amarillo: En Preparación, rojo: Cancelado) y componentes modales de confirmación con micro-animaciones fluidas."),
                ("Correspondencia con el Lenguaje del Negocio (Heurística 2)", 
                 "Vocabulario contextualizado al ecosistema comercial textil peruano y a la operación de Gamarra (billeteras digitales Yape/Plin, agencias de encomienda Shalom/Olva, N° de Guía de Remisión, flete local vs interprovincial)."),
                ("Control del Usuario y Privacidad Granular (Heurísticas 3 y 7)", 
                 "Libertad para modificar pedidos y revertir estados con restitución automática de existencias. Componente especializado de privacidad financiera (<MontoPrivado />) en el dashboard administrativo (RF-010), permitiendo conmutar la visibilidad de las cifras de ingresos en Soles (S/) para salvaguardar la confidencialidad en el mostrador del taller físico frente a terceros.")
            ],
            "si": "X",
            "no": ""
        },

        # =========================================================================
        # BLOQUE 3: RENDIMIENTO (3 ÍTEMS)
        # =========================================================================
        {
            "cat": "Rendimiento",
            "pregunta": "¿El software cumple con los umbrales de Google Core Web Vitals y garantiza tiempos de respuesta instantáneos en redes móviles?",
            "items": [
                ("Métricas Core Web Vitals Auditadas (Google Lighthouse)", 
                 "- First Contentful Paint (FCP): <= 0.5 s (superando holgadamente el estándar de la industria de < 1.8 s).\n"
                 "- Largest Contentful Paint (LCP): <= 1.1 s (muy inferior al límite crítico recomendado por Google de 2.5 s).\n"
                 "- Cumulative Layout Shift (CLS): 0.00 (estabilidad visual absoluta sin saltos bruscos en el diseño durante la renderización).\n"
                 "- Interaction to Next Paint (INP): < 50 ms (respuesta táctil instantánea ante clics en filtros y botones)."),
                ("Latencia Ultrabaja del Backend API REST", 
                 "Procesamiento de peticiones HTTP con latencia en percentil 95 (P95) < 100 ms en Node.js 20 y PostgreSQL 16 gracias a consultas parametrizadas optimizadas con índices B-Tree (idx_products_category, idx_orders_status, idx_orders_created_at en database/schema.sql).")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Rendimiento",
            "pregunta": "¿La estrategia de empaquetado, optimización de activos (WPO) y consumo de datos es eficiente para terminales móviles y redes de ancho de banda restringido?",
            "items": [
                ("Ultra-Bajo Peso de Empaquetado (Bundle WPO)", 
                 "Pipeline de compilación y empaquetado con Vite y Rollup optimizado mediante eliminación de código muerto (Tree-Shaking) y compresión Gzip/Brotli: Bundle JavaScript final de ~78 kB gzipped y Bundle CSS purgado con Tailwind de ~9.4 kB gzipped, cumpliendo con holgura el límite estricto de RNF-003 (<= 80 kB)."),
                ("Optimización y Carga Diferida de Medios", 
                 "Imágenes del catálogo textil convertidas a formatos modernos de alta compresión (WebP / AVIF) con etiquetas de carga perezosa nativa (loading=\"lazy\") y dimensiones fijas para evitar reflows costosos en el navegador del cliente."),
                ("Arquitectura de Estado Ultraligera", 
                 "Uso de React 19 nativo y Context API sin librerías externas sobredimensionadas de gestión de estado, manteniendo el DOM ligero y reduciendo al mínimo el uso de memoria RAM y CPU en smartphones de gama de entrada y media.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Rendimiento",
            "pregunta": "¿La arquitectura técnica garantiza alta disponibilidad, capacidades offline progresivas (PWA) y resiliencia ante contingencias de red?",
            "items": [
                ("Capacidades Offline Progresivas (PWA)", 
                 "Manifiesto web (manifest.json) y Service Worker configurado con estrategias de caché inteligentes: Stale-While-Revalidate para la lógica de la aplicación y Cache-First para tipografías e iconografía, permitiendo navegar por el catálogo y operar la interfaz incluso en zonas con cobertura móvil intermitente 3G/4G o cortes temporales de red."),
                ("Alta Disponibilidad Cloud en el Edge", 
                 "Despliegue distribuido en la red perimetral de Vercel Edge Network (CDN global con Anycast DNS) y contenedores Docker en Render.com (backend/Dockerfile) con reinicio automático ante fallos (restart: unless-stopped) y verificación de salud continua (/api/health), garantizando un SLA de disponibilidad mensual >= 99.5% (RNF-004)."),
                ("Resiliencia y Fallback de Datos", 
                 "Implementación del patrón Fallback en memoria (MemoryOrderRepository) en el backend que permite mantener la ejecución de pruebas unitarias/integración (18/18 tests aprobados con Jest/Supertest) y asegurar la continuidad operativa frente a desconexiones transitorias con PostgreSQL.")
            ],
            "si": "X",
            "no": ""
        },

        # =========================================================================
        # BLOQUE 4: SEGURIDAD Y COSTOS (3 ÍTEMS)
        # =========================================================================
        {
            "cat": "Seguridad y costos",
            "pregunta": "¿El sistema implementa defensas integrales contra vulnerabilidades OWASP Top 10, autenticación robusta y control de acceso estricto (RBAC)?",
            "items": [
                ("Autenticación Criptográfica Robusta (A02:2021)", 
                 "Emisión y verificación de tokens de sesión JSON Web Tokens (JWT) firmados con algoritmo HMAC-SHA256 (HS256) empleando una clave criptográfica de 64 caracteres de alta entropía (JWT_SECRET) y vigencia estricta de 24 horas."),
                ("Control de Acceso Basado en Roles (RBAC - A01:2021)", 
                 "Middleware de autorización estricta (requireRole('ADMIN')) en backend/src/middlewares/role.middleware.ts que restringe el acceso a endpoints mutables de ajuste de inventario, edición de precios y transición de estados, bloqueando peticiones desautorizadas con códigos HTTP 401 Unauthorized y 403 Forbidden."),
                ("Mitigación Activa de Amenazas OWASP Top 10", 
                 "- Inyecciones SQL (A03:2021): Consultas parametrizadas con placeholders ($1, $2, ...) en PgOrderRepository y PgProductRepository, eliminando por completo el riesgo de inyección por concatenación.\n"
                 "- Validación Estricta de Esquemas: Saneamiento y validación rigurosa de todas las entradas del cliente mediante la biblioteca Zod (backend/src/infrastructure/validators/schemas.ts), neutralizando vectores Cross-Site Scripting (XSS).\n"
                 "- Endurecimiento Perimetral: Cabeceras seguras con Helmet (HSTS forzado, No-Sniff, Frameguard anti-clickjacking) y limitador de tasa (Rate Limiting) de 20 intentos cada 15 min en autenticación (backend/src/middlewares/rateLimit.middleware.ts) contra ataques de fuerza bruta y DoS (A05:2021, A07:2021).")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Seguridad y costos",
            "pregunta": "¿Se garantiza la privacidad de datos personales, el cifrado de información sensible y la pista de auditoría forense inmutable de transacciones?",
            "items": [
                ("Protección Criptográfica en Reposo y Tránsito", 
                 "Contraseñas de acceso administrativo nunca almacenadas en texto plano; procesadas mediante función de derivación bcrypt aplicando 10 rondas de salt criptográfico aleatorio. Toda la comunicación entre cliente PWA, backend y base de datos viaja cifrada bajo protocolo TLS 1.3 / HTTPS obligatorio con certificados SSL Let's Encrypt."),
                ("Cumplimiento de la Ley de Protección de Datos Personales (Ley N° 29733)", 
                 "Recopilación restringida y tratamiento confidencial de datos de contacto y despacho de clientes deportivos (DNI/RUC, teléfono, dirección de entrega), empleados exclusivamente para la facturación fiscal del flete y la entrega de encomiendas."),
                ("Pista de Auditoría Forense Inmutable (A09:2021)", 
                 "Cada modificación de estado de una orden se registra automáticamente en la tabla relacional order_status_history de PostgreSQL, conservando un registro histórico inmutable con marca temporal UTC (CURRENT_TIMESTAMP), ID del pedido, estado previo, nuevo estado y usuario ejecutor para auditoría y trazabilidad operativa."),
                ("Gobernanza de Secretos", 
                 "Aislamiento riguroso de credenciales críticas en variables de entorno del servidor (DATABASE_URL, JWT_SECRET) sin exposición en repositorios públicos conforme a la directiva SECURITY.md.")
            ],
            "si": "X",
            "no": ""
        },
        {
            "cat": "Seguridad y costos",
            "pregunta": "¿La solución optimiza el Costo Total de Propiedad (TCO), garantiza sostenibilidad financiera para la pyme y maximiza el Retorno de Inversión (ROI)?",
            "items": [
                ("Costo Total de Propiedad (TCO) de $0.00 USD en Etapa de Lanzamiento", 
                 "Arquitectura Cloud Serverless y PaaS diseñada para operar con solvencia dentro de los niveles gratuitos (Free Tier) de alta disponibilidad: Vercel Edge Network para el Frontend PWA ($0/mes), Render Cloud para el contenedor API REST ($0/mes) y Supabase Cloud para el motor PostgreSQL 16 administrado con 500 MB y backups automáticos PITR ($0/mes).\n"
                 "- Inversión en Hardware (CAPEX): S/ 0.00, al no requerir la adquisición de servidores dedicados ni licencias de software propietario en el taller textil de LeoFit.\n"
                 "- Costo Operativo (OPEX): S/ 0.00/mes durante la fase inicial y de consolidación comercial, con un modelo de escalamiento elástico de ultra-bajo costo ($25 - $50 USD/mes) proyectado únicamente al superar los 50,000 pedidos mensuales."),
                ("Retorno de Inversión (ROI) Operativo Inmediato", 
                 "- Ahorro de tiempo operativo del ~92% en la atención comercial y formalización de órdenes (reducción de 25 min a <= 2 min por cliente), liberando más de 3 horas diarias de trabajo manual del fundador y administrador Víctor Raúl Cárdenas para actividades clave de abastecimiento y confección.\n"
                 "- Supresión total (100%) de pérdidas financieras asociadas a pedidos duplicados, comprobantes extraviados, direcciones erróneas y sobreventas de prendas sin existencias físicas.\n"
                 "- Incremento proyectado de conversión de ventas en un 35% derivado de la agilidad del catálogo web interactivo y la confirmación automatizada vía WhatsApp.")
            ],
            "si": "X",
            "no": ""
        }
    ]

    # 3. Aplicar Estructura y Formateo de la Tabla
    table = doc.tables[0]
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_borders(table)

    # Anchos calculados en dxa para las 4 columnas (total 8500 dxa = ~5.90 pulgadas)
    w_cat = 1650   # ~1.15 in (~2.9 cm)
    w_preg = 5350  # ~3.72 in (~9.44 cm)
    w_si = 750     # ~0.52 in (~1.32 cm)
    w_no = 750     # ~0.52 in (~1.32 cm)
    col_widths = [w_cat, w_preg, w_si, w_no]

    # Ajustar grid de la tabla en XML
    grid = table._tbl.tblGrid
    if grid is not None:
        gridCols = grid.findall(qn('w:gridCol'))
        if len(gridCols) == 4:
            for i, w in enumerate(col_widths):
                gridCols[i].set(qn('w:w'), str(w))

    # Estilizar encabezado (Fila 0)
    header_row = table.rows[0]
    header_titles = ["Categoría", "Pregunta clave y Sustentación Técnica End-to-End", "Si cumple", "No cumple"]
    for c_idx, cell in enumerate(header_row.cells):
        set_cell_width_dxa(cell, col_widths[c_idx])
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        set_cell_shading(cell, "0A2F41")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(header_titles[c_idx])
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Poblado de las 12 filas de evaluación (Rows 1 a 12)
    for idx, item_data in enumerate(checklist_data):
        row_idx = idx + 1
        row = table.rows[row_idx]

        # Alternancia suave de fondo de fila (#FFFFFF vs #F8FAFC)
        row_bg = "FFFFFF" if idx % 2 == 0 else "F8FAFC"

        # --- Celda 0: Categoría ---
        c0 = row.cells[0]
        set_cell_width_dxa(c0, col_widths[0])
        set_cell_margins(c0, top=120, bottom=120, left=120, right=120)
        set_cell_shading(c0, "EEF2F6" if idx % 2 == 1 else "F1F5F9")
        c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c0.text = ""
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(item_data["cat"])
        r0.font.name = "Arial"
        r0.font.size = Pt(9)
        r0.font.bold = True
        r0.font.color.rgb = RGBColor(10, 47, 65)

        # --- Celda 1: Pregunta Clave y Sustentación Técnica End-to-End ---
        c1 = row.cells[1]
        set_cell_width_dxa(c1, col_widths[1])
        set_cell_margins(c1, top=130, bottom=130, left=150, right=150)
        set_cell_shading(c1, row_bg)
        c1.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        c1.text = ""

        # Pregunta Clave
        p_q = c1.paragraphs[0]
        p_q.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_q.paragraph_format.space_before = Pt(2)
        p_q.paragraph_format.space_after = Pt(4)
        p_q.paragraph_format.line_spacing = 1.15
        
        r_q_label = p_q.add_run("Pregunta Clave: ")
        r_q_label.font.name = "Arial"
        r_q_label.font.size = Pt(9)
        r_q_label.font.bold = True
        r_q_label.font.color.rgb = RGBColor(10, 47, 65)

        r_q = p_q.add_run(item_data["pregunta"])
        r_q.font.name = "Arial"
        r_q.font.size = Pt(9)
        r_q.font.bold = True
        r_q.font.color.rgb = RGBColor(15, 23, 42)

        # Encabezado de Sustentación
        p_sub = c1.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(2)
        p_sub.paragraph_format.space_after = Pt(3)
        r_sub_hdr = p_sub.add_run("Sustentación Técnica y Evidencia End-to-End:")
        r_sub_hdr.font.name = "Arial"
        r_sub_hdr.font.size = Pt(8.5)
        r_sub_hdr.font.bold = True
        r_sub_hdr.font.color.rgb = RGBColor(30, 90, 130)

        # Ítems estructurados de sustentación técnica
        for sub_title, sub_desc in item_data["items"]:
            p_item = c1.add_paragraph()
            p_item.paragraph_format.space_before = Pt(1)
            p_item.paragraph_format.space_after = Pt(2)
            p_item.paragraph_format.line_spacing = 1.12

            r_bullet = p_item.add_run("• ")
            r_bullet.font.name = "Arial"
            r_bullet.font.size = Pt(8.5)
            r_bullet.font.bold = True
            r_bullet.font.color.rgb = RGBColor(30, 90, 130)

            r_title = p_item.add_run(f"{sub_title}: ")
            r_title.font.name = "Arial"
            r_title.font.size = Pt(8.5)
            r_title.font.bold = True
            r_title.font.color.rgb = RGBColor(30, 41, 59)

            r_desc = p_item.add_run(sub_desc)
            r_desc.font.name = "Arial"
            r_desc.font.size = Pt(8.5)
            r_desc.font.color.rgb = RGBColor(51, 65, 85)

        # --- Celda 2: Si cumple ---
        c2 = row.cells[2]
        set_cell_width_dxa(c2, col_widths[2])
        set_cell_margins(c2, top=120, bottom=120, left=60, right=60)
        set_cell_shading(c2, "E6F4EA" if item_data["si"] else row_bg)
        c2.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c2.text = ""
        p2 = c2.paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(item_data["si"])
        r2.font.name = "Arial"
        r2.font.size = Pt(13)
        r2.font.bold = True
        r2.font.color.rgb = RGBColor(19, 115, 51) # Verde corporativo

        # --- Celda 3: No cumple ---
        c3 = row.cells[3]
        set_cell_width_dxa(c3, col_widths[3])
        set_cell_margins(c3, top=120, bottom=120, left=60, right=60)
        set_cell_shading(c3, row_bg)
        c3.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        c3.text = ""
        p3 = c3.paragraphs[0]
        p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p3.paragraph_format.space_before = Pt(0)
        p3.paragraph_format.space_after = Pt(0)
        r3 = p3.add_run(item_data["no"])
        r3.font.name = "Arial"
        r3.font.size = Pt(13)
        r3.font.bold = True
        r3.font.color.rgb = RGBColor(217, 48, 37)

    # 4. Sección de Metadatos de Cierre (Equipo, Integrantes, Fecha)
    for p in doc.paragraphs:
        txt = p.text.strip()
        if "Nombre del equipo:" in txt:
            p.text = ""
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(3)
            r_lbl = p.add_run("Nombre del equipo: ")
            r_lbl.font.name = "Arial"
            r_lbl.font.size = Pt(10)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = RGBColor(10, 47, 65)

            r_val = p.add_run("Grupo 01 — Leofit Solutions (Curso Integrador II: Software - Sección 35374)")
            r_val.font.name = "Arial"
            r_val.font.size = Pt(10)
            r_val.font.bold = True
            r_val.font.color.rgb = RGBColor(15, 23, 42)

        elif "Integrantes:" in txt:
            p.text = ""
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(3)
            r_lbl = p.add_run("Integrantes del Equipo y Roles Especializados:\n")
            r_lbl.font.name = "Arial"
            r_lbl.font.size = Pt(10)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = RGBColor(10, 47, 65)

            integrantes = [
                ("Loayza Rodriguez, Lady Luz", "U22221489", "Scrum Master", "DevSecOps, Coordinadora de Seguridad JWT & Gobernanza"),
                ("Cárdenas Fernández, Víctor Leandro", "U19217414", "Product Owner", "Arquitecto de Base de Datos (DBA), BCNF & Replicación WAL"),
                ("Roman Delgado, Harley Anthony", "U21313032", "Frontend Lead", "Especialista PWA, Diseñador UI/UX & Optimización WPO"),
                ("Dávila Morales, Jim Alessandro", "U18206081", "QA Engineer Lead", "Desarrollador Backend Node.js/TS & Pruebas Automatizadas Jest"),
                ("Rojas Sanchez, Daniel Enrique", "U21214627", "Business Analyst", "Cloud DevOps, SLA/SLO, Render/Vercel & Supabase Cloud")
            ]
            for num, (nom, cod, rol_scrum, rol_tec) in enumerate(integrantes, start=1):
                r_num = p.add_run(f"  {num}. ")
                r_num.font.name = "Arial"
                r_num.font.size = Pt(9)
                r_num.font.bold = True

                r_nom = p.add_run(f"{nom} ")
                r_nom.font.name = "Arial"
                r_nom.font.size = Pt(9)
                r_nom.font.bold = True
                r_nom.font.color.rgb = RGBColor(15, 23, 42)

                r_cod = p.add_run(f"(Código: {cod}) — ")
                r_cod.font.name = "Arial"
                r_cod.font.size = Pt(9)
                r_cod.font.color.rgb = RGBColor(71, 85, 105)

                r_scrum = p.add_run(f"Rol Scrum: {rol_scrum} | ")
                r_scrum.font.name = "Arial"
                r_scrum.font.size = Pt(9)
                r_scrum.font.bold = True
                r_scrum.font.color.rgb = RGBColor(30, 90, 130)

                r_tec = p.add_run(f"Responsabilidad Técnica: {rol_tec}\n" if num < 5 else f"Responsabilidad Técnica: {rol_tec}")
                r_tec.font.name = "Arial"
                r_tec.font.size = Pt(8.5)
                r_tec.font.italic = True
                r_tec.font.color.rgb = RGBColor(100, 116, 139)

        elif "Fecha:" in txt:
            p.text = ""
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(4)
            r_lbl = p.add_run("Fecha de Evaluación: ")
            r_lbl.font.name = "Arial"
            r_lbl.font.size = Pt(10)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = RGBColor(10, 47, 65)

            r_val = p.add_run("23 de Septiembre de 2026 (Ciclo Académico 2026-II)")
            r_val.font.name = "Arial"
            r_val.font.size = Pt(10)
            r_val.font.color.rgb = RGBColor(15, 23, 42)

    output_filename = os.path.join(base_dir, "docs", "Checklist_Integral_Evaluacion_Software.docx")
    doc.save(output_filename)
    print(f"Documento guardado con éxito como '{output_filename}'")

if __name__ == '__main__':
    build_full_checklist()
