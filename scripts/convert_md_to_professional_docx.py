# -*- coding: utf-8 -*-
"""
Convertidor profesional de Markdown a Microsoft Word (.docx).
Procesa la sintaxis inline (negritas **, cursivas *, codigo `, formulas $)
y genera estilos nativos en python-docx sin dejar asteriscos literales.
"""

import os
import glob
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def parse_inline_formatting(paragraph, text, default_color=RGBColor(30, 41, 59), font_size=Pt(11), font_name='Calibri'):
    """
    Parsea tokens inline:
    - **negrita**
    - *cursiva*
    - `codigo`
    - $\ge$, $\le$, etc. (limpia delimitadores LaTeX)
    """
    # Regex para capturar tokens: **bold**, *italic*, `code`, $math$
    # Grupos: 1: bold, 2: italic, 3: code, 4: math
    token_pattern = re.compile(
        r'(\*\*(.+?)\*\*)|'       # **negrita**
        r'(\*(.+?)\*)|'           # *cursiva*
        r'(`(.+?)`)|'             # `codigo`
        r'(\$(.+?)\$)'            # $formula$
    )
    
    pos = 0
    for match in token_pattern.finditer(text):
        start, end = match.span()
        # Texto normal antes del token
        if start > pos:
            normal_text = text[pos:start]
            if normal_text:
                run = paragraph.add_run(normal_text)
                run.font.name = font_name
                run.font.size = font_size
                run.font.color.rgb = default_color
                
        # Evaluar qué grupo coincidió
        if match.group(1): # Bold
            bold_text = match.group(2)
            run = paragraph.add_run(bold_text)
            run.font.name = font_name
            run.font.size = font_size
            run.font.bold = True
            run.font.color.rgb = default_color
        elif match.group(3): # Italic
            italic_text = match.group(4)
            run = paragraph.add_run(italic_text)
            run.font.name = font_name
            run.font.size = font_size
            run.font.italic = True
            run.font.color.rgb = default_color
        elif match.group(5): # Code
            code_text = match.group(6)
            run = paragraph.add_run(code_text)
            run.font.name = 'Consolas'
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(194, 65, 12) # Dark orange/rust
        elif match.group(7): # Math
            math_text = match.group(8)
            # Limpiar comandos LaTeX comunes
            math_text = math_text.replace(r'\ge', '≥').replace(r'\le', '≤')
            math_text = math_text.replace(r'\times', '×').replace(r'\%', '%')
            math_text = math_text.replace(r'\text', '').replace('{', '').replace('}', '')
            run = paragraph.add_run(math_text)
            run.font.name = font_name
            run.font.size = font_size
            run.font.italic = True
            run.font.color.rgb = default_color
            
        pos = end
        
    # Texto restante después del último token
    if pos < len(text):
        remaining_text = text[pos:]
        if remaining_text:
            run = paragraph.add_run(remaining_text)
            run.font.name = font_name
            run.font.size = font_size
            run.font.color.rgb = default_color

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Establece padding interno en celdas de Word (en dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def convert_md_to_docx(md_filepath, docx_filepath):
    print(f"Transformando {md_filepath} -> {docx_filepath}...")
    with open(md_filepath, 'r', encoding='utf-8') as f:
        md_text = f.read()
        
    doc = docx.Document()
    
    # Configuración de márgenes estándar (1 pulgada = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Estilo base
    styles = doc.styles
    normal_style = styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(30, 41, 59)
    
    lines = md_text.split('\n')
    i = 0
    in_table = False
    table_rows = []
    
    while i < len(lines):
        line = lines[i]
        
        # 1. Detección de Tablas Markdown
        if line.strip().startswith('|') and line.strip().endswith('|'):
            if not in_table:
                in_table = True
                table_rows = []
            # Ignorar línea separadora de columnas (|:---|:---:|)
            if not all(c in '|:- ' for c in line.strip()):
                raw_cells = [c.strip() for c in line.strip().split('|')[1:-1]]
                table_rows.append(raw_cells)
            i += 1
            continue
        else:
            if in_table:
                # Renderizar tabla acumulada
                if table_rows:
                    cols_count = max(len(r) for r in table_rows)
                    t = doc.add_table(rows=len(table_rows), cols=cols_count)
                    t.alignment = WD_TABLE_ALIGNMENT.CENTER
                    
                    for r_idx, row in enumerate(table_rows):
                        # Establecer altura mínima de fila
                        row_tr = t.rows[r_idx]._tr.get_or_add_trPr()
                        trHeight = OxmlElement('w:trHeight')
                        trHeight.set(qn('w:val'), '280') # dxa
                        row_tr.append(trHeight)
                        
                        for c_idx, cell_value in enumerate(row):
                            if c_idx < cols_count:
                                cell = t.cell(r_idx, c_idx)
                                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                                set_cell_margins(cell, top=120, bottom=120, left=150, right=150)
                                
                                # Limpiar párrafo por defecto
                                cell_p = cell.paragraphs[0]
                                cell_p.paragraph_format.space_before = Pt(0)
                                cell_p.paragraph_format.space_after = Pt(0)
                                cell_p.paragraph_format.line_spacing = 1.15
                                
                                is_header = (r_idx == 0)
                                
                                if is_header:
                                    # Cabecera con fondo oscuro
                                    shading = parse_xml(r'<w:shd {} w:fill="0F172A"/>'.format(nsdecls('w')))
                                    cell._tc.get_or_add_tcPr().append(shading)
                                    parse_inline_formatting(
                                        cell_p,
                                        cell_value,
                                        default_color=RGBColor(255, 255, 255),
                                        font_size=Pt(10),
                                        font_name='Calibri'
                                    )
                                    for r in cell_p.runs:
                                        r.font.bold = True
                                else:
                                    # Fila de datos
                                    if r_idx % 2 == 1:
                                        shading = parse_xml(r'<w:shd {} w:fill="F8FAFC"/>'.format(nsdecls('w')))
                                        cell._tc.get_or_add_tcPr().append(shading)
                                        
                                    # Procesar saltos de línea internos (<br>)
                                    sub_lines = cell_value.split('<br>')
                                    for sub_idx, sub_l in enumerate(sub_lines):
                                        if sub_idx > 0:
                                            cell_p = cell.add_paragraph()
                                            cell_p.paragraph_format.space_before = Pt(2)
                                            cell_p.paragraph_format.space_after = Pt(0)
                                            cell_p.paragraph_format.line_spacing = 1.15
                                        parse_inline_formatting(
                                            cell_p,
                                            sub_l.strip(),
                                            default_color=RGBColor(30, 41, 59),
                                            font_size=Pt(9.5),
                                            font_name='Calibri'
                                        )
                    # Espacio posterior a la tabla
                    spacer = doc.add_paragraph()
                    spacer.paragraph_format.space_before = Pt(0)
                    spacer.paragraph_format.space_after = Pt(6)
                    
                in_table = False
                table_rows = []
                
        # 2. Encabezados H1, H2, H3
        if line.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            parse_inline_formatting(p, line[2:].strip(), default_color=RGBColor(15, 23, 42), font_size=Pt(18))
            for r in p.runs:
                r.font.bold = True
        elif line.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            parse_inline_formatting(p, line[3:].strip(), default_color=RGBColor(249, 115, 22), font_size=Pt(14))
            for r in p.runs:
                r.font.bold = True
        elif line.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            parse_inline_formatting(p, line[4:].strip(), default_color=RGBColor(30, 41, 59), font_size=Pt(12))
            for r in p.runs:
                r.font.bold = True
        elif line.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            parse_inline_formatting(p, line[5:].strip(), default_color=RGBColor(71, 85, 105), font_size=Pt(11))
            for r in p.runs:
                r.font.bold = True
                
        # 3. Listas con Viñetas
        elif line.startswith('* ') or line.startswith('- ') or (line.strip().startswith('• ')):
            clean_bullet = line.strip()
            if clean_bullet.startswith('* ') or clean_bullet.startswith('- '):
                clean_bullet = clean_bullet[2:]
            elif clean_bullet.startswith('• '):
                clean_bullet = clean_bullet[2:]
                
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            parse_inline_formatting(p, clean_bullet, default_color=RGBColor(30, 41, 59), font_size=Pt(10.5))
            
        # 4. Listas Numeradas (1. , 2. )
        elif re.match(r'^\d+\.\s+', line.strip()):
            num_match = re.match(r'^\d+\.\s+', line.strip())
            num_prefix = num_match.group(0)
            num_content = line.strip()[len(num_prefix):]
            
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            parse_inline_formatting(p, num_content, default_color=RGBColor(30, 41, 59), font_size=Pt(10.5))
            
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
            p.paragraph_format.line_spacing = 1.05
            
            shading = parse_xml(r'<w:shd {} w:fill="F1F5F9"/>'.format(nsdecls('w')))
            p._p.get_or_add_pPr().append(shading)
            
            run = p.add_run('\n'.join(code_lines))
            run.font.name = 'Consolas'
            run.font.size = Pt(9.0)
            run.font.color.rgb = RGBColor(15, 23, 42)
            
        # 6. Separador horizontal
        elif line.strip() == '---':
            pass
            
        # 7. Párrafos normales
        elif line.strip():
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            parse_inline_formatting(p, line.strip(), default_color=RGBColor(30, 41, 59), font_size=Pt(11))
            
        i += 1
        
    doc.save(docx_filepath)
    print(f"[DOCX OK] Guardado exitosamente: {docx_filepath}")

def convert_all_md_to_docx():
    print("=== INICIANDO CONVERSIÓN RIGUROSA DE MD A DOCX ===")
    md_files = sorted(glob.glob("docs/*.md"))
    for md in md_files:
        docx_out = md.replace(".md", ".docx")
        convert_md_to_docx(md, docx_out)
    print(f"=== {len(md_files)} DOCUMENTOS DOCX GENERADOS EXITOSAMENTE ===")

if __name__ == '__main__':
    convert_all_md_to_docx()
