# -*- coding: utf-8 -*-
"""
@file export_markdown_to_docx.py
@description Generador de dos fases:
             1. Compila Markdown a HTML corporativo, formal y de alto impacto visual (00_HTML/).
             2. Convierte el HTML generado a documentos Word completamente editables (.docx)
                en 01_DOCX/, aplicando estilos avanzados (encabezados corporativos, sombreado
                Navy #0F172A, filas alternadas #F8FAFC, bordes sutiles y encabezados/pies).
@project LeoFit Pedidos Sistema - Sustentación Proyecto Final (Semana 18)
@author Grupo 01 - UTP
"""

import os
import sys
import re
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar solo en maquina de desarrollo con los anexos presentes.")

ENTREGABLES_DIR = os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP")
HTML_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "00_HTML"))
DOCX_DIR = os.path.abspath(os.path.join(ENTREGABLES_DIR, "01_DOCX"))
CSS_FILE = os.path.join(HTML_DIR, "style.css")

os.makedirs(HTML_DIR, exist_ok=True)
os.makedirs(DOCX_DIR, exist_ok=True)

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
        "docx_dest": os.path.join(DOCX_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_PROYECTO_FINAL.docx")
    },
    {
        "id": "ADR-001",
        "title": "ADR-001: ELECCIÓN DE RENDER + NEON POSTGRESQL FRENTE A AWS",
        "subtitle": "Justificación Técnica, Comparativa de Costos y Umbrales Cuantitativos de Migración",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.md"),
        "html_dest": os.path.join(HTML_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "01_ADR-001_ELECCION_RENDER_NEON_VS_AWS.docx")
    },
    {
        "id": "ADR-002",
        "title": "ADR-002: ARQUITECTURA OBJETIVO NATIVA EN AWS Y COMPLEMENTOS",
        "subtitle": "Diseño C4 Contenedores, Topología VPC Multi-AZ y Servicios Especializados",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.md"),
        "html_dest": os.path.join(HTML_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.html"),
        "docx_dest": os.path.join(DOCX_DIR, "02_ADR-002_ARQUITECTURA_OBJETIVO_AWS_Y_COMPLEMENTOS.docx")
    },
    {
        "id": "DOC-SUNAT-001",
        "title": "CUMPLIMIENTO NORMATIVO SUNAT PARA COMPROBANTES ELECTRÓNICOS (CPE)",
        "subtitle": "Estándar OASIS UBL 2.1, Firma Digital INDECOPI, OSE y Gap Analysis del Repositorio",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "03_CUMPLIMIENTO_SUNAT_CPE.md"),
        "html_dest": os.path.join(HTML_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.html"),
        "docx_dest": os.path.join(DOCX_DIR, "03_CUMPLIMIENTO_SUNAT_CPE.docx")
    },
    {
        "id": "DOC-PAY-001",
        "title": "INTEGRACIÓN DE PASARELA DE PAGOS: SANDBOX FRENTE A PRODUCCIÓN",
        "subtitle": "Diferencias Operativas, Alcance PCI-DSS SAQ A, Webhooks HMAC y Transición Comercial",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.md"),
        "html_dest": os.path.join(HTML_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.html"),
        "docx_dest": os.path.join(DOCX_DIR, "04_INTEGRACION_PAGOS_SANDBOX_VS_PRODUCCION.docx")
    },
    {
        "id": "DOC-ARCH-001",
        "title": "ARQUITECTURA DEL REPOSITORIO, ESTÁNDARES DE INGENIERÍA Y ONBOARDING",
        "subtitle": "Diagrama C4 Real, Responsabilidades por Módulo y Guía de Incorporación en < 1 Día",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.md"),
        "html_dest": os.path.join(HTML_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.html"),
        "docx_dest": os.path.join(DOCX_DIR, "05_ARQUITECTURA_REPOSITORIO_Y_ESTANDARES.docx")
    },
    {
        "id": "DOC-TRAC-001",
        "title": "MATRIZ DE TRAZABILIDAD Y RESPUESTAS TÉCNICAS ANTE EL JURADO",
        "subtitle": "Mapeo Integral de Preguntas del Jurado, Anexos Técnicos y Evidencias de Código",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "06_MATRIZ_TRAZABILIDAD_JURADO.md"),
        "html_dest": os.path.join(HTML_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "06_MATRIZ_TRAZABILIDAD_JURADO.docx")
    },
    {
        "id": "DOC-COMP-001",
        "title": "COMPENDIO GENERAL DE ANEXOS TÉCNICOS Y GUÍA PARA EL JURADO EVALUADOR",
        "subtitle": "Índice Maestro de Arquitectura y Respuestas Técnicas de Sustentación",
        "src": os.path.join(PROYECTO_FINAL_DIR, "01_ANEXOS_TECNICOS", "README.md"),
        "html_dest": os.path.join(HTML_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.html"),
        "docx_dest": os.path.join(DOCX_DIR, "COMPENDIO_ANEXOS_TECNICOS_LEOFIT.docx")
    },
    {
        "id": "AUD-REAL-001",
        "title": "AUDITORÍA TÉCNICA E INVENTARIO REAL DEL CÓDIGO FUENTE",
        "subtitle": "Inspección Forense Read-Only, Servicios Cloud, Pruebas y Gaps Normativos",
        "src": os.path.join(PROYECTO_FINAL_DIR, "03_AUDITORIA_READONLY", "00_INVENTARIO_REAL.md"),
        "html_dest": os.path.join(HTML_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.html"),
        "docx_dest": os.path.join(DOCX_DIR, "AUDITORIA_INVENTARIO_REAL_CODIGO.docx")
    }
]

def clean_markdown_content(md_content):
    """
    Sanitiza y adapta el markdown:
    - Remueve emojis residuales.
    - Convierte bloques ```mermaid a contenedores visuales con clase 'mermaid'.
    - Adapta callouts GitHub (> [!NOTE]) a alertas HTML estilizadas.
    """
    # 1. Remover emojis residuales
    cleaned = re.sub(r'[\U00010000-\U0010ffff\u2600-\u27bf]', '', md_content)
    
    # 2. Convertir bloques mermaid a div con clase mermaid
    mermaid_pattern = re.compile(r'```mermaid(.*?)```', re.DOTALL)
    def mermaid_replacer(match):
        code = match.group(1).strip()
        return f'\n<div class="diagram-container"><div class="diagram-header">Diagrama Técnico de Arquitectura (Mermaid.js)</div><div class="diagram-body"><pre class="mermaid">{code}</pre></div><div class="diagram-caption">Figura: Arquitectura y Flujo de Software LeoFit</div></div>\n'
    cleaned = mermaid_pattern.sub(mermaid_replacer, cleaned)
    
    # 3. Callouts tipo alert
    cleaned = re.sub(r'^>\s*\[!NOTE\]\s*(.*)$', r'<div class="alert-box alert-note"><strong>NOTA TÉCNICA:</strong> \1</div>', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s*\[!TIP\]\s*(.*)$', r'<div class="alert-box alert-tip"><strong>RECOMENDACIÓN TÉCNICA:</strong> \1</div>', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s*\[!WARNING\]\s*(.*)$', r'<div class="alert-box alert-warning"><strong>ADVERTENCIA:</strong> \1</div>', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s*\[!IMPORTANT\]\s*(.*)$', r'<div class="alert-box alert-warning"><strong>IMPORTANTE:</strong> \1</div>', cleaned, flags=re.MULTILINE)

    return cleaned

def generate_html_document(doc_info):
    """
    Convierte el archivo Markdown a un documento HTML formal, estilizado y profesional.
    """
    src_file = doc_info["src"]
    with open(src_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    cleaned_md = clean_markdown_content(md_text)

    # Convertir Markdown a HTML fragmento usando Pandoc
    cmd = ["pandoc", "-f", "markdown+raw_html", "-t", "html"]
    res = subprocess.run(cmd, input=cleaned_md, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"Error en Pandoc al generar HTML para {src_file}: {res.stderr}")
    body_html = res.stdout

    # Plantilla HTML ejecutiva completa con estilos incrustados y Mermaid.js
    full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{doc_info["title"]} | LeoFit Solutions</title>
  <style>
{CSS_CONTENT}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      if (typeof mermaid !== 'undefined') {{
        mermaid.initialize({{
          startOnLoad: true,
          theme: 'neutral',
          securityLevel: 'loose',
          fontFamily: 'Inter, Segoe UI, sans-serif'
        }});
      }}
    }});
  </script>
</head>
<body>
  <div class="document-container">
    <header class="executive-cover">
      <div class="institutional-bar">
        <div class="institutional-title">
          Universidad Tecnológica del Perú (UTP) &bull; Facultad de Ingeniería
        </div>
        <div class="institutional-meta">
          Curso Integrador II: Software (100000S12F) &bull; Sección 35374 (Grupo 01)
        </div>
      </div>
      
      <div class="doc-hero">
        <span class="doc-badge-pill">{doc_info["id"]} &bull; SUSTENTACIÓN PROYECTO FINAL</span>
        <h1 class="doc-main-title">{doc_info["title"]}</h1>
        <p class="doc-subtitle">{doc_info["subtitle"]}</p>
      </div>
      
      <div class="metadata-grid">
        <div class="metadata-item">
          <span class="metadata-label">Docente Asesor</span>
          <span class="metadata-value">Ing. Enrique Lee Huamani Uriarte</span>
        </div>
        <div class="metadata-item">
          <span class="metadata-label">Empresa Beneficiaria</span>
          <span class="metadata-value">LeoFit Confecciones y Diseños Deportivos S.A.C.</span>
        </div>
        <div class="metadata-item">
          <span class="metadata-label">Versión de Producción</span>
          <span class="metadata-value">Release v2.0.0 (PostgreSQL 16 / Clean Architecture)</span>
        </div>
        <div class="metadata-item">
          <span class="metadata-label">Equipo de Ingeniería</span>
          <span class="metadata-value">Lady Loayza, Víctor Cárdenas, Harley Roman, Jim Dávila, Daniel Rojas</span>
        </div>
      </div>
    </header>

    <main class="document-body">
{body_html}
    </main>

    <footer class="document-footer">
      <div>
        <strong>LeoFit Solutions &bull; Grupo 01</strong> &mdash; Sistema Web PWA de Gestión de Pedidos Multicanal
      </div>
      <div>
        Documento Técnico de Arquitectura y Auditoría Oficial
      </div>
    </footer>
  </div>
</body>
</html>"""

    with open(doc_info["html_dest"], "w", encoding="utf-8") as f:
        f.write(full_html)
        
    return doc_info["html_dest"]

def convert_html_to_docx(html_path, docx_path):
    """
    Convierte el documento HTML generado a formato Word (.docx) mediante Pandoc.
    """
    cmd = [
        "pandoc",
        html_path,
        "-o", docx_path,
        "--from", "html",
        "--to", "docx"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        raise RuntimeError(f"Fallo Pandoc al convertir {html_path} a DOCX: {res.stderr}")

def enhance_docx_formatting(docx_path, doc_title):
    """
    Aplica diseño corporativo formal sobre el archivo Word editable:
    - Márgenes de 2.54 cm (1 pulgada).
    - Encabezado y pie de página institucional.
    - Tipografía Calibri limpia.
    - Título y encabezados en paleta Navy #0F172A y Blue #1665D8.
    - Tablas con sombreado de encabezado Navy, texto blanco, filas alternadas #F8FAFC y bordes.
    - Cajas de código y citas con fondo suave.
    """
    doc = docx.Document(docx_path)
    
    # 1. Configurar márgenes y encabezados de página
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Encabezado
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.runs[0] if len(hp.runs) > 0 else hp.add_run()
        hrun.text = "LeoFit Solutions — Sistema de Gestión de Pedidos Multicanal | UTP"
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(100, 116, 139) # Slate 500
        
        # Pie de página
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        frun = fp.runs[0] if len(fp.runs) > 0 else fp.add_run()
        frun.text = "Evaluación Proyecto Final (Ciclo 2026-I) — Grupo 01 | Documentación Técnica Oficial"
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 116, 139)

    # 2. Formatear párrafos y títulos
    for p in doc.paragraphs:
        # Formato de fuentes
        for r in p.runs:
            r.font.name = "Calibri"
            
        style_name = p.style.name if p.style else ""
        if "Heading 1" in style_name or "Título 1" in style_name:
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(16)
                r.font.bold = True
                r.font.color.rgb = RGBColor(15, 23, 42) # Navy #0F172A
        elif "Heading 2" in style_name or "Título 2" in style_name:
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(13.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(22, 101, 216) # Cobalt #1665D8
        elif "Heading 3" in style_name or "Título 3" in style_name:
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(11.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(51, 65, 85) # Slate #334155

    # 3. Formatear tablas con alta fidelidad
    for table in doc.tables:
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        row_count = len(table.rows)
        if row_count == 0:
            continue
            
        # Encabezado de la tabla (fila 0)
        header_tr = table.rows[0]._tr.get_or_add_trPr()
        header_tr.append(parse_xml(r'<w:tblHeader {}/>'.format(nsdecls('w'))))
        
        for cell in table.rows[0].cells:
            # Fondo Navy
            shd = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(shd)
            # Bordes
            borders = parse_xml(r'''
                <w:tcBorders {} >
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="0F172A"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="0F172A"/>
                    <w:bottom w:val="single" w:sz="8" w:space="0" w:color="1665D8"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="0F172A"/>
                </w:tcBorders>
            '''.format(nsdecls('w')))
            cell._tc.get_or_add_tcPr().append(borders)
            
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.bold = True
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = RGBColor(255, 255, 255)

        # Filas de datos
        for row_idx in range(1, row_count):
            row = table.rows[row_idx]
            # No partir fila entre páginas
            row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit {}/>'.format(nsdecls('w'))))
            is_even = (row_idx % 2 == 0)
            fill_color = "F8FAFC" if is_even else "FFFFFF"
            
            for cell in row.cells:
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
                    for r in p.runs:
                        r.font.name = "Calibri"
                        r.font.size = Pt(9.5)
                        r.font.color.rgb = RGBColor(30, 41, 59)

    doc.save(docx_path)

def main():
    print("======================================================================")
    print("CADENA DE CONSTRUCCION BIDIRECCIONAL: MARKDOWN -> HTML -> WORD (.DOCX)")
    print("======================================================================")
    print(f"Directorio HTML: {HTML_DIR}")
    print(f"Directorio DOCX: {DOCX_DIR}")
    print("")

    success_count = 0
    total = len(DOCUMENTS)

    for doc_info in DOCUMENTS:
        doc_name = os.path.basename(doc_info["docx_dest"])
        html_name = os.path.basename(doc_info["html_dest"])
        print(f"Procesando [{doc_info['id']}]: {os.path.basename(doc_info['src'])}")

        try:
            # 1. Generar HTML estilizado
            html_path = generate_html_document(doc_info)
            html_size_kb = os.path.getsize(html_path) / 1024.0
            print(f"  [OK] HTML generado: {html_name} ({html_size_kb:.1f} KB)")

            # 2. Convertir HTML a Word (.docx) mediante Pandoc
            docx_path = doc_info["docx_dest"]
            convert_html_to_docx(html_path, docx_path)

            # 3. Aplicar diseño y formato corporativo avanzado en Word
            enhance_docx_formatting(docx_path, doc_info["title"])
            docx_size_kb = os.path.getsize(docx_path) / 1024.0
            print(f"  [OK] Word (.docx) editado y estilizado: {doc_name} ({docx_size_kb:.1f} KB)")

            # 4. Validar integridad de apertura
            v = docx.Document(docx_path)
            assert len(v.paragraphs) > 0 or len(v.tables) > 0
            success_count += 1
            print(f"  [OK] Integridad verificada: {len(v.paragraphs)} parrafos, {len(v.tables)} tablas.\n")

        except Exception as e:
            print(f"  [ERROR] Fallo procesando {doc_name}: {e}\n")
            sys.exit(1)

    print("======================================================================")
    print(f"EXPORTACION COMPLETADA EXITOSAMENTE: {success_count}/{total} DOCUMENTOS")
    print("Versiones HTML visuales y Word editables listas en _PROYECTO_FINAL_LOCAL.")
    print("======================================================================")

if __name__ == "__main__":
    main()
