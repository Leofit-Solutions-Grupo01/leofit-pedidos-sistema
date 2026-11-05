import pptx
from pptx import Presentation

prs = Presentation('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
s24 = prs.slides[23]

print("--- TEXTBOX 6 ---")
tb6 = s24.shapes[2]
for p in tb6.text_frame.paragraphs:
    print(f"P: font_size={p.font.size} bold={p.font.bold} text='{p.text}'")

print("\n--- TABLE 8 ---")
tbl = s24.shapes[4].table
print(f"Table rows: {len(tbl.rows)}, cols: {len(tbl.columns)}")
for r_idx, r in enumerate(tbl.rows):
    print(f"Row {r_idx} height: {r.height/914400:.2f}in")
    for c_idx, c in enumerate(r.cells):
        txt = c.text.replace('\n', ' ')
        print(f"  Col {c_idx} (w={tbl.columns[c_idx].width/914400:.2f}in): {txt}")
