import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

# Unified Color Palette
COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A - Tech Navy (Titles, Key Badges)
COLOR_TEXT_DARK = RGBColor(15, 23, 42)   # #0F172A - Slate 900 (High contrast body)
COLOR_TEXT_MUTED = RGBColor(71, 85, 105) # #475569 - Slate 600 (Subtitles, notes)
COLOR_GREEN = RGBColor(21, 128, 61)      # #15803D - Green 700 (Success, 100% metrics)
COLOR_BLUE = RGBColor(37, 99, 235)       # #2563EB - Royal Blue (Accent links, PWA)
COLOR_AMBER = RGBColor(180, 83, 9)       # #B45309 - Amber (Gateways, limits)
COLOR_RED = RGBColor(185, 28, 28)        # #B91C1C - Red (AS-IS problem items)

FONT_PRIMARY = "Calibri"
FONT_CODE = "Consolas"

def process_shape(shape, slide_idx):
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            p_text = p.text.strip()
            if not p_text:
                continue
            
            for r in p.runs:
                txt = r.text.strip()
                if not txt:
                    continue
                
                # Check if this is a code snippet
                is_code = any(kw in p_text for kw in ['SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'CREATE', 'TRIGGER', 'interface', 'class', 'export', 'import', 'req: Request', 'const ']) or (r.font.name and 'consolas' in r.font.name.lower())
                
                if is_code:
                    r.font.name = FONT_CODE
                    if r.font.size and r.font.size.pt > 13:
                        r.font.size = Pt(11.5)
                    continue

                # Default font family to clean corporate Calibri
                r.font.name = FONT_PRIMARY
                
                # SLIDE 02 (AGENDA) - Specific Tuning
                if slide_idx == 1:
                    if shape.name == "TextBox 2" or "Agenda" in txt:
                        r.font.size = Pt(36)
                        r.font.bold = True
                        r.font.color.rgb = COLOR_NAVY
                    elif shape.name in ["TextBox 3", "TextBox 11"] or "Criterio de Evaluación" in txt or "Artefactos y Responsable" in txt:
                        r.font.size = Pt(15)
                        r.font.bold = True
                    elif any(kw in txt for kw in ["1. Pruebas", "2. Pruebas", "3. Usabilidad", "4. Plataforma", "5. Sustentación", "Seguridad Defensiva", "Concurrencia", "Auditoría", "Demostración"]):
                        r.font.size = Pt(13)
                        r.font.bold = True
                        r.font.color.rgb = COLOR_NAVY
                    else:
                        r.font.size = Pt(12)
                        r.font.bold = False
                        r.font.color.rgb = COLOR_TEXT_DARK
                    continue

                # Main Section Headers (Slides 3, 8, 14, 19, 27)
                if any(kw in txt for kw in ["Criterio 1:", "Criterio 2:", "Criterio 3:", "Criterio 4:", "Criterio 5:"]):
                    r.font.size = Pt(32)
                    r.font.bold = True
                    r.font.color.rgb = COLOR_NAVY
                    continue
                
                # Subtitles on Section Headers
                if any(kw in txt for kw in ["ISO 25010 · 194 Tests", "Interoperabilidad Externa", "ISO 25010 · SUS Score", "Topología Multi-Cloud", "Aportes al Proyecto"]):
                    r.font.size = Pt(18)
                    r.font.bold = False
                    r.font.color.rgb = COLOR_TEXT_MUTED
                    continue

                # Large numeric metrics (e.g. 194, 88.5, 38.2s, 0.0%)
                if txt in ["194", "88.5", "0.0%", "38.2 s", "100%"]:
                    r.font.bold = True
                    continue

                # Fix odd Canva decimal sizes to standard typography scale
                if r.font.size:
                    sz_pt = r.font.size.pt
                    if sz_pt > 50:
                        pass # keep huge hero titles
                    elif sz_pt > 35:
                        r.font.size = Pt(32)
                    elif sz_pt > 22:
                        r.font.size = Pt(22)
                    elif sz_pt > 17:
                        r.font.size = Pt(16.5)
                    elif sz_pt > 14:
                        r.font.size = Pt(14)
                    elif sz_pt > 11:
                        r.font.size = Pt(12.5)

    # Process child shapes if it's a group
    if shape.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
        for child in shape.shapes:
            process_shape(child, slide_idx)

print("Processing all 43 slides for consistent typography, font sizes, and colors...")
for idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        process_shape(shape, idx)

prs.save(pptx_path)
print(f"Saved beautified presentation to {pptx_path}!")

