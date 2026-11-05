import pptx
import sys

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s26 = prs.slides[25] # Slide 26 is index 25

print("=== SLIDE 26 SHAPES ===")
for shp in s26.shapes:
    print(f"[{shp.name}] type={shp.shape_type}, left={shp.left/914400:.2f}, top={shp.top/914400:.2f}, w={shp.width/914400:.2f}, h={shp.height/914400:.2f}")
    if shp.has_text_frame:
        print(f"  Text: {repr(shp.text_frame.text[:60])}")

