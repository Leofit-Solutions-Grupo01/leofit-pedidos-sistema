import re
import sys
from pptx import Presentation

sys.stdout.reconfigure(encoding='utf-8')
pptx_path = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx'
prs = Presentation(pptx_path)

# Detailed audit of every slide
replacements_count = 0

def clean_text(text):
    global replacements_count
    orig = text
    
    # Emojis & checkmarks
    text = text.replace('✅', '')
    text = text.replace('✓', '•')
    text = text.replace('● ● ●', '[CONSOLE]')
    text = text.replace('●', '•')
    
    # Strip any potential emoji unicode codepoints
    # Range 1F300 - 1FAFF, 2600 - 27BF, etc.
    cleaned = []
    for ch in text:
        cp = ord(ch)
        if (0x1F300 <= cp <= 0x1FAFF) or (0x2600 <= cp <= 0x27BF and ch not in ['•']):
            # It's an emoji/symbol, skip it
            continue
        cleaned.append(ch)
    text = "".join(cleaned)
    
    # Clean up double spaces or trailing spaces around removed emojis
    text = re.sub(r' +', ' ', text)
    text = re.sub(r' \n', '\n', text)
    
    if orig != text:
        replacements_count += 1
        return text.strip()
    return orig

print("Scanning and removing emojis across all slides...")

for slide_idx, slide in enumerate(prs.slides):
    slide_num = slide_idx + 1
    for shape in slide.shapes:
        if shape.has_text_frame:
            for p in shape.text_frame.paragraphs:
                for r in p.runs:
                    new_r = clean_text(r.text)
                    if new_r != r.text:
                        print(f"Slide {slide_num} (shape {shape.name}) replaced: {repr(r.text)} -> {repr(new_r)}")
                        r.text = new_r
                # Also check paragraph text directly if no runs or combined
                new_p = clean_text(p.text)
                if new_p != p.text:
                    # If paragraph had emoji outside individual runs
                    print(f"Slide {slide_num} (shape {shape.name} p) replaced: {repr(p.text)} -> {repr(new_p)}")
                    p.text = new_p

        elif shape.has_table:
            for r_idx, row in enumerate(shape.table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for p in cell.text_frame.paragraphs:
                        for r in p.runs:
                            new_r = clean_text(r.text)
                            if new_r != r.text:
                                print(f"Slide {slide_num} (table[{r_idx},{c_idx}]) replaced: {repr(r.text)} -> {repr(new_r)}")
                                r.text = new_r
                        new_p = clean_text(p.text)
                        if new_p != p.text:
                            print(f"Slide {slide_num} (table[{r_idx},{c_idx}] p) replaced: {repr(p.text)} -> {repr(new_p)}")
                            p.text = new_p

print(f"\nTotal replacements performed: {replacements_count}")
prs.save(pptx_path)
print("Presentation saved successfully without any emojis.")

