import pptx
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')
prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')

print("Starting deep visual inspection across all 43 slides...")

for idx, s in enumerate(prs.slides):
    slide_num = idx + 1
    
    # 1. Inspect groups and shapes for text color vs fill color
    for shp in s.shapes:
        if shp.shape_type == 6: # group
            # Find fills
            fills = []
            for c in shp.shapes:
                xml = c._element.xml
                for line in xml.split('><'):
                    if 'srgbClr' in line and 'val="' in line:
                        v = line.split('val="')[1].split('"')[0]
                        fills.append(v)
            # Find text runs
            for c in shp.shapes:
                if c.has_text_frame:
                    for p in c.text_frame.paragraphs:
                        for r in p.runs:
                            color = str(r.font.color.rgb) if r.font and r.font.color and r.font.color.type == 1 else 'None'
                            # If text color equals one of the fills
                            for f in fills:
                                if color == f and color != 'None':
                                    print(f"[INVISIBLE TEXT] Slide {slide_num} Group {shp.name} -> {c.name}: Text '{r.text.strip()}' has color {color} matching fill {f}!")
                                elif (f in ['1E3A8A', '0F172A', '1E293B', '15803D', '000000'] and color in ['1E3A8A', '0F172A', '1E293B', '334155', '000000']):
                                    print(f"[LOW CONTRAST] Slide {slide_num} Group {shp.name} -> {c.name}: Dark text '{r.text.strip()}' ({color}) on dark fill {f}!")
                                elif (f in ['FFFFFF', 'F8FAFC', 'EFF6FF', 'F1F5F9'] and color in ['FFFFFF', 'F8FAFC', 'F1F5F9', 'None']):
                                    print(f"[LOW CONTRAST] Slide {slide_num} Group {shp.name} -> {c.name}: Light text '{r.text.strip()}' ({color}) on light fill {f}!")

    # 2. Check standalone text boxes that might have a background shape behind them
    # For each text box, check if there's a shape right behind it
    for shp in s.shapes:
        if shp.has_text_frame and shp.shape_type != 6:
            # check runs
            for p in shp.text_frame.paragraphs:
                for r in p.runs:
                    color = str(r.font.color.rgb) if r.font and r.font.color and r.font.color.type == 1 else 'None'
                    # if color is white on a slide with no dark background, or dark on dark
                    # check if shp itself has a fill
                    xml = shp._element.xml
                    for line in xml.split('><'):
                        if 'srgbClr' in line and 'val="' in line:
                            fill = line.split('val="')[1].split('"')[0]
                            if color == fill:
                                print(f"[INVISIBLE TEXT] Slide {slide_num} {shp.name}: Text '{r.text.strip()}' has color {color} matching self fill {fill}!")

