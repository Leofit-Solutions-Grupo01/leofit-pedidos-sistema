import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

# Precise Design Colors
COLOR_WHITE = RGBColor(255, 255, 255)       # #FFFFFF - Pure White
COLOR_LIGHT_TEXT = RGBColor(241, 245, 249)  # #F1F5F9 - Slate 100 (Bright, clear on dark)
COLOR_SKY_BLUE = RGBColor(56, 189, 248)     # #38BDF8 - Sky Blue 400 (Accents on dark)
COLOR_EMERALD = RGBColor(74, 222, 128)      # #4ADE80 - Emerald 400 (Success accents on dark)
COLOR_GOLD = RGBColor(250, 204, 21)         # #FACC15 - Gold 400 (Highlights on dark)
COLOR_PEACH = RGBColor(253, 186, 116)       # #FDBA74 - Peach 300 (Headers on dark)
COLOR_ROSE = RGBColor(244, 114, 182)        # #F472B6 - Rose 400 (Badges on dark)

COLOR_NAVY = RGBColor(30, 58, 138)          # #1E3A8A - Tech Navy (Titles on light)
COLOR_DARK_TEXT = RGBColor(15, 23, 42)      # #0F172A - Slate 900 (Body on light)
COLOR_MUTED_TEXT = RGBColor(51, 65, 85)     # #334155 - Slate 700 (Subtitles on light)
COLOR_DARK_GREEN = RGBColor(21, 128, 61)    # #15803D - Green 700 (Metrics on light)

print("Applying strict WCAG 2.1 Contrast Rules across all slides...")

# -------------------------------------------------------------
# SLIDE 08 (Index 7) - Criterio 2: Interoperabilidad Externa
# -------------------------------------------------------------
s8 = prs.slides[7]
for shp in s8.shapes:
    if shp.shape_type == pptx.enum.shapes.MSO_SHAPE_TYPE.GROUP:
        for c in shp.shapes:
            if c.name == "TextBox 12": # API BACKEND central dark card
                for p in c.text_frame.paragraphs:
                    for r in p.runs:
                        t = r.text.strip()
                        if "API BACKEND" in t:
                            r.font.color.rgb = COLOR_SKY_BLUE
                            r.font.bold = True
                        elif "Node.js" in t:
                            r.font.color.rgb = COLOR_WHITE
                            r.font.bold = True
                        elif "Envelope" in t:
                            r.font.color.rgb = COLOR_LIGHT_TEXT
            elif c.name in ["TextBox 19", "TextBox 26", "TextBox 33", "TextBox 40"]: # ms badges
                for p in c.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.color.rgb = COLOR_WHITE
                        r.font.bold = True
            elif c.name == "TextBox 51": # 7 / 7 tests badge (on light green #DCFCE7)
                for p in c.text_frame.paragraphs:
                    for r in p.runs:
                        r.font.color.rgb = COLOR_DARK_GREEN
                        r.font.bold = True

# -------------------------------------------------------------
# SLIDE 19 (Index 18) - Criterio 4: Topología Multi-Cloud
# -------------------------------------------------------------
s19 = prs.slides[18]
# Bottom 4 dark containers (Freeform 42, 46, 50, 54 have dark fill #0F172A)
dark_box_headers = {"TextBox 43", "TextBox 47", "TextBox 51", "TextBox 55"}
dark_box_bodies = {"TextBox 44", "TextBox 48", "TextBox 52", "TextBox 56"}

for shp in s19.shapes:
    if shp.name in dark_box_headers:
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.color.rgb = COLOR_PEACH
                r.font.bold = True
    elif shp.name in dark_box_bodies:
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.color.rgb = COLOR_LIGHT_TEXT # Bright legible white/slate on dark container!
                r.font.bold = False

# -------------------------------------------------------------
# SLIDE 20 (Index 19) - Validación en Producción Cloud
# -------------------------------------------------------------
s20 = prs.slides[19]
# 4 dark container cards at bottom (Freeform 7, 10, 13, 16 have dark fill #1E293B)
for shp in s20.shapes:
    if shp.name == "TextBox 8":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                if "Frontend" in r.text:
                    r.font.color.rgb = COLOR_SKY_BLUE
                    r.font.bold = True
                else:
                    r.font.color.rgb = COLOR_WHITE
                    r.font.bold = False
    elif shp.name == "TextBox 11":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                if "Backend" in r.text:
                    r.font.color.rgb = COLOR_EMERALD
                    r.font.bold = True
                else:
                    r.font.color.rgb = COLOR_WHITE
                    r.font.bold = False
    elif shp.name == "TextBox 14":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                if "Persistencia" in r.text:
                    r.font.color.rgb = COLOR_GOLD
                    r.font.bold = True
                else:
                    r.font.color.rgb = COLOR_WHITE
                    r.font.bold = False
    elif shp.name == "TextBox 17":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                if "Garantía" in r.text:
                    r.font.color.rgb = COLOR_ROSE
                    r.font.bold = True
                else:
                    r.font.color.rgb = COLOR_WHITE
                    r.font.bold = False

# -------------------------------------------------------------
# SLIDE 13 (Index 12) - Concurrencia SELECT FOR UPDATE
# -------------------------------------------------------------
s13 = prs.slides[12]
# Code box TextBox 7 is on dark container #0F172A
for shp in s13.shapes:
    if shp.name == "TextBox 7":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                r.font.color.rgb = COLOR_LIGHT_TEXT
                r.font.name = "Consolas"

# -------------------------------------------------------------
# SLIDE 23 (Index 22) - Monitoreo /api/health
# -------------------------------------------------------------
s23 = prs.slides[22]
# JSON box TextBox 6 is on dark container #0F172A
for shp in s23.shapes:
    if shp.name == "TextBox 6":
        for p in shp.text_frame.paragraphs:
            for r in p.runs:
                if "UP" in r.text or "connected" in r.text:
                    r.font.color.rgb = COLOR_EMERALD
                    r.font.bold = True
                else:
                    r.font.color.rgb = COLOR_LIGHT_TEXT
                r.font.name = "Consolas"

# -------------------------------------------------------------
# GENERAL SCAN: CODE BLOCKS ON DARK CONTAINERS
# Slides 09, 10, 11, 12, 28, 29
# Ensure all code snippets on dark background use crisp light text!
# -------------------------------------------------------------
code_slides = [8, 9, 10, 11, 27, 28] # indices for slides 9, 10, 11, 12, 28, 29
for c_idx in code_slides:
    s = prs.slides[c_idx]
    for shp in s.shapes:
        if shp.has_text_frame:
            for p in shp.text_frame.paragraphs:
                p_text = p.text
                if any(kw in p_text for kw in ['SELECT ', 'CREATE OR REPLACE', 'export class', 'export interface', 'req: Request', 'const canonicalBody', 'TABLE products', 'RAISE EXCEPTION']):
                    for r in p.runs:
                        r.font.name = "Consolas"
                        r.font.color.rgb = COLOR_LIGHT_TEXT

prs.save(pptx_path)
print(f"Successfully applied WCAG 2.1 Contrast Rules to {pptx_path}!")

