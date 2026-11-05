import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A - Navy
COLOR_DARK_TEXT = RGBColor(15, 23, 42)   # #0F172A - Slate 900
COLOR_MUTED = RGBColor(71, 85, 105)      # #475569 - Slate 600

print("Fixing all text superpositions in Criterio 5 (Slides 28, 29, 31, 32)...")

# =========================================================================
# 1. SLIDE 28: C4 Nivel 2 y Clean Architecture
# =========================================================================
s28 = prs.slides[27]

for shp in s28.shapes:
    if shp.name == 'TextBox 12':
        # This was overlapping Contenedor 1 because of 2 lines at 24pt
        # Make it a clean single-line container header
        shp.top = Inches(2.72)
        shp.left = Inches(1.33)
        shp.width = Inches(7.56)
        shp.height = Inches(0.40)
        p = shp.text_frame.paragraphs[0]
        p.text = "Arquitectura de Contenedores (C4 Nivel 2)"
        p.font.name = 'Arial'
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        print("Fixed Slide 28 TextBox 12 header (no overlap with Contenedor 1)!")

    elif shp.name == 'TextBox 15':
        shp.top = Inches(3.30)

    elif shp.name == 'TextBox 16':
        shp.top = Inches(3.72)

# =========================================================================
# 2. SLIDE 29: Arquitectura de Datos y Normalización 3FN / BCNF
# =========================================================================
s29 = prs.slides[28]

for shp in s29.shapes:
    if shp.name == 'TextBox 12':
        # Single-line container header to prevent collision with TABLE products
        shp.top = Inches(2.65)
        shp.left = Inches(1.33)
        shp.width = Inches(7.56)
        shp.height = Inches(0.40)
        p = shp.text_frame.paragraphs[0]
        p.text = "Esquema Relacional Normalizado (3FN / BCNF)"
        p.font.name = 'Arial'
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(15)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        print("Fixed Slide 29 TextBox 12 header!")

    elif shp.name == 'TextBox 15':
        # TABLE products was F1F5F9 (white on white) and overlapping!
        shp.top = Inches(3.22)
        p = shp.text_frame.paragraphs[0]
        p.font.color.rgb = COLOR_NAVY
        p.font.bold = True
        for r in p.runs:
            r.font.color.rgb = COLOR_NAVY
            r.font.bold = True
        print("Fixed Slide 29 TextBox 15 (TABLE products) font color to Navy Bold!")

    elif shp.name == 'TextBox 16':
        shp.top = Inches(3.54)

# =========================================================================
# 3. SLIDE 31: LEAN CANVAS (Eliminate all overlaps in cards)
# =========================================================================
s31 = prs.slides[30]

# Precise coordinates and font sizes for Lean Canvas cards:
# Column 1 (Problema): top=1.95 (hdr), 2.45 (body)
# Column 2 Upper (Solución): top=1.95 (hdr), 2.45 (body)
# Column 2 Lower (Métricas): top=4.95 (hdr), 5.40 (body)
# Column 3 (Propuesta): top=1.95 (hdr), 2.45 (body)
# Column 4 Upper (Ventaja): top=1.95 (hdr), 2.45 (body)
# Column 4 Lower (Canales): top=4.95 (hdr), 5.40 (body)
# Column 5 (Clientes): top=1.95 (hdr), 2.45 (body)
# Bottom Left (Costos): top=8.10 (hdr), 8.55 (body)
# Bottom Right (Ingresos): top=8.10 (hdr), 8.55 (body)

lean_fixes = {
    # Column 1: PROBLEMA
    'TextBox 24': {'top': 1.95, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 25': {'top': 2.45, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': '• Gestión manual por WhatsApp.\n• Descoordinación de stock físico en Gamarra.\n• Ciclo lento de toma de orden (45–120 min).\n• 14.2% de errores en despacho y sobreventas.'},
    
    # Column 2 Upper: SOLUCIÓN
    'TextBox 26': {'top': 1.95, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 27': {'top': 2.45, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': '• Catálogo textil PWA con stock en vivo.\n• Checkout guiado en 3 pasos (38.2 s).\n• Generación de rótulo QR para courier.\n• Notificación automática vía WhatsApp API.'},
    
    # Column 2 Lower: MÉTRICAS CLAVE
    'TextBox 28': {'top': 4.90, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 29': {'top': 5.35, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': '• Tiempo captura: 38.2 s (-98.6%).\n• Tasa de conversión: +35% estimada.\n• 0.0% sobreventas (Bloqueo ACID).\n• SUS Usabilidad: 88.5 / 100 (Grado A).'},
    
    # Column 3: PROPUESTA DE VALOR
    'TextBox 30': {'top': 1.95, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 31': {'top': 2.45, 'size': 12, 'space': 4, 'color': COLOR_DARK_TEXT,
                   'text': 'Plataforma Web PWA ultraligera que permite al cliente armar pedidos textiles en segundos con stock reactivo en tiempo real y confirmación inmediata sin demoras.'},
    
    # Column 4 Upper: VENTAJA INJUSTA
    'TextBox 32': {'top': 1.95, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 33': {'top': 2.45, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': '• Trato directo del fundador de LeoFit.\n• PWA ultrarrápida (Lighthouse 98/100, < 1.5 s).\n• Control estricto de inventario por SKU.'},
    
    # Column 4 Lower: CANALES
    'TextBox 34': {'top': 4.90, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 35': {'top': 5.35, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': '• PWA Web Responsive (GitHub Pages CDN).\n• Mensajería directa vía WhatsApp Cloud API.\n• Panel web de administración y despacho.'},
    
    # Column 5: SEGMENTO DE CLIENTES
    'TextBox 36': {'top': 1.95, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 37': {'top': 2.45, 'size': 11.5, 'space': 3, 'color': COLOR_DARK_TEXT,
                   'text': 'Público Objetivo:\nDeportistas, academias y clientes particulares (18 a 45 años) en Lima y provincias que buscan ropa deportiva de alta calidad.'},
    
    # Bottom Left: ESTRUCTURA DE COSTOS
    'TextBox 40': {'top': 8.10, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 38': {'top': 8.55, 'size': 11.5, 'space': 2, 'color': COLOR_DARK_TEXT,
                   'text': '• Infraestructura Cloud (Render PaaS + Neon PostgreSQL Serverless).\n• Desarrollo de software, auditoría de calidad ISO 25010 y CI/CD.\n• Adquisición de telas deportivas, confección y embalaje.\n• Envíos a nivel nacional mediante Olva Courier y Shalom.'},
    
    # Bottom Right: FLUJO DE INGRESOS
    'TextBox 41': {'top': 8.10, 'size': 13, 'bold': True, 'color': COLOR_NAVY},
    'TextBox 39': {'top': 8.55, 'size': 11.5, 'space': 2, 'color': COLOR_DARK_TEXT,
                   'text': '• Venta directa de indumentaria deportiva (Margen bruto: 35% - 45%).\n• Confección por volumen para clubes y academias deportivas.\n• Servicio de personalización textil (estampados y sublimación).'}
}

for shp in s31.shapes:
    if shp.name in lean_fixes:
        cfg = lean_fixes[shp.name]
        shp.top = Inches(cfg['top'])
        if 'text' in cfg:
            shp.text_frame.text = cfg['text']
        for p in shp.text_frame.paragraphs:
            if 'space' in cfg:
                p.space_after = Pt(cfg['space'])
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(cfg['size'])
                if 'bold' in cfg:
                    r.font.bold = cfg['bold']
                if 'color' in cfg:
                    r.font.color.rgb = cfg['color']

print("Fixed Slide 31 Lean Canvas cards (clean layout, zero overlaps)!")

# =========================================================================
# 4. SLIDE 32: MUCHAS GRACIAS (Pill text on single line)
# =========================================================================
s32 = prs.slides[31]

for shp in s32.shapes:
    if shp.name == 'TextBox 7':
        # Expand width and set font to 14pt so it fits cleanly on one line
        shp.top = Inches(7.98)
        shp.left = Inches(5.95)
        shp.width = Inches(8.35)
        p = shp.text_frame.paragraphs[0]
        p.alignment = pptx.enum.text.PP_ALIGN.CENTER
        p.text = "Sustentación Técnica Final · Sistema Web PWA LeoFit v2.0.0 · Grupo 01"
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(13.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        print("Fixed Slide 32 pill text (fits perfectly on single line)!")

prs.save(pptx_path)
print("Saved all Criterio 5 fixes to PPTX successfully!")

