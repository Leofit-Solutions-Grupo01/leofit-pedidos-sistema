import pptx
import sys

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s20 = prs.slides[19]

print("=== SLIDE 20 SHAPES ===")
for shp in s20.shapes:
    if shp.has_text_frame:
        print(f"[{shp.name}] left={shp.left/914400:.2f}, top={shp.top/914400:.2f}, w={shp.width/914400:.2f}, h={shp.height/914400:.2f}")
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                print(f"  run: {repr(r.text)} | size={r.font.size.pt if r.font.size else 'None'} | color={r.font.color.rgb if r.font and r.font.color and r.font.color.type == 1 else 'None'}")

