import pptx
import sys
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

prs = pptx.Presentation(r'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')

print(f"Auditing {len(prs.slides)} slides for overlaps and contrast...")

for i, s in enumerate(prs.slides):
    slide_num = i + 1
    # Check pictures
    pics = [shp for shp in s.shapes if shp.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.PICTURE]
    text_boxes = [shp for shp in s.shapes if shp.has_text_frame]
    
    # Check overlaps between pictures and text
    for p in pics:
        p_top = p.top / 914400
        p_bottom = (p.top + p.height) / 914400
        p_left = p.left / 914400
        p_right = (p.left + p.width) / 914400
        
        for tb in text_boxes:
            tb_top = tb.top / 914400
            tb_bottom = (tb.top + tb.height) / 914400
            tb_left = tb.left / 914400
            tb_right = (tb.left + tb.width) / 914400
            
            overlap_x = max(0, min(p_right, tb_right) - max(p_left, tb_left))
            overlap_y = max(0, min(p_bottom, tb_bottom) - max(p_top, tb_top))
            
            if overlap_x > 0.3 and overlap_y > 0.3:
                print(f"[OVERLAP ALERT] Slide {slide_num}: Picture {p.name} (top={p_top:.2f}, h={p.height/914400:.2f}) overlaps {tb.name} (top={tb_top:.2f}, h={tb.height/914400:.2f}) text='{tb.text_frame.text[:40].strip()}'")

    # Check for dark text inside groups with dark shapes
    for shp in s.shapes:
        if shp.shape_type == 6: # group
            # look for freeforms with dark fills
            dark_fills = []
            for c in shp.shapes:
                if c.shape_type == 5: # freeform
                    xml = c._element.xml
                    for line in xml.split('><'):
                        if 'srgbClr' in line:
                            val = line.split('val="')[-1].split('"')[0] if 'val="' in line else ''
                            if val in ['1E3A8A', '0F172A', '1E293B', '15803D', 'B91C1C', '0369A1']:
                                dark_fills.append((c.name, val))
            if dark_fills:
                # check if there's any text in this group
                for c in shp.shapes:
                    if c.has_text_frame:
                        for p in c.text_frame.paragraphs:
                            for r in p.runs:
                                color = str(r.font.color.rgb) if r.font and r.font.color and r.font.color.type == 1 else 'None'
                                if color in ['1E3A8A', '0F172A', '1E293B', '334155', 'None', 'B91C1C']:
                                    print(f"[CONTRAST ALERT] Slide {slide_num} Group {shp.name} -> {c.name}: dark fill {dark_fills[0][1]} but text color '{color}'! Text='{r.text.strip()}'")
