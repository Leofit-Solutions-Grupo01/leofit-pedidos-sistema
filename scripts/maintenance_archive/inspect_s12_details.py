import pptx
import sys
from pptx.dml.color import RGBColor
from pptx.util import Pt

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s12 = prs.slides[11]

print("--- Detailed inspection of Slide 12 State Machine ---")
for shp in s12.shapes:
    if shp.name in ['Group 22', 'TextBox 24', 'Group 25', 'AutoShape 28', 'Group 29', 'AutoShape 32', 'Group 33', 'AutoShape 36', 'Group 37', 'TextBox 40']:
        print(f"Shape: {shp.name} (type={shp.shape_type})")
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    c = r.font.color.rgb if r.font and r.font.color and r.font.color.type == 1 else 'None'
                    print(f"  Text: {repr(r.text)} | Color: {c} | Size: {r.font.size.pt if r.font.size else 'None'} | Bold: {r.font.bold}")
        elif shp.shape_type == 6:
            for c in shp.shapes:
                if c.has_text_frame:
                    for p in c.text_frame.paragraphs:
                        for r in p.runs:
                            clr = r.font.color.rgb if r.font and r.font.color and r.font.color.type == 1 else 'None'
                            print(f"  Child {c.name}: {repr(r.text)} | Color: {clr} | Size: {r.font.size.pt if r.font.size else 'None'} | Bold: {r.font.bold}")

