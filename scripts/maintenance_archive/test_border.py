import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

prs = Presentation('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
slide = prs.slides[23] # Slide 24
table_shape = [s for s in slide.shapes if s.has_table][0]
tbl = table_shape.table

# Test styling cell 0,0
cell = tbl.cell(0, 0)
tcPr = cell._tc.get_or_add_tcPr()
ln = parse_xml(f'<a:lnB xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700" cmpd="s"><a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill></a:lnB>')
tcPr.append(ln)
print("Border XML added successfully")

