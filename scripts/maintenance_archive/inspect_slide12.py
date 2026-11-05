import pptx
import sys

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s12 = prs.slides[11]

def inspect_fill_and_text(shp, prefix=''):
    xml = shp._element.xml
    fills = []
    for line in xml.split('><'):
        if 'srgbClr' in line:
            fills.append(line)
    fill_info = fills[0][:80] if fills else 'None'
    print(f"{prefix}{shp.name} (type={shp.shape_type}) fill_first={fill_info}")
    if shp.has_text_frame:
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                c = r.font.color.rgb if r.font and r.font.color and r.font.color.type == 1 else 'None'
                sz = r.font.size.pt if r.font.size else 'None'
                print(f"{prefix}  text: {repr(r.text)} | color: {c} | size: {sz}")
    elif shp.shape_type == 6:
        for c in shp.shapes:
            inspect_fill_and_text(c, prefix + '  ')

for shp in s12.shapes:
    if any(k in shp.name for k in ['22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40']):
        inspect_fill_and_text(shp)

