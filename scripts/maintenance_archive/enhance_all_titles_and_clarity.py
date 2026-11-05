import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"C:\Users\Loayza\Downloads\leofit-pedidos-sistema\docs\00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3\GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)        # #1E3A8A - Tech Navy
COLOR_SUBTITLE = RGBColor(71, 85, 105)    # #475569 - Slate 600
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_TEXT_DARK = RGBColor(15, 23, 42)    # #0F172A
COLOR_BG_CARD = RGBColor(241, 245, 249)   # #F1F5F9 - Light slate
COLOR_BLUE = RGBColor(37, 99, 235)        # #2563EB

FONT_FAMILY = "Calibri"

def add_header_banner(slide, title_text, subtitle_text, top_in=0.45, h_in=1.6):
    tx_box = slide.shapes.add_textbox(Inches(0.6), Inches(top_in), Inches(18.8), Inches(h_in))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    # Title
    p1 = tf.paragraphs[0]
    p1.text = title_text
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_NAVY
    p1.space_after = Pt(4)
    
    # Subtitle
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(16.5)
    p2.font.bold = False
    p2.font.color.rgb = COLOR_SUBTITLE

print("Applying clarity titles and aesthetic enhancements to specific slides...")

# Slide 15 (Index 14) - Demostración Catálogo y Variantes
s15 = prs.slides[14]
add_header_banner(
    s15,
    "Criterio 3: Demostración de Interfaz PWA — Catálogo Textil y Stock Reactivo",
    "Gestión multicanal de prendas deportivas: variantes por talla y color, carga reactiva y control de stock en vivo",
    top_in=0.5, h_in=1.8
)

# Slide 16 (Index 15) - Prevención de Errores Inline
s16 = prs.slides[15]
add_header_banner(
    s16,
    "Criterio 3: Demostración de Interfaz PWA — Prevención Activa de Errores",
    "Filosofía 'prevenir antes que culpar': validaciones inline reactivas, bloqueo de tallas agotadas y preservación de estado",
    top_in=0.5, h_in=1.8
)

# Slide 17 (Index 16) - Checkout Rápido y Rótulo QR
s17 = prs.slides[16]
add_header_banner(
    s17,
    "Criterio 3: Demostración de Interfaz PWA — Checkout en 3 Pasos y Rótulo QR",
    "Toma de pedidos ágil en 38.2 s (-98.6%) con autollenado de clientes y generación automática de rótulo para Olva/Shalom",
    top_in=0.35, h_in=1.5
)

# Slide 18 (Index 17) - URL Producción
s18 = prs.slides[17]
add_header_banner(
    s18,
    "Demostración en Producción Cloud: URL Pública Oficial PWA",
    "Desplegado Serverless en GitHub Pages Edge CDN bajo HTTPS TLS 1.3 con Service Worker y persistencia IndexedDB",
    top_in=0.35, h_in=1.5
)

# Slide 05 (Index 4) - Pirámide de Pruebas
s5 = prs.slides[4]
# Check existing text box
for shp in s5.shapes:
    if shp.has_text_frame and "Pirámide" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Criterio 1: Pirámide de Pruebas y Quality Gate CI/CD"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        # Add explanatory subtitle if not present
        if len(tf.paragraphs) == 1:
            p2 = tf.add_paragraph()
            p2.text = "69 Pruebas Unitarias (Vitest) · 125 Pruebas Integración (Jest/Supertest) · Quality Gate Automatizado en GitHub Actions"
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(16.5)
            p2.font.color.rgb = COLOR_SUBTITLE

# Slide 06 (Index 5) - Plan de Pruebas
s6 = prs.slides[5]
for shp in s6.shapes:
    if shp.has_text_frame and "DESPLIEGUE" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Plan de Pruebas Automatizadas del Sistema (194 Tests)"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY

# Slide 20 (Index 19) - Validación Cloud
s20 = prs.slides[19]
for shp in s20.shapes:
    if shp.has_text_frame and "URL Oficial" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Validación y Verificación del Sistema en Producción Cloud"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY

# Slide 22 (Index 21) - Diagrama Multi-Cloud
s22 = prs.slides[21]
for shp in s22.shapes:
    if shp.has_text_frame and "Diagrama de Arquitectura" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Diagrama de Arquitectura de Despliegue Multi-Cloud"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        if len(tf.paragraphs) == 1:
            p2 = tf.add_paragraph()
            p2.text = "Topología Desacoplada: GitHub Pages Edge CDN (Frontend) ↔ Render PaaS (Backend) ↔ Neon Serverless PostgreSQL 16"
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(16.5)
            p2.font.color.rgb = COLOR_SUBTITLE

# Slide 25 (Index 24) - Evidencia Despliegue
s25 = prs.slides[24]
for shp in s25.shapes:
    if shp.has_text_frame and "Evidencia de pruebas" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Evidencias de Pruebas de Despliegue y CI/CD en GitHub Actions"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        if len(tf.paragraphs) == 1:
            p2 = tf.add_paragraph()
            p2.text = "Pipeline en verde: Build de Vite, suite de 194 pruebas automatizadas y despliegue continuo sin errores"
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(16.5)
            p2.font.color.rgb = COLOR_SUBTITLE

# Slide 26 (Index 25) - Evidencia BD
s26 = prs.slides[25]
for shp in s26.shapes:
    if shp.has_text_frame and "Evidencias de monitoreo" in shp.text_frame.text:
        tf = shp.text_frame
        p = tf.paragraphs[0]
        p.text = "Monitoreo y Administración de Base de Datos en Neon Console"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        if len(tf.paragraphs) == 1:
            p2 = tf.add_paragraph()
            p2.text = "Clúster PostgreSQL 16 Serverless (neon.tech): Conexión SSL activa, PgBouncer Pooler y telemetría de consultas"
            p2.font.name = FONT_FAMILY
            p2.font.size = Pt(16.5)
            p2.font.color.rgb = COLOR_SUBTITLE

prs.save(pptx_path)
print(f"Successfully saved updated presentation to {pptx_path}!")

