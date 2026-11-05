import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

PPTX_PATH = 'docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx'

def set_cell_border(cell, color="CBD5E1", width="12700"):
    tcPr = cell._tc.get_or_add_tcPr()
    for border_name in ['lnL', 'lnR', 'lnT', 'lnB']:
        ln = parse_xml(
            f'<a:{border_name} xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="{width}" cmpd="s">'
            f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'</a:{border_name}>'
        )
        tcPr.append(ln)

def set_cell_background(cell, hex_color):
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor.from_string(hex_color)

def remove_shape(shape):
    sp = shape._element
    sp.getparent().remove(sp)

def update_slide_24(prs):
    print("Fine-tuning Slide 24 left container...")
    s24 = prs.slides[23]
    
    card_arch = [s for s in s24.shapes if s.name == 'Card_ArchContainer24'][0]
    tf_a = card_arch.text_frame
    tf_a.clear()
    tf_a.margin_left = tf_a.margin_right = Inches(0.28)
    tf_a.margin_top = Inches(0.22)
    tf_a.margin_bottom = Inches(0.20)
    
    def add_arch_section(title, items, is_first=False):
        p_head = tf_a.paragraphs[0] if is_first else tf_a.add_paragraph()
        p_head.text = title
        p_head.font.name = "Segoe UI"
        p_head.font.size = Pt(12)
        p_head.font.bold = True
        p_head.font.color.rgb = RGBColor(30, 58, 138)
        p_head.alignment = PP_ALIGN.LEFT
        if not is_first:
            p_head.space_before = Pt(10)
        p_head.space_after = Pt(2)
        
        for item in items:
            p_item = tf_a.add_paragraph()
            p_item.text = f"•  {item}"
            p_item.font.name = "Segoe UI"
            p_item.font.size = Pt(10)
            p_item.font.color.rgb = RGBColor(51, 65, 85)
            p_item.alignment = PP_ALIGN.LEFT
            p_item.space_before = Pt(1)
            p_item.space_after = Pt(1)

    add_arch_section("1. Arquitectura Multi-Cloud de 3 Capas:", [
        "PWA / Frontend: GitHub Pages Edge CDN (HTTPS TLS 1.3)",
        "API / Backend: Render Cloud Web Service (Node.js 20 LTS en contenedor Docker)",
        "Base de Datos: Clúster Serverless PostgreSQL 16 en Neon Cloud (SSL Obligatorio)"
    ], is_first=True)

    add_arch_section("2. Seguridad Defensiva y Hardening:", [
        "Protocolo HTTPS TLS 1.3 con directivas estrictas HSTS y CSP",
        "Conexión a Base de Datos mediante canal SSL obligatorio (verify-full)",
        "Autenticación Stateless JWT con algoritmo HS256 y rotación de firmas",
        "CORS restringido estrictamente al dominio de producción del cliente"
    ])

    add_arch_section("3. Proceso de Despliegue y CI/CD:", [
        "Pipeline automatizado en GitHub Actions (3 workflows coordinados)",
        "Verificación de esquemas TypeScript y 194 pruebas automatizadas previas",
        "Estrategia de despliegue continuo (Continuous Deployment) con tag semántico"
    ])

    add_arch_section("4. Observabilidad y Monitoreo Activo:", [
        "Telemetría activa en endpoint público /api/health (HTTP 200)",
        "Logs centralizados en Render y reinicio automático por fallos (Health Check)"
    ])

    # 5. Stack Tecnológico & Gobernanza Cloud
    p_st = tf_a.add_paragraph()
    p_st.text = "5. Gobernanza y Stack Tecnológico Certificado:"
    p_st.font.name = "Segoe UI"
    p_st.font.size = Pt(12)
    p_st.font.bold = True
    p_st.font.color.rgb = RGBColor(30, 58, 138)
    p_st.space_before = Pt(10)
    p_st.space_after = Pt(2)

    for item in [
        "Runtime Backend: Node.js 20.x LTS | Express 4.19 | TypeScript 5.4",
        "Frontend PWA: React 19 | Tailwind CSS 4 | Vite 6 | Workbox PWA Service Worker",
        "Base de Datos Cloud: PostgreSQL 16 Serverless (Pool de conexiones Neon SSL)",
        "Aislamiento y Calidad: Vitest + Supertest + Jest (194 tests) + OWASP Top 10"
    ]:
        p_item = tf_a.add_paragraph()
        p_item.text = f"•  {item}"
        p_item.font.name = "Segoe UI"
        p_item.font.size = Pt(10)
        p_item.font.color.rgb = RGBColor(51, 65, 85)
        p_item.space_before = Pt(1)
        p_item.space_after = Pt(1)

    print("Slide 24 fine-tuned successfully.")

def main():
    prs = Presentation(PPTX_PATH)
    update_slide_24(prs)
    prs.save(PPTX_PATH)
    print("Presentation saved successfully.")

if __name__ == '__main__':
    main()
