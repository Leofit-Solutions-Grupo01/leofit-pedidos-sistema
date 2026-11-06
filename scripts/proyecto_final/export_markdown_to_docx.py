# -*- coding: utf-8 -*-
"""
@file export_markdown_to_docx.py
@description Compilador Maestro de Alta Estética y Formalidad Ejecutiva (Nivel Consultoría Big 4 / Tesis de Grado):
             1. Pre-renderiza diagramas Mermaid a PNG en alta resolución (04_IMAGENES_DIAGRAMAS/).
             2. Procesa Markdown eliminando duplicados de encabezados y estructurando la jerarquía.
             3. Inserta Portada de Lujo Institucional UTP dedicada en Página 1.
             4. Inserta Ficha Técnica de Control Documental al inicio de la Página 2 (justo tras el salto de página).
             5. Promueve secciones a Heading 1 con barra azul vertical (#1E40AF) y fondo sutil (#F8FAFC).
             6. Aplica el Algoritmo de Ancho Proporcional Inteligente a todas las tablas (fijando w:tblGrid,
                w:tblLayout="fixed", padding generoso de 6pt/8pt y filas alternadas).
             7. Enmarca diagramas en tarjetas arquitectónicas ejecutivas con membrete y pie explicativo.
             8. Configura encabezados y pies dinámicos diferenciados (Página X de Y).
@project LeoFit Pedidos Sistema - Sustentación Proyecto Final (Semana 18)
@author Grupo 01 - UTP (Lead Architect: Lady Loayza)
"""

import os
import sys
import re
import math
import hashlib
import subprocess
import tempfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar en el entorno del equipo.")

ENTREGABLES_DIR = os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP")
HTML_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "00_HTML"))
DOCX_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "01_DOCX"))
DIAG_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "04_IMAGENES_DIAGRAMAS"))
CSS_FILE = os.path.join(HTML_DIR, "style.css")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(DOCX_DIR, exist_ok=True)
os.makedirs(DIAG_DIR, exist_ok=True)

# Leer estilos CSS maestros
CSS_CONTENT = ""
if os.path.exists(CSS_FILE):
    with open(CSS_FILE, "r", encoding="utf-8") as f:
        CSS_CONTENT = f.read()

DOCUMENTS = [
    {
        "id": "ENT-OFIC-001",
        "title": "HOJA OFICIAL DE ENTREGA ACADÉMICA Y ENLACES DEL PROYECTO FINAL",
        "subtitle": "Sustentación Oficial y Auditoría Técnica de Arquitectura (Semana 18)",
        "src": os.path.join(PROYECTO_FINAL_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md"),
        "html_dest": os.path.join(HTML_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.html"),
        "docx_dest": os.path.join(DOCX_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.docx"),
        "category": "ENTREGABLE OFICIAL DE SUSTENTACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Hoja de Entrega y Enlaces Oficiales"
    },
    {
        "id": "ADR-001",
        "title": "ADR-001: ELECCIÓN DE RENDER + NEON POSTGRESQL FRENTE A AWS",
        "subtitle": "Registro de Decisión Arquitectónica para Etapa de Validación MVP y Sustentación",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md"),
        "html_dest": os.path.join(HTML_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Architecture Decision Record (ADR)"
    },
    {
        "id": "ADR-002",
        "title": "ADR-002: ARQUITECTURA OBJETIVO NATIVA AWS Y COMPLEMENTOS EMPRESARIALES",
        "subtitle": "Diseño de Alta Disponibilidad, Escalabilidad Horizontal y Contingencia Operativa",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md"),
        "html_dest": os.path.join(HTML_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Architecture Decision Record (ADR)"
    },
    {
        "id": "DOC-SUNAT-001",
        "title": "ANEXO 03: CUMPLIMIENTO NORMATIVO SUNAT Y COMPROBANTES DE PAGO (CPE)",
        "subtitle": "Estándar UBL 2.1, Flujo de Facturación Electrónica, PSE/OSE y Contingencia Fiscal",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "03_CUMPLIMIENTO_SUNAT_CPE.md"),
        "html_dest": os.path.join(HTML_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.html"),
        "docx_dest": os.path.join(DOCX_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.docx"),
        "category": "CUMPLIMIENTO NORMATIVO Y TRIBUTARIO",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Especificación Técnica Normativa"
    },
    {
        "id": "DOC-PAY-001",
        "title": "ANEXO 04: INTEGRACIÓN DE PASARELA DE PAGOS Y CUMPLIMIENTO PCI-DSS",
        "subtitle": "Arquitectura de Tokenización Segura, Sandbox y Transición a Producción",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md"),
        "html_dest": os.path.join(HTML_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.html"),
        "docx_dest": os.path.join(DOCX_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.docx"),
        "category": "SEGURIDAD FINANCIERA Y PAGOS",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Especificación de Integración Financiera"
    },
    {
        "id": "DOC-ARCH-001",
        "title": "ANEXO 05: ARQUITECTURA DEL REPOSITORIO, PATRONES Y ESTÁNDARES DE CÓDIGO",
        "subtitle": "Estructura Modular Clean Architecture, Convenciones TypeScript y Flujo CI/CD",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md"),
        "html_dest": os.path.join(HTML_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.html"),
        "docx_dest": os.path.join(DOCX_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.docx"),
        "category": "ESTÁNDARES DE INGENIERÍA",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Guía Oficial de Arquitectura y Estándares"
    },
    {
        "id": "DOC-TRAC-001",
        "title": "ANEXO 06: MATRIZ DE TRAZABILIDAD ACADÉMICA Y RÚBRICA DE EVALUACIÓN",
        "subtitle": "Mapeo Integral de Criterios del Jurado contra Evidencias Reales de Código",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "06_MATRIZ_TRAZABILIDAD_JURADO.md"),
        "html_dest": os.path.join(HTML_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.docx"),
        "category": "TRAZABILIDAD Y EVALUACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Matriz de Trazabilidad Jurado UTP"
    },
    {
        "id": "DOC-COMP-001",
        "title": "COMPENDIO GENERAL DE ANEXOS TÉCNICOS Y ARQUITECTURA OFICIAL",
        "subtitle": "Índice Maestro de Especificaciones de Ingeniería - Proyecto LeoFit",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "README.md"),
        "html_dest": os.path.join(HTML_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.html"),
        "docx_dest": os.path.join(DOCX_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.docx"),
        "category": "COMPENDIO MAESTRO",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Compendio Ejecutivo de Ingeniería"
    },
    {
        "id": "AUD-REAL-001",
        "title": "INVENTARIO REAL DEL CÓDIGO FUENTE Y AUDITORÍA DE ARQUITECTURA",
        "subtitle": "Auditoría Forense de Archivos, Rutas y Métricas de Calidad ISO 25010",
        "src": os.path.join(PROYECTO_FINAL_DIR, "03_AUDITORIA_READONLY", "00_INVENTARIO_REAL.md"),
        "html_dest": os.path.join(HTML_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.docx"),
        "category": "AUDITORÍA FORENSE DE SOFTWARE",
        "version": "v2.4.0",
        "date": "Noviembre 2026",
        "doc_type": "Reporte de Auditoría Forense"
    }
]

def render_mermaid_diagram(code_text, doc_id, index):
    """
    Renderiza un bloque Mermaid a PNG en alta resolución (escala 2x, fondo blanco).
    """
    clean_code = code_text.strip()
    h = hashlib.md5(clean_code.encode("utf-8")).hexdigest()[:8]
    png_filename = f"{doc_id}_diag_{index+1}_{h}.png"
    png_path = os.path.join(DIAG_DIR, png_filename)

    if os.path.exists(png_path) and os.path.getsize(png_path) > 1000:
        return png_path

    temp_mmd = os.path.join(DIAG_DIR, f"temp_{doc_id}_{index}.mmd")
    with open(temp_mmd, "w", encoding="utf-8") as tf:
        tf.write(clean_code)

    cmd = ["mmdc.cmd", "-i", temp_mmd, "-o", png_path, "-b", "white", "-s", "2"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
        if res.returncode == 0 and os.path.exists(png_path):
            return png_path
    except Exception:
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
    return None

def clean_and_restructure_markdown(src_path, doc_info):
    """
    Preprocesa el Markdown fuente:
    1. Reemplaza bloques Mermaid por imágenes PNG vectorizadas con marco formal.
    2. Elimina el encabezado principal repetido (título `# ...` y metadatos sueltos iniciales)
       ya que estos vivirán en la Portada (Pág 1) y en la Ficha Técnica (Pág 2).
    3. Promueve los títulos de sección (`## 1. ...` -> `# 1. ...`) para que Pandoc
       los interprete como Heading 1 principales.
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    doc_id = doc_info["id"]

    # 1. Reemplazo de Mermaid por PNG con pie formal
    blocks = list(re.finditer(r"```mermaid(.*?)```", content, re.DOTALL))
    if blocks:
        new_content = ""
        last_end = 0
        for idx, match in enumerate(blocks):
            start, end = match.span()
            new_content += content[last_end:start]
            mermaid_code = match.group(1)
            png_path = render_mermaid_diagram(mermaid_code, doc_id, idx)

            if png_path and os.path.exists(png_path):
                norm_png = png_path.replace("\\", "/")
                card_markup = (
                    f"\n\n"
                    f"**DIAGRAMA ARQUITECTÓNICO OFICIAL | FIGURA {idx+1}**\n\n"
                    f"![Figura {idx+1}: Diagrama Arquitectónico Oficial]({norm_png})\n\n"
                    f"*Figura {idx+1}: Especificación visual y flujo de componentes técnicos del sistema LeoFit ({doc_id}).*\n\n"
                )
                new_content += card_markup
            else:
                new_content += f"\n\n```text\n[Diagrama Arquitectónico {doc_id} #{idx+1}]\n```\n\n"
            last_end = end
        new_content += content[last_end:]
        content = new_content

    # 2. Separar encabezado inicial repetido del cuerpo real
    lines = content.splitlines()
    body_lines = []
    found_first_section = False

    for line in lines:
        if not found_first_section:
            # Detectar el primer título numerado de sección (# 1., ## 1., ### 1.)
            if re.match(r"^#{1,3}\s+\d+\.", line):
                found_first_section = True
                body_lines.append(line)
            else:
                # Omitir metadatos sueltos, líneas divisoras o encabezados repetitivos
                continue
        else:
            body_lines.append(line)

    restructured_text = "\n".join(body_lines)

    # 3. Promover títulos de sección (## 1. -> # 1. y ### 1.1 -> ## 1.1)
    restructured_text = re.sub(r"^#{2,3}\s+(\d+\..*)$", r"# \1", restructured_text, flags=re.MULTILINE)
    restructured_text = re.sub(r"^#{3,4}\s+(\d+\.\d+\..*)$", r"## \1", restructured_text, flags=re.MULTILINE)

    return restructured_text

def generate_formal_html(doc_info, processed_md):
    """
    Compila el Markdown procesado a una versión HTML ejecutiva y visualmente elegante.
    """
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tf:
        tf.write(processed_md)
        temp_md = tf.name

    try:
        cmd = ["pandoc", temp_md, "--from=gfm", "--to=html5"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        body_html = res.stdout
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)

    html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_info['id']} - {doc_info['title']}</title>
  <style>
{CSS_CONTENT}
  </style>
</head>
<body>
  <div class="document-container">
    <div class="executive-cover">
      <div class="institutional-bar">
        <div class="institutional-title">Universidad Tecnológica del Perú &bull; Facultad de Ingeniería</div>
        <div class="institutional-meta">Curso Integrador II: Sistemas de Información &bull; Ciclo 2026-I</div>
      </div>
      <div class="doc-hero">
        <div class="doc-badge-pill">{doc_info['category']} &bull; {doc_info['id']}</div>
        <h1 class="doc-hero-title">{doc_info['title']}</h1>
        <div class="doc-hero-subtitle">{doc_info['subtitle']}</div>
      </div>
      <div class="metadata-grid">
        <div class="meta-card">
          <div class="meta-label">PROYECTO</div>
          <div class="meta-value">LeoFit - Gestión de Pedidos Multicanal</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">LÍDER DE ARQUITECTURA</div>
          <div class="meta-value">Lady Loayza (Lead Architect)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">EQUIPO DE INGENIERÍA</div>
          <div class="meta-value">Grupo 01 (Sistemas e Informática)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">DOCENTE EVALUADOR</div>
          <div class="meta-value">Ing. Enrique Lee Huamani Uriarte</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">VERSIÓN / FECHA</div>
          <div class="meta-value">{doc_info['version']} &bull; {doc_info['date']}</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">CLASIFICACIÓN</div>
          <div class="meta-value">Oficial (Confidencialidad Académica)</div>
        </div>
      </div>
    </div>
    <div class="document-body">
{body_html}
    </div>
  </div>
</body>
</html>
"""
    with open(doc_info["html_dest"], "w", encoding="utf-8") as f:
        f.write(html_template)

    return doc_info["html_dest"]

def convert_md_to_docx_via_pandoc(processed_md, dest_docx):
    """
    Compila el Markdown procesado a documento Word nativo.
    """
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False) as tf:
        tf.write(processed_md)
        temp_md = tf.name

    try:
        cmd = [
            "pandoc",
            temp_md,
            "-o", dest_docx,
            "--from=gfm",
            "--to=docx"
        ]
        subprocess.run(cmd, capture_output=True, text=True, check=True)
    finally:
        if os.path.exists(temp_md):
            os.remove(temp_md)

def apply_table_cell_margins(table, top_dxa=120, bottom_dxa=120, left_dxa=160, right_dxa=160):
    """Aplica márgenes celulares generosos (padding de 6pt arriba/abajo y 8pt a los lados)."""
    tblPr = table._tbl.tblPr
    tblCellMar = parse_xml(r'''
        <w:tblCellMar {} >
            <w:top w:w="{}" w:type="dxa"/>
            <w:bottom w:w="{}" w:type="dxa"/>
            <w:left w:w="{}" w:type="dxa"/>
            <w:right w:w="{}" w:type="dxa"/>
        </w:tblCellMar>
    '''.format(nsdecls('w'), top_dxa, bottom_dxa, left_dxa, right_dxa))
    tblPr.append(tblCellMar)

def insert_cover_and_brief_card(doc, doc_info):
    """
    Construye de forma estricta y ordenada:
    1. La Portada Institucional UTP de Lujo en la Página 1.
    2. El Salto de Página Formal de Portada.
    3. La Ficha Técnica Resumen (Card 2x4) en la cabecera de la Página 2.
    4. Deja la primera sección del cuerpo (# 1.) inmediatamente después de la Ficha Técnica.
    """
    if not doc.paragraphs:
        doc.add_paragraph()
    p_first = doc.paragraphs[0]

    # --- PÁGINA 1: PORTADA DE LUJO ---

    # 1. Membrete Institucional UTP
    p_inst1 = p_first.insert_paragraph_before("UNIVERSIDAD TECNOLÓGICA DEL PERÚ")
    p_inst1.paragraph_format.space_before = Pt(0)
    p_inst1.paragraph_format.space_after = Pt(2)
    r1 = p_inst1.runs[0]
    r1.font.name = "Calibri"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)

    p_inst2 = p_first.insert_paragraph_before("FACULTAD DE INGENIERÍA  |  CARRERA DE INGENIERÍA DE SISTEMAS E INFORMÁTICA")
    p_inst2.paragraph_format.space_before = Pt(0)
    p_inst2.paragraph_format.space_after = Pt(2)
    r2 = p_inst2.runs[0]
    r2.font.name = "Calibri"
    r2.font.size = Pt(9)
    r2.font.color.rgb = RGBColor(100, 116, 139)

    p_inst3 = p_first.insert_paragraph_before("CURSO INTEGRADOR II: SISTEMAS DE INFORMACIÓN (SEMANA 18 - CICLO 2026-I)")
    p_inst3.paragraph_format.space_before = Pt(0)
    p_inst3.paragraph_format.space_after = Pt(14)
    r3 = p_inst3.runs[0]
    r3.font.name = "Calibri"
    r3.font.size = Pt(9.5)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(30, 64, 175)

    # 2. Barra Bicolor Superior (Navy + Cobalt)
    bar_tbl = doc.add_table(rows=1, cols=2)
    bar_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_navy = bar_tbl.rows[0].cells[0]
    c_blue = bar_tbl.rows[0].cells[1]
    c_navy.width = Inches(5.2)
    c_blue.width = Inches(1.3)
    shd_navy = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
    shd_blue = parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w')))
    c_navy._tc.get_or_add_tcPr().append(shd_navy)
    c_blue._tc.get_or_add_tcPr().append(shd_blue)
    tr_pr = bar_tbl.rows[0]._tr.get_or_add_trPr()
    tr_pr.append(parse_xml(r'<w:trHeight {} w:val="60" w:hRule="exact"/>'.format(nsdecls('w'))))
    p_first._p.addprevious(bar_tbl._tbl)

    # 3. Espaciador
    p_sp1 = p_first.insert_paragraph_before("")
    p_sp1.paragraph_format.space_before = Pt(24)
    p_sp1.paragraph_format.space_after = Pt(0)

    # 4. Badge Pill de Identificación Documental
    badge_tbl = doc.add_table(rows=1, cols=1)
    badge_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    b_cell = badge_tbl.rows[0].cells[0]
    b_cell.width = Inches(5.2)
    b_shd = parse_xml(r'<w:shd {} w:fill="EEF2FF"/>'.format(nsdecls('w')))
    b_border = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="single" w:sz="6" w:space="0" w:color="C7D2FE"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="C7D2FE"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="C7D2FE"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="C7D2FE"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    b_cell._tc.get_or_add_tcPr().append(b_shd)
    b_cell._tc.get_or_add_tcPr().append(b_border)
    b_p = b_cell.paragraphs[0]
    b_p.paragraph_format.space_before = Pt(4)
    b_p.paragraph_format.space_after = Pt(4)
    b_run = b_p.add_run(f"[ DOCUMENTO TÉCNICO OFICIAL  |  {doc_info['id']}  |  SUSTENTACIÓN FINAL ]")
    b_run.font.name = "Calibri"
    b_run.font.size = Pt(8.5)
    b_run.font.bold = True
    b_run.font.color.rgb = RGBColor(30, 64, 175)
    p_first._p.addprevious(badge_tbl._tbl)

    # 5. Título Principal y Subtítulo
    p_title = p_first.insert_paragraph_before(doc_info["title"])
    p_title.paragraph_format.space_before = Pt(16)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.line_spacing = 1.15
    rt = p_title.runs[0]
    rt.font.name = "Calibri"
    rt.font.size = Pt(23)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = p_first.insert_paragraph_before(doc_info["subtitle"])
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(16)
    rsub = p_sub.runs[0]
    rsub.font.name = "Calibri"
    rsub.font.size = Pt(12)
    rsub.font.color.rgb = RGBColor(71, 85, 105)

    # 6. Regla Divisoria Cobalt
    rule_tbl = doc.add_table(rows=1, cols=1)
    rule_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rcell = rule_tbl.rows[0].cells[0]
    rcell.width = Inches(6.5)
    rshd = parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w')))
    rcell._tc.get_or_add_tcPr().append(rshd)
    r_tr = rule_tbl.rows[0]._tr.get_or_add_trPr()
    r_tr.append(parse_xml(r'<w:trHeight {} w:val="24" w:hRule="exact"/>'.format(nsdecls('w'))))
    p_first._p.addprevious(rule_tbl._tbl)

    # 7. Espaciador
    p_sp2 = p_first.insert_paragraph_before("")
    p_sp2.paragraph_format.space_before = Pt(16)
    p_sp2.paragraph_format.space_after = Pt(0)

    # 8. Matriz Institucional de Metadatos (Card 2x7)
    meta_tbl = doc.add_table(rows=7, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(meta_tbl, top_dxa=90, bottom_dxa=90, left_dxa=160, right_dxa=160)

    metadata_rows = [
        ("PROYECTO:", "Sistema de Gestión de Pedidos y Despacho Multicanal (LeoFit Solutions)"),
        ("DOCUMENTO TÉCNICO:", f"{doc_info['id']} — {doc_info['doc_type']}"),
        ("LÍDER DE ARQUITECTURA:", "Lady Luz Loayza Rodríguez (Scrum Master / DevSecOps Lead)"),
        ("EQUIPO DE INGENIERÍA:", "Grupo 01 (Loayza, Cárdenas, Roman, Dávila, Rojas)"),
        ("DOCENTE EVALUADOR:", "Ing. Enrique Lee Huamani Uriarte (Docente Asesor Evaluador)"),
        ("FECHA DE EMISIÓN / VERSIÓN:", f"{doc_info['date']}  |  Versión Oficial {doc_info['version']}"),
        ("CLASIFICACIÓN ACADÉMICA:", "OFICIAL — Sustentación de Proyecto Final (Confidencialidad Académica)")
    ]

    for idx, (label, val) in enumerate(metadata_rows):
        row = meta_tbl.rows[idx]
        row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
        c1, c2 = row.cells[0], row.cells[1]
        c1.width = Inches(2.2)
        c2.width = Inches(4.3)

        shd1 = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
        shd2 = parse_xml(r'<w:shd {} w:fill="FFFFFF"/>'.format(nsdecls('w')))
        c1._tc.get_or_add_tcPr().append(shd1)
        c2._tc.get_or_add_tcPr().append(shd2)

        bdr1 = parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        '''.format(nsdecls('w')))
        bdr2 = parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        '''.format(nsdecls('w')))
        c1._tc.get_or_add_tcPr().append(bdr1)
        c2._tc.get_or_add_tcPr().append(bdr2)

        p_c1 = c1.paragraphs[0]
        p_c1.paragraph_format.space_before = Pt(2)
        p_c1.paragraph_format.space_after = Pt(2)
        r_c1 = p_c1.add_run(label)
        r_c1.font.name = "Calibri"
        r_c1.font.size = Pt(8.5)
        r_c1.font.bold = True
        r_c1.font.color.rgb = RGBColor(51, 65, 85)

        p_c2 = c2.paragraphs[0]
        p_c2.paragraph_format.space_before = Pt(2)
        p_c2.paragraph_format.space_after = Pt(2)
        r_c2 = p_c2.add_run(val)
        r_c2.font.name = "Calibri"
        r_c2.font.size = Pt(8.5)
        r_c2.font.color.rgb = RGBColor(15, 23, 42)

    p_first._p.addprevious(meta_tbl._tbl)

    # 9. Pie Institucional de Portada
    p_foot = p_first.insert_paragraph_before("Lima, Perú  —  Ciclo Académico 2026-I  —  Sustentación de Proyecto Final")
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(24)
    p_foot.paragraph_format.space_after = Pt(0)
    rf = p_foot.runs[0]
    rf.font.name = "Calibri"
    rf.font.size = Pt(8.5)
    rf.font.color.rgb = RGBColor(148, 163, 184)

    # 10. Salto de Página Formal (Termina Página 1)
    p_break = p_first.insert_paragraph_before()
    p_break.paragraph_format.space_before = Pt(0)
    p_break.paragraph_format.space_after = Pt(0)
    p_break.add_run().add_break(WD_BREAK.PAGE)

    # --- PÁGINA 2: FICHA TÉCNICA RESUMEN AL INICIO ---
    f_tbl = doc.add_table(rows=2, cols=4)
    f_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(f_tbl, top_dxa=70, bottom_dxa=70, left_dxa=100, right_dxa=100)

    tblPr = f_tbl._tbl.tblPr
    tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))

    col_widths = [Inches(1.625), Inches(1.625), Inches(1.625), Inches(1.625)]
    grid_cols = ''.join([r'<w:gridCol {} w:w="2340"/>'.format(nsdecls('w')) for _ in range(4)])
    f_tbl._tbl.append(parse_xml(r'<w:tblGrid {}>{}</w:tblGrid>'.format(nsdecls('w'), grid_cols)))

    headers = ["CÓDIGO OFICIAL", "ESTADO TÉCNICO", "VERSIÓN EVALUADA", "CLASIFICACIÓN"]
    values = [doc_info["id"], "APROBADO", doc_info["version"], "OFICIAL UTP"]

    row_hdr = f_tbl.rows[0]
    row_hdr._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    for idx, cell in enumerate(row_hdr.cells):
        cell.width = col_widths[idx]
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="2340" w:type="dxa"/>'.format(nsdecls('w'))))
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w'))))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(headers[idx])
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    row_val = f_tbl.rows[1]
    row_val._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
    for idx, cell in enumerate(row_val.cells):
        cell.width = col_widths[idx]
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="2340" w:type="dxa"/>'.format(nsdecls('w'))))
        cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w'))))
        cell._tc.get_or_add_tcPr().append(parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            </w:tcBorders>
        '''.format(nsdecls('w'))))
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(values[idx])
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(30, 64, 175)

    p_first._p.addprevious(f_tbl._tbl)

    # Espaciador antes de la Sección 1
    p_sp3 = p_first.insert_paragraph_before("")
    p_sp3.paragraph_format.space_before = Pt(14)
    p_sp3.paragraph_format.space_after = Pt(0)

    # Si p_first quedó vacío como separador previo, limpiarlo
    if not p_first.text.strip():
        p_first._p.getparent().remove(p_first._p)

def setup_headers_and_footers(section, doc_info):
    """
    Configura encabezados y pies dinámicos diferenciados (Página 1 sin numeración).
    """
    section.different_first_page_header_footer = True

    # 1. ENCABEZADO PÁGINAS 2+
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""

    tbl_h = header.add_table(rows=1, cols=2, width=Inches(6.5))
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_hl, c_hr = tbl_h.rows[0].cells[0], tbl_h.rows[0].cells[1]
    c_hl.width = Inches(4.5)
    c_hr.width = Inches(2.0)

    bdr_h = parse_xml(r'''
        <w:tcBorders {} >
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    c_hl._tc.get_or_add_tcPr().append(bdr_h)
    c_hr._tc.get_or_add_tcPr().append(parse_xml(r'''
        <w:tcBorders {} >
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w'))))

    p_hl = c_hl.paragraphs[0]
    p_hl.paragraph_format.space_before = Pt(0)
    p_hl.paragraph_format.space_after = Pt(4)
    r_hl = p_hl.add_run(f"LEOFIT SOLUTIONS  |  {doc_info['id']}")
    r_hl.font.name = "Calibri"
    r_hl.font.size = Pt(8)
    r_hl.font.bold = True
    r_hl.font.color.rgb = RGBColor(100, 116, 139)

    p_hr = c_hr.paragraphs[0]
    p_hr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_hr.paragraph_format.space_before = Pt(0)
    p_hr.paragraph_format.space_after = Pt(4)
    r_hr = p_hr.add_run("SEMANA 18 — PROYECTO FINAL")
    r_hr.font.name = "Calibri"
    r_hr.font.size = Pt(8)
    r_hr.font.color.rgb = RGBColor(100, 116, 139)

    # 2. PIE DE PÁGINA PÁGINAS 2+
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""

    tbl_f = footer.add_table(rows=1, cols=2, width=Inches(6.5))
    tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_fl, c_fr = tbl_f.rows[0].cells[0], tbl_f.rows[0].cells[1]
    c_fl.width = Inches(4.5)
    c_fr.width = Inches(2.0)

    bdr_f = parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w')))
    c_fl._tc.get_or_add_tcPr().append(bdr_f)
    c_fr._tc.get_or_add_tcPr().append(parse_xml(r'''
        <w:tcBorders {} >
            <w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>
    '''.format(nsdecls('w'))))

    p_fl = c_fl.paragraphs[0]
    p_fl.paragraph_format.space_before = Pt(4)
    p_fl.paragraph_format.space_after = Pt(0)
    r_fl = p_fl.add_run("Confidencial — Material Oficial de Sustentación Académica UTP")
    r_fl.font.name = "Calibri"
    r_fl.font.size = Pt(8)
    r_fl.font.color.rgb = RGBColor(148, 163, 184)

    p_fr = c_fr.paragraphs[0]
    p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_fr.paragraph_format.space_before = Pt(4)
    p_fr.paragraph_format.space_after = Pt(0)
    r_fr_pre = p_fr.add_run("Página ")
    r_fr_pre.font.name = "Calibri"
    r_fr_pre.font.size = Pt(8)
    r_fr_pre.font.color.rgb = RGBColor(100, 116, 139)

    fld1 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instr1 = parse_xml(r'<w:instrText {} xml:space="preserve"> PAGE </w:instrText>'.format(nsdecls('w')))
    fld2 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fld3 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    p_fr._p.append(fld1)
    p_fr._p.append(instr1)
    p_fr._p.append(fld2)
    p_fr._p.append(fld3)

    r_fr_mid = p_fr.add_run(" de ")
    r_fr_mid.font.name = "Calibri"
    r_fr_mid.font.size = Pt(8)
    r_fr_mid.font.color.rgb = RGBColor(100, 116, 139)

    fld4 = parse_xml(r'<w:fldChar {} w:fldCharType="begin"/>'.format(nsdecls('w')))
    instr2 = parse_xml(r'<w:instrText {} xml:space="preserve"> NUMPAGES </w:instrText>'.format(nsdecls('w')))
    fld5 = parse_xml(r'<w:fldChar {} w:fldCharType="separate"/>'.format(nsdecls('w')))
    fld6 = parse_xml(r'<w:fldChar {} w:fldCharType="end"/>'.format(nsdecls('w')))
    p_fr._p.append(fld4)
    p_fr._p.append(instr2)
    p_fr._p.append(fld5)
    p_fr._p.append(fld6)

def format_all_tables_with_intelligent_widths(doc):
    """
    Aplica el Algoritmo de Ancho Proporcional Inteligente a todas las tablas del cuerpo,
    fijando el layout, configurando márgenes celulares generosos y eliminando texto apretado.
    """
    total_table_inches = 6.5

    for table in doc.tables:
        row_count = len(table.rows)
        if row_count == 0:
            continue

        first_cell_text = table.rows[0].cells[0].text.strip()
        # Omitir tablas que forman parte de la portada o ficha técnica
        if first_cell_text in ["UNIVERSIDAD TECNOLÓGICA DEL PERÚ", "PROYECTO:", "CÓDIGO OFICIAL", "LEOFIT SOLUTIONS"]:
            continue
        if "DOCUMENTO TÉCNICO OFICIAL" in first_cell_text:
            continue

        col_count = len(table.columns)
        if col_count == 0:
            continue

        # 1. Analizar longitud de caracteres por columna
        cols_lengths = [[] for _ in range(col_count)]
        for row in table.rows:
            for c_idx, cell in enumerate(row.cells):
                if c_idx < col_count:
                    cols_lengths[c_idx].append(len(cell.text.strip()))

        weights = []
        for c_idx in range(col_count):
            lens = cols_lengths[c_idx]
            if lens:
                avg_len = sum(lens) / len(lens)
                max_len = max(lens)
                # Fórmula de ponderación: raíz cuadrada de max_len + longitud promedio suavizada
                w = math.sqrt(max(1, max_len)) + (avg_len ** 0.55)
            else:
                w = 1.0
            weights.append(max(1.0, w))

        sum_w = sum(weights)
        col_widths_in = [round((w / sum_w) * total_table_inches, 2) for w in weights]
        diff = total_table_inches - sum(col_widths_in)
        col_widths_in[-1] += round(diff, 2)

        col_widths_dxa = [int(w * 1440) for w in col_widths_in]

        # 2. Configurar layout de tabla fijo
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        apply_table_cell_margins(table, top_dxa=110, bottom_dxa=110, left_dxa=150, right_dxa=150)

        tblPr = table._tbl.tblPr
        tblPr.append(parse_xml(r'<w:tblLayout {} w:type="fixed"/>'.format(nsdecls('w'))))

        grid_cols_xml = ''.join([r'<w:gridCol {} w:w="{}"/>'.format(nsdecls('w'), w) for w in col_widths_dxa])
        table._tbl.append(parse_xml(r'<w:tblGrid {}>{}</w:tblGrid>'.format(nsdecls('w'), grid_cols_xml)))

        # 3. Fila 0: Cabecera Ejecutiva Navy (#0F172A)
        hdr_row = table.rows[0]
        hdr_row._tr.get_or_add_trPr().append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))
        hdr_row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))

        for c_idx, cell in enumerate(hdr_row.cells):
            cell.width = Inches(col_widths_in[c_idx])
            cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="{}" w:type="dxa"/>'.format(nsdecls('w'), col_widths_dxa[c_idx])))
            cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w'))))
            bdr = parse_xml(r'''
                <w:tcBorders {} >
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="1E293B"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                </w:tcBorders>
            '''.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(bdr)

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(3)
                p.paragraph_format.space_after = Pt(3)
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)

        # 4. Filas de Datos (Cebra y Bordes Sutiles)
        for r_idx in range(1, row_count):
            row = table.rows[r_idx]
            row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
            is_even = (r_idx % 2 == 0)
            fill_color = "F8FAFC" if is_even else "FFFFFF"

            for c_idx, cell in enumerate(row.cells):
                cell.width = Inches(col_widths_in[c_idx])
                cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:tcW {} w:w="{}" w:type="dxa"/>'.format(nsdecls('w'), col_widths_dxa[c_idx])))
                cell._tc.get_or_add_tcPr().append(parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_color)))
                bdr = parse_xml(r'''
                    <w:tcBorders {} >
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    </w:tcBorders>
                '''.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(bdr)

                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    for r in p.runs:
                        r.font.name = "Calibri"
                        r.font.size = Pt(9)
                        r.font.color.rgb = RGBColor(30, 41, 59)

def polish_document_elements(doc, doc_info):
    """
    Aplica jerarquía de títulos de alta presencia (H1 con barra azul lateral y fondo tenue),
    párrafos justificados con interlineado 1.15 y cajas de figuras centradas.
    """
    for p in doc.paragraphs:
        txt = p.text.strip()
        style_name = p.style.name if p.style else ""

        # Heading 1 (Secciones Principales: 1. Contexto, 2. Decisión...)
        if style_name.startswith("Heading 1"):
            p.paragraph_format.space_before = Pt(20)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            
            pPr = p._p.get_or_add_pPr()
            # Barra lateral azul Cobalt #1E40AF sólida de 3.5pt con 8pt de padding
            pBdr = parse_xml(r'''
                <w:pBdr {} >
                    <w:left w:val="single" w:sz="28" w:space="8" w:color="1E40AF"/>
                </w:pBdr>
            '''.format(nsdecls('w')))
            pPr.append(pBdr)
            shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
            pPr.append(shd)

            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(14)
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)

        # Heading 2 (Subsecciones: 6.1, 6.2...)
        elif style_name.startswith("Heading 2"):
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(12)
                r.font.bold = True
                r.font.color.rgb = RGBColor(30, 64, 175)

        # Heading 3
        elif style_name.startswith("Heading 3"):
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(10.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(51, 65, 85)

        # Encabezado de diagramas
        elif "DIAGRAMA ARQUITECTÓNICO OFICIAL" in txt:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            pPr = p._p.get_or_add_pPr()
            shd = parse_xml(r'<w:shd {} w:fill="EEF2FF"/>'.format(nsdecls('w')))
            pPr.append(shd)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(30, 64, 175)

        # Leyendas de figuras
        elif txt.startswith("Figura ") or txt.startswith("*Figura "):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(16)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.italic = True
                r.font.color.rgb = RGBColor(100, 116, 139)

        # Citas / Callouts
        elif style_name in ["Quote", "Block Text"]:
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(r'''
                <w:pBdr {} >
                    <w:left w:val="single" w:sz="24" w:space="8" w:color="2563EB"/>
                </w:pBdr>
            '''.format(nsdecls('w')))
            pPr.append(pBdr)
            shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
            pPr.append(shd)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)

        # Párrafos regulares
        else:
            if "drawing" in p._p.xml:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(8)
                p.paragraph_format.space_after = Pt(4)
            else:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(5)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(10)
                    r.font.color.rgb = RGBColor(30, 41, 59)

def main():
    print("======================================================================")
    print("COMPILADOR EJECUTIVO DE ENTREGABLES OFICIALES (CALIDAD BIG 4 / UTP)")
    print("======================================================================")
    print(f"Directorio HTML: {HTML_DIR}")
    print(f"Directorio DOCX: {DOCX_DIR}")
    print(f"Directorio Diagramas: {DIAG_DIR}")
    print("")

    success_count = 0
    total = len(DOCUMENTS)

    for doc_info in DOCUMENTS:
        doc_id = doc_info["id"]
        doc_name = os.path.basename(doc_info["docx_dest"])
        html_name = os.path.basename(doc_info["html_dest"])
        print(f"Procesando [{doc_id}]: {os.path.basename(doc_info['src'])}")

        try:
            # 1. Limpieza de duplicados y reestructuración de jerarquías Markdown
            processed_md = clean_and_restructure_markdown(doc_info["src"], doc_info)

            # 2. Generación de versión HTML corporativa
            html_path = generate_formal_html(doc_info, processed_md)
            html_size_kb = os.path.getsize(html_path) / 1024.0
            print(f"  [OK] HTML formal generado: {html_name} ({html_size_kb:.1f} KB)")

            # 3. Compilación a DOCX base mediante Pandoc
            docx_path = doc_info["docx_dest"]
            convert_md_to_docx_via_pandoc(processed_md, docx_path)

            # 4. Enriquecimiento tipográfico y estructural de lujo en python-docx
            doc = docx.Document(docx_path)
            sec = doc.sections[0]
            sec.top_margin = Inches(1.0)
            sec.bottom_margin = Inches(1.0)
            sec.left_margin = Inches(1.0)
            sec.right_margin = Inches(1.0)

            # Configurar encabezados/pies dinámicos diferenciados
            setup_headers_and_footers(sec, doc_info)

            # Insertar Portada de Lujo (Pág 1) y Ficha Técnica (Pág 2) en orden estricto
            insert_cover_and_brief_card(doc, doc_info)

            # Aplicar formato de alta presencia a títulos y párrafos
            polish_document_elements(doc, doc_info)

            # Aplicar Algoritmo de Ancho Proporcional Inteligente a todas las tablas
            format_all_tables_with_intelligent_widths(doc)

            # Guardar documento final
            doc.save(docx_path)
            docx_size_kb = os.path.getsize(docx_path) / 1024.0
            print(f"  [OK] Word (.docx) ejecutiva finalizada: {doc_name} ({docx_size_kb:.1f} KB)")

            # Validación de integridad de apertura
            v = docx.Document(docx_path)
            print(f"  [OK] Integridad verificada: {len(v.paragraphs)} párrafos, {len(v.tables)} tablas.\n")
            success_count += 1

        except Exception as e:
            print(f"  [ERROR] Falló procesamiento de {doc_name}: {e}\n")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    print("======================================================================")
    print(f"EXPORTACION COMPLETADA EXITOSAMENTE: {success_count}/{total} DOCUMENTOS")
    print("Versiones HTML visuales y Word ejecutivas listas en _PROYECTO_FINAL_LOCAL.")
    print("======================================================================")

if __name__ == "__main__":
    main()
