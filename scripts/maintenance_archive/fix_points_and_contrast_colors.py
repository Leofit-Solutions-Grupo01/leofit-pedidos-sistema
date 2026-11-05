import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)        # #1E3A8A - Tech Navy (High contrast, bold)
COLOR_TEXT_DARK = RGBColor(15, 23, 42)    # #0F172A - Slate 900 (High contrast body text)
COLOR_TEXT_MUTED = RGBColor(51, 65, 85)   # #334155 - Slate 700 (Clean secondary text)

def fix_text_and_colors(shape, slide_idx):
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            p_text = p.text
            
            # 1. Remove point notations like (4 pts), (2 pts), (16 Puntos), (16 Pts)
            replacements = [
                (" (4 pts)", ""),
                (" (4 PTS)", ""),
                ("(4 pts)", ""),
                ("(4 PTS)", ""),
                (" (2 pts)", ""),
                (" (2 PTS)", ""),
                ("(2 pts)", ""),
                ("(2 PTS)", ""),
                (" · Rúbrica de Evaluación APF3 (16 Puntos)", ""),
                (" · Rúbrica APF3 (16 Puntos)", ""),
                (" (16 Puntos)", ""),
                (" (16 Pts)", ""),
                (" (16 pts)", ""),
            ]
            
            for old_s, new_s in replacements:
                if old_s in p_text:
                    for r in p.runs:
                        if old_s in r.text:
                            r.text = r.text.replace(old_s, new_s)
            
            # Check if paragraph is code (Consolas or SQL/JSON keywords)
            is_code_block = any(kw in p_text for kw in [
                'SELECT ', 'FROM ', 'WHERE ', 'INSERT INTO', 'UPDATE ', 'CREATE OR REPLACE',
                'RETURNS TRIGGER', 'BEGIN', 'COMMIT', 'ROLLBACK', 'export class', 'export interface',
                'req: Request', 'res: Response', 'const canonicalBody', 'status: "UP"', 'uptimeSeconds'
            ])
            
            # 2. Fix white or illegible light colors on non-code elements
            for r in p.runs:
                txt = r.text.strip()
                if not txt:
                    continue
                
                # Check run font color
                c_hex = None
                try:
                    if r.font.color and r.font.color.rgb:
                        c_hex = str(r.font.color.rgb).upper()
                except:
                    pass
                
                # If text is white or very light pastel (CBD5E1, E2E8F0, F1F5F9, F8FAFC, FFFFFF)
                if c_hex in ['FFFFFF', 'CBD5E1', 'E2E8F0', 'F1F5F9', 'F8FAFC']:
                    # Only keep white/light text if it's strictly a code snippet on dark background
                    if is_code_block or (r.font.name and 'consolas' in r.font.name.lower()):
                        continue # leave code text styling intact
                    
                    # Otherwise, it's a heading, card text, table text, or label that looks invisible
                    # Make it high-contrast Navy or Dark Slate!
                    if r.font.bold or (r.font.size and r.font.size.pt > 15):
                        r.font.color.rgb = COLOR_NAVY
                        r.font.bold = True
                    else:
                        r.font.color.rgb = COLOR_TEXT_DARK
                        
                # Ensure titles and section headers are always crisp Navy
                if any(kw in txt for kw in ["Criterio 1:", "Criterio 2:", "Criterio 3:", "Criterio 4:", "Criterio 5:", "Agenda Oficial", "Demostración de Interfaz"]):
                    r.font.color.rgb = COLOR_NAVY
                    r.font.bold = True

    # Traverse groups recursively
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
        for child in shape.shapes:
            fix_text_and_colors(child, slide_idx)

print("Fixing point notations and high-contrast colors across all 43 slides...")
for idx, slide in enumerate(prs.slides):
    for shp in slide.shapes:
        fix_text_and_colors(shp, idx)

prs.save(pptx_path)
print(f"Successfully saved updated presentation to {pptx_path}!")

