# -*- coding: utf-8 -*-
"""
Script generador del Informe Final Maestro APF1 con estructura editorial completa:
- Portada institucional UTP.
- Formato IEEE / Academico riguroso.
- Tablas estilizadas con cabeceras oscuras y padding.
- 10 Figuras de diagramas y mockups integradas en alta resolucion con captions formales.
- Eliminacion de cualquier artefacto visual o asterisco no parseado.
- Compilacion automatica a MD, DOCX y PDF mediante Microsoft Word COM.
"""

import os
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import win32com.client
import pythoncom

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def parse_inline(p, text, default_color=RGBColor(30, 41, 59), font_size=Pt(11), font_name='Calibri'):
    token_pattern = re.compile(
        r'(\*\*(.+?)\*\*)|'       # **bold**
        r'(\*(.+?)\*)|'           # *italic*
        r'(`(.+?)`)|'             # `code`
        r'(\$(.+?)\$)'            # $formula$
    )
    pos = 0
    for m in token_pattern.finditer(text):
        start, end = m.span()
        if start > pos:
            t = text[pos:start]
            if t:
                run = p.add_run(t)
                run.font.name = font_name
                run.font.size = font_size
                run.font.color.rgb = default_color
        if m.group(1): # Bold
            run = p.add_run(m.group(2))
            run.font.name = font_name
            run.font.size = font_size
            run.font.bold = True
            run.font.color.rgb = default_color
        elif m.group(3): # Italic
            run = p.add_run(m.group(4))
            run.font.name = font_name
            run.font.size = font_size
            run.font.italic = True
            run.font.color.rgb = default_color
        elif m.group(5): # Code
            run = p.add_run(m.group(6))
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(194, 65, 12)
        elif m.group(7): # Math
            math_t = m.group(8).replace(r'\ge', '≥').replace(r'\le', '≤').replace(r'\%', '%')
            math_t = math_t.replace(r'\text', '').replace('{', '').replace('}', '')
            run = p.add_run(math_t)
            run.font.name = font_name
            run.font.size = font_size
            run.font.italic = True
            run.font.color.rgb = default_color
        pos = end
    if pos < len(text):
        t = text[pos:]
        if t:
            run = p.add_run(t)
            run.font.name = font_name
            run.font.size = font_size
            run.font.color.rgb = default_color

def create_master_docx(docx_path):
    print("Creando documento maestro DOCX con portada, tablas y figuras integradas...")
    doc = docx.Document()
    
    # Page setup
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
    # Styles
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    # ==================== PORTADA INSTITUCIONAL ====================
    p_uni = doc.add_paragraph()
    p_uni.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_uni.paragraph_format.space_before = Pt(36)
    p_uni.paragraph_format.space_after = Pt(2)
    r = p_uni.add_run("UNIVERSIDAD TECNOLÓGICA DEL PERÚ")
    r.font.name = 'Calibri'
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p_fac = doc.add_paragraph()
    p_fac.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fac.paragraph_format.space_before = Pt(2)
    p_fac.paragraph_format.space_after = Pt(4)
    r = p_fac.add_run("FACULTAD DE INGENIERÍA DE SISTEMAS E INFORMÁTICA")
    r.font.name = 'Calibri'
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(71, 85, 105)
    
    p_cur = doc.add_paragraph()
    p_cur.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cur.paragraph_format.space_before = Pt(0)
    p_cur.paragraph_format.space_after = Pt(48)
    r = p_cur.add_run("CURSO INTEGRADOR II: SOFTWARE (100000S12F)")
    r.font.name = 'Calibri'
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(249, 115, 22) # Orange
    
    # Línea decorativa
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_after = Pt(36)
    r = p_line.add_run("____________________________________________________")
    r.font.color.rgb = RGBColor(203, 213, 225)
    
    p_tit = doc.add_paragraph()
    p_tit.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tit.paragraph_format.space_before = Pt(12)
    p_tit.paragraph_format.space_after = Pt(12)
    r = p_tit.add_run("INFORME DE AVANCE DE PROYECTO FINAL 1 (APF1)")
    r.font.name = 'Calibri'
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(48)
    r = p_sub.add_run("SISTEMA WEB PWA DE GESTIÓN Y TOMA DE PEDIDOS MULTICANAL PARA LA EMPRESA LEOFIT")
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = RGBColor(51, 65, 85)
    
    # Tabla de Integrantes en Portada
    t_team = doc.add_table(rows=6, cols=3)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["N°", "Apellidos y Nombres", "Rol Técnico Asignado"]
    for c_idx, h in enumerate(headers):
        cell = t_team.cell(0, c_idx)
        cell.text = h
        shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
        cell._tc.get_or_add_tcPr().append(shading)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                
    members = [
        ("1", "Loayza Rodriguez, Lady Luz", "Scrum Master / Coordinación General / UX-UI"),
        ("2", "Cárdenas Fernández, Víctor Leandro", "Product Owner / Arquitecto Back-End y BD"),
        ("3", "Roman Delgado, Harley Anthony", "Front-End Lead / Especialista PWA y WPO"),
        ("4", "Dávila Morales, Jim Alessandro", "Ingeniero QA / Testing Automatizado y CI/CD"),
        ("5", "Rojas Sanchez, Daniel Enrique", "Analista Funcional / Modelado de Procesos")
    ]
    for r_idx, (num, name, role) in enumerate(members, start=1):
        t_team.cell(r_idx, 0).text = num
        t_team.cell(r_idx, 0).paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        t_team.cell(r_idx, 1).text = name
        t_team.cell(r_idx, 2).text = role
        for c_idx in range(3):
            cell = t_team.cell(r_idx, c_idx)
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            if r_idx % 2 == 1:
                shading = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                cell._tc.get_or_add_tcPr().append(shading)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
                    
    # Pie de portada
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(48)
    p_foot.paragraph_format.space_after = Pt(0)
    r = p_foot.add_run("Lima, Perú\n2026")
    r.font.name = 'Calibri'
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(100, 116, 139)
    
    doc.add_page_break()
    
    # ==================== CONTENIDO DEL INFORME ====================
    with open("docs/INFORME_FINAL_APF1_LEOFIT.md", "r", encoding="utf-8") as f:
        md_text = f.read()
        
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []
    
    # Saltar encabezado duplicado en MD ya que la portada lo contiene
    while i < len(lines) and not lines[i].startswith('## ÍNDICE GENERAL'):
        i += 1
        
    while i < len(lines):
        line = lines[i]
        
        # 1. Tablas
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            if not all(c in '|:- ' for c in line.strip()):
                raw_cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                table_rows.append(raw_cells)
            i += 1
            continue
        else:
            if in_table:
                if table_rows:
                    cols_count = max(len(r) for r in table_rows)
                    t = doc.add_table(rows=len(table_rows), cols=cols_count)
                    t.alignment = WD_TABLE_ALIGNMENT.CENTER
                    for r_idx, row in enumerate(table_rows):
                        for c_idx, cell_value in enumerate(row):
                            if c_idx < cols_count:
                                cell = t.cell(r_idx, c_idx)
                                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                                set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
                                cell_p = cell.paragraphs[0]
                                cell_p.paragraph_format.space_before = Pt(0)
                                cell_p.paragraph_format.space_after = Pt(0)
                                cell_p.paragraph_format.line_spacing = 1.15
                                
                                is_header = (r_idx == 0)
                                if is_header:
                                    shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
                                    cell._tc.get_or_add_tcPr().append(shading)
                                    parse_inline(cell_p, cell_value, default_color=RGBColor(255, 255, 255), font_size=Pt(9.5))
                                    for run in cell_p.runs:
                                        run.font.bold = True
                                else:
                                    if r_idx % 2 == 1:
                                        shading = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                                        cell._tc.get_or_add_tcPr().append(shading)
                                    sub_lines = cell_value.split('<br>')
                                    for sub_idx, sub_l in enumerate(sub_lines):
                                        if sub_idx > 0:
                                            cell_p = cell.add_paragraph()
                                            cell_p.paragraph_format.space_before = Pt(2)
                                            cell_p.paragraph_format.space_after = Pt(0)
                                            cell_p.paragraph_format.line_spacing = 1.15
                                        parse_inline(cell_p, sub_l.strip(), default_color=RGBColor(30, 41, 59), font_size=Pt(9))
                    spacer = doc.add_paragraph()
                    spacer.paragraph_format.space_before = Pt(0)
                    spacer.paragraph_format.space_after = Pt(6)
                in_table = False
                table_rows = []
                
        # 2. Encabezados H1, H2, H3
        if line.startswith('# '):
            doc.add_page_break() # Salto de página antes de cada sección mayor
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            parse_inline(p, line[2:].strip(), default_color=RGBColor(15, 23, 42), font_size=Pt(16))
            for run in p.runs:
                run.font.bold = True
        elif line.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            parse_inline(p, line[3:].strip(), default_color=RGBColor(249, 115, 22), font_size=Pt(13))
            for run in p.runs:
                run.font.bold = True
        elif line.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            parse_inline(p, line[4:].strip(), default_color=RGBColor(30, 41, 59), font_size=Pt(11.5))
            for run in p.runs:
                run.font.bold = True
                
        # 3. Listas con Viñetas
        elif line.startswith('* ') or line.startswith('- ') or line.strip().startswith('• '):
            clean_b = line.strip()
            if clean_b.startswith('* ') or clean_b.startswith('- ') or clean_b.startswith('• '):
                clean_b = clean_b[2:]
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            parse_inline(p, clean_b, default_color=RGBColor(30, 41, 59), font_size=Pt(10.5))
            
        # 4. Listas Numeradas
        elif re.match(r'^\d+\.\s+', line.strip()):
            m = re.match(r'^\d+\.\s+', line.strip())
            content_num = line.strip()[len(m.group(0)):]
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            parse_inline(p, content_num, default_color=RGBColor(30, 41, 59), font_size=Pt(10.5))
            
        # 5. Bloques de Código / Diagramas ASCII
        elif line.strip().startswith('```'):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            shading = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
            p._p.get_or_add_pPr().append(shading)
            run = p.add_run('\n'.join(code_lines))
            run.font.name = 'Consolas'
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(15, 23, 42)
            
        # 6. Detección e Inserción de Figuras / Diagramas
        elif "diagrams/01_BPMN_AS-IS.png" in line:
            # Insertar Figura 1
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(10)
            p_img.paragraph_format.space_after = Pt(4)
            doc.add_picture("diagrams/01_BPMN_AS-IS.png", width=Inches(6.2))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(12)
            r = p_cap.add_run("Figura 1: Diagrama de Procesos Actual (AS-IS) bajo estándar BPMN 2.0")
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 116, 139)
            
        elif "frontend/mockups/01_Login.png" in line or line.strip().startswith("* `01_Login.png`") or line.strip().startswith("- `01_Login.png`"):
            # Insertar los 5 Mockups de Alta Fidelidad
            mockup_list = [
                ("frontend/mockups/01_Login.png", "Figura 4: Mockup de Pantalla de Autenticación / Login Administrativo"),
                ("frontend/mockups/02_Dashboard.png", "Figura 5: Mockup del Dashboard Principal con Métricas Operativas en Vivo"),
                ("frontend/mockups/03_Listado_Pedidos.png", "Figura 6: Mockup de la Bandeja de Gestión y Filtrado de Pedidos"),
                ("frontend/mockups/04_Formulario_Pedido.png", "Figura 7: Mockup del Formulario Modal de Toma y Registro de Pedidos"),
                ("frontend/mockups/05_Gestion_Productos.png", "Figura 8: Mockup del Módulo de Control de Catálogo e Inventario")
            ]
            for img_p, cap in mockup_list:
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(2)
                doc.add_picture(img_p, width=Inches(5.6))
                
                p_cap = doc.add_paragraph()
                p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_cap.paragraph_format.space_after = Pt(10)
                r = p_cap.add_run(cap)
                r.font.name = 'Calibri'
                r.font.size = Pt(9.5)
                r.font.italic = True
                r.font.color.rgb = RGBColor(100, 116, 139)
                
            # Saltar las líneas de texto de mockups que ya se insertaron como figuras
            while i < len(lines) and (lines[i].strip().startswith("* `0") or lines[i].strip().startswith("- `0")):
                i += 1
            continue
            
        elif "diagrams/02_Mapa_Riesgos.png" in line or "Heatmap de Riesgos" in line:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            doc.add_picture("diagrams/02_Mapa_Riesgos.png", width=Inches(5.8))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r = p_cap.add_run("Figura 9: Mapa de Riesgos y Heatmap Cuantitativo (Probabilidad x Impacto 5x5)")
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 116, 139)
            
        elif "diagrams/03_Arquitectura_Inicial.png" in line or "Arquitectura Limpia (Clean Architecture)" in line:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            doc.add_picture("diagrams/03_Arquitectura_Inicial.png", width=Inches(5.8))
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r = p_cap.add_run("Figura 10: Arquitectura de Software Multicapa del Sistema PWA LeoFit")
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.italic = True
            r.font.color.rgb = RGBColor(100, 116, 139)
            
        elif line.strip() == '---':
            pass
            
        # 7. Párrafos normales
        elif line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            parse_inline(p, line.strip(), default_color=RGBColor(30, 41, 59), font_size=Pt(11))
            
        i += 1
        
    doc.save(docx_path)
    print(f"[DOCX MAESTRO OK] Guardado exitosamente: {docx_path}")

def export_master_to_pdf(docx_path, pdf_path):
    print("Exportando documento maestro a PDF vía Word COM...")
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    try:
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        wb = word.Documents.Open(abs_docx)
        wb.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
        wb.Close()
        print(f"[PDF MAESTRO OK] Exportado exitosamente: {pdf_path}")
    except Exception as e:
        print(f"[ERROR] Error al exportar PDF: {e}")
    finally:
        word.Quit()

if __name__ == '__main__':
    docx_file = "docs/INFORME_FINAL_APF1_LEOFIT.docx"
    pdf_file = "docs/INFORME_FINAL_APF1_LEOFIT.pdf"
    create_master_docx(docx_file)
    export_master_to_pdf(docx_file, pdf_file)
