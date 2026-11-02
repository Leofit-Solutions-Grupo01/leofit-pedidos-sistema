# -*- coding: utf-8 -*-
"""
Generador de la presentación APF3 (PPTX nativo, 13 diapositivas, ~10 min).
- Diagramas y gráficos NATIVOS de PowerPoint (editables), pensados para entenderse en segundos.
- Todas las cifras provienen del informe INFORME_FINAL_APF3_LEOFIT (misma fuente de verdad).
Uso:  python scripts/generate_apf3_pptx.py
"""
import os
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.oxml.ns import qn

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "docs", "01_entregable_final_apf3", "presentacion_sustentacion",
                   "APF3_LEOFIT_Presentacion.pptx")

def C(h): return RGBColor.from_string(h)
NAVY, DARK, ORANGE = "1E3A8A", "0F172A", "C2410C"
GREEN, LGREEN, RED, LRED = "15803D", "DCFCE7", "B91C1C", "FEE2E2"
GRAY, LGRAY, BLUE, LBLUE = "475569", "F1F5F9", "2563EB", "DBEAFE"
AMBER, LAMBER, WHITE = "B45309", "FEF3C7", "FFFFFF"
FONT = "Calibri"
TOTAL = 13

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def txt(s, x, y, w, h, text, size=16, bold=False, color=DARK, align="l", anchor="t", italic=False):
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
        r.font.size, r.font.bold, r.font.italic, r.font.name = Pt(size), bold, italic, FONT
        r.font.color.rgb = C(color)
    return tb


def box(s, x, y, w, h, text="", fill=LBLUE, line=None, size=16, bold=False, color=DARK,
        align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, lw=1.5, radius=0.08):
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
        r.font.size, r.font.bold, r.font.name = Pt(size), bold, FONT
        r.font.color.rgb = C(color)
    return sh


def arrow(s, x1, y1, x2, y2, color=GRAY, w=3.0, dash=False):
    cn = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    cn.line.color.rgb = C(color)
    cn.line.width = Pt(w)
    ln = cn.line._get_or_add_ln()
    if dash:
        d = ln.makeelement(qn("a:prstDash"), {"val": "dash"})
        ln.append(d)
    ln.append(ln.makeelement(qn("a:tailEnd"), {"type": "triangle", "w": "med", "len": "med"}))
    return cn


def base(n, title, subtitle, presenter, notes):
    s = prs.slides.add_slide(BLANK)
    txt(s, 0.5, 0.28, 12.3, 0.7, title, size=30, bold=True, color=NAVY, anchor="m")
    box(s, 0.55, 1.0, 1.3, 0.06, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
    txt(s, 0.5, 1.1, 12.3, 0.5, subtitle, size=18, color=GRAY, anchor="m")
    txt(s, 0.5, 7.08, 8, 0.3, "LeoFit PWA · Sustentación Final APF3 · Grupo 01 · UTP 2026-I", size=11, color="94A3B8")
    txt(s, 8.3, 7.08, 4.55, 0.3, f"Expone: {presenter}   |   {n} / {TOTAL}", size=11, color="94A3B8", align="r")
    s.notes_slide.notes_text_frame.text = notes
    return s


def chart_text(chart, size=14):
    chart.font.size = Pt(size)
    chart.font.name = FONT


# =====================================================================
# 1. PORTADA
# =====================================================================
s = prs.slides.add_slide(BLANK)
bg = s.background.fill
bg.solid(); bg.fore_color.rgb = C(DARK)
box(s, 0, 0, 0.35, 7.5, fill=ORANGE, shape=MSO_SHAPE.RECTANGLE)
txt(s, 0.9, 0.7, 11.5, 0.5, "SUSTENTACIÓN FINAL · AVANCE DE PROYECTO FINAL 3 (APF3)", size=18, bold=True, color="FDBA74")
txt(s, 0.9, 1.25, 11.8, 1.3, "LeoFit PWA", size=66, bold=True, color=WHITE)
txt(s, 0.9, 2.5, 11.8, 1.0, "Sistema Web de Gestión de Pedidos y Control de Inventario Multicanal",
    size=28, color="CBD5E1")
txt(s, 0.9, 3.45, 11.8, 0.8,
    "Curso Integrador II: Software (100000S12F) · UTP · Ciclo 2026-I\nDocente asesor: Ing. Enrique L. Huamani U. · Cliente: LeoFit Confecciones y Diseños Deportivos S.A.C.",
    size=16, color="94A3B8")
chips = [("38.2 s", "por pedido"), ("0 %", "sobreventas"), ("194", "pruebas aprobadas"), ("88.5", "SUS / 100")]
for i, (big, small) in enumerate(chips):
    x = 0.9 + i * 3.0
    box(s, x, 4.45, 2.75, 1.0, fill="1E293B", line="334155")
    txt(s, x, 4.47, 2.75, 0.6, big, size=30, bold=True, color="FDBA74", align="c", anchor="m")
    txt(s, x, 5.0, 2.75, 0.4, small, size=14, color="CBD5E1", align="c")
team = [("Lady L. Loayza R.", "Scrum Master · DevSecOps"), ("Víctor L. Cárdenas F.", "Product Owner · DBA"),
        ("Harley A. Roman D.", "Frontend · PWA / UX"), ("Jim A. Dávila M.", "QA Lead · Backend"),
        ("Daniel E. Rojas S.", "Analista · Cloud DevOps")]
for i, (n_, r_) in enumerate(team):
    x = 0.9 + i * 2.4
    box(s, x, 5.85, 2.25, 1.1, fill="0B1220", line="475569")
    txt(s, x, 5.9, 2.25, 0.55, n_, size=14, bold=True, color=WHITE, align="c", anchor="m")
    txt(s, x, 6.42, 2.25, 0.45, r_, size=12, color="94A3B8", align="c")
s.notes_slide.notes_text_frame.text = (
    "[Lady Loayza · 30 s] Buenas tardes, docente y jurado. Presentamos LeoFit PWA: el sistema que digitaliza la toma de pedidos y el inventario "
    "de una microempresa textil de Gamarra. En 10 minutos mostraremos: el problema, la arquitectura, la seguridad, la calidad, la nube y una demo.")

# =====================================================================
# 2. IMPACTO: ANTES vs AHORA
# =====================================================================
s = base(2, "De 2 horas a 38 segundos", "El problema de LeoFit y el resultado medido en el estudio de campo (Cap. 2 y 13)",
         "Daniel Rojas",
         "[Daniel Rojas · 45 s] LeoFit tomaba pedidos por WhatsApp y libreta: entre 45 y 120 minutos por pedido, 14.2% de errores de despacho y "
         "ventas perdidas por sobreventa. Con la PWA el pedido toma 38.2 segundos, 0.4% de errores y 0 sobreventas gracias a bloqueos transaccionales.")
rows = [("Tiempo por pedido", "45–120 min", "38.2 s", 6.0, 0.20, "≈ −99 %"),
        ("Errores de despacho", "14.2 %", "0.4 %", 6.0, 0.17, "−97 %"),
        ("Sobreventas (22 % de fuga comercial)", "Frecuentes", "0.0 %", 6.0, 0.10, "CERO")]
for i, (lab, ant, aho, wmax, wmin, badge) in enumerate(rows):
    y = 1.8 + i * 1.7
    box(s, 0.5, y, 3.2, 1.45, lab, fill=LGRAY, line="CBD5E1", size=19, bold=True, color=NAVY)
    box(s, 3.95, y + 0.1, wmax, 0.55, f"ANTES  {ant}", fill=RED, size=18, bold=True, color=WHITE, align="l")
    box(s, 3.95, y + 0.8, wmin, 0.55, "", fill=GREEN)
    txt(s, 3.95 + wmin + 0.1, y + 0.8, 4, 0.55, f"AHORA  {aho}", size=20, bold=True, color=GREEN, anchor="m")
    box(s, 10.4, y + 0.15, 2.4, 1.15, badge, fill=LGREEN, line=GREEN, size=26, bold=True, color=GREEN)

# =====================================================================
# 3. PROCESO AS-IS vs TO-BE
# =====================================================================
s = base(3, "Proceso de negocio: de manual a digital", "BPMN 2.0 AS-IS → TO-BE (Figuras 1 y 2 del informe)", "Daniel Rojas",
         "[Daniel Rojas · 45 s] Arriba el proceso actual: cada consulta obligaba a revisar estantes a mano, mandar fotos y verificar capturas de pago. "
         "Abajo el proceso rediseñado: catálogo con stock en vivo, pedido atómico, pago conciliado por webhook firmado y despacho con rótulo QR y tracking.")
txt(s, 0.5, 1.65, 6, 0.4, "ANTES (AS-IS) · WhatsApp + libreta", size=18, bold=True, color=RED)
asis = ["Consulta\nWhatsApp", "Revisión\nmanual", "Fotos\npor chat", "Pago por\ncaptura", "Libreta y\ndespacho"]
asis_c = ["Sin canal estructurado", "Operador revisa estantes", "Datos bancarios a mano", "Pago sin verificar", "14.2 % de errores"]
for i in range(5):
    x = 0.5 + i * 2.5
    box(s, x, 2.05, 2.6, 1.25, asis[i], fill=RED, size=17, bold=True, color=WHITE,
        shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
    txt(s, x + 0.2, 3.35, 2.3, 0.6, asis_c[i], size=14, color=RED, align="c")
arrow(s, 6.67, 3.95, 6.67, 4.45, color=ORANGE, w=5)
txt(s, 6.85, 3.95, 5, 0.5, "Rediseño digital", size=16, bold=True, color=ORANGE, anchor="m")
txt(s, 0.5, 4.5, 6, 0.4, "AHORA (TO-BE) · LeoFit PWA", size=18, bold=True, color=GREEN)
tobe = ["Catálogo\nPWA", "Carrito y\ncheckout", "Pedido\nACID", "Pago Yape /\nPlin", "Kanban\n+ QR"]
tobe_c = ["Stock por talla y color en vivo", "Flete Lima / Provincia", "Reserva sin sobreventa", "Webhook firmado HMAC", "Tracking #LFT-XXX"]
for i in range(5):
    x = 0.5 + i * 2.5
    box(s, x, 4.9, 2.6, 1.25, tobe[i], fill=GREEN, size=17, bold=True, color=WHITE,
        shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
    txt(s, x + 0.2, 6.2, 2.3, 0.7, tobe_c[i], size=14, color=GREEN, align="c")

# =====================================================================
# 4. ARQUITECTURA
# =====================================================================
s = base(4, "Arquitectura: 3 capas desacopladas", "C4 Nivel 2 + Clean Architecture con Repository Factory (Figuras 9, 10 y 14)",
         "Víctor Cárdenas",
         "[Víctor Cárdenas · 45 s] Tres contenedores desacoplados: la PWA en React 19 sobre GitHub Pages, la API REST en Node 20 y Express sobre Render, "
         "y PostgreSQL 16. Dentro de la API aplicamos Clean Architecture: los casos de uso dependen de interfaces de repositorio, así que en pruebas "
         "usamos memoria y en producción el pool de PostgreSQL. Además integramos servicios externos mediante adaptadores.")
box(s, 0.5, 1.8, 3.0, 4.9, "", fill=LBLUE, line=BLUE, lw=2)
txt(s, 0.5, 1.85, 3.0, 0.45, "CLIENTE · PWA", size=17, bold=True, color=NAVY, align="c")
for j, t in enumerate(["React 19 + TypeScript", "Vite 6 · Tailwind 4", "AppContext + caché", "Service Worker", "jsPDF · QR"]):
    box(s, 0.7, 2.4 + j * 0.78, 2.6, 0.62, t, fill=WHITE, line=BLUE, size=15, bold=True, color=NAVY)
txt(s, 0.5, 6.35, 3.0, 0.35, "GitHub Pages · CDN · TLS 1.3", size=12, color=GRAY, align="c")

box(s, 4.5, 1.8, 4.6, 4.9, "", fill=LGREEN, line=GREEN, lw=2)
txt(s, 4.5, 1.85, 4.6, 0.45, "API REST v2.0.0 · Node 20 + Express", size=17, bold=True, color=GREEN, align="c")
layers = [("Rutas + Middlewares (JWT · RBAC · Zod)", GREEN), ("Controladores", GREEN),
          ("Casos de uso (reglas de negocio)", GREEN), ("Repository Factory (interfaces)", ORANGE)]
for j, (t, col) in enumerate(layers):
    box(s, 4.7, 2.4 + j * 0.72, 4.2, 0.58, t, fill=WHITE, line=col, size=14, bold=True, color=col)
    if j < 3:
        arrow(s, 6.8, 2.98 + j * 0.72, 6.8, 3.12 + j * 0.72, color=GRAY, w=2)
box(s, 4.7, 5.35, 2.0, 0.62, "PgPool", fill=ORANGE, size=15, bold=True, color=WHITE)
box(s, 6.9, 5.35, 2.0, 0.62, "Memoria (tests)", fill="94A3B8", size=14, bold=True, color=WHITE)
arrow(s, 6.1, 4.98, 5.7, 5.35, color=ORANGE, w=2); arrow(s, 7.5, 4.98, 7.9, 5.35, color="94A3B8", w=2)
txt(s, 4.5, 6.35, 4.6, 0.35, "27 endpoints · Render Web Service (Docker)", size=12, color=GRAY, align="c")

box(s, 10.2, 1.8, 2.65, 2.2, "", fill=LAMBER, line=AMBER, lw=2)
txt(s, 10.2, 1.85, 2.65, 0.4, "PostgreSQL 16", size=17, bold=True, color=AMBER, align="c")
box(s, 10.4, 2.35, 2.25, 0.55, "Transacciones ACID", fill=WHITE, line=AMBER, size=14, bold=True, color=AMBER)
box(s, 10.4, 3.0, 2.25, 0.55, "Triggers · 3FN/BCNF", fill=WHITE, line=AMBER, size=14, bold=True, color=AMBER)
box(s, 10.2, 4.3, 2.65, 2.4, "", fill=LGRAY, line="94A3B8", lw=2)
txt(s, 10.2, 4.33, 2.65, 0.4, "Servicios externos", size=16, bold=True, color=GRAY, align="c")
for j, t in enumerate(["WhatsApp Cloud", "Yape / Plin (webhook)", "SUNAT · RENIEC"]):
    box(s, 10.4, 4.8 + j * 0.62, 2.25, 0.5, t, fill=WHITE, line="94A3B8", size=13, bold=True, color=GRAY)
arrow(s, 3.5, 4.25, 4.5, 4.25, color=NAVY, w=4)
txt(s, 3.45, 3.55, 1.1, 0.6, "HTTPS\nJSON+JWT", size=11, bold=True, color=NAVY, align="c")
arrow(s, 9.1, 2.9, 10.2, 2.9, color=AMBER, w=4)
txt(s, 9.05, 2.2, 1.2, 0.6, "SSL\npool", size=11, bold=True, color=AMBER, align="c")
arrow(s, 9.1, 5.5, 10.2, 5.5, color="94A3B8", w=3, dash=True)

# =====================================================================
# 5. MODELO DE DATOS
# =====================================================================
s = base(5, "Modelo de datos normalizado (PostgreSQL 16)", "14 tablas en 3FN/BCNF · 14 índices B-Tree · Figura 11 y Tabla 12 del informe",
         "Víctor Cárdenas",
         "[Víctor Cárdenas · 40 s] El modelo está normalizado hasta 3FN y BCNF con 14 tablas. El corazón es product_variants, que aísla talla y color con su propio stock "
         "y una restricción CHECK stock >= 0. Un pedido enlaza cliente, usuario y método de pago, y su detalle dispara el trigger de descuento. "
         "Además guardamos historial de estados, comprobantes SUNAT e idempotency keys para reintentos seguros.")

def ent(x, y, w, h, name, fields, col=NAVY, light=LBLUE):
    box(s, x, y, w, h, "", fill=WHITE, line=col, lw=2, radius=0.04)
    box(s, x, y, w, 0.42, name, fill=col, size=15, bold=True, color=WHITE, radius=0.04)
    txt(s, x + 0.05, y + 0.44, w - 0.1, h - 0.45, fields, size=12, color=DARK, anchor="m")
    return (x, y, w, h)

E = {}
E["categories"] = ent(0.5, 1.8, 2.2, 1.0, "categories", "PK id\nnombre")
E["products"] = ent(3.2, 1.8, 2.2, 1.0, "products", "PK id\nFK category_id")
E["variants"] = ent(5.9, 1.8, 2.6, 1.25, "product_variants", "PK id · SKU único\nFK product, size, color\nCHECK stock ≥ 0", col=GREEN)
E["sizes"] = ent(9.0, 1.8, 3.85, 0.62, "sizes · 6 tallas", "")
E["colors"] = ent(9.0, 2.5, 3.85, 0.62, "colors · 10 colores", "")
E["clients"] = ent(0.5, 3.55, 2.2, 1.0, "clients", "PK id\nteléfono UNIQUE")
E["users"] = ent(0.5, 4.75, 2.2, 1.0, "users", "PK id (UUID)\nrol ADMIN / OPERATOR")
E["pay"] = ent(0.5, 5.95, 2.2, 0.85, "payment_methods", "YAPE · PLIN · …")
E["orders"] = ent(3.4, 4.25, 2.3, 1.45, "orders", "PK id · código único\nFK client, user, pago\nestado (enum)", col=ORANGE)
E["items"] = ent(6.3, 3.55, 2.3, 1.0, "order_items", "FK order, variant\n⚡ trigger descuenta stock", col=ORANGE)
E["inv"] = ent(6.3, 4.75, 2.3, 0.95, "invoices", "SUNAT B001 / F001\nIGV 18 %", col=ORANGE)
E["idem"] = ent(6.3, 5.9, 2.3, 0.9, "idempotency_keys", "RFC 8785 (JCS)", col=ORANGE)
E["hist"] = ent(3.4, 6.0, 2.3, 0.85, "order_status_history", "bitácora de estados", col=ORANGE)

def edge(a, b, how):
    ax, ay, aw, ah = E[a]; bx, by, bw, bh = E[b]
    pts = {"r-l": (ax + aw, ay + ah / 2, bx, by + bh / 2), "b-t": (ax + aw / 2, ay + ah, bx + bw / 2, by),
           "t-b": (ax + aw / 2, ay, bx + bw / 2, by + bh), "l-r": (ax, ay + ah / 2, bx + bw, by + bh / 2)}[how]
    arrow(s, *pts, color=GRAY, w=2)

edge("categories", "products", "r-l"); edge("products", "variants", "r-l")
arrow(s, 9.0, 2.11, 8.5, 2.11, color=GRAY, w=2); arrow(s, 9.0, 2.81, 8.5, 2.81, color=GRAY, w=2)
edge("clients", "orders", "r-l"); edge("users", "orders", "r-l"); edge("pay", "orders", "r-l")
edge("orders", "items", "r-l"); edge("orders", "inv", "r-l"); edge("orders", "idem", "r-l"); edge("orders", "hist", "b-t")
arrow(s, 7.45, 3.55, 7.2, 3.05, color=GREEN, w=3)
box(s, 9.0, 3.35, 3.85, 1.05, "Reserva atómica\nSELECT … FOR UPDATE + trigger\n⇒ imposible vender sin stock",
    fill=LGREEN, line=GREEN, size=14, bold=True, color=GREEN)
box(s, 9.0, 4.6, 3.85, 0.95, "Integridad en el motor\nFK · CHECK · UNIQUE · ENUM", fill=LBLUE, line=BLUE, size=14, bold=True, color=NAVY)
box(s, 9.0, 5.75, 3.85, 1.05, "Auditoría y reintentos seguros\nhistorial de estados + idempotencia", fill=LAMBER, line=AMBER,
    size=14, bold=True, color=AMBER)

# =====================================================================
# 6. ACID + ESTADOS
# =====================================================================
s = base(6, "Cero sobreventas: transacción ACID + máquina de estados", "Pedido atómico con bloqueo pesimista (Figuras 12 y 13 del informe)",
         "Víctor Cárdenas",
         "[Víctor Cárdenas · 50 s] Cuando dos clientes compran el último polo, la API abre una transacción, bloquea la fila de la variante con SELECT FOR UPDATE y valida el stock. "
         "Si no alcanza, hace ROLLBACK; si alcanza, inserta el pedido, el trigger descuenta y confirma en menos de 45 ms. Ante deadlocks reintenta hasta 10 veces con backoff exponencial. "
         "Abajo, el pedido avanza por una máquina de estados auditada; cancelar restituye el stock.")
steps = [("Zod valida\nel payload", BLUE), ("BEGIN", NAVY), ("SELECT … FOR UPDATE\n(bloquea variante)", NAVY)]
for i, (t, col) in enumerate(steps):
    box(s, 0.5 + i * 2.45, 1.85, 2.2, 1.1, t, fill=col, size=15, bold=True, color=WHITE)
    arrow(s, 2.7 + i * 2.45, 2.4, 2.95 + i * 2.45, 2.4, color=GRAY, w=3)
box(s, 7.9, 1.75, 1.9, 1.3, "¿Hay\nstock?", fill=LAMBER, line=AMBER, size=17, bold=True, color=AMBER, shape=MSO_SHAPE.DIAMOND)
arrow(s, 7.85, 2.4, 7.9, 2.4, color=GRAY, w=3)
box(s, 10.2, 1.85, 2.65, 0.55, "SÍ → INSERT + trigger descuenta", fill=GREEN, size=13, bold=True, color=WHITE)
box(s, 10.2, 2.55, 2.65, 0.55, "NO → ROLLBACK + error controlado", fill=RED, size=13, bold=True, color=WHITE)
arrow(s, 9.8, 2.25, 10.2, 2.12, color=GREEN, w=3); arrow(s, 9.3, 3.05, 10.2, 2.82, color=RED, w=3)
box(s, 10.2, 3.25, 2.65, 0.55, "COMMIT en < 45 ms", fill=LGREEN, line=GREEN, size=14, bold=True, color=GREEN)
box(s, 0.5, 3.2, 9.3, 0.7, "Conflicto 40001 / deadlock 40P01 → reintento hasta 10 veces · backoff exponencial + jitter 20 %",
    fill=LGRAY, line="94A3B8", size=15, bold=True, color=GRAY)
txt(s, 0.5, 4.15, 8, 0.45, "Ciclo de vida del pedido (auditado en order_status_history)", size=17, bold=True, color=NAVY)
est = [("RECIBIDO", "2563EB"), ("PREPARACIÓN", "7C3AED"), ("EN CAMINO", "D97706"), ("ENTREGADO", GREEN)]
for i, (t, col) in enumerate(est):
    box(s, 0.5 + i * 3.15, 4.7, 2.6, 0.95, t, fill=col, size=19, bold=True, color=WHITE)
    if i < 3:
        arrow(s, 3.1 + i * 3.15, 5.17, 3.65 + i * 3.15, 5.17, color=GRAY, w=4)
box(s, 3.65, 6.25, 5.0, 0.65, "CANCELADO · restituye stock", fill=LRED, line=RED, size=17, bold=True, color=RED)
for i in range(3):
    arrow(s, 1.8 + i * 3.15, 5.65, 4.4 + i * 1.8, 6.25, color=RED, w=2, dash=True)

# =====================================================================
# 7. SEGURIDAD + RBAC
# =====================================================================
s = base(7, "Seguridad en profundidad y control de roles", "OWASP Top 10 · 0 vulnerabilidades en npm audit · RBAC ADMIN / OPERATOR (Cap. 10)",
         "Lady Loayza",
         "[Lady Loayza · 55 s] Cada petición atraviesa cinco compuertas: Helmet y CORS, límite de intentos de login, JWT con arranque fail-fast que rechaza alg none, "
         "control de roles y validación Zod, y finalmente SQL parametrizado. Las contraseñas usan bcrypt con hash ficticio contra timing attacks y los webhooks "
         "se firman con HMAC-SHA256. Abajo: el administrador tiene acceso total; el operador solo despacha y recibe 403 en acciones críticas.")
gates = [("Helmet + CORS\nHSTS · CSP", BLUE), ("Rate limit login\n20 / 15 min", BLUE), ("JWT HS256\nfail-fast · sin alg:none", NAVY),
         ("RBAC\nADMIN / OPERATOR", NAVY), ("Zod + SQL\nparametrizado", GREEN)]
box(s, 0.5, 1.8, 1.1, 1.2, "Request", fill=DARK, size=14, bold=True, color=WHITE)
for i, (t, col) in enumerate(gates):
    x = 1.85 + i * 2.2
    arrow(s, x - 0.25, 2.4, x, 2.4, color=GRAY, w=3)
    box(s, x, 1.8, 1.95, 1.2, t, fill=col, size=13, bold=True, color=WHITE)
box(s, 0.5, 3.2, 6.1, 0.55, "bcrypt 10 rondas + hash ficticio (anti timing attack)", fill=LGRAY, line="94A3B8", size=14, bold=True, color=GRAY)
box(s, 6.75, 3.2, 6.1, 0.55, "Webhooks: HMAC-SHA256 + timingSafeEqual", fill=LGRAY, line="94A3B8", size=14, bold=True, color=GRAY)
box(s, 0.5, 3.95, 6.1, 2.95, "", fill=LGREEN, line=GREEN, lw=2)
txt(s, 0.5, 3.98, 6.1, 0.45, "ADMINISTRADOR · acceso total", size=17, bold=True, color=GREEN, align="c")
adm = ["Métricas y KPIs del dashboard", "Crear / eliminar prendas", "Ajustar stock por variante", "Crear y cancelar pedidos", "Emitir factura / boleta SUNAT"]
for j, t in enumerate(adm):
    box(s, 0.7 + (j % 2) * 2.9, 4.5 + (j // 2) * 0.78, 2.75, 0.65, "✔ " + t, fill=WHITE, line=GREEN, size=12, bold=True, color=GREEN)
box(s, 6.75, 3.95, 6.1, 2.95, "", fill=LAMBER, line=AMBER, lw=2)
txt(s, 6.75, 3.98, 6.1, 0.45, "OPERADOR · mínimo privilegio", size=17, bold=True, color=AMBER, align="c")
ok = ["Consultar catálogo y pedidos", "Crear pedido", "Avanzar estado de despacho"]
bad = ["Crear / borrar prendas", "Ajustar stock manual", "Cancelar pedidos"]
for j, t in enumerate(ok):
    box(s, 6.95 + (j % 2) * 2.9, 4.5 + (j // 2) * 0.78, 2.75, 0.65, "✔ " + t, fill=WHITE, line=GREEN, size=12, bold=True, color=GREEN)
for j, t in enumerate(bad):
    k = j + 3
    box(s, 6.95 + (k % 2) * 2.9, 4.5 + (k // 2) * 0.78, 2.75, 0.65, "✖ 403  " + t, fill=LRED, line=RED, size=12, bold=True, color=RED)

# =====================================================================
# 8. CALIDAD
# =====================================================================
s = base(8, "Calidad: 194 pruebas automatizadas, 0 fallos", "Shift-Left: TypeScript + Zod → pruebas unitarias → integración Supertest → CI en cada push (Cap. 11)",
         "Jim Dávila",
         "[Jim Dávila · 55 s] Tenemos 194 pruebas aprobadas: 125 en backend con Jest y Supertest en 17 suites, y 69 en frontend con Vitest en 10 suites. "
         "La cobertura de líneas en lógica de dominio es 76.16%, con 100% en rutas, validadores Zod y utilidades JWT y de contraseñas. "
         "El adaptador PostgreSQL se valida en la suite de integración física, por eso su cobertura unitaria es baja.")
cd = CategoryChartData(); cd.categories = ["Backend · Jest (17 suites)", "Frontend · Vitest (10 suites)"]; cd.add_series("Pruebas", (125, 69))
gf = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.4), Inches(1.7), Inches(4.6), Inches(4.4), cd)
ch = gf.chart; chart_text(ch, 14); ch.has_title = False; ch.has_legend = True
ch.legend.include_in_layout = False; ch.legend.position = 2  # bottom
from pptx.enum.chart import XL_LEGEND_POSITION
ch.legend.position = XL_LEGEND_POSITION.BOTTOM
pl = ch.plots[0]; pl.has_data_labels = True
pl.data_labels.font.size = Pt(18); pl.data_labels.font.bold = True; pl.data_labels.font.color.rgb = C(WHITE)
pl.data_labels.show_value = True
for idx, col in enumerate([NAVY, ORANGE]):
    pt = pl.series[0].points[idx]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = C(col)
pl._element.find(qn("c:holeSize")).set("val", "55")
txt(s, 1.65, 3.15, 2.1, 0.9, "194", size=44, bold=True, color=NAVY, align="c", anchor="m")
txt(s, 1.65, 3.85, 2.1, 0.4, "aprobadas", size=14, color=GRAY, align="c")

cd2 = CategoryChartData()
mods = [("pg.repositories*", 6.7), ("controllers", 65.0), ("memory.repos", 74.9), ("middlewares", 80.9),
        ("routes", 100), ("validators (Zod)", 100), ("jwt.utils", 100), ("password.utils", 100)]
cd2.categories = [m[0] for m in mods]; cd2.add_series("Cobertura de líneas (%)", [m[1] for m in mods])
gf2 = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(5.2), Inches(1.65), Inches(7.7), Inches(4.2), cd2)
c2 = gf2.chart; chart_text(c2, 14); c2.has_legend = False
p2 = c2.plots[0]; p2.gap_width = 45; p2.has_data_labels = True
p2.data_labels.font.size = Pt(14); p2.data_labels.font.bold = True
p2.data_labels.number_format = '0.0"%"'; p2.data_labels.number_format_is_linked = False
p2.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
c2.value_axis.maximum_scale = 115; c2.value_axis.minimum_scale = 0
c2.value_axis.has_major_gridlines = False; c2.value_axis.visible = False
for i, m in enumerate(mods):
    col = ORANGE if m[1] < 20 else (NAVY if m[1] < 80 else GREEN)
    pt = p2.series[0].points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = C(col)
box(s, 5.3, 5.85, 3.7, 0.9, "76.16 %\ncobertura de líneas (dominio)", fill=LGREEN, line=GREEN, size=15, bold=True, color=GREEN)
txt(s, 9.1, 5.85, 3.8, 0.9, "* Adaptador PostgreSQL validado en la suite de integración física (RUN_INTEGRATION_TESTS).", size=12, color=GRAY, anchor="m")
box(s, 0.5, 6.25, 4.5, 0.6, "Shift-Left: defectos detectados antes de producción", fill=LBLUE, line=BLUE, size=14, bold=True, color=NAVY)

# =====================================================================
# 9. INTEROPERABILIDAD
# =====================================================================
s = base(9, "Interoperabilidad con servicios externos", "7 pruebas automatizadas de integración · 7 / 7 aprobadas (Cap. 12, Anexo F)",
         "Harley Roman",
         "[Harley Roman · 40 s] La API es el centro: notifica por WhatsApp con el enlace de tracking, concilia pagos de Yape y Plin mediante webhooks firmados, "
         "valida DNI en RENIEC y RUC en SUNAT, y la PWA genera rótulos con QR para Olva y Shalom. Siete pruebas automáticas lo verifican, todas bajo 30 ms. "
         "Con transparencia: hoy esos servicios operan con adaptadores simulados de alta fidelidad, listos para credenciales productivas.")
hub = box(s, 4.9, 3.3, 3.5, 1.7, "API LeoFit\nNode 20", fill=NAVY, size=20, bold=True, color=WHITE, shape=MSO_SHAPE.OVAL)
nodes = [(0.5, 1.8, "WhatsApp Cloud\nenvío #LFT-XXX + URL tracking", "27 ms", BLUE),
         (0.5, 4.8, "Yape / Plin\nwebhook firmado HMAC-SHA256", "3 ms", GREEN),
         (9.3, 1.8, "RENIEC\nDNI · 8 dígitos", "5 ms", AMBER),
         (9.3, 4.8, "SUNAT\nRUC · 11 dígitos · HABIDO", "4 ms", AMBER)]
for x, y, t, ms, col in nodes:
    box(s, x, y, 3.55, 1.5, t, fill=WHITE, line=col, lw=3, size=15, bold=True, color=col)
    box(s, x + 2.55, y - 0.2, 1.0, 0.45, ms, fill=col, size=14, bold=True, color=WHITE)
arrow(s, 4.05, 2.7, 5.5, 3.6, color=BLUE, w=3); arrow(s, 5.5, 4.7, 4.05, 5.5, color=GREEN, w=3)
arrow(s, 7.8, 3.6, 9.3, 2.7, color=AMBER, w=3); arrow(s, 7.8, 4.7, 9.3, 5.5, color=AMBER, w=3)
box(s, 4.5, 5.55, 4.3, 1.3, "Rótulo de despacho con QR\nOlva Courier · Shalom\n(generado en la PWA con jsPDF)", fill=LGRAY, line="94A3B8",
    size=14, bold=True, color=GRAY)
arrow(s, 6.65, 5.55, 6.65, 5.05, color=GRAY, w=3)
box(s, 4.5, 1.8, 4.3, 0.9, "✔ 7 / 7 pruebas ext-01 … ext-07", fill=LGREEN, line=GREEN, size=17, bold=True, color=GREEN)
txt(s, 0.5, 6.55, 3.7, 0.45, "Adaptadores simulados de alta fidelidad", size=12, italic=True, color=GRAY)

# =====================================================================
# 10. USABILIDAD
# =====================================================================
s = base(10, "Usabilidad certificada bajo ISO/IEC 25010", "Estudio SUS + pruebas Vitest + Core Web Vitals (Cap. 13, Anexo G)",
         "Harley Roman",
         "[Harley Roman · 45 s] Aplicamos el cuestionario SUS a diez usuarios reales: 88.5 sobre 100, Grado A. Cubrimos los cuatro subatributos de ISO 25010 con nueve pruebas "
         "automáticas, y en producción el sitio alcanza LCP de 1.4 s, INP de 45 ms y CLS de 0.01, todos en el rango excelente de Google.")
cd3 = CategoryChartData(); cd3.categories = ["SUS", "Margen"]; cd3.add_series("SUS", (88.5, 11.5))
gf3 = s.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(0.4), Inches(1.7), Inches(4.2), Inches(4.2), cd3)
c3 = gf3.chart; chart_text(c3, 12); c3.has_title = False; c3.has_legend = False
p3 = c3.plots[0]; p3.has_data_labels = False
for idx, col in enumerate([GREEN, "E2E8F0"]):
    pt = p3.series[0].points[idx]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = C(col)
p3._element.find(qn("c:holeSize")).set("val", "70")
txt(s, 1.2, 3.1, 2.6, 0.9, "88.5", size=54, bold=True, color=GREEN, align="c", anchor="m")
txt(s, 1.2, 3.95, 2.6, 0.4, "de 100 · Grado A", size=16, bold=True, color=GRAY, align="c")
txt(s, 0.5, 5.8, 4.0, 0.5, "Escala SUS · 10 usuarios reales", size=15, bold=True, color=NAVY, align="c")
pil = [("Aprendizaje", "Checkout en 3 pasos\ncatálogo por disciplina"), ("Protección de errores", "Tallas sin stock bloqueadas\nvalidación DNI / RUC"),
       ("Asistencia", "Código #LFT-XXX\nportal público de tracking"), ("Involucramiento", "Micro-interacciones\nmodo alto contraste")]
for i, (t, d) in enumerate(pil):
    x = 4.9 + (i % 2) * 4.0; y = 1.8 + (i // 2) * 1.95
    box(s, x, y, 3.8, 1.8, "", fill=LBLUE, line=BLUE, lw=2)
    txt(s, x, y + 0.08, 3.8, 0.5, t, size=18, bold=True, color=NAVY, align="c")
    txt(s, x + 0.1, y + 0.62, 3.6, 1.1, d, size=15, color=DARK, align="c")
vit = [("LCP", "1.4 s"), ("INP", "45 ms"), ("CLS", "0.01"), ("TTFB", "< 180 ms")]
for i, (k, v) in enumerate(vit):
    x = 4.9 + i * 2.0
    box(s, x, 5.8, 1.85, 1.05, "", fill=LGREEN, line=GREEN, lw=2)
    txt(s, x, 5.82, 1.85, 0.5, v, size=22, bold=True, color=GREEN, align="c", anchor="m")
    txt(s, x, 6.35, 1.85, 0.4, k + " ✔ excelente", size=12, bold=True, color=GRAY, align="c")
box(s, 0.6, 6.4, 3.9, 0.5, "9 pruebas Vitest ISO 25010 ✔", fill=LGREEN, line=GREEN, size=14, bold=True, color=GREEN)

# =====================================================================
# 11. CLOUD + CI/CD
# =====================================================================
s = base(11, "Despliegue en la nube y CI/CD automatizado", "Topología desplegada + 3 workflows de GitHub Actions (Cap. 15, Figuras 23 y 24)",
         "Daniel Rojas",
         "[Daniel Rojas · 45 s] En producción el usuario entra a la PWA servida por la CDN de GitHub Pages con TLS 1.3; esta consume la API REST en un contenedor Docker en Render, "
         "que conecta a PostgreSQL 16 por SSL con pool de conexiones. Cada push a main dispara tres workflows: backend con compilación, lint y las 125 pruebas; "
         "escaneo de seguridad con npm audit; y despliegue del frontend con Vite a GitHub Pages.")
topo = [("Usuario\nmóvil / PC", DARK), ("GitHub Pages\nPWA · CDN · TLS 1.3", NAVY), ("Render Web Service\nDocker · Node 20 LTS", GREEN), ("PostgreSQL 16\nSSL · pool de conexiones", AMBER)]
for i, (t, col) in enumerate(topo):
    x = 0.5 + i * 3.2
    box(s, x, 1.85, 2.7, 1.5, t, fill=col, size=16, bold=True, color=WHITE)
    if i < 3:
        arrow(s, x + 2.7, 2.6, x + 3.2, 2.6, color=GRAY, w=4)
txt(s, 0.5, 3.5, 12, 0.4, "Pipeline CI/CD (cada push a main)", size=18, bold=True, color=NAVY)
box(s, 0.5, 4.5, 2.0, 1.2, "git push\nmain", fill=DARK, size=17, bold=True, color=WHITE)
wf = [("backend-ci-cd.yml", "Compila TS · lint\n125 pruebas Jest", GREEN), ("security-scan.yml", "SAST · npm audit\n0 vulnerabilidades", RED),
      ("deploy.yml", "Build Vite\n→ rama gh-pages", BLUE)]
for i, (n_, d_, col) in enumerate(wf):
    y = 3.95 + i * 0.8
    box(s, 3.2, y, 5.3, 0.7, "", fill=WHITE, line=col, lw=2.5)
    txt(s, 3.3, y + 0.02, 2.5, 0.66, n_, size=14, bold=True, color=col, anchor="m")
    txt(s, 5.7, y + 0.02, 2.8, 0.66, d_.replace("\n", " · "), size=12, color=DARK, anchor="m")
    arrow(s, 2.5, 5.1, 3.2, y + 0.35, color=GRAY, w=2.5)
    arrow(s, 8.5, y + 0.35, 9.2, 5.1, color=GRAY, w=2.5)
box(s, 9.2, 4.5, 3.65, 1.2, "Producción actualizada\nPWA + API en HTTPS", fill=LGREEN, line=GREEN, size=16, bold=True, color=GREEN)
box(s, 0.5, 6.45, 12.35, 0.5, "render.yaml + Docker garantizan despliegue reproducible · variables de entorno seguras (DATABASE_URL, JWT_SECRET)",
    fill=LGRAY, line="94A3B8", size=14, bold=True, color=GRAY)

# =====================================================================
# 12. RENDIMIENTO Y RESILIENCIA
# =====================================================================
s = base(12, "Rendimiento, concurrencia y resiliencia", "k6 (50 usuarios) · coexistencia ISO/IEC 25010 · simulacro de recuperación ante desastres (Cap. 12, 14, 16)",
         "Daniel Rojas",
         "[Daniel Rojas · 40 s] Con k6 simulamos 50 usuarios concurrentes por 6 minutos comprando el mismo stock: p95 menor a 250 ms y cero sobreventas. "
         "La prueba de coexistencia de ISO 25010 midió 4.42 ms en lectura y 3.44 ms en escritura sin errores. En el simulacro de recuperación restauramos la base en 3.2 segundos "
         "frente a un objetivo de 15 minutos, con cero transacciones perdidas.")
kp = [("50 VUs · 6 min", "k6: compras simultáneas\ndel mismo stock", NAVY), ("0.0 %", "sobreventa de stock\nbajo carga", GREEN),
      ("p95 < 250 ms", "latencia en lectura\ny escritura", BLUE), ("0 % error", "coexistencia ISO 25010\n4.42 ms lect · 3.44 ms escr", AMBER)]
for i, (big, small, col) in enumerate(kp):
    x = 0.5 + i * 3.1
    box(s, x, 1.85, 2.95, 2.1, "", fill=WHITE, line=col, lw=3)
    txt(s, x, 2.0, 2.95, 0.8, big, size=28, bold=True, color=col, align="c", anchor="m")
    txt(s, x + 0.1, 2.9, 2.75, 0.95, small, size=14, color=GRAY, align="c")
txt(s, 0.5, 4.2, 12, 0.45, "Recuperación ante desastres (DRP): tiempo de restauración", size=18, bold=True, color=NAVY)
box(s, 0.5, 4.8, 12.0, 0.6, "Objetivo RTO: < 15 minutos", fill="CBD5E1", size=17, bold=True, color=DARK, align="l")
box(s, 0.5, 5.55, 0.18, 0.6, "", fill=GREEN)
txt(s, 0.8, 5.55, 8, 0.6, "Real: 3.2 segundos  ·  RPO = 0 transacciones perdidas", size=20, bold=True, color=GREEN, anchor="m")
box(s, 0.5, 6.35, 6.0, 0.55, "Deuda técnica saneada: 100 %", fill=LGREEN, line=GREEN, size=15, bold=True, color=GREEN)
box(s, 6.75, 6.35, 5.75, 0.55, "Seguridad SAST: 0 vulnerabilidades", fill=LGREEN, line=GREEN, size=15, bold=True, color=GREEN)

# =====================================================================
# 13. DEMO + CIERRE
# =====================================================================
s = base(13, "Demo en vivo y conclusiones", "Sistema real en producción · limitaciones transparentes y hoja de ruta (Cap. 18 y 19)",
         "Equipo completo",
         "[Lady Loayza / Equipo · 60 s] Mostramos el flujo real en producción: login del operador, catálogo con stock, creación del pedido con descuento inmediato, y tracking público. "
         "Cerramos con tres mensajes: logramos 38.2 segundos por pedido, cero sobreventas y 194 pruebas aprobadas; somos transparentes con dos limitaciones, el arranque en frío del plan gratuito "
         "de Render y los servicios externos simulados; y proponemos migrar a una instancia dedicada y conectar credenciales productivas. Muchas gracias; quedamos atentos a sus preguntas.")
box(s, 0.5, 1.75, 12.35, 0.6, "https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/", fill=LAMBER, line=ORANGE, size=20, bold=True, color=ORANGE)
demo = ["Login\noperador", "Catálogo\ntalla y color", "Pedido\ncon stock", "Tracking\npúblico #LFT", "Privacidad\nde montos"]
for i, t in enumerate(demo):
    box(s, 0.5 + i * 2.5, 2.55, 2.6, 1.15, t, fill=NAVY, size=16, bold=True, color=WHITE,
        shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
cards = [("LOGROS", GREEN, LGREEN, "38.2 s por pedido\n0 sobreventas\n194 pruebas · 76.16 % cobertura\nSUS 88.5 · RTO 3.2 s"),
         ("LIMITACIONES", AMBER, LAMBER, "Arranque en frío del plan\ngratuito de Render (15 min)\nServicios externos con\nadaptadores simulados"),
         ("HOJA DE RUTA", BLUE, LBLUE, "Instancia cloud dedicada\n(SLA 99.95 %)\nCredenciales productivas\nWhatsApp / pasarelas")]
for i, (t, col, light, body) in enumerate(cards):
    x = 0.5 + i * 4.15
    box(s, x, 4.0, 4.05, 2.9, "", fill=light, line=col, lw=2.5)
    txt(s, x, 4.05, 4.05, 0.5, t, size=20, bold=True, color=col, align="c")
    txt(s, x + 0.15, 4.6, 3.75, 2.2, body, size=16, color=DARK, align="c", anchor="m")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("PPTX generado:", OUT, "| diapositivas:", len(prs.slides))
