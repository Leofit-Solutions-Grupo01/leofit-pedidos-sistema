import pptx
from pptx import Presentation

prs = Presentation('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s30 = prs.slides[29]
print('Slide 30 total shapes:', len(s30.shapes))
for i, s in enumerate(s30.shapes):
    txt = s.text[:30].replace('\n', ' ') if s.has_text_frame else ''
    print(f'[{i}] id={s.shape_id} name={s.name} left={s.left/914400:.2f}in top={s.top/914400:.2f}in w={s.width/914400:.2f}in h={s.height/914400:.2f}in | {txt}')

