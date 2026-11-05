import sys
from pptx import Presentation

sys.stdout.reconfigure(encoding='utf-8')

backup_path = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software_ORIGINAL_BACKUP.pptx'
current_path = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx'

prs_orig = Presentation(backup_path)
prs_curr = Presentation(current_path)

# 1. Restore exact text on code/bullet slides that had formatting altered by strip
slides_to_restore = [4, 9, 10, 21, 23, 27, 28, 29] # 1-based slide numbers
# (Note: slide 24 and 30 were created by us and must NOT be restored from backup)

for s_num in slides_to_restore:
    s_idx = s_num - 1
    s_orig = prs_orig.slides[s_idx]
    s_curr = prs_curr.slides[s_idx]
    
    # Restore matching shapes text
    for shp_curr in s_curr.shapes:
        if shp_curr.has_text_frame:
            match_orig = [s for s in s_orig.shapes if s.name == shp_curr.name]
            if match_orig and match_orig[0].has_text_frame:
                shp_orig = match_orig[0]
                # If paragraph counts match, restore paragraph texts
                if len(shp_curr.text_frame.paragraphs) == len(shp_orig.text_frame.paragraphs):
                    for p_curr, p_orig in zip(shp_curr.text_frame.paragraphs, shp_orig.text_frame.paragraphs):
                        p_curr.text = p_orig.text
        elif shp_curr.has_table:
            match_orig = [s for s in s_orig.shapes if s.name == shp_curr.name]
            if match_orig and match_orig[0].has_table:
                t_orig = match_orig[0].table
                t_curr = shp_curr.table
                for r_idx in range(len(t_curr.rows)):
                    for c_idx in range(len(t_curr.columns)):
                        cell_curr = t_curr.cell(r_idx, c_idx)
                        cell_orig = t_orig.cell(r_idx, c_idx)
                        for p_curr, p_orig in zip(cell_curr.text_frame.paragraphs, cell_orig.text_frame.paragraphs):
                            p_curr.text = p_orig.text

print("Restored original code and text formatting on affected slides.")

# 2. Targeted Emoji Cleaner: ONLY replaces exact emojis/symbols without touching ANY other whitespace or character
EMOJI_TARGETS = {
    '✅': '',
    '✓': '•',
    '● ● ●': '[CONSOLE]',
    '●': '•',
    '⚡': '',
    '🏢': '',
    '📍': '',
    '💰': '',
    '👤': '',
    '🌐': '',
    '🔒': '',
    '🚀': '',
    '💻': '',
    '📊': '',
    '📈': '',
}

def remove_emojis_precise(text):
    for em, rep in EMOJI_TARGETS.items():
        text = text.replace(em, rep)
    return text

emoji_count = 0
for slide_idx, slide in enumerate(prs_curr.slides):
    slide_num = slide_idx + 1
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    cleaned_r = remove_emojis_precise(r.text)
                    if cleaned_r != r.text:
                        print(f"Slide {slide_num} {shape.name} run: {repr(r.text)} -> {repr(cleaned_r)}")
                        r.text = cleaned_r
                        emoji_count += 1
                cleaned_p = remove_emojis_precise(p.text)
                if cleaned_p != p.text:
                    print(f"Slide {slide_num} {shape.name} para: {repr(p.text)} -> {repr(cleaned_p)}")
                    p.text = cleaned_p
                    emoji_count += 1
        elif shape.has_table:
            for r_idx, row in enumerate(shape.table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for p in cell.text_frame.paragraphs:
                        for r in p.runs:
                            cleaned_r = remove_emojis_precise(r.text)
                            if cleaned_r != r.text:
                                print(f"Slide {slide_num} table[{r_idx},{c_idx}] run: {repr(r.text)} -> {repr(cleaned_r)}")
                                r.text = cleaned_r
                                emoji_count += 1
                        cleaned_p = remove_emojis_precise(p.text)
                        if cleaned_p != p.text:
                            print(f"Slide {slide_num} table[{r_idx},{c_idx}] para: {repr(p.text)} -> {repr(cleaned_p)}")
                            p.text = cleaned_p
                            emoji_count += 1

print(f"Total targeted emoji replacements: {emoji_count}")

prs_curr.save(current_path)
print("Saved cleanly to", current_path)

