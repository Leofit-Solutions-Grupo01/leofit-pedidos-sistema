# -*- coding: utf-8 -*-
"""
@file export_markdown_to_docx.py
@description Compilador Maestro de Alta Estética y Formalidad Ejecutiva:
             1. Renderiza diagramas Mermaid a PNG en alta resolución (04_IMAGENES_DIAGRAMAS/).
             2. Compila Markdown a HTML corporativo con portada institucional UTP y diseño de revista técnica (00_HTML/).
             3. Genera documentos Microsoft Word (.docx) 100% editables con portada ejecutiva dedicada,
                encabezados y pies dinámicos (Página X de Y), barra vertical azul en títulos H1,
                tablas tipo consultoría Big 4 (Navy #0F172A, filas alternadas #F8FAFC, padding cómodo,
                anchos proporcionales) y figuras centradas con pie explicativo (01_DOCX/).
@project LeoFit Pedidos Sistema - Sustentación Proyecto Final (Semana 18)
@author Grupo 01 - UTP (Lead Architect: Lady Loayza)
"""

import os
import sys
import re
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
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar en el entorno de desarrollo del equipo.")

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
        "subtitle": "Sustentación y Auditoría Técnica de Arquitectura (Semana 18)",
        "src": os.path.join(PROYECTO_FINAL_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.md"),
        "html_dest": os.path.join(HTML_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.html"),
        "docx_dest": os.path.join(DOCX_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.docx"),
        "category": "ENTREGABLE OFICIAL DE SUSTENTACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
    },
    {
        "id": "ADR-001",
        "title": "ADR-001: ELECCIÓN DE RENDER + NEON POSTGRESQL FRENTE A AWS",
        "subtitle": "Registro de Decisión Arquitectónica para Etapa de Validación MVP",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md"),
        "html_dest": os.path.join(HTML_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
    },
    {
        "id": "ADR-002",
        "title": "ADR-002: ARQUITECTURA OBJETIVO NATIVA AWS Y COMPLEMENTOS EMPRESARIALES",
        "subtitle": "Diseño de Alta Disponibilidad, Escalabilidad y Contingencia Operativa",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md"),
        "html_dest": os.path.join(HTML_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.docx"),
        "category": "ARQUITECTURA DE SOFTWARE (ADR)",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
    },
    {
        "id": "DOC-SUNAT-001",
        "title": "ANEXO 03: CUMPLIMIENTO NORMATIVO SUNAT Y COMPROBANTES DE PAGO (CPE)",
        "subtitle": "Estándar UBL 2.1, Flujo de Facturación Electrónica y Contingencia Fiscal",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "03_CUMPLIMIENTO_SUNAT_CPE.md"),
        "html_dest": os.path.join(HTML_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.html"),
        "docx_dest": os.path.join(DOCX_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.docx"),
        "category": "CUMPLIMIENTO NORMATIVO Y TRIBUTARIO",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
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
        "date": "Noviembre 2026"
    },
    {
        "id": "DOC-ARCH-001",
        "title": "ANEXO 05: ARQUITECTURA DEL REPOSITORIO, PATRONES Y ESTÁNDARES DE CÓDIGO",
        "subtitle": "Estructura Modular Clean Architecture, Convenciones y Flujo CI/CD",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md"),
        "html_dest": os.path.join(HTML_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.html"),
        "docx_dest": os.path.join(DOCX_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.docx"),
        "category": "ESTÁNDARES DE INGENIERÍA",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
    },
    {
        "id": "DOC-TRAC-001",
        "title": "ANEXO 06: MATRIZ DE TRAZABILIDAD ACADÉMICA Y RÚBRICA DE EVALUACIÓN",
        "subtitle": "Mapeo Integral de Criterios del Jurado contra Evidencias de Código",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "06_MATRIZ_TRAZABILIDAD_JURADO.md"),
        "html_dest": os.path.join(HTML_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.docx"),
        "category": "TRAZABILIDAD Y EVALUACIÓN",
        "version": "v2.4.0",
        "date": "Noviembre 2026"
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
        "date": "Noviembre 2026"
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
        "date": "Noviembre 2026"
    }
]

def render_mermaid_diagram(code_text, doc_id, index):
    """
    Renderiza un bloque Mermaid a PNG en 04_IMAGENES_DIAGRAMAS/ mediante mmdc.
    Utiliza hash determinístico para cachear y evitar re-renderizados innecesarios.
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
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
        if res.returncode == 0 and os.path.exists(png_path):
            return png_path
    except Exception as e:
        if os.path.exists(temp_mmd):
            os.remove(temp_mmd)
    return None

def preprocess_markdown(src_path, doc_id):
    """
    Lee el archivo Markdown y sustituye los bloques ```mermaid por imágenes PNG pre-renderizadas.
    """
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = list(re.finditer(r"```mermaid(.*?)```", content, re.DOTALL))
    if not blocks:
        return content

    new_content = ""
    last_end = 0

    for idx, match in enumerate(blocks):
        start, end = match.span()
        new_content += content[last_end:start]
        mermaid_code = match.group(1)
        png_path = render_mermaid_diagram(mermaid_code, doc_id, idx)

        if png_path and os.path.exists(png_path):
            norm_png = png_path.replace("\\", "/")
            replacement = (
                f"\n\n![Diagrama Arquitectónico Oficial]({norm_png})\n\n"
                f"*Figura {idx+1}: Diagrama Arquitectónico Oficial del Sistema LeoFit - {doc_id}*\n\n"
            )
            new_content += replacement
        else:
            new_content += f"\n\n```text\n[Diagrama Arquitectónico {doc_id} #{idx+1}]\n```\n\n"

        last_end = end

    new_content += content[last_end:]
    return new_content

def generate_formal_html(doc_info, processed_md):
    """
    Compila el Markdown procesado a un documento HTML formal y de alto impacto visual.
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
          <div class="meta-value">Lady Loayza</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">EQUIPO TÉCNICO</div>
          <div class="meta-value">Grupo 01 (Sistemas e Informática)</div>
        </div>
        <div class="meta-card">
          <div class="meta-label">EVALUADOR ACADÉMICO</div>
          <div class="meta-value">Docente Jurado Calificador UTP</div>
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
    Ejecuta Pandoc sobre el Markdown pre-procesado con imágenes vectorizadas.
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

def apply_table_cell_margins(table, top_dxa=100, bottom_dxa=100, left_dxa=140, right_dxa=140):
    """Configura márgenes internos (padding) en una tabla Word OXML."""
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

def add_executive_cover_page(doc, doc_info):
    """
    Construye e inserta una portada ejecutiva institucional UTP dedicada en la Página 1,
    seguida de un salto de página formal para que el contenido inicie limpiamente en la Página 2.
    """
    if not doc.paragraphs:
        doc.add_paragraph()
    p0 = doc.paragraphs[0]

    # 1. Encabezado Institucional UTP
    p_inst1 = p0.insert_paragraph_before("UNIVERSIDAD TECNOLÓGICA DEL PERÚ")
    p_inst1.paragraph_format.space_before = Pt(0)
    p_inst1.paragraph_format.space_after = Pt(2)
    r1 = p_inst1.runs[0]
    r1.font.name = "Calibri"
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(15, 23, 42)

    p_inst2 = p0.insert_paragraph_before("FACULTAD DE INGENIERÍA | INGENIERÍA DE SISTEMAS E INFORMÁTICA")
    p_inst2.paragraph_format.space_before = Pt(0)
    p_inst2.paragraph_format.space_after = Pt(2)
    r2 = p_inst2.runs[0]
    r2.font.name = "Calibri"
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = RGBColor(100, 116, 139)

    p_inst3 = p0.insert_paragraph_before("CURSO INTEGRADOR II: SISTEMAS DE INFORMACIÓN (SEMANA 18 - CICLO 2026-I)")
    p_inst3.paragraph_format.space_before = Pt(0)
    p_inst3.paragraph_format.space_after = Pt(14)
    r3 = p_inst3.runs[0]
    r3.font.name = "Calibri"
    r3.font.size = Pt(9)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(30, 64, 175)

    # 2. Barra de Acento Decorativa (Navy + Cobalt)
    bar_tbl = doc.add_table(rows=1, cols=2)
    bar_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_navy = bar_tbl.rows[0].cells[0]
    cell_blue = bar_tbl.rows[0].cells[1]
    cell_navy.width = Inches(5.2)
    cell_blue.width = Inches(1.3)
    shd_navy = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
    shd_blue = parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w')))
    cell_navy._tc.get_or_add_tcPr().append(shd_navy)
    cell_blue._tc.get_or_add_tcPr().append(shd_blue)
    tr_pr = bar_tbl.rows[0]._tr.get_or_add_trPr()
    tr_pr.append(parse_xml(r'<w:trHeight {} w:val="60" w:hRule="exact"/>'.format(nsdecls('w'))))
    p0._p.addprevious(bar_tbl._tbl)

    # 3. Espaciador
    p_sp1 = p0.insert_paragraph_before("")
    p_sp1.paragraph_format.space_before = Pt(20)
    p_sp1.paragraph_format.space_after = Pt(0)

    # 4. Badge Pill de Identificación Documental
    badge_tbl = doc.add_table(rows=1, cols=1)
    badge_tbl.alignment = WD_TABLE_ALIGNMENT.LEFT
    b_cell = badge_tbl.rows[0].cells[0]
    b_cell.width = Inches(5.0)
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
    b_p.paragraph_format.space_before = Pt(3)
    b_p.paragraph_format.space_after = Pt(3)
    b_run = b_p.add_run(f"[ DOCUMENTO TÉCNICO OFICIAL | {doc_info['id']} | SUSTENTACIÓN FINAL ]")
    b_run.font.name = "Calibri"
    b_run.font.size = Pt(8.5)
    b_run.font.bold = True
    b_run.font.color.rgb = RGBColor(30, 64, 175)
    p0._p.addprevious(badge_tbl._tbl)

    # 5. Título Principal y Subtítulo
    p_title = p0.insert_paragraph_before(doc_info["title"])
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.line_spacing = 1.15
    rt = p_title.runs[0]
    rt.font.name = "Calibri"
    rt.font.size = Pt(22)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(15, 23, 42)

    p_sub = p0.insert_paragraph_before(doc_info["subtitle"])
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    rsub = p_sub.runs[0]
    rsub.font.name = "Calibri"
    rsub.font.size = Pt(12)
    rsub.font.color.rgb = RGBColor(71, 85, 105)

    # 6. Regla de Separación Cobalt Blue
    rule_tbl = doc.add_table(rows=1, cols=1)
    rule_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rcell = rule_tbl.rows[0].cells[0]
    rcell.width = Inches(6.5)
    rshd = parse_xml(r'<w:shd {} w:fill="2563EB"/>'.format(nsdecls('w')))
    rcell._tc.get_or_add_tcPr().append(rshd)
    r_tr = rule_tbl.rows[0]._tr.get_or_add_trPr()
    r_tr.append(parse_xml(r'<w:trHeight {} w:val="24" w:hRule="exact"/>'.format(nsdecls('w'))))
    p0._p.addprevious(rule_tbl._tbl)

    # 7. Espaciador
    p_sp2 = p0.insert_paragraph_before("")
    p_sp2.paragraph_format.space_before = Pt(14)
    p_sp2.paragraph_format.space_after = Pt(0)

    # 8. Matriz de Metadatos Institucionales (Card Ejecutiva 2 x 7)
    meta_tbl = doc.add_table(rows=7, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_table_cell_margins(meta_tbl, top_dxa=80, bottom_dxa=80, left_dxa=140, right_dxa=140)

    metadata_rows = [
        ("PROYECTO:", "Sistema de Gestión de Pedidos y Despacho Multicanal (LeoFit Solutions)"),
        ("DOCUMENTO TÉCNICO:", f"{doc_info['id']} - {doc_info['title']}"),
        ("LÍDER DE ARQUITECTURA:", "Lady Loayza (Lead Software Architect)"),
        ("EQUIPO DE INGENIERÍA:", "Grupo 01 (Carrera de Ingeniería de Sistemas e Informática)"),
        ("DOCENTE EVALUADOR:", "Mg. Jurado Calificador de Sustentación UTP"),
        ("FECHA DE EMISIÓN / VERSIÓN:", f"{doc_info['date']} | Versión Oficial {doc_info['version']}"),
        ("CLASIFICACIÓN ACADÉMICA:", "OFICIAL - Sustentación Académica de Proyecto Final (Confidencial)")
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

        bdr = parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            </w:tcBorders>
        '''.format(nsdecls('w')))
        c1._tc.get_or_add_tcPr().append(bdr)
        c2._tc.get_or_add_tcPr().append(parse_xml(r'''
            <w:tcBorders {} >
                <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            </w:tcBorders>
        '''.format(nsdecls('w'))))

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

    p0._p.addprevious(meta_tbl._tbl)

    # 9. Salto de Página Formal de Portada
    p_break = p0.insert_paragraph_before()
    p_break.paragraph_format.space_before = Pt(0)
    p_break.paragraph_format.space_after = Pt(0)
    p_break.add_run().add_break(WD_BREAK.PAGE)

def setup_headers_and_footers(section, doc_info):
    """
    Configura encabezados y pies de página ejecutivos diferenciados para que la portada (Página 1)
    no contenga numeración ni membretes, y las páginas 2+ incluyan la paginación dinámica 'Página X de Y'.
    """
    section.different_first_page_header_footer = True

    # 1. ENCABEZADO DE PÁGINAS 2+
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(0)

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
    r_hr = p_hr.add_run("PROYECTO FINAL (SEMANA 18)")
    r_hr.font.name = "Calibri"
    r_hr.font.size = Pt(8)
    r_hr.font.color.rgb = RGBColor(100, 116, 139)

    # 2. PIE DE PÁGINA DE PÁGINAS 2+
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""
    fp.paragraph_format.space_before = Pt(0)
    fp.paragraph_format.space_after = Pt(0)

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
    r_fl = p_fl.add_run("Confidencial - Material Oficial de Sustentación UTP (Grupo 01)")
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

def polish_document_elements(doc, doc_info):
    """
    Aplica tipografía ejecutiva, jerarquía de títulos con barra azul lateral,
    tablas estandarizadas tipo consultoría y paneles de alerta en todo el cuerpo.
    """
    for p in doc.paragraphs:
        txt = p.text.strip()
        style_name = p.style.name if p.style else ""

        # Heading 1
        if style_name.startswith("Heading 1"):
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(r'''
                <w:pBdr {} >
                    <w:left w:val="single" w:sz="24" w:space="8" w:color="1E40AF"/>
                </w:pBdr>
            '''.format(nsdecls('w')))
            pPr.append(pBdr)

            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(14.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42)

        # Heading 2
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

        # Pie de figuras / leyendas de imágenes
        elif txt.startswith("Figura ") or txt.startswith("*Figura ") or "Diagrama Arquitectónico" in txt:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(14)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8.5)
                r.font.italic = True
                r.font.color.rgb = RGBColor(100, 116, 139)

        # Citas y Callouts
        elif style_name in ["Quote", "Block Text"]:
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            pPr = p._p.get_or_add_pPr()
            pBdr = parse_xml(r'''
                <w:pBdr {} >
                    <w:left w:val="single" w:sz="20" w:space="6" w:color="2563EB"/>
                </w:pBdr>
            '''.format(nsdecls('w')))
            pPr.append(pBdr)
            shd = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
            pPr.append(shd)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(30, 41, 59)

        # Párrafos normales
        else:
            if "drawing" in p._p.xml:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_before = Pt(10)
                p.paragraph_format.space_after = Pt(2)
            else:
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(4.5)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(10)
                    r.font.color.rgb = RGBColor(30, 41, 59)

    # TABLAS DEL CUERPO
    for table in doc.tables:
        row_count = len(table.rows)
        if row_count == 0:
            continue

        first_cell_text = table.rows[0].cells[0].text.strip()
        if first_cell_text in ["UNIVERSIDAD TECNOLÓGICA DEL PERÚ", "PROYECTO:", "LEOFIT SOLUTIONS"]:
            continue
        if "DOCUMENTO TÉCNICO OFICIAL" in first_cell_text:
            continue

        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        apply_table_cell_margins(table, top_dxa=90, bottom_dxa=90, left_dxa=130, right_dxa=130)

        col_count = len(table.columns)
        total_width = Inches(6.5)
        col_width = total_width / max(1, col_count)

        header_row = table.rows[0]
        header_row._tr.get_or_add_trPr().append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))
        header_row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))

        for cell in header_row.cells:
            cell.width = col_width
            shd = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shd)
            borders = parse_xml(r'''
                <w:tcBorders {} >
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                    <w:bottom w:val="single" w:sz="6" w:space="0" w:color="1E293B"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="334155"/>
                </w:tcBorders>
            '''.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(borders)

            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9)
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(255, 255, 255)

        for r_idx in range(1, row_count):
            row = table.rows[r_idx]
            row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
            is_even = (r_idx % 2 == 0)
            fill_color = "F8FAFC" if is_even else "FFFFFF"

            for cell in row.cells:
                cell.width = col_width
                shd = parse_xml(r'<w:shd {} w:fill="{}"/>'.format(nsdecls('w'), fill_color))
                cell._tc.get_or_add_tcPr().append(shd)
                borders = parse_xml(r'''
                    <w:tcBorders {} >
                        <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                        <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    </w:tcBorders>
                '''.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(borders)

                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(1)
                    for r in p.runs:
                        r.font.name = "Calibri"
                        r.font.size = Pt(9)
                        r.font.color.rgb = RGBColor(30, 41, 59)

def main():
    print("======================================================================")
    print("COMPILADOR EJECUTIVO DE ENTREGABLES OFICIALES (HTML + WORD .DOCX)")
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
            processed_md = preprocess_markdown(doc_info["src"], doc_id)

            html_path = generate_formal_html(doc_info, processed_md)
            html_size_kb = os.path.getsize(html_path) / 1024.0
            print(f"  [OK] HTML formal generado: {html_name} ({html_size_kb:.1f} KB)")

            docx_path = doc_info["docx_dest"]
            convert_md_to_docx_via_pandoc(processed_md, docx_path)

            doc = docx.Document(docx_path)
            sec = doc.sections[0]
            sec.top_margin = Inches(1.0)
            sec.bottom_margin = Inches(1.0)
            sec.left_margin = Inches(1.0)
            sec.right_margin = Inches(1.0)

            setup_headers_and_footers(sec, doc_info)
            add_executive_cover_page(doc, doc_info)
            polish_document_elements(doc, doc_info)

            doc.save(docx_path)
            docx_size_kb = os.path.getsize(docx_path) / 1024.0
            print(f"  [OK] Word (.docx) ejecutiva finalizada: {doc_name} ({docx_size_kb:.1f} KB)")

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
