import sys
from collections import defaultdict
from pptx import Presentation

sys.stdout.reconfigure(encoding='utf-8')
pptx_path = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx'
prs = Presentation(pptx_path)

non_ascii_chars = defaultdict(list)

for slide_idx, slide in enumerate(prs.slides):
    slide_num = slide_idx + 1
    
    def check_text(txt, loc):
        for ch in txt:
            cp = ord(ch)
            # Skip standard spanish accents, punctuation, quotes, dashes, etc.
            # á, é, í, ó, ú, ñ, Á, É, Í, Ó, Ú, Ñ, ü, Ü, ¿, ¡, —, –, •, ·, º, ª, «, », ©, ®, °, %, $, etc.
            standard_latin_ext = [
                'á','é','í','ó','ú','ñ','ü','Á','É','Í','Ó','Ú','Ñ','Ü',
                '¿','¡','—','–','•','·','º','ª','«','»','©','®','°','±',
                '“','”','‘','’','…','′','″'
            ]
            if cp > 127 and ch not in standard_latin_ext:
                non_ascii_chars[(ch, hex(cp))].append((slide_num, loc, txt.strip()[:60]))

    for shape in slide.shapes:
        if shape.has_text_frame:
            for p_idx, p in enumerate(shape.text_frame.paragraphs):
                check_text(p.text, f"{shape.name}:p{p_idx}")
        elif shape.has_table:
            for r_idx, row in enumerate(shape.table.rows):
                for c_idx, cell in enumerate(row.cells):
                    for p_idx, p in enumerate(cell.text_frame.paragraphs):
                        check_text(p.text, f"{shape.name}[r{r_idx},c{c_idx}]:p{p_idx}")

print("Distinct non-standard characters found:")
for (ch, hex_cp), occurrences in sorted(non_ascii_chars.items(), key=lambda x: x[0][1]):
    print(f"Char: {repr(ch)} ({hex_cp}) | Occurrences: {len(occurrences)}")
    for occ in occurrences[:3]:
        print(f"   Slide {occ[0]:2d} | {occ[1]} | {repr(occ[2])}")
