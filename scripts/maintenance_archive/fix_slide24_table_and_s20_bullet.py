import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml import parse_xml
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A
COLOR_DARK_TEXT = RGBColor(15, 23, 42)   # #0F172A
COLOR_WHITE = RGBColor(255, 255, 255)

# =========================================================================
# 1. FIX SLIDE 20: Remove hollow circle bullet from TextBox 3
# =========================================================================
s20 = prs.slides[19]
tb3 = [s for s in s20.shapes if s.name == 'TextBox 3'][0]
for p in tb3.text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr()
    for child in list(pPr):
        if 'bu' in child.tag:
            pPr.remove(child)
    pPr.append(parse_xml('<a:buNone xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    if 'marL' in pPr.attrib:
        del pPr.attrib['marL']
    if 'indent' in pPr.attrib:
        del pPr.attrib['indent']

print("Fixed Slide 20 TextBox 3 bullets!")

# =========================================================================
# 2. FIX SLIDE 24: Replace clipped Object 7 with native PowerPoint Table
# =========================================================================
s24 = prs.slides[23]

# Remove Object 7
for shp in list(s24.shapes):
    if shp.name == 'Object 7':
        sp = shp._element
        sp.getparent().remove(sp)
        print("Removed clipped Object 7 from Slide 24!")

# Also fix TextBox 6 bullet on line 0
tb6 = [s for s in s24.shapes if s.name == 'TextBox 6'][0]
for p in tb6.text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr()
    for child in list(pPr):
        if 'bu' in child.tag:
            pPr.remove(child)
    pPr.append(parse_xml('<a:buNone xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))
    if 'marL' in pPr.attrib:
        del pPr.attrib['marL']
    if 'indent' in pPr.attrib:
        del pPr.attrib['indent']

# Add native clean PowerPoint Table
table_shape = s24.shapes.add_table(6, 3, Inches(9.50), Inches(2.80), Inches(8.80), Inches(4.50))
table = table_shape.table

# Set column widths
table.columns[0].width = Inches(1.80)  # Variable
table.columns[1].width = Inches(2.80)  # Descripción
table.columns[2].width = Inches(4.20)  # Valor en Producción

headers = ["Variable de Entorno", "Descripción Técnica", "Configuración en Producción"]
rows_data = [
    ("NODE_ENV", "Entorno de ejecución del runtime", "production (optimización V8)"),
    ("PORT", "Puerto de escucha HTTP del contenedor", "5000 (Render Web Service)"),
    ("DATABASE_URL", "Cadena de conexión PostgreSQL 16", "neon.tech (SSL obligatorio)"),
    ("JWT_SECRET", "Clave simétrica para firma y verificación", "Secreto criptográfico de 64 bytes"),
    ("CORS_ORIGIN", "Dominio web cliente autorizado", "https://leofit-solutions-grupo01.github.io")
]

# Populate Header
for c_idx, h_text in enumerate(headers):
    cell = table.cell(0, c_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.name = 'Arial'
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.alignment = PP_ALIGN.LEFT

# Populate Data Rows
for r_idx, row_values in enumerate(rows_data):
    for c_idx, val in enumerate(row_values):
        cell = table.cell(r_idx + 1, c_idx)
        p = cell.text_frame.paragraphs[0]
        p.text = val
        p.font.name = 'Arial'
        p.font.size = Pt(11)
        p.font.bold = (c_idx == 0) # Bold for variable name
        p.font.color.rgb = COLOR_NAVY if c_idx == 0 else COLOR_DARK_TEXT
        p.alignment = PP_ALIGN.LEFT

print("Added native high-contrast PowerPoint Table on Slide 24!")

prs.save(pptx_path)
print("Saved Slide 20 and 24 fixes successfully!")

