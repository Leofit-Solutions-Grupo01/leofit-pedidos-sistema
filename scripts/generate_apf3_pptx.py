# -*- coding: utf-8 -*-
"""
Generador Maestro de la Presentación de Alta Ingeniería APF3 (LeoFit PWA)
Audiencia: Perfiles Técnicos Senior, MBAs en Ingeniería y Arquitectura de Datos.
- Enfoque: Código real, contratos, esquemas DDL, garantías ACID, criptografía y telemetría.
- Formato: PowerPoint (.pptx) nativo de 13 láminas (~10 minutos de sustentación).
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.oxml.ns import qn

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PPTX = os.path.join(REPO, "docs", "01_entregable_final_apf3", "presentacion_sustentacion", "APF3_LEOFIT_Presentacion.pptx")
OUT_PDF = os.path.join(REPO, "docs", "01_entregable_final_apf3", "presentacion_sustentacion", "APF3_LEOFIT_Presentacion.pdf")

def C(h): return RGBColor.from_string(h)

# Paleta Técnica Profesional
NAVY    = "1E3A8A"  # Azul Primario Institucional
DARK    = "0F172A"  # Slate 900
CODEBG  = "090D16"  # Slate 950 Terminal
ORANGE  = "C2410C"  # Acento Operativo
GREEN   = "15803D"  # Éxito / 200 OK
LGREEN  = "DCFCE7"  # Verde Claro Fondo
RED     = "B91C1C"  # Error / 403 / Alerta
LRED    = "FEE2E2"  # Rojo Claro Fondo
GRAY    = "475569"  # Slate 600
LGRAY   = "F8FAFC"  # Slate 50 Fondo
BLUE    = "2563EB"  # Azul Eléctrico
LBLUE   = "EFF6FF"  # Azul Claro Fondo
AMBER   = "B45309"  # Amarillo/Ámbar
LAMBER  = "FEF3C7"  # Ámbar Claro Fondo
WHITE   = "FFFFFF"

FONT_MAIN = "Calibri"
FONT_CODE = "Consolas"
TOTAL_SLIDES = 13

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]

def txt(s, x, y, w, h, text, size=16, bold=False, color=DARK, align="l", anchor="t", italic=False, font=FONT_MAIN):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        r = p.add_run()
        r.text = line
        r.font.size, r.font.bold, r.font.italic, r.font.name = Pt(size), bold, italic, font
        r.font.color.rgb = C(color)
    return tb

def box(s, x, y, w, h, text="", fill=LBLUE, line=None, size=15, bold=False, color=DARK,
        align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.5, radius=0.08, font=FONT_MAIN):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = radius
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = C(fill)
    if line:
        sh.line.color.rgb = C(line)
        sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    tf = sh.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    for i, line_t in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        r = p.add_run()
        r.text = line_t
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, font
        r.font.color.rgb = C(color)
    return sh

def arrow(s, x1, y1, x2, y2, color=GRAY, w=2.5, dash=False):
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    cn.line.color.rgb = C(color)
    cn.line.width = Pt(w)
    ln = cn.line._get_or_add_ln()
    if dash:
        d = ln.makeelement(qn("a:prstDash"), {"val": "dash"})
        ln.append(d)
    ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    return cn

def code_box(s, x, y, w, h, title, code_lines, font_size=10.0):
    """Renderiza un bloque de código técnico estilo terminal oscuro."""
    # Contenedor exterior
    box(s, x, y, w, h, "", fill=CODEBG, line="334155", lw=1.5, radius=0.03)
    # Barra superior del terminal
    box(s, x, y, w, 0.36, "", fill="1E293B", line=None, radius=0.03)
    # Botones terminal
    box(s, x + 0.12, y + 0.12, 0.12, 0.12, "", fill="EF4444", shape=MSO_SHAPE.OVAL)
    box(s, x + 0.30, y + 0.12, 0.12, 0.12, "", fill="F59E0B", shape=MSO_SHAPE.OVAL)
    box(s, x + 0.48, y + 0.12, 0.12, 0.12, "", fill="10B981", shape=MSO_SHAPE.OVAL)
    txt(s, x + 0.70, y + 0.05, w - 0.75, 0.28, title, size=11, bold=True, color="94A3B8", font=FONT_CODE)
    
    # Texto de código
    tb = s.shapes.add_textbox(Inches(x + 0.12), Inches(y + 0.40), Inches(w - 0.24), Inches(h - 0.44))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    
    for i, line in enumerate(code_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        
        # Coloración sintáctica elemental
        stripped = line.strip()
        if stripped.startswith("--") or stripped.startswith("//") or stripped.startswith("/*"):
            col = "64748B"  # Comentario gris
        elif any(k in line for k in ["SELECT", "FROM", "WHERE", "UPDATE", "INSERT", "CREATE", "BEGIN", "COMMIT", "ROLLBACK", "TRIGGER"]):
            col = "38BDF8"  # SQL keyword azul cielo
        elif any(k in line for k in ["interface", "class", "async", "await", "const", "return", "throw", "try", "catch"]):
            col = "F43F5E"  # JS keyword rosa
        elif any(k in line for k in ["FOR UPDATE", "SERIALIZABLE", "READ COMMITTED"]):
            col = "34D399"  # Aislamiento verde esmeralda
        elif any(k in line for k in ["40001", "40P01", "403", "401"]):
            col = "F59E0B"  # Códigos de error naranja
        else:
            col = "E2E8F0"  # Texto plano
            
        r = p.add_run()
        r.text = line
        r.font.name = FONT_CODE
        r.font.size = Pt(font_size)
        r.font.color.rgb = C(col)
    return tb

def base_slide(num, title, subtitle, presenter, notes):
    s = prs.slides.add_slide(BLANK)
    # Título principal
    txt(s, 0.5, 0.25, 12.3, 0.65, title, size=28, bold=True, color=NAVY, anchor="m")
    # Barra de acento
    box(s, 0.55, 0.95, 1.4, 0.06, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    # Subtítulo técnico
    txt(s, 0.5, 1.05, 12.3, 0.45, subtitle, size=16, color=GRAY, anchor="m")
    # Footer institucional
    txt(s, 0.5, 7.10, 8.5, 0.3, "LeoFit PWA · Memoria Técnica APF3 · UTP Curso Integrador II (100000S12F) · 2026-I", size=10, color="94A3B8")
    txt(s, 9.0, 7.10, 3.8, 0.3, f"Defiende: {presenter}  |  Lámina {num} / {TOTAL_SLIDES}", size=10, color="94A3B8", align="r")
    s.notes_slide.notes_text_frame.text = notes
    return s

print("Generando presentación técnica de alta fidelidad...")
# =====================================================================
# SCRIPT COMPLETO DE GENERACIÓN DE PRESENTACIÓN DE ALTA INGENIERÍA
# =====================================================================

# ---------------------------------------------------------------------
# LÁMINA 1: PORTADA & FICHA TÉCNICA DE ARQUITECTURA
# ---------------------------------------------------------------------
s1 = prs.slides.add_slide(BLANK)
s1.background.fill.solid()
s1.background.fill.fore_color.rgb = C(DARK)
box(s1, 0, 0, 0.40, 7.5, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)

txt(s1, 0.9, 0.55, 11.8, 0.45, "SUSTENTACIÓN TÉCNICA FINAL · AVANCE DE PROYECTO FINAL 3 (APF3)", size=16, bold=True, color="FDBA74")
txt(s1, 0.9, 1.05, 11.8, 1.15, "LeoFit PWA — Arquitectura y Datos", size=54, bold=True, color=WHITE)
txt(s1, 0.9, 2.15, 11.8, 0.55, "Sistema Web PWA de Gestión de Pedidos Multicanal y Control Transaccional de Inventario", size=22, color="CBD5E1")

# Panel de Especificación Técnica del Stack
box(s1, 0.9, 2.85, 11.6, 1.45, "", fill="1E293B", line="334155", lw=1.5, radius=0.03)
txt(s1, 1.1, 2.95, 11.2, 0.35, "ESPECIFICACIÓN FORMAL DE INGENIERÍA Y ENTORNO DE PRODUCCIÓN", size=13, bold=True, color="38BDF8")

stack_cols = [
    ("Backend Runtime", "Node.js 20 LTS · Express\nTypeScript 5.6 (Strict Mode)\nClean Architecture (3 Capas)"),
    ("Base de Datos", "PostgreSQL 16 Relacional\nNormalización 3FN / BCNF\nLocks Pesimistas + Triggers"),
    ("Frontend & PWA", "React 19 · Vite 6 · Tailwind 4\nService Worker (PWA Offline)\njsPDF Client-Side Engine"),
    ("Seguridad & QA", "OWASP Top 10 · JWT fail-fast\n194 Pruebas (Jest + Vitest)\nIstanbul Coverage 76.16 %")
]
for i, (head, desc) in enumerate(stack_cols):
    x = 1.1 + i * 2.8
    box(s1, x, 3.30, 2.65, 0.88, "", fill="0F172A", line="475569", lw=1.0, radius=0.03)
    txt(s1, x + 0.1, 3.35, 2.45, 0.28, head, size=12, bold=True, color="FDBA74")
    txt(s1, x + 0.1, 3.63, 2.45, 0.50, desc, size=10, color="CBD5E1")

# Chips de Métricas Auditadas
chips_s1 = [
    ("38.2 s", "Captura de Pedido (-98.6%)"),
    ("0.0 %", "Sobreventas (ACID Lock)"),
    ("194 / 194", "Tests Aprobados (0 Fallos)"),
    ("88.5 / 100", "Usabilidad SUS (Grado A)")
]
for i, (big, sub) in enumerate(chips_s1):
    x = 0.9 + i * 2.95
    box(s1, x, 4.45, 2.75, 1.15, "", fill="111827", line=NAVY, lw=2.0)
    txt(s1, x, 4.52, 2.75, 0.60, big, size=32, bold=True, color="38BDF8", align="c", anchor="m")
    txt(s1, x, 5.15, 2.75, 0.38, sub, size=13, color="94A3B8", align="c")

# Roles Técnicos
team_s1 = [
    ("Lady L. Loayza R.", "Scrum Master / DevSecOps\nOWASP · JWT · Criptografía"),
    ("Víctor L. Cárdenas F.", "Product Owner / DBA\nPostgreSQL 16 · ACID · 3FN"),
    ("Harley A. Roman D.", "Frontend Lead / UI-UX\nReact 19 PWA · ISO 25010"),
    ("Jim A. Dávila M.", "QA Lead / Backend\n194 Tests · Istanbul · CI/CD"),
    ("Daniel E. Rojas S.", "Analista / Cloud DevOps\nk6 Stress · Multi-Cloud · DRP")
]
for i, (nom, rol) in enumerate(team_s1):
    x = 0.9 + i * 2.36
    box(s1, x, 5.80, 2.22, 1.25, "", fill="0F172A", line="334155", lw=1.2, radius=0.03)
    txt(s1, x + 0.05, 5.88, 2.12, 0.40, nom, size=13, bold=True, color=WHITE, align="c")
    txt(s1, x + 0.05, 6.30, 2.12, 0.68, rol, size=11, color="94A3B8", align="c")

s1.notes_slide.notes_text_frame.text = (
    "[Lady Loayza · 45 s] Estimados miembros del jurado evaluador, ingenieros y arquitectos de datos: Muy buenas tardes. "
    "Iniciamos la defensa técnica de LeoFit PWA, sistema transaccional de pedidos y control de inventario multicanal para una microempresa textil en Gamarra. "
    "En los próximos 10 minutos demostraremos que el sistema no es un prototipo conceptual: opera en producción sobre un clúster PostgreSQL 16 con "
    "aislamiento transaccional ACID, bloqueo pesimista contra sobreventas, 194 pruebas automatizadas verificadas con 76.16% de cobertura de dominio, "
    "y certificación de calidad bajo la norma ISO/IEC 25010 con un puntaje SUS de 88.5."
)

# ---------------------------------------------------------------------
# LÁMINA 2: DIAGNÓSTICO OPERATIVO & ANÁLISIS DE BRECHAS (AS-IS vs TO-BE)
# ---------------------------------------------------------------------
s2 = base_slide(2, "Diagnóstico Cuantitativo: Fricción Operativa y Brechas",
                "Modelado de Procesos BPMN 2.0 y Estudio de Campo UAT en Gamarra (Capítulo 2)", "Daniel Rojas",
                "[Daniel Rojas · 45 s] LeoFit enfrentaba pérdidas severas por operar sin canal transaccional: pedidos manuales en WhatsApp con "
                "latencias de 45 a 120 minutos, 14.2% de errores en despachos y 22% de fuga de ventas por sobreventas al vender prendas ya agotadas. "
                "Con LeoFit PWA, el pedido se captura en 38.2 segundos promedio mediante validación reactiva de existencias, los errores cayeron al 0.4% "
                "gracias a rótulos generados por código, y la sobreventa se erradicó a 0.0% mediante bloqueos pesimistas en base de datos.")

# Panel Izquierdo: Fricción AS-IS
box(s2, 0.5, 1.70, 5.9, 4.45, "", fill=LRED, line=RED, lw=2.0)
txt(s2, 0.7, 1.80, 5.5, 0.40, "PROCESO INFORMAL PREVIO (BPMN 2.0 AS-IS)", size=16, bold=True, color=RED)

asis_points = [
    ("Canal No Estructurado", "Atención dispersa por chats informales de WhatsApp; sin validación de identidad."),
    ("Latencia de Ciclo: 45–120 min", "El operador debe suspender la atención para verificar físicamente estantes en almacén."),
    ("Tasa de Error en Despacho: 14.2%", "Transcripción manual en libreta de papel: tallas trocadas, fletes mal calculados."),
    ("Fuga Comercial: 22% por Quiebres", "Sobreventa de prendas agotadas; fricción con el cliente y reclamos por devoluciones."),
    ("Cero Trazabilidad Fiscal", "Cotejo visual de capturas bancarias falsificables; sin comprobantes SUNAT.")
]
for i, (tit, des) in enumerate(asis_points):
    y = 2.30 + i * 0.74
    box(s2, 0.7, y, 5.5, 0.65, "", fill=WHITE, line=RED, lw=1.0, radius=0.03)
    txt(s2, 0.8, y + 0.05, 5.3, 0.28, "✖ " + tit, size=13, bold=True, color=RED)
    txt(s2, 0.8, y + 0.32, 5.3, 0.28, des, size=11, color=DARK)

# Panel Derecho: Solución Determinística TO-BE
box(s2, 6.9, 1.70, 5.9, 4.45, "", fill=LGREEN, line=GREEN, lw=2.0)
txt(s2, 7.1, 1.80, 5.5, 0.40, "SISTEMA TRANSACCIONAL LEOFIT PWA (TO-BE)", size=16, bold=True, color=GREEN)

tobe_points = [
    ("Catálogo Reactivo con Stock en Vivo", "Variantes por talla y color; validación de existencias antes de ingresar al carrito."),
    ("Tiempo de Captura: 38.2 segundos", "Checkout guiado en 3 pasos con autollenado de clientes recurrentes (-98.6%)."),
    ("Tasa de Error en Despacho: 0.4%", "Generación determinística de rótulos con código QR para Olva Courier / Shalom (-97.2%)."),
    ("Sobreventa de Existencias: 0.0%", "Bloqueo pesimista `SELECT FOR UPDATE` + trigger atómico en PostgreSQL 16."),
    ("Integración Externa Verificada", "Notificación WhatsApp con enlace #LFT-XXX y validación de padrones SUNAT/RENIEC.")
]
for i, (tit, des) in enumerate(tobe_points):
    y = 2.30 + i * 0.74
    box(s2, 7.1, y, 5.5, 0.65, "", fill=WHITE, line=GREEN, lw=1.0, radius=0.03)
    txt(s2, 7.2, y + 0.05, 5.3, 0.28, "✔ " + tit, size=13, bold=True, color=GREEN)
    txt(s2, 7.2, y + 0.32, 5.3, 0.28, des, size=11, color=DARK)

# Tabla Resumen de Métricas Inferiores
metrics_bar = [
    ("Tiempo por Pedido", "45 a 120 min", "38.2 s", "-98.6 %", GREEN),
    ("Errores de Despacho", "14.2 %", "0.4 %", "-97.2 %", GREEN),
    ("Sobreventa de Stock", "Frecuentes (22%)", "0.0 %", "CERO", GREEN),
    ("Disponibilidad de Datos", "Papel / Local", "Nube TLS 1.3", "100 %", BLUE)
]
for i, (var, pre, post, imp, col) in enumerate(metrics_bar):
    x = 0.5 + i * 3.16
    box(s2, x, 6.25, 3.00, 0.70, f"{var}: {post} ({imp})", fill=WHITE, line=col, lw=2.0, size=13, bold=True, color=col)

# ---------------------------------------------------------------------
# LÁMINA 3: ARQUITECTURA C4 NIVEL 2 & CLEAN ARCHITECTURE (DIP)
# ---------------------------------------------------------------------
s3 = base_slide(3, "Arquitectura de Software: C4 Nivel 2 y Clean Architecture",
                "Desacoplamiento Estructural, Inversión de Dependencias y Repository Factory (Capítulo 6)", "Víctor Cárdenas",
                "[Víctor Cárdenas · 50 s] La arquitectura se modeló bajo el estándar C4 Nivel 2 en tres contenedores desacoplados. "
                "Aplicamos el Principio de Inversión de Dependencias (DIP) mediante el patrón Repository Factory. "
                "Los casos de uso de la capa de dominio dependen estrictamente de interfaces abstractas como IOrderRepository. "
                "Esto permite que las 194 pruebas automatizadas corran en memoria en milisegundos con MemoryOrderRepository, "
                "mientras en producción inyectamos PgOrderRepository conectado al pool nativo de PostgreSQL 16 con SSL.")

# Columna Izquierda: Diagrama Arquitectónico C4
box(s3, 0.5, 1.70, 5.8, 5.25, "", fill=LBLUE, line=BLUE, lw=2.0)
txt(s3, 0.7, 1.80, 5.4, 0.35, "MODELO DE CONTENEDORES (C4 NIVEL 2)", size=16, bold=True, color=NAVY)

# Contenedor 1: PWA
box(s3, 0.7, 2.25, 5.4, 1.25, "", fill=WHITE, line=BLUE, lw=1.5, radius=0.03)
txt(s3, 0.85, 2.30, 5.1, 0.30, "Contenedor 1: Frontend SPA / PWA (React 19 + TypeScript)", size=13, bold=True, color=NAVY)
txt(s3, 0.85, 2.60, 5.1, 0.80, "• Empaquetador: Vite 6 · Estilos: Tailwind CSS 4\n• Estado Global: AppContext con caché optimista en memoria\n• PWA: Service Worker con estrategia Network-First para catálogo\n• Despliegue: GitHub Pages Edge CDN (TLS 1.3)", size=11, color=DARK)

arrow(s3, 3.4, 3.50, 3.4, 3.80, color=NAVY, w=3.0)
txt(s3, 3.5, 3.52, 2.5, 0.25, "HTTPS / JSON + JWT Bearer", size=10, bold=True, color=NAVY)

# Contenedor 2: API REST
box(s3, 0.7, 3.80, 5.4, 1.45, "", fill=WHITE, line=GREEN, lw=1.5, radius=0.03)
txt(s3, 0.85, 3.85, 5.1, 0.30, "Contenedor 2: Backend API RESTful (Node.js 20 LTS + Express)", size=13, bold=True, color=GREEN)
txt(s3, 0.85, 4.15, 5.1, 1.00, "• 27 Endpoints RESTful con formato Envelope JSON estandarizado\n• Middlewares: Helmet, Rate-Limit, Zod Validator, JWT Fail-Fast\n• Clean Architecture: Controladores → Casos de Uso → Repositorios\n• Runtime: Contenedor Docker desplegado en Render Web Service", size=11, color=DARK)

arrow(s3, 3.4, 5.25, 3.4, 5.55, color=AMBER, w=3.0)
txt(s3, 3.5, 5.27, 2.5, 0.25, "TCP / SSL Pool (Port 5432)", size=10, bold=True, color=AMBER)

# Contenedor 3: PostgreSQL
box(s3, 0.7, 5.55, 5.4, 1.25, "", fill=WHITE, line=AMBER, lw=1.5, radius=0.03)
txt(s3, 0.85, 5.60, 5.1, 0.30, "Contenedor 3: Base de Datos Relacional (PostgreSQL 16)", size=13, bold=True, color=AMBER)
txt(s3, 0.85, 5.90, 5.1, 0.80, "• Normalización 3FN/BCNF · 14 Índices B-Tree optimizados\n• Triggers PL/pgSQL para descuento atómico de inventario\n• Conexiones gestionadas con pg.Pool y statement timeouts duros", size=11, color=DARK)

# Columna Derecha: Código Fuente Real de Clean Architecture
code_s3 = [
    "// 1. Contrato Abstracto en Capa de Dominio (DIP)",
    "export interface IOrderRepository {",
    "  create(dto: CreateOrderDTO, isolation?: IsolationLevel): Promise<Order>;",
    "  findById(id: number): Promise<Order | null>;",
    "  updateStatus(id: number, status: OrderStatus, user: string): Promise<void>;",
    "}",
    "",
    "// 2. Inyector de Dependencias (Repository Factory)",
    "export class RepositoryFactory {",
    "  static getOrderRepository(): IOrderRepository {",
    "    if (process.env.USE_MEMORY_DB === 'true') {",
    "      return new MemoryOrderRepository(); // Mock en memoria (< 15 ms)",
    "    }",
    "    return new PgOrderRepository(dbPool);  // Pool PostgreSQL 16 Real",
    "  }",
    "}",
    "",
    "// 3. Caso de Uso Puro desacoplado de la Infraestructura",
    "export class CreateOrderUseCase {",
    "  constructor(private orderRepo: IOrderRepository) {}",
    "  async execute(dto: CreateOrderDTO): Promise<Order> {",
    "    return await this.orderRepo.create(dto, 'READ COMMITTED');",
    "  }",
    "}"
]
code_box(s3, 6.7, 1.70, 6.1, 5.25, "src/infrastructure/repositories/factory.ts · Inversión de Dependencias (DIP)", code_s3, font_size=10.0)

# ---------------------------------------------------------------------
# LÁMINA 4: ARQUITECTURA DE DATOS: NORMALIZACIÓN 3FN/BCNF EN POSTGRESQL 16
# ---------------------------------------------------------------------
s4 = base_slide(4, "Arquitectura de Datos: Normalización 3FN / BCNF",
                "Integridad Referencial, Restricciones CHECK y Llaves Primarias Compuestas (Capítulo 7)", "Víctor Cárdenas",
                "[Víctor Cárdenas · 45 s] El esquema de persistencia se diseñó en PostgreSQL 16 normalizado formalmente hasta 3FN y BCNF. "
                "Para evitar anomalías de inserción y redundancia textil, separamos products de product_variants, vinculando tallas y colores mediante foreign keys. "
                "Cada variante cuenta con SKU único y restricción matemática CHECK stock >= 0. "
                "Las tablas transaccionales orders y order_items registran auditoría inmutable en order_status_history, mientras invoices almacena los comprobantes fiscales y "
                "idempotency_keys previene duplicidades según el estándar RFC 8785.")

# Columna Izquierda: Esquema Relacional de Tablas Core
box(s4, 0.5, 1.70, 5.8, 5.25, "", fill=LGRAY, line="CBD5E1", lw=1.5, radius=0.03)
txt(s4, 0.7, 1.80, 5.4, 0.35, "ESQUEMA RELACIONAL PRINCIPAL (3FN / BCNF)", size=16, bold=True, color=NAVY)

tables_info = [
    ("products", "id (PK SERIAL), category_id (FK), name, description, is_active"),
    ("product_variants", "id (PK SERIAL), product_id (FK), size_id (FK), color_id (FK), sku (UQ), stock (CHECK >= 0)"),
    ("orders", "id (PK SERIAL), order_number (UQ), client_id (FK), total, status (ENUM)"),
    ("order_items", "id (PK SERIAL), order_id (FK CASCADE), variant_id (FK), quantity, unit_price"),
    ("order_status_history", "id (PK), order_id (FK), previous_status, new_status, changed_by, created_at"),
    ("invoices", "id (PK), order_id (UQ FK), invoice_type, series, number, igv_amount, total"),
    ("idempotency_keys", "key (PK), scope_hash, request_path, status_code, locked_until, expires_at")
]
for i, (tname, tcols) in enumerate(tables_info):
    y = 2.16 + i * 0.58
    box(s4, 0.7, y, 5.4, 0.52, "", fill=WHITE, line=NAVY, lw=1.2, radius=0.03)
    txt(s4, 0.85, y + 0.03, 5.1, 0.24, "TABLE " + tname, size=11.5, bold=True, color=NAVY)
    txt(s4, 0.85, y + 0.26, 5.1, 0.24, tcols, size=9.5, color=DARK)

txt(s4, 0.7, 6.32, 5.4, 0.40, "Integridad: 14 Índices B-Tree optimizan búsquedas por SKU, teléfono y estado.", size=11, bold=True, color=GRAY)

# Columna Derecha: Código SQL DDL Real
code_s4 = [
    "-- database/migrations/001_initial_schema.sql",
    "CREATE TABLE product_variants (",
    "  id SERIAL PRIMARY KEY,",
    "  product_id INT NOT NULL REFERENCES products(id) ON DELETE CASCADE,",
    "  size_id INT NOT NULL REFERENCES sizes(id),",
    "  color_id INT NOT NULL REFERENCES colors(id),",
    "  sku VARCHAR(50) UNIQUE NOT NULL,",
    "  stock INT NOT NULL CHECK (stock >= 0), -- Restricción de Dominio",
    "  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
    ");",
    "",
    "CREATE TABLE orders (",
    "  id SERIAL PRIMARY KEY,",
    "  order_number VARCHAR(30) UNIQUE NOT NULL, -- LEO-YYYYMMDD-NNNNNN",
    "  client_id INT NOT NULL REFERENCES clients(id),",
    "  status order_status_enum NOT NULL DEFAULT 'RECIBIDO',",
    "  total DECIMAL(10,2) NOT NULL CHECK (total >= 0),",
    "  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP",
    ");",
    "",
    "-- Índices B-Tree para consultas concurrentes de alta frecuencia",
    "CREATE INDEX idx_variants_sku ON product_variants(sku);",
    "CREATE INDEX idx_orders_client_status ON orders(client_id, status);"
]
code_box(s4, 6.7, 1.70, 6.1, 5.25, "database/schema.sql · DDL con Restricciones e Índices B-Tree", code_s4, font_size=10.0)

# ---------------------------------------------------------------------
# LÁMINA 5: CONSISTENCIA ACID, BLOQUEO PESIMISTA Y TRIGGER PL/PGSQL
# ---------------------------------------------------------------------
s5 = base_slide(5, "Consistencia ACID: Bloqueo Pesimista y Descuento Atómico",
                "Prevención Matemática de Sobreventas (Zero Overselling) y Reintentos contra Deadlocks (Capítulo 7)", "Víctor Cárdenas",
                "[Víctor Cárdenas · 55 s] Para resolver la concurrencia destructiva, implementamos un esquema de doble barrera. "
                "En primer lugar, PgOrderRepository ejecuta SELECT ... FOR UPDATE sobre la fila de la variante textil seleccionada, "
                "bloqueando la fila en memoria del motor PostgreSQL antes de que otra transacción pueda leerla. "
                "En segundo lugar, un trigger en PL/pgSQL descuenta el stock atómicamente al insertar en order_items, respaldado por el constraint CHECK stock >= 0. "
                "Si ocurre un deadlock (código 40P01) o fallo de serialización (40001), nuestro middleware aplica reintento automático de hasta 10 veces "
                "con retroceso exponencial y un 20% de jitter para disipar resonancias.")

# Columna Izquierda: Trigger PL/pgSQL
code_s5_left = [
    "-- 1. Trigger de Descuento Atómico en PostgreSQL 16",
    "CREATE OR REPLACE FUNCTION fn_decrement_stock_on_order()",
    "RETURNS TRIGGER AS $$",
    "BEGIN",
    "  -- Valida existencia antes de aplicar descuento",
    "  IF (SELECT stock FROM product_variants WHERE id = NEW.variant_id) < NEW.quantity THEN",
    "    RAISE EXCEPTION 'STOCK_INSUFFICIENT: Existencias no disponibles';",
    "  END IF;",
    "",
    "  UPDATE product_variants",
    "  SET stock = stock - NEW.quantity,",
    "      updated_at = CURRENT_TIMESTAMP",
    "  WHERE id = NEW.variant_id;",
    "  RETURN NEW;",
    "END; $$ LANGUAGE plpgsql;",
    "",
    "CREATE TRIGGER trg_decrement_stock_on_order",
    "AFTER INSERT ON order_items FOR EACH ROW",
    "EXECUTE FUNCTION fn_decrement_stock_on_order();"
]
code_box(s5, 0.5, 1.70, 6.0, 3.80, "PostgreSQL · Trigger Atómico fn_decrement_stock_on_order()", code_s5_left, font_size=9.5)

# Bloque Inferior Izquierdo: Máquina de Estados
box(s5, 0.5, 5.65, 6.0, 1.30, "", fill=LBLUE, line=BLUE, lw=1.5, radius=0.03)
txt(s5, 0.65, 5.70, 5.7, 0.25, "MÁQUINA DE ESTADOS FINITA (order_status_history)", size=12, bold=True, color=NAVY)
states_s5 = ["RECIBIDO", "PREPARACION", "EN_CAMINO", "ENTREGADO"]
for i, st in enumerate(states_s5):
    x = 0.65 + i * 1.40
    box(s5, x, 6.00, 1.25, 0.45, st, fill=NAVY if i < 3 else GREEN, size=11, bold=True, color=WHITE)
    if i < 3:
        arrow(s5, x + 1.25, 6.22, x + 1.40, 6.22, color=GRAY, w=2.0)
txt(s5, 0.65, 6.55, 5.7, 0.30, "Compensación: Cancelar restituye stock atómicamente a product_variants.", size=10, italic=True, color=RED)

# Columna Derecha: Bloqueo Pesimista y Algoritmo de Backoff
code_s5_right = [
    "// 2. Bloqueo Pesimista y Manejo de Concurrencia (TypeScript)",
    "await client.query('BEGIN ISOLATION LEVEL READ COMMITTED');",
    "try {",
    "  for (const item of dto.items) {",
    "    // Bloqueo exclusivo a nivel de fila (Row-Level Lock)",
    "    const res = await client.query(",
    "      'SELECT stock, sku FROM product_variants WHERE id = $1 FOR UPDATE',",
    "      [item.variantId]",
    "    );",
    "    if (res.rows[0].stock < item.quantity) {",
    "      throw new Error(`Stock insuficiente para SKU ${res.rows[0].sku}`);",
    "    }",
    "  }",
    "  await client.query('INSERT INTO orders ...');",
    "  await client.query('COMMIT'); // Descuento atómico confirmado",
    "} catch (e: any) {",
    "  await client.query('ROLLBACK');",
    "  // Recuperación ante Códigos PostgreSQL: 40001 y 40P01",
    "  if ((e.code === '40001' || e.code === '40P01') && attempt < MAX_RETRIES) {",
    "    const backoff = Math.min(MAX_MS, BASE_MS * Math.pow(2, attempt - 1));",
    "    const jitter = backoff * 0.2; // 20% Jitter contra colisiones en red",
    "    await sleep(backoff - jitter + Math.random() * (jitter * 2));",
    "    continue; // Reintento transparente sin error al cliente",
    "  }",
    "  throw e;",
    "}"
]
code_box(s5, 6.7, 1.70, 6.1, 5.25, "src/infrastructure/repositories/pg.repositories.ts · SELECT FOR UPDATE", code_s5_right, font_size=9.2)

# ---------------------------------------------------------------------
# LÁMINA 6: CIBERSEGURIDAD DEFENSIVA Y MITIGACIÓN OWASP TOP 10
# ---------------------------------------------------------------------
s6 = base_slide(6, "Ciberseguridad Defensiva y Mitigación OWASP Top 10",
                "Pipeline Perimetral, Criptografía de Credenciales y Prevención de Timing Attacks (Capítulo 10)", "Lady Loayza",
                "[Lady Loayza · 50 s] La seguridad se construyó bajo el principio de defensa en profundidad. "
                "Cada solicitud atraviesa cinco compuertas perimetrales: Helmet con Content Security Policy, rate limiter en login a 20 peticiones por 15 minutos, "
                "validación estricta de JWT con arranque fail-fast que rechaza claves menores a 32 caracteres y el algoritmo 'none', "
                "y validación estructural de esquemas con Zod, neutralizando inyecciones SQL mediante consultas 100% parametrizadas. "
                "Para webhooks, empleamos firmas HMAC-SHA256 con comparación en tiempo constante usando crypto.timingSafeEqual, "
                "y en autenticación mitigamos timing attacks ejecutando un hash ficticio si el usuario no existe.")

# Top Pipeline Perimetral en 5 Compuertas
gates_s6 = [
    ("1. Helmet + CORS", "HSTS, CSP estricto,\nAnti-Clickjacking"),
    ("2. Rate Limiter", "20 req / 15 min en Login\nAnti Fuerza Bruta"),
    ("3. JWT Fail-Fast", "HS256 >= 32 chars\nRechazo de alg:none"),
    ("4. RBAC Guard", "Aislamiento por rol\nrequireRole('ADMIN')"),
    ("5. Zod + SQL Params", "Tipado estricto en runtime\nConsultas con $1, $2...")
]
for i, (gtit, gdes) in enumerate(gates_s6):
    x = 0.5 + i * 2.50
    box(s6, x, 1.70, 2.35, 1.15, "", fill=LBLUE, line=BLUE, lw=1.5, radius=0.03)
    txt(s6, x + 0.1, 1.78, 2.15, 0.28, gtit, size=12, bold=True, color=NAVY)
    txt(s6, x + 0.1, 2.10, 2.15, 0.65, gdes, size=10, color=DARK)
    if i < 4:
        arrow(s6, x + 2.35, 2.25, x + 2.50, 2.25, color=GRAY, w=2.5)

# Código 1: Timing-Safe Equal en Webhooks
code_s6_left = [
    "// src/middlewares/webhookAuth.ts",
    "// Mitigación de Timing Attacks en Verificación de Webhooks",
    "export function verifyHmacSignature(rawBody: Buffer, signature: string, secret: string): boolean {",
    "  const hmac = crypto.createHmac('sha256', secret);",
    "  const calculatedDigest = hmac.update(rawBody).digest();",
    "  const receivedDigest = Buffer.from(signature, 'hex');",
    "",
    "  // Comparación en tiempo constante (Zero Timing Attack Leak)",
    "  if (calculatedDigest.length !== receivedDigest.length) return false;",
    "  return crypto.timingSafeEqual(calculatedDigest, receivedDigest);",
    "}"
]
code_box(s6, 0.5, 3.10, 6.0, 3.85, "crypto.timingSafeEqual() · Validación HMAC-SHA256 en Webhooks", code_s6_left, font_size=9.5)

# Código 2: Bcrypt con Dummy Hash contra Enumeración
code_s6_right = [
    "// src/infrastructure/security/password.utils.ts",
    "// Mitigación de Enumeración de Usuarios mediante Timing Attacks",
    "const DUMMY_HASH = '$2a$10$wK...fakehashforconstanttimingexecution';",
    "",
    "export async function verifyUserCredentials(email: string, pass: string): Promise<User> {",
    "  const user = await userRepo.findByEmail(email);",
    "  // Se ejecuta bcrypt.compare SIEMPRE, exista o no el usuario",
    "  const hashToTest = user ? user.passwordHash : DUMMY_HASH;",
    "  const isMatch = await bcrypt.compare(pass, hashToTest);",
    "",
    "  if (!user || !isMatch) {",
    "    throw new HttpError(401, 'Credenciales de acceso inválidas');",
    "  }",
    "  return user;",
    "}"
]
code_box(s6, 6.7, 3.10, 6.1, 3.85, "password.utils.ts · Bcrypt 10 Rondas + Hash Ficticio Anti-Enumeración", code_s6_right, font_size=9.5)

# ---------------------------------------------------------------------
# LÁMINA 7: MATRIZ DE CONTROL DE ACCESO BASADO EN ROLES (RBAC)
# ---------------------------------------------------------------------
s7 = base_slide(7, "Control de Acceso Basado en Roles (RBAC)",
                "Matriz de Autorización, Middlewares de Seguridad y Trazabilidad de Auditoría (Capítulo 10)", "Lady Loayza",
                "[Lady Loayza · 45 s] Diseñamos una matriz RBAC formal que aplica el principio de mínimo privilegio. "
                "El rol OPERATOR tiene permisos de solo lectura para el catálogo y órdenes, y puede crear pedidos y avanzar su estado en el despacho, "
                "pero tiene bloqueadas con HTTP 403 Forbidden todas las operaciones destructivas o de alteración de stock manual. "
                "El rol ADMIN ostenta autorización total, incluyendo creación y soft-delete de prendas, ajuste físico de existencias y emisión de facturación SUNAT. "
                "Todas las mutaciones se registran en una tabla inmutable audit_log con IP, usuario y timestamp.")

# Middleware RBAC en Código Real
code_s7_top = [
    "// src/middlewares/role.middleware.ts · Compuerta Contractual RBAC",
    "export const requireRole = (requiredRole: 'ADMIN' | 'OPERATOR') => {",
    "  return (req: Request, res: Response, next: NextFunction) => {",
    "    if (!req.user) return res.status(401).json({ success: false, error: 'Token JWT ausente o inválido' });",
    "    if (requiredRole === 'ADMIN' && req.user.role !== 'ADMIN') {",
    "      return res.status(403).json({ success: false, error: 'Acceso denegado: Requiere privilegios de Administrador' });",
    "    }",
    "    next();",
    "  };",
    "};"
]
code_box(s7, 0.5, 1.70, 12.3, 1.85, "src/middlewares/role.middleware.ts · Verificación de Privilegios en Runtime", code_s7_top, font_size=9.8)

# Panel Izquierdo: ADMIN
box(s7, 0.5, 3.80, 6.0, 3.15, "", fill=LGREEN, line=GREEN, lw=2.0)
txt(s7, 0.7, 3.88, 5.6, 0.32, "ROL ADMINISTRADOR (admin@leofit.pe) · AUTORIZADO", size=13, bold=True, color=GREEN)

adm_ops = [
    ("200 OK", "GET /api/dashboard/metrics", "KPIs de ventas, facturación y rotación de stock"),
    ("201 CREATED", "POST /api/products", "Alta de prenda en catálogo + registro en audit_log"),
    ("200 OK", "PATCH /api/products/variant/:id/stock", "Ajuste manual de inventario físico en almacén"),
    ("200 OK", "DELETE /api/products/:id", "Soft-delete de prenda (is_active = FALSE)"),
    ("201 CREATED", "POST /api/invoices/emit", "Emisión electrónica formal de Factura/Boleta a SUNAT")
]
for i, (cod, ep, des) in enumerate(adm_ops):
    y = 4.28 + i * 0.50
    box(s7, 0.7, y, 5.6, 0.45, "", fill=WHITE, line=GREEN, lw=1.0, radius=0.03)
    txt(s7, 0.8, y + 0.05, 1.3, 0.35, cod, size=11, bold=True, color=GREEN, font=FONT_CODE)
    txt(s7, 2.1, y + 0.05, 4.1, 0.35, ep + " — " + des, size=10, color=DARK)

# Panel Derecho: OPERATOR
box(s7, 6.8, 3.80, 6.0, 3.15, "", fill=LAMBER, line=AMBER, lw=2.0)
txt(s7, 7.0, 3.88, 5.6, 0.32, "ROL OPERADOR (operador@leofit.pe) · MÍNIMO PRIVILEGIO", size=13, bold=True, color=AMBER)

opr_ops = [
    ("200 OK", "GET /api/products & /orders", "Consulta de catálogo y pedidos para empaque", GREEN),
    ("201 CREATED", "POST /api/orders", "Creación de pedido telefónico con descuento de stock", GREEN),
    ("200 OK", "PATCH /api/orders/:id/status", "Transición de estado: PREPARACIÓN → EN_CAMINO", GREEN),
    ("403 FORBIDDEN", "POST / PUT / DELETE /products", "BLOQUEADO: Restringido estrictamente a Administrador", RED),
    ("403 FORBIDDEN", "PATCH /variant/:id/stock", "BLOQUEADO: No puede alterar stock físico manual", RED)
]
for i, (cod, ep, des, col) in enumerate(opr_ops):
    y = 4.28 + i * 0.50
    box(s7, 7.0, y, 5.6, 0.45, "", fill=WHITE, line=col, lw=1.0, radius=0.03)
    txt(s7, 7.1, y + 0.05, 1.4, 0.35, cod, size=11, bold=True, color=col, font=FONT_CODE)
    txt(s7, 8.5, y + 0.05, 4.0, 0.35, ep + " — " + des, size=10, color=DARK)

# ---------------------------------------------------------------------
# LÁMINA 8: IDEMPOTENCIA RFC 8785 (JCS) & PROTOCOLO ENVELOPE JSON
# ---------------------------------------------------------------------
s8 = base_slide(8, "Idempotencia RFC 8785 (JCS) y Protocolo Envelope JSON",
                "Garantía contra Doble Ejecución ante Reintentos de Red y Contratos RESTful (Capítulo 8)", "Jim Dávila",
                "[Jim Dávila · 45 s] En redes móviles inestables como las de Gamarra, los reintentos automáticos del cliente pueden generar duplicidad de órdenes. "
                "Para evitarlo, implementamos el estándar RFC 8785 (JSON Canonicalization Scheme). "
                "El middleware canonicaliza el payload eliminando diferencias de ordenamiento de claves y calcula un hash SHA-256 (scope_hash). "
                "Mediante un bloqueo consultivo transaccional nativo (pg_try_advisory_xact_lock), aseguramos que dos peticiones concurrentes con la misma llave "
                "no colisionen: la segunda espera o retorna inmediatamente la respuesta cacheada sin re-ejecutar el descuento de existencias.")

# Columna Izquierda: Algoritmo de Idempotencia
code_s8_left = [
    "// src/middlewares/idempotency.middleware.ts",
    "// 1. Canonicidad RFC 8785 y Hash Criptográfico",
    "const canonicalBody = canonicalize(req.body); // JSON determinístico",
    "const scopeHash = crypto.createHash('sha256').update(canonicalBody).digest('hex');",
    "",
    "// 2. Bloqueo Transaccional Consultivo en PostgreSQL (CERO Lock Leaks)",
    "const lock = await client.query(",
    "  'SELECT pg_try_advisory_xact_lock($1, hashtext($2)) AS locked',",
    "  [userId, idempotencyKey]",
    ");",
    "if (!lock.rows[0].locked) {",
    "  return res.status(409).json({ error: 'Operación en curso concurrente' });",
    "}",
    "",
    "// 3. Verificación de Ejecución Previa",
    "const existing = await client.query(",
    "  'SELECT status, response_body FROM idempotency_keys WHERE key = $1',",
    "  [idempotencyKey]",
    ");",
    "if (existing.rows.length > 0 && existing.rows[0].status === 'COMPLETED') {",
    "  return res.status(200).json(existing.rows[0].response_body); // Retorno cached",
    "}"
]
code_box(s8, 0.5, 1.70, 6.2, 5.25, "idempotency.middleware.ts · RFC 8785 + pg_try_advisory_xact_lock", code_s8_left, font_size=9.2)

# Columna Derecha: Protocolo Envelope JSON y Estándar de Errores
code_s8_right = [
    "// Formato Estándar de Respuesta (Envelope JSON RFC)",
    "{",
    '  "success": true,',
    '  "data": {',
    '    "orderId": 108,',
    '    "orderNumber": "LEO-20261101-000108",',
    '    "status": "RECIBIDO",',
    '    "total": 145.00,',
    '    "trackingUrl": "https://leofit.pe/rastreo?code=LFT-A92B"',
    "  },",
    '  "meta": {',
    '    "timestamp": "2026-11-01T20:15:00.000Z",',
    '    "requestId": "req_8f1a9c3d4e",',
    '    "serverTimeMs": 32.4',
    "  }",
    "}",
    "",
    "// Estructura de Error Tipificado (RFC 7807)",
    "{",
    '  "success": false,',
    '  "error": "Stock insuficiente para SKU POLO-RUN-BLK-M",',
    '  "code": "STOCK_CONFLICT_409",',
    '  "details": { "sku": "POLO-RUN-BLK-M", "available": 0, "requested": 2 }',
    "}"
]
code_box(s8, 6.9, 1.70, 5.9, 5.25, "Protocolo Envelope JSON y Formato de Errores Estructurados", code_s8_right, font_size=9.2)

# ---------------------------------------------------------------------
# LÁMINA 9: ASEGURAMIENTO DE CALIDAD SHIFT-LEFT & 194 PRUEBAS
# ---------------------------------------------------------------------
s9 = base_slide(9, "Calidad de Software: 194 Pruebas Automatizadas (100% Pass)",
                "Estrategia Shift-Left, Cobertura Istanbul y Pirámide de Pruebas (Capítulo 11)", "Jim Dávila",
                "[Jim Dávila · 50 s] La verificación de calidad se rige por la filosofía Shift-Left. "
                "Contamos con 194 pruebas automatizadas divididas en 125 pruebas en backend con Jest y Supertest, y 69 pruebas en frontend con Vitest. "
                "Alcanzamos una cobertura del 76.16% en la lógica de dominio del backend y el 100% en rutas, validadores de entrada Zod y utilidades criptográficas. "
                "Con transparencia técnica para el jurado: el módulo pg.repositories refleja 6.7% en el reporte unitario porque se aísla intencionalmente para la suite "
                "de integración física sobre la base de datos real, validada con el flag RUN_INTEGRATION_TESTS.")

# Gráfico Donut de Suites de Pruebas
cd9 = CategoryChartData()
cd9.categories = ["Backend: Jest (17 suites)", "Frontend: Vitest (10 suites)"]
cd9.add_series("Pruebas", (125, 69))
gf9 = s9.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.4), Inches(1.70), Inches(4.6), Inches(4.3), cd9)
ch9 = gf9.chart
ch9.has_title = False
ch9.has_legend = True
ch9.legend.position = XL_LEGEND_POSITION.BOTTOM
ch9.legend.font.size = Pt(11)
ch9.legend.font.name = FONT_MAIN
pl9 = ch9.plots[0]
pl9.has_data_labels = True
pl9.data_labels.font.size = Pt(16)
pl9.data_labels.font.bold = True
pl9.data_labels.font.color.rgb = C(WHITE)
for idx, col in enumerate([NAVY, ORANGE]):
    pt = pl9.series[0].points[idx]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = C(col)
pl9._element.find(qn("c:holeSize")).set("val", "55")
txt(s9, 1.65, 3.10, 2.1, 0.8, "194", size=42, bold=True, color=NAVY, align="c", anchor="m")
txt(s9, 1.65, 3.80, 2.1, 0.35, "APROBADAS (0 fallos)", size=11, bold=True, color=GREEN, align="c")

# Gráfico de Barras de Cobertura Istanbul
cd9_cov = CategoryChartData()
cov_mods = [
    ("pg.repositories*", 6.7),
    ("controllers", 65.0),
    ("memory.repositories", 74.9),
    ("middlewares", 80.9),
    ("routes", 100.0),
    ("validators (Zod)", 100.0),
    ("jwt.utils", 100.0),
    ("password.utils", 100.0)
]
cd9_cov.categories = [m[0] for m in cov_mods]
cd9_cov.add_series("Cobertura de Líneas (%)", [m[1] for m in cov_mods])
gf9_cov = s9.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(5.2), Inches(1.65), Inches(7.7), Inches(4.2), cd9_cov)
c9 = gf9_cov.chart
c9.has_title = False
c9.has_legend = False
p9 = c9.plots[0]
p9.gap_width = 45
p9.has_data_labels = True
p9.data_labels.font.size = Pt(13)
p9.data_labels.font.bold = True
p9.data_labels.number_format = '0.0"%"'
p9.data_labels.number_format_is_linked = False
p9.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
c9.value_axis.maximum_scale = 115
c9.value_axis.minimum_scale = 0
c9.value_axis.visible = False
for i, m in enumerate(cov_mods):
    col = ORANGE if m[1] < 20 else (NAVY if m[1] < 80 else GREEN)
    pt = p9.series[0].points[i]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = C(col)

box(s9, 5.3, 5.90, 3.8, 0.90, "76.16 % COBERTURA GLOBAL\n(Lógica de Dominio del Backend)", fill=LGREEN, line=GREEN, size=14, bold=True, color=GREEN)
txt(s9, 9.3, 5.95, 3.6, 0.85, "* pg.repositories: Validado al 100% en suite de integración física independiente ejecutada contra PostgreSQL.", size=11, color=GRAY, anchor="m")
box(s9, 0.5, 6.25, 4.4, 0.55, "Integración Continua: GitHub Actions en cada Push", fill=LBLUE, line=BLUE, size=13, bold=True, color=NAVY)

# ---------------------------------------------------------------------
# LÁMINA 10: INTEROPERABILIDAD EXTERNA Y PRUEBAS DE INTEGRACIÓN
# ---------------------------------------------------------------------
s10 = base_slide(10, "Interoperabilidad: Servicios Externos y Gateways",
                 "SLA, Latencias Contractuales y Pruebas Automatizadas (Capítulo 12, Anexo F)", "Harley Roman",
                 "[Harley Roman · 45 s] En el Bloque V defendemos la interoperabilidad externa de LeoFit. "
                 "La API backend se conecta con cuatro ecosistemas externos: WhatsApp Cloud API para notificaciones con enlace unívoco de rastreo, "
                 "pasarelas de pago móvil Yape y Plin mediante webhooks firmados con HMAC-SHA256, y los padrones de identidad tributaria de RENIEC y SUNAT. "
                 "La suite de pruebas automatizadas integration_external.test.ts evalúa los siete contratos de integración con latencias menores a 30 ms. "
                 "Con rigor académico: actualmente estos servicios operan mediante adaptadores simulados de alta fidelidad, listos para enlazar llaves productivas.")

# Hub Central y Nodos
box(s10, 5.0, 3.30, 3.3, 1.60, "API BACKEND\nNode.js 20 · Express\nEnvelope JSON", fill=NAVY, size=17, bold=True, color=WHITE, shape=MSO_SHAPE.OVAL)

ext_nodes = [
    (0.5, 1.70, "WhatsApp Cloud API", "Notificación automática al comprador\nCódigo unívoco #LFT-XXX + URL de tracking", "27 ms", BLUE),
    (0.5, 4.80, "Pasarelas Yape / Plin", "Conciliación asíncrona mediante webhooks\nFirma HMAC-SHA256 + token de liquidación", "3 ms", GREEN),
    (9.2, 1.70, "RENIEC Gateway", "Validación estricta de DNI (8 dígitos numéricos)\nRechazo HTTP 400 ante caracteres alfabéticos", "5 ms", AMBER),
    (9.2, 4.80, "SUNAT Facturación", "Validación de RUC (11 dígitos) y condición 'HABIDO'\nEmisión electrónica con desglose IGV 18%", "4 ms", AMBER)
]
for x, y, nname, ndesc, nlat, ncol in ext_nodes:
    box(s10, x, y, 3.65, 1.45, "", fill=WHITE, line=ncol, lw=2.5, radius=0.03)
    txt(s10, x + 0.15, y + 0.08, 3.35, 0.30, nname, size=14, bold=True, color=ncol)
    txt(s10, x + 0.15, y + 0.38, 3.35, 0.65, ndesc, size=11, color=DARK)
    box(s10, x + 2.50, y - 0.20, 1.05, 0.40, nlat, fill=ncol, size=13, bold=True, color=WHITE)

# Conectores hacia el Hub
arrow(s10, 4.15, 2.45, 5.30, 3.50, color=BLUE, w=3.0)
arrow(s10, 5.30, 4.60, 4.15, 5.50, color=GREEN, w=3.0)
arrow(s10, 8.00, 3.50, 9.20, 2.45, color=AMBER, w=3.0)
arrow(s10, 8.00, 4.60, 9.20, 5.50, color=AMBER, w=3.0)

# Rótulos de Despacho con QR
box(s10, 4.5, 5.50, 4.3, 1.35, "Motor de Rótulos con Código QR (jsPDF)\nGeneración client-side para Olva Courier y Shalom\nCódigo de barras térmico + tracking unívoco", fill=LGRAY, line="94A3B8", lw=1.5, size=13, bold=True, color=GRAY)
arrow(s10, 6.65, 5.50, 6.65, 4.90, color=GRAY, w=2.5)

# Badge de Tests
box(s10, 4.6, 1.70, 4.1, 0.70, "✔ 7 / 7 PRUEBAS DE INTEGRACIÓN APROBADAS\n(integration_external.test.ts en Jest)", fill=LGREEN, line=GREEN, size=13, bold=True, color=GREEN)
txt(s10, 0.5, 6.55, 3.8, 0.40, "Arquitectura con adaptadores simulados de alta fidelidad contractual.", size=11, italic=True, color=GRAY)

# ---------------------------------------------------------------------
# LÁMINA 11: AUDITORÍA DE USABILIDAD Y CALIDAD ISO/IEC 25010
# ---------------------------------------------------------------------
s11 = base_slide(11, "Auditoría de Usabilidad y Calidad ISO/IEC 25010",
                 "Estudio Formal SUS (88.5/100), 4 Pilares del Estándar y Core Web Vitals (Capítulo 13)", "Harley Roman",
                 "[Harley Roman · 45 s] La usabilidad se auditó bajo la norma internacional ISO/IEC 25010 en cuatro subatributos: "
                 "Facilidad de Aprendizaje con checkout en tres pasos; Protección contra Errores bloqueando tallas sin stock en la interfaz; "
                 "Asistencia al Usuario con portal público de rastreo; e Involucramiento con micro-interacciones fluidas y modo de alto contraste. "
                 "En el estudio de campo con diez usuarios representativos alcanzamos 88.5 sobre 100 en la Escala SUS, ubicándonos en Grado A Excelente. "
                 "En telemetría web de Google, logramos un LCP de 1.4 segundos y una estabilidad visual casi perfecta de 0.01.")

# Gráfico Donut SUS Score
cd11 = CategoryChartData()
cd11.categories = ["SUS Score", "Margen"]
cd11.add_series("Puntaje", (88.5, 11.5))
gf11 = s11.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.4), Inches(1.70), Inches(4.3), Inches(4.3), cd11)
c11 = gf11.chart
c11.has_title = False
c11.has_legend = False
p11 = c11.plots[0]
for idx, col in enumerate([GREEN, "E2E8F0"]):
    pt = p11.series[0].points[idx]
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = C(col)
p11._element.find(qn("c:holeSize")).set("val", "70")
txt(s11, 1.25, 3.05, 2.6, 0.85, "88.5", size=56, bold=True, color=GREEN, align="c", anchor="m")
txt(s11, 1.25, 3.90, 2.6, 0.35, "de 100 · GRADO A", size=15, bold=True, color=GRAY, align="c")
txt(s11, 0.5, 5.75, 4.1, 0.45, "System Usability Scale (SUS) · 10 Usuarios UAT", size=14, bold=True, color=NAVY, align="c")
box(s11, 0.5, 6.25, 4.1, 0.55, "✔ 9 Pruebas en Vitest (usability_iso25010.test.ts)", fill=LGREEN, line=GREEN, size=12, bold=True, color=GREEN)

# Los 4 Pilares ISO 25010
pilares = [
    ("1. Facilidad de Aprendizaje (Learnability)", "Curva intuitiva inmediata: Checkout guiado en 3 pasos con autollenado de datos recurrentes."),
    ("2. Protección contra Errores (Error Protection)", "Prevención activa: Deshabilitación de tallas sin existencias y validación sintáctica de DNI/RUC."),
    ("3. Asistencia al Usuario (User Assistance)", "Transparencia de proceso: Generación de código #LFT-XXX y portal público de tracking sin login."),
    ("4. Involucramiento Estético (User Engagement)", "Feedback visual reactivo: Micro-interacciones fluidas y conmutador de alto contraste WCAG AAA.")
]
for i, (ptit, pdes) in enumerate(pilares):
    x = 4.9 + (i % 2) * 4.0
    y = 1.70 + (i // 2) * 1.95
    box(s11, x, y, 3.85, 1.80, "", fill=LBLUE, line=BLUE, lw=2.0, radius=0.03)
    txt(s11, x + 0.15, y + 0.10, 3.55, 0.40, ptit, size=14, bold=True, color=NAVY)
    txt(s11, x + 0.15, y + 0.55, 3.55, 1.15, pdes, size=12, color=DARK)

# Core Web Vitals
vitals = [("LCP", "1.4 s", "Carga"), ("INP", "45 ms", "Interacción"), ("CLS", "0.01", "Estabilidad"), ("TTFB", "< 180 ms", "Respuesta")]
for i, (vk, vv, vlbl) in enumerate(vitals):
    x = 4.9 + i * 2.02
    box(s11, x, 5.75, 1.88, 1.05, "", fill=LGREEN, line=GREEN, lw=2.0, radius=0.03)
    txt(s11, x, 5.80, 1.88, 0.45, vv, size=22, bold=True, color=GREEN, align="c", anchor="m")
    txt(s11, x, 6.30, 1.88, 0.40, f"{vk} ({vlbl}) ✔", size=11, bold=True, color=GRAY, align="c")

# ---------------------------------------------------------------------
# LÁMINA 12: CONCURRENCIA TRANSACCIONAL K6, COEXISTENCIA Y DRP
# ---------------------------------------------------------------------
s12 = base_slide(12, "Concurrencia Transaccional (k6), Coexistencia y DRP",
                 "Evaluación de Estrés (50 VUs), Benchmark ISO 25010 y Recuperación ante Desastres (Capítulos 12, 14 y 16)", "Daniel Rojas",
                 "[Daniel Rojas · 45 s] Para certificar el aislamiento transaccional bajo condiciones extremas, ejecutamos una prueba de estrés con k6. "
                 "Cincuenta usuarios virtuales realizaron compras simultáneas del mismo stock durante seis minutos continuos. "
                 "La latencia percentil 95 se mantuvo por debajo de 250 milisegundos y la tasa de sobreventa fue exactamente cero por ciento. "
                 "En la prueba de coexistencia bajo ISO 25010, obtuvimos latencias de 4.42 ms en lectura y 3.44 ms en escritura con cero por ciento de errores. "
                 "Finalmente, en el simulacro de recuperación ante desastres (DRP) restauramos la base de datos completa en 3.2 segundos frente a un objetivo de 15 minutos.")

# 4 Cajas de Métricas k6 y Coexistencia
k6_metrics = [
    ("50 VUs · 6 min", "Prueba de Carga k6 Concurrente\nRampa sostenida de compras", NAVY),
    ("0.0 %", "Tasa de Sobreventa de Inventario\nConsistencia ACID garantizada", GREEN),
    ("p95 < 250 ms", "Latencia en Lectura y Escritura\nPercentil 95 en endpoints REST", BLUE),
    ("4.42 / 3.44 ms", "Coexistencia ISO 25010\nLectura y escritura en paralelo (0% error)", AMBER)
]
for i, (big, sub, col) in enumerate(k6_metrics):
    x = 0.5 + i * 3.16
    box(s12, x, 1.70, 3.00, 2.05, "", fill=WHITE, line=col, lw=2.5, radius=0.03)
    txt(s12, x, 1.85, 3.00, 0.65, big, size=26, bold=True, color=col, align="c", anchor="m")
    txt(s12, x + 0.1, 2.65, 2.80, 0.95, sub, size=12, color=GRAY, align="c")

# Plan de Recuperación ante Desastres (DRP)
txt(s12, 0.5, 3.95, 12.3, 0.40, "SIMULACRO DE RECUPERACIÓN ANTE DESASTRES (DRP / BCP) — POSTGRESQL 16", size=15, bold=True, color=NAVY)

box(s12, 0.5, 4.45, 12.3, 0.60, "RTO Objetivo según SLA Institucional: < 15 minutos (900 segundos)", fill="CBD5E1", size=14, bold=True, color=DARK, align="l")
box(s12, 0.5, 5.20, 0.35, 0.65, "", fill=GREEN, shape=MSO_SHAPE.RECTANGLE)
txt(s12, 1.0, 5.20, 11.5, 0.65, "RTO Real Medido en Simulacro (pg_restore): 3.2 segundos  |  RPO = 0 Transacciones Perdidas (WAL Sync)", size=17, bold=True, color=GREEN, anchor="m")

box(s12, 0.5, 6.15, 6.0, 0.65, "Deuda Técnica: 100% Saneada (0 Pasivos Pendientes)", fill=LGREEN, line=GREEN, size=13, bold=True, color=GREEN)
box(s12, 6.8, 6.15, 6.0, 0.65, "Seguridad SAST: 0 Vulnerabilidades detectadas en npm audit", fill=LGREEN, line=GREEN, size=13, bold=True, color=GREEN)

# ---------------------------------------------------------------------
# LÁMINA 13: TOPOLOGÍA CLOUD, DEMO EN VIVO Y ROADMAP TÉCNICO
# ---------------------------------------------------------------------
s13 = base_slide(13, "Topología Cloud Desplegada, Demo en Vivo y Roadmap",
                 "Infraestructura en Producción, Pipelines CI/CD y Evolución Tecnológica (Capítulos 15, 18 y 19)", "Equipo Completo",
                 "[Lady Loayza / Equipo · 60 s] Para concluir, el sistema opera en vivo sobre una topología multi-proveedor: "
                 "el frontend se distribuye vía GitHub Pages con compresión Brotli y TLS 1.3, consumiendo la API backend en Render mediante HTTPS, "
                 "conectada al clúster PostgreSQL 16 con SSL. "
                 "Invitamos al jurado a constatar la operatividad en tiempo real en la URL de producción. "
                 "Somos transparentes en declarar nuestras limitaciones: la latencia de arranque en frío por el plan gratuito de Render "
                 "y el uso de adaptadores simulados en servicios externos. "
                 "Nuestro roadmap contempla migrar a una instancia cloud dedicada y habilitar credenciales comerciales. Quedamos a su disposición para la ronda de preguntas.")

# Banner de URL Productiva
box(s13, 0.5, 1.70, 12.3, 0.65, "URL DE PRODUCCIÓN: https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/  |  API: /api/health (200 OK)",
    fill=LAMBER, line=ORANGE, lw=2.0, size=15, bold=True, color=ORANGE)

# Topología Cloud en Bloques
topo_boxes = [
    ("Frontend PWA (Cliente)", "GitHub Pages CDN\nCompresión Brotli / Gzip\nCertificado TLS 1.3"),
    ("Backend REST API", "Render Web Service (Docker)\nNode.js 20 LTS + Express\nPool de Conexiones Activo"),
    ("Base de Datos Gestionada", "PostgreSQL 16 Serverless\nConexión SSL Cifrada (Puerto 5432)\nBackups Automatizados"),
    ("CI/CD Automation", "3 Workflows en GitHub Actions\nBuild Vite + Jest + npm audit\nDespliegue Continuo a gh-pages")
]
for i, (bname, bdesc) in enumerate(topo_boxes):
    x = 0.5 + i * 3.16
    box(s13, x, 2.50, 3.00, 1.40, "", fill=LBLUE, line=BLUE, lw=1.5, radius=0.03)
    txt(s13, x + 0.1, 2.58, 2.80, 0.30, bname, size=13, bold=True, color=NAVY)
    txt(s13, x + 0.1, 2.92, 2.80, 0.88, bdesc, size=11, color=DARK)

# Matriz de Cierre: Logros vs Limitaciones vs Roadmap
balance_cards = [
    ("LOGROS DEMOSTRADOS", GREEN, LGREEN, "• 38.2 s tiempo de captura (-98.6%)\n• 0.0% tasa de sobreventa (ACID)\n• 194 pruebas automatizadas (0 fallos)\n• SUS 88.5 / 100 (Grado A Excelente)\n• DRP RTO = 3.2 s / RPO = 0 pérdidas"),
    ("LIMITACIONES TRANSPARENTES", AMBER, LAMBER, "• Cold Start en Render Free (15 min inactividad)\n• Servicios externos operando con mocks de alta fidelidad contractual\n• Concurrencia sujeta a límites de pool en nivel gratuito"),
    ("ROADMAP DE EVOLUCIÓN", BLUE, LBLUE, "• Fase 1: Instancia cloud dedicada (SLA 99.95%)\n• Fase 2: Credenciales productivas WhatsApp y Pasarelas de Pago\n• Fase 3: Módulo de Facturación Electrónica SUNAT directo con PSE")
]
for i, (btit, bcol, blgt, bbody) in enumerate(balance_cards):
    x = 0.5 + i * 4.16
    box(s13, x, 4.05, 4.00, 2.85, "", fill=blgt, line=bcol, lw=2.0, radius=0.03)
    txt(s13, x, 4.15, 4.00, 0.35, btit, size=15, bold=True, color=bcol, align="c")
    txt(s13, x + 0.15, 4.60, 3.70, 2.20, bbody, size=12, color=DARK)

# Guardar Presentación Maestra
os.makedirs(os.path.dirname(OUT_PPTX), exist_ok=True)
prs.save(OUT_PPTX)
print(f"[OK] Presentación generada exitosamente: {OUT_PPTX}")
