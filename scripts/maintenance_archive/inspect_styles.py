import pptx
from pptx import Presentation

prs = Presentation('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')

for i, s in enumerate(prs.slides):
    title = ""
    for shp in s.shapes:
        if shp.has_text_frame and shp.text.strip():
            title = shp.text.split('\n')[0][:50]
            break
    print(f"Slide index {i} (1-based: {i+1}): {title}")
