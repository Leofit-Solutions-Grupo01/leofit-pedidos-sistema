import pptx
from pptx.oxml import parse_xml

prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s6 = prs.slides[5]
tb7 = [s for s in s6.shapes if s.name == 'TextBox 7'][0]

for p in tb7.text_frame.paragraphs:
    pPr = p._p.get_or_add_pPr()
    for child in list(pPr):
        if 'bu' in child.tag:
            pPr.remove(child)
    pPr.append(parse_xml('<a:buNone xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

prs.save(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
print("Successfully set a:buNone on all paragraphs of TextBox 7")

