import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF - Pure White
COLOR_NAVY = RGBColor(30, 58, 138)          # #1E3A8A - Tech Navy
COLOR_DARK_TEXT = RGBColor(15, 23, 42)      # #0F172A - Slate 900
COLOR_MUTED_TEXT = RGBColor(71, 85, 105)    # #475569 - Slate 600
COLOR_RED = RGBColor(185, 28, 28)           # #B91C1C - Red 700
COLOR_GREEN = RGBColor(21, 128, 61)         # #15803D - Green 700

print("Applying visual and aesthetic fixes...")

# =========================================================================
# 1. FIX SLIDE 12: MÁQUINA DE ESTADOS FINITA (order_status_history)
# =========================================================================
s12 = prs.slides[11]

for shp in s12.shapes:
    # State badges text (RECIBIDO, PREPARACION, EN_CAMINO, ENTREGADO)
    if shp.name in ['Group 25', 'Group 29', 'Group 33', 'Group 37']:
        for c in shp.shapes:
            if c.has_text_frame:
                for p in c.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.name = 'Arial'
                        r.font.size = Pt(14)
                        r.font.bold = True
                        r.font.color.rgb = COLOR_WHITE  # Crisp White on dark badge!
                print(f"Fixed Slide 12 {shp.name} -> {c.name} text to White Bold!")
    elif shp.name == 'TextBox 24':
        # Title of State Machine
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(16.5)
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
    elif shp.name == 'TextBox 40':
        # Compensation note
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(13)
                r.font.bold = True
                r.font.color.rgb = COLOR_RED

# =========================================================================
# 2. FIX SLIDE 18: CLEAR ACCIDENTAL TEXT IN FREEFORM 2
# =========================================================================
s18 = prs.slides[17]
for shp in s18.shapes:
    if shp.name == 'Freeform 2' and shp.has_text_frame:
        shp.text_frame.text = ''
        print("Cleared accidental text in Slide 18 Freeform 2!")

# =========================================================================
# 3. FIX SLIDE 06: PLAN DE PRUEBAS AUTOMATIZADAS (NO OVERLAP)
# =========================================================================
s6 = prs.slides[5]

# Reposition TextBox 5 (Title)
for shp in s6.shapes:
    if shp.name == 'TextBox 5':
        shp.top = Inches(0.65)
        shp.left = Inches(1.12)
        shp.width = Inches(16.78)
        shp.height = Inches(0.60)
        p = shp.text_frame.paragraphs[0]
        p.text = "Plan de Pruebas Automatizadas del Sistema (194 Tests)"
        p.font.name = 'Arial'
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(26)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY

    elif shp.name == 'TextBox 6':
        shp.top = Inches(1.30)
        shp.left = Inches(1.12)
        shp.width = Inches(16.78)
        shp.height = Inches(0.35)
        p = shp.text_frame.paragraphs[0]
        p.text = "1) Estrategia de Calidad ISO/IEC 25010 · Cobertura Integral Frontend y Backend"
        p.font.name = 'Arial'
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_MUTED_TEXT
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(14)
            r.font.bold = True
            r.font.color.rgb = COLOR_MUTED_TEXT

    elif shp.name == 'TextBox 7':
        shp.top = Inches(1.75)
        shp.left = Inches(1.12)
        shp.width = Inches(16.50)
        shp.height = Inches(1.30)
        tf = shp.text_frame
        tf.clear()
        
        # P1: Frontend
        p1 = tf.paragraphs[0]
        p1.space_after = Pt(4)
        r1_b = p1.add_run()
        r1_b.text = "• Frontend PWA: "
        r1_b.font.name = 'Arial'
        r1_b.font.size = Pt(13.5)
        r1_b.font.bold = True
        r1_b.font.color.rgb = COLOR_NAVY
        
        r1_t = p1.add_run()
        r1_t.text = "69 pruebas automatizadas con Vitest y React Testing Library (10 suites, 100% éxito) · Renderizado reactivo, catálogo y WCAG 2.1 AAA."
        r1_t.font.name = 'Arial'
        r1_t.font.size = Pt(13.5)
        r1_t.font.bold = False
        r1_t.font.color.rgb = COLOR_DARK_TEXT
        
        # P2: Backend
        p2 = tf.add_paragraph()
        p2.space_after = Pt(4)
        r2_b = p2.add_run()
        r2_b.text = "• Backend REST: "
        r2_b.font.name = 'Arial'
        r2_b.font.size = Pt(13.5)
        r2_b.font.bold = True
        r2_b.font.color.rgb = COLOR_GREEN
        
        r2_t = p2.add_run()
        r2_t.text = "125 pruebas automatizadas con Jest y Supertest (17 suites, 99.49% éxito) · Transaccionalidad ACID, deduplicación RFC 8785 y OWASP Top 10."
        r2_t.font.name = 'Arial'
        r2_t.font.size = Pt(13.5)
        r2_t.font.bold = False
        r2_t.font.color.rgb = COLOR_DARK_TEXT

        # P3: Quality Gate
        p3 = tf.add_paragraph()
        r3_b = p3.add_run()
        r3_b.text = "• Integración Continua: "
        r3_b.font.name = 'Arial'
        r3_b.font.size = Pt(13.5)
        r3_b.font.bold = True
        r3_b.font.color.rgb = RGBColor(180, 83, 9) # Amber 700
        
        r3_t = p3.add_run()
        r3_t.text = "194 pruebas continuas integradas en GitHub Actions ejecutadas en cada commit con Quality Gate automático."
        r3_t.font.name = 'Arial'
        r3_t.font.size = Pt(13.5)
        r3_t.font.bold = False
        r3_t.font.color.rgb = COLOR_DARK_TEXT

# Remove any existing Picture on Slide 6
for shp in list(s6.shapes):
    if shp.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE:
        sp = shp._element
        sp.getparent().remove(sp)

# Re-insert picture with exact dimensions and ZERO overlap
img_path = r"docs/04_diagramas_arquitectura_y_negocio/apf3/fig_pruebas_por_suite.png"
# Picture starts at top=3.25 inches (TextBox 7 ends at ~3.05 inches)
# Height = 7.30 inches, Width = 15.35 inches
pic = s6.shapes.add_picture(img_path, Inches(1.12), Inches(3.25), height=Inches(7.30))
print(f"Slide 6 layout perfected! Pic left={pic.left/914400:.2f}, top={pic.top/914400:.2f}, w={pic.width/914400:.2f}, h={pic.height/914400:.2f}")

prs.save(pptx_path)
print("Saved all visual enhancements to PPTX successfully!")

