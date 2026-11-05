import pptx
from pptx.util import Pt
from pptx.dml.color import RGBColor
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)
COLOR_SUBTITLE = RGBColor(71, 85, 105)

# 1. Update Slide 30 (Index 29)
s30 = prs.slides[29]
for shp in s30.shapes:
    if shp.has_text_frame:
        for p in shp.text_frame.paragraphs:
            txt = p.text.strip()
            if "Bloque I:" in txt:
                p.text = "Criterio 5: Impacto Cuantitativo en el Negocio (AS-IS vs TO-BE)"
                p.font.name = "Calibri"
                p.font.size = Pt(28)
                p.font.bold = True
                p.font.color.rgb = COLOR_NAVY
                print("Updated Slide 30 title!")
            elif "Diagnóstico en Gamarra" in txt:
                p.text = "Cuadro Comparativo de Brechas Operativas y Mejoras Demostradas en Producción"
                p.font.name = "Calibri"
                p.font.size = Pt(16.5)
                p.font.bold = False
                p.font.color.rgb = COLOR_SUBTITLE
                print("Updated Slide 30 subtitle!")
            elif "Diagnóstico de Brechas" in txt:
                p.text = "Matriz de Reducción de Tiempos, Errores y Cero Sobreventas"
                p.font.name = "Calibri"
                p.font.bold = True
                p.font.color.rgb = COLOR_NAVY
                print("Updated Slide 30 table header!")

# 2. Update Slide 13 (Index 12) - Remove old APF2 comment
s13 = prs.slides[12]
for shp in s13.shapes:
    if shp.has_text_frame:
        for p in shp.text_frame.paragraphs:
            if "Informe APF2" in p.text:
                for r in p.runs:
                    if "Informe APF2" in r.text:
                        r.text = r.text.replace("Informe APF2", "LeoFit v2.0.0")
                        print("Updated Slide 13 code comment from APF2 to LeoFit v2.0.0!")

# 3. Update Slide 28 (Index 27) - Clean title
s28 = prs.slides[27]
for shp in s28.shapes:
    if shp.has_text_frame and "MODELO DE CONTENEDORES" in shp.text_frame.text:
        p = shp.text_frame.paragraphs[0]
        p.text = "Criterio 5: Modelo de Contenedores (C4 Nivel 2) y Clean Architecture"
        p.font.name = "Calibri"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        print("Updated Slide 28 title!")

# 4. Update Slide 29 (Index 28) - Clean title
s29 = prs.slides[28]
for shp in s29.shapes:
    if shp.has_text_frame and "ESQUEMA RELACIONAL" in shp.text_frame.text:
        p = shp.text_frame.paragraphs[0]
        p.text = "Criterio 5: Arquitectura de Datos y Normalización 3FN / BCNF"
        p.font.name = "Calibri"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        print("Updated Slide 29 title!")

# 5. Update Slide 31 (Index 30) - Clean title
s31 = prs.slides[30]
for shp in s31.shapes:
    if shp.has_text_frame and "LEAN CANVAS" in shp.text_frame.text:
        p = shp.text_frame.paragraphs[0]
        p.text = "Criterio 5: Lean Canvas — Modelo de Negocio LeoFit S.A.C."
        p.font.name = "Calibri"
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        print("Updated Slide 31 title!")

# 6. Update Slide 32 (Index 31) - Clean closing
s32 = prs.slides[31]
for shp in s32.shapes:
    if shp.has_text_frame:
        for p in shp.text_frame.paragraphs:
            if "Gestión y Toma de Pedidos" in p.text:
                p.text = "Sustentación Técnica Final · Sistema Web PWA LeoFit v2.0.0 · Grupo 01"
                p.font.name = "Calibri"
                p.font.size = Pt(20)
                p.font.color.rgb = COLOR_SUBTITLE
                print("Updated Slide 32 subtitle!")

prs.save(pptx_path)
print("Saved all updates to PPTX successfully!")

