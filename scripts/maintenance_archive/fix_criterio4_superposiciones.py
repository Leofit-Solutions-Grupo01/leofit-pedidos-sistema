import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import sys

sys.stdout.reconfigure(encoding='utf-8')

pptx_path = r"docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx"
prs = pptx.Presentation(pptx_path)

COLOR_NAVY = RGBColor(30, 58, 138)       # #1E3A8A - Tech Navy
COLOR_DARK_TEXT = RGBColor(15, 23, 42)   # #0F172A - Slate 900
COLOR_MUTED = RGBColor(71, 85, 105)      # #475569 - Slate 600

print("Fixing all superpositions in Criterio 4 (VALIDACIÓN Y VERIFICACIÓN EN LA PLATAFORMA CLOUD)...")

# =========================================================================
# 1. SLIDE 20: VALIDACIÓN Y VERIFICACIÓN EN LA PLATAFORMA CLOUD
# =========================================================================
s20 = prs.slides[19]

# Top main title banner
for shp in s20.shapes:
    if shp.name == 'TextBox 4':
        shp.top = Inches(0.80)
        shp.left = Inches(1.12)
        shp.width = Inches(16.78)
        shp.height = Inches(0.80)
        p = shp.text_frame.paragraphs[0]
        p.text = "VALIDACIÓN Y VERIFICACIÓN DEL SISTEMA EN LA PLATAFORMA CLOUD"
        p.font.name = 'Arial'
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(28)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY

    elif shp.name == 'TextBox 2':
        # Subtitle header on a single clean line
        shp.top = Inches(1.80)
        shp.left = Inches(1.12)
        shp.width = Inches(12.0)
        shp.height = Inches(0.40)
        p = shp.text_frame.paragraphs[0]
        p.text = "1) Verificación y Pruebas Operativas en Producción Cloud"
        p.font.name = 'Arial'
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(16)
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        print("Fixed Slide 20 TextBox 2 subtitle header!")

    elif shp.name == 'TextBox 3':
        # 4 verification items with 13.5 pt font, NO overlap!
        shp.top = Inches(2.35)
        shp.left = Inches(1.12)
        shp.width = Inches(11.80)
        shp.height = Inches(2.10)
        tf = shp.text_frame
        tf.clear()
        
        items_c4 = [
            ("• Autenticación en la Nube: ", "Inicio de sesión seguro con credenciales y emisión de JWT Bearer."),
            ("• Persistencia Transaccional: ", "Registro de pedidos con inserción atómica en clúster Neon PostgreSQL 16."),
            ("• Seguridad Perimetral: ", "Conexiones cifradas bajo protocolo HTTPS TLS 1.3 y autorización por roles RBAC."),
            ("• Cumplimiento de Rúbrica: ", "Validación precisa de funcionalidad y despliegue continuo en la nube.")
        ]
        
        for idx, (hdr, bdy) in enumerate(items_c4):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(4)
            r1 = p.add_run()
            r1.text = hdr
            r1.font.name = 'Arial'
            r1.font.size = Pt(13.5)
            r1.font.bold = True
            r1.font.color.rgb = COLOR_NAVY
            
            r2 = p.add_run()
            r2.text = bdy
            r2.font.name = 'Arial'
            r2.font.size = Pt(13.5)
            r2.font.bold = False
            r2.font.color.rgb = COLOR_DARK_TEXT
        print("Fixed Slide 20 TextBox 3 verification items (zero overlap)!")

    elif shp.name == 'TextBox 18':
        # BCNF Justification block below TextBox 3
        shp.top = Inches(4.75)
        shp.left = Inches(1.12)
        shp.width = Inches(12.0)
        shp.height = Inches(5.80)
        tf = shp.text_frame
        tf.clear()
        
        # Header
        p_hdr = tf.paragraphs[0]
        p_hdr.space_after = Pt(6)
        r_h = p_hdr.add_run()
        r_h.text = "2) Justificación de Arquitectura Relacional y Forma Normal Boyce-Codd (BCNF)"
        r_h.font.name = 'Arial'
        r_h.font.size = Pt(15.5)
        r_h.font.bold = True
        r_h.font.color.rgb = COLOR_NAVY
        
        bcnf_items = [
            ("• Principio BCNF: ", "En cada dependencia funcional X → Y, X es superclave estricta."),
            ("• Erradicación de Redundancias: ", "Segregación de prendas textiles de sus variantes por talla y color con stock independiente."),
            ("• Consistencia Histórica: ", "Cabecera orders desacoplada de order_items congelando precio unitario de venta."),
            ("• Auditoría Inmutable: ", "Tabla order_status_history registra transiciones con timestamp UTC y usuario auditor."),
            ("• Restricciones DDL: ", "ON DELETE RESTRICT en FKs para proteger órdenes; CHECK(total_amount >= 0) y CHECK(stock_current >= 0)."),
            ("• Índices B-Tree Optimizados: ", "idx_orders_client_id, idx_product_variants_sku, idx_orders_status para consultas < 5 ms.")
        ]
        
        for hdr, bdy in bcnf_items:
            p = tf.add_paragraph()
            p.space_after = Pt(4)
            r1 = p.add_run()
            r1.text = hdr
            r1.font.name = 'Arial'
            r1.font.size = Pt(12.5)
            r1.font.bold = True
            r1.font.color.rgb = COLOR_NAVY
            
            r2 = p.add_run()
            r2.text = bdy
            r2.font.name = 'Arial'
            r2.font.size = Pt(12.5)
            r2.font.bold = False
            r2.font.color.rgb = COLOR_DARK_TEXT
        print("Fixed Slide 20 TextBox 18 BCNF justification (clean layout, zero overlap)!")

# =========================================================================
# 2. SLIDE 24: MANUAL DE DESPLIEGUE (Expand OLE Table & format text)
# =========================================================================
s24 = prs.slides[23]

for shp in s24.shapes:
    if shp.name == 'TextBox 5':
        p = shp.text_frame.paragraphs[0]
        p.font.name = 'Arial'
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY

    elif shp.name == 'TextBox 6':
        # Format left architectural summary
        shp.top = Inches(1.85)
        shp.left = Inches(1.12)
        shp.width = Inches(8.0)
        shp.height = Inches(8.5)
        tf = shp.text_frame
        tf.clear()
        
        sections = [
            ("Arquitectura Multi-Cloud:", [
                "• PWA / Frontend: GitHub Pages Edge CDN (HTTPS TLS 1.3)",
                "• API / Backend: Render Cloud Platform (Node.js 20 LTS)",
                "• Base de Datos: Clúster Serverless PostgreSQL 16 en Neon"
            ]),
            ("Seguridad Defensiva:", [
                "• Protocolo HTTPS TLS 1.3 con HSTS y CSP estricto",
                "• Conexión a Base de Datos mediante canal SSL obligatorio",
                "• Autenticación JWT Stateless con algoritmo HS256",
                "• CORS restringido al dominio de producción del cliente"
            ]),
            ("Proceso de Despliegue y CI/CD:", [
                "• Pipeline automatizado en GitHub Actions (3 workflows)",
                "• Verificación de esquemas TypeScript y 194 pruebas previas"
            ]),
            ("Monitoreo en Producción:", [
                "• Telemetría activa en endpoint público /api/health (HTTP 200)"
            ])
        ]
        
        for s_idx, (sec_title, sec_bullets) in enumerate(sections):
            p_sec = tf.paragraphs[0] if s_idx == 0 else tf.add_paragraph()
            p_sec.space_after = Pt(3)
            r_s = p_sec.add_run()
            r_s.text = sec_title
            r_s.font.name = 'Arial'
            r_s.font.size = Pt(14)
            r_s.font.bold = True
            r_s.font.color.rgb = COLOR_NAVY
            
            for b in sec_bullets:
                p_b = tf.add_paragraph()
                p_b.space_after = Pt(2)
                r_b = p_b.add_run()
                r_b.text = b
                r_b.font.name = 'Arial'
                r_b.font.size = Pt(12)
                r_b.font.color.rgb = COLOR_DARK_TEXT
        print("Fixed Slide 24 TextBox 6 formatting!")

    elif shp.name == 'TextBox 8':
        shp.left = Inches(9.50)
        shp.top = Inches(2.20)
        p = shp.text_frame.paragraphs[0]
        p.text = "Variables de Entorno en Producción (Render Secrets):"
        p.font.name = 'Arial'
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = COLOR_NAVY

    elif shp.name == 'Object 7':
        # Expand width to prevent clipping
        shp.left = Inches(9.50)
        shp.top = Inches(2.80)
        shp.width = Inches(8.80)
        shp.height = Inches(4.50)
        print("Expanded Slide 24 Object 7 width to 8.80 inches (no clipping)!")

prs.save(pptx_path)
print("Saved all Criterio 4 visual fixes to PPTX successfully!")

