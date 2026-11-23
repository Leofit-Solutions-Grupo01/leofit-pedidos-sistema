# -*- coding: utf-8 -*-
"""
@file apa7_formatter.py
@description Motor de Maquetación y Estandarización Normas APA 7ma Edición (American Psychological Association)
             para los informes técnicos en Word (.docx) del Proyecto Final LeoFit Solutions:
             1. Márgenes uniformes de 1 pulgada (2.54 cm) en los 4 lados.
             2. Tipografía académica estandarizada: Times New Roman 12 pt (cuerpo) y Consolas 9.5 pt (código).
             3. Portada Académica APA 7ma Edición con afiliación institucional UTP, autores, códigos, asesor y fecha.
             4. Encabezado con Cornisa (Running Head en MAYÚSCULAS) y numeración de página superior derecha.
             5. Jerarquía de 5 Niveles de Títulos APA 7:
                - Nivel 1: Centrado, Negrita.
                - Nivel 2: Alineado a la izquierda, Negrita.
                - Nivel 3: Alineado a la izquierda, Negrita y Cursiva.
                - Nivel 4: Sangría de 1.27 cm, Negrita.
                - Nivel 5: Sangría de 1.27 cm, Negrita y Cursiva.
             6. Párrafos de cuerpo con sangría de primera línea de 1.27 cm (0.5 pulgadas) e interlineado formal.
             7. Tablas bajo estándar estricto APA 7:
                - CERO bordes verticales (left=none, right=none, insideV=none).
                - Bordes horizontales superior de tabla, inferior de cabecera e inferior de tabla (1 pt #0F172A).
                - Etiqueta en dos líneas: 'Tabla X' (Negrita) y 'Título de la tabla' (Cursiva).
             8. Figuras bajo estándar estricto APA 7:
                - Etiqueta superior en dos líneas: 'Figura X' (Negrita) y 'Título de la figura' (Cursiva).
                - Imagen centrada y 'Nota.' descriptiva al pie.
             9. Referencias Bibliográficas con sangría francesa (hanging indent) de 1.27 cm (0.5 pulgadas)
                y orden alfabético sin numeración.
"""

import os
import re
import math
import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

BODY_FONT = "Times New Roman"
CODE_FONT = "Consolas"
NAVY_RGB = RGBColor(0x0F, 0x17, 0x2A)
DARK_RGB = RGBColor(0x1E, 0x29, 0x3B)
MUTED_RGB = RGBColor(0x47, 0x55, 0x69)
BLACK_RGB = RGBColor(0x00, 0x00, 0x00)


def set_run_font(run, font_name=BODY_FONT, size_pt=12, bold=None, italic=None, color_rgb=BLACK_RGB):
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    if bold is not None:
        run.font.bold = bold
    if italic is not None:
        run.font.italic = italic
    if color_rgb is not None:
        run.font.color.rgb = color_rgb
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(attr), font_name)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(attr)) is not None:
            del rf.attrib[qn(attr)]


def set_style_font(style, font_name=BODY_FONT, size_pt=12, bold=False, italic=False, color_rgb=BLACK_RGB):
    if not hasattr(style, "font") or style.font is None:
        return
    style.font.name = font_name
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    style.font.italic = italic
    style.font.color.rgb = color_rgb
    rpr = style.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(attr), font_name)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(attr)) is not None:
            del rf.attrib[qn(attr)]


def apply_apa7_margins_and_styles(doc):
    """Configura márgenes de 1 pulgada (2.54 cm) en todas las secciones y estilos base APA 7."""
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)

    # Estilo Normal APA 7
    if "Normal" in doc.styles:
        st_norm = doc.styles["Normal"]
        set_style_font(st_norm, BODY_FONT, 12, bold=False, italic=False, color_rgb=BLACK_RGB)
        st_norm.paragraph_format.line_spacing = 1.5
        st_norm.paragraph_format.space_before = Pt(0)
        st_norm.paragraph_format.space_after = Pt(6)

    # Estilos de Títulos APA 7 (Niveles 1 a 5)
    heading_specs = {
        "Heading 1": (14, True, False, WD_ALIGN_PARAGRAPH.CENTER, 18, 8, Inches(0)),
        "Heading 2": (13, True, False, WD_ALIGN_PARAGRAPH.LEFT, 14, 6, Inches(0)),
        "Heading 3": (12, True, True, WD_ALIGN_PARAGRAPH.LEFT, 12, 4, Inches(0)),
        "Heading 4": (12, True, False, WD_ALIGN_PARAGRAPH.LEFT, 10, 4, Inches(0.5)),
        "Heading 5": (12, True, True, WD_ALIGN_PARAGRAPH.LEFT, 10, 4, Inches(0.5)),
    }
    for h_name, (sz, bld, itl, align, sb, sa, ind) in heading_specs.items():
        if h_name in doc.styles:
            st = doc.styles[h_name]
            set_style_font(st, BODY_FONT, sz, bold=bld, italic=itl, color_rgb=NAVY_RGB)
            st.paragraph_format.alignment = align
            st.paragraph_format.space_before = Pt(sb)
            st.paragraph_format.space_after = Pt(sa)
            st.paragraph_format.first_line_indent = ind
            st.paragraph_format.keep_with_next = True


def setup_apa7_running_head(doc, running_head_text="EVALUACIÓN DE CALIDAD ISO/IEC 25010 — LEOFIT SOLUTIONS"):
    """Configura la cornisa (Running Head) en mayúsculas a la izquierda y número de página a la derecha."""
    sec = doc.sections[0]
    sec.different_first_page_header_footer = True

    # Limpiar primera página (o dejar solo número de página según APA 7)
    first_h = sec.first_page_header
    first_h.is_linked_to_previous = False
    for p in first_h.paragraphs:
        p.text = ""

    first_f = sec.first_page_footer
    first_f.is_linked_to_previous = False
    for p in first_f.paragraphs:
        p.text = ""

    header = sec.header
    header.is_linked_to_previous = False
    # Limpiar tablas o párrafos previos del header
    for tbl in list(header.tables):
        tbl._element.getparent().remove(tbl._element)
    for p in header.paragraphs:
        p.text = ""

    hp = header.paragraphs[0]
    hp.paragraph_format.space_before = Pt(0)
    hp.paragraph_format.space_after = Pt(4)

    tbl_h = header.add_table(rows=1, cols=2, width=Inches(6.5))
    tbl_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left, c_right = tbl_h.rows[0].cells[0], tbl_h.rows[0].cells[1]
    c_left.width = Inches(5.0)
    c_right.width = Inches(1.5)

    bdr_bottom = r'''
        <w:tcBorders %s>
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''' % nsdecls('w')
    c_left._tc.get_or_add_tcPr().append(parse_xml(bdr_bottom))
    c_right._tc.get_or_add_tcPr().append(parse_xml(bdr_bottom))

    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_l.paragraph_format.space_before = Pt(0)
    p_l.paragraph_format.space_after = Pt(2)
    p_l.paragraph_format.first_line_indent = Inches(0)
    r_l = p_l.add_run(running_head_text[:50].upper())
    set_run_font(r_l, BODY_FONT, 10, bold=False, italic=False, color_rgb=MUTED_RGB)

    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r.paragraph_format.space_before = Pt(0)
    p_r.paragraph_format.space_after = Pt(2)
    p_r.paragraph_format.first_line_indent = Inches(0)

    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instr1 = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    r_page = p_r.add_run()
    set_run_font(r_page, BODY_FONT, 11, bold=False, italic=False, color_rgb=BLACK_RGB)
    r_page._r.append(fld1)
    r_page._r.append(instr1)
    r_page._r.append(fld2)
    r_page._r.append(fld3)


def format_all_tables_apa7(doc):
    """
    Aplica el formato estricto de Tablas APA 7ma Edición a todas las tablas de datos:
    - CERO bordes verticales (left=none, right=none, insideV=none).
    - Borde horizontal superior de la tabla (1.0 pt #0F172A).
    - Borde horizontal inferior de la cabecera (1.0 pt #0F172A).
    - Borde horizontal inferior al final de la tabla (1.0 pt #0F172A).
    - Sin bordes verticales internos ni externos.
    - Fuente Times New Roman 10 pt en celdas para legibilidad óptima y ajuste a 6.5 pulgadas.
    """
    total_table_inches = 6.5

    for table in doc.tables:
        row_count = len(table.rows)
        col_count = len(table.columns)
        if row_count == 0 or col_count == 0:
            continue

        # Calcular anchos proporcionales según contenido
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
                w = math.sqrt(max(1, max_len)) + (avg_len ** 0.55)
            else:
                w = 1.0
            weights.append(max(1.0, w))

        sum_w = sum(weights)
        col_widths_in = [round((w / sum_w) * total_table_inches, 2) for w in weights]
        diff = total_table_inches - sum(col_widths_in)
        col_widths_in[-1] = round(col_widths_in[-1] + diff, 2)
        col_widths_dxa = [max(720, int(w * 1440)) for w in col_widths_in]

        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        tblPr = table._tbl.tblPr

        # Limpiar tblBorders, tblCellMar, tblLayout previos para evitar duplicados XML
        for tag in ("w:tblBorders", "w:tblCellMar", "w:tblLayout"):
            old = tblPr.find(qn(tag))
            if old is not None:
                tblPr.remove(old)

        # Márgenes internos de celda
        cell_mar = parse_xml(r'''
            <w:tblCellMar %s>
                <w:top w:w="80" w:type="dxa"/>
                <w:left w:w="110" w:type="dxa"/>
                <w:bottom w:w="80" w:type="dxa"/>
                <w:right w:w="110" w:type="dxa"/>
            </w:tblCellMar>
        ''' % nsdecls('w'))
        tblPr.append(cell_mar)

        # Bordes estrictos APA 7: Top y Bottom sólidos, CERO bordes verticales
        tbl_borders = parse_xml(r'''
            <w:tblBorders %s>
                <w:top w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
                <w:left w:val="none"/>
                <w:bottom w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
                <w:right w:val="none"/>
                <w:insideH w:val="none"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''' % nsdecls('w'))
        tblPr.append(tbl_borders)

        # Formatear filas
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            if trPr.find(qn("w:cantSplit")) is None:
                trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
            if r_idx == 0 and trPr.find(qn("w:tblHeader")) is None:
                trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))

            for c_idx, cell in enumerate(row.cells):
                if c_idx < len(col_widths_in):
                    cell.width = Inches(col_widths_in[c_idx])
                tcPr = cell._tc.get_or_add_tcPr()

                # Limpiar bordes y sombreados anteriores de celda para imponer APA 7 puro
                for tag in ("w:tcBorders", "w:shd"):
                    old = tcPr.find(qn(tag))
                    if old is not None:
                        tcPr.remove(old)

                if r_idx == 0:
                    # Cabecera APA 7: Borde inferior sólido 1 pt, fondo blanco o gris muy sutil (#F8FAFC)
                    tcPr.append(parse_xml(r'<w:shd %s w:val="clear" w:color="auto" w:fill="F8FAFC"/>' % nsdecls('w')))
                    tcPr.append(parse_xml(r'''
                        <w:tcBorders %s>
                            <w:top w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
                            <w:left w:val="none"/>
                            <w:bottom w:val="single" w:sz="8" w:space="0" w:color="0F172A"/>
                            <w:right w:val="none"/>
                        </w:tcBorders>
                    ''' % nsdecls('w')))
                elif r_idx == row_count - 1:
                    # Última fila APA 7: Borde inferior sólido 1 pt
                    tcPr.append(parse_xml(r'''
                        <w:tcBorders %s>
                            <w:top w:val="none"/>
                            <w:left w:val="none"/>
                            <w:bottom w:val="single" w:sz="10" w:space="0" w:color="0F172A"/>
                            <w:right w:val="none"/>
                        </w:tcBorders>
                    ''' % nsdecls('w')))
                else:
                    # Filas intermedias APA 7: Sin bordes verticales, línea divisoria horizontal tenue opcional
                    tcPr.append(parse_xml(r'''
                        <w:tcBorders %s>
                            <w:top w:val="none"/>
                            <w:left w:val="none"/>
                            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="E2E8F0"/>
                            <w:right w:val="none"/>
                        </w:tcBorders>
                    ''' % nsdecls('w')))

                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent = Inches(0)
                    p.paragraph_format.left_indent = Inches(0)
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    p.paragraph_format.line_spacing = 1.15
                    for r in p.runs:
                        is_code = r.font.name in ("Consolas", "Courier New")
                        set_run_font(
                            r,
                            CODE_FONT if is_code else BODY_FONT,
                            9.5 if is_code else 10,
                            bold=(True if r_idx == 0 else r.font.bold),
                            italic=r.font.italic,
                            color_rgb=(NAVY_RGB if r_idx == 0 else DARK_RGB)
                        )


def build_formal_apa7_cover(doc, title, subtitle, doc_code="INF-S14-S15"):
    """
    Elimina los encabezados crudos de portada al inicio del documento compilado por Pandoc
    e inserta una Portada Académica APA 7ma Edición formal y limpia en la Página 1.
    """
    # Detectar dónde empieza el cuerpo real ("Ficha de Control del Documento" o "Resumen Ejecutivo")
    cut_idx = 0
    for idx, p in enumerate(doc.paragraphs[:30]):
        txt = p.text.strip().lower()
        if "ficha de control" in txt or "resumen ejecutivo" in txt or "1. identificación" in txt:
            cut_idx = idx
            break

    if cut_idx > 0:
        for p in list(doc.paragraphs[:cut_idx]):
            p._element.getparent().remove(p._element)

    p_anchor = doc.paragraphs[0]

    def add_cover_line(text, size=12, bold=False, italic=False, space_before=0, space_after=6, color=BLACK_RGB):
        p = p_anchor.insert_paragraph_before("")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.first_line_indent = Inches(0)
        p.paragraph_format.left_indent = Inches(0)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.5
        r = p.add_run(text)
        set_run_font(r, BODY_FONT, size, bold=bold, italic=italic, color_rgb=color)
        return p

    # Estructura formal de Portada Académica APA 7ma Edición
    add_cover_line("UNIVERSIDAD TECNOLÓGICA DEL PERÚ", size=14, bold=True, space_before=12, space_after=2, color=NAVY_RGB)
    add_cover_line("Facultad de Ingeniería de Sistemas e Informática", size=12, bold=False, space_after=24, color=DARK_RGB)

    # Título del Informe en Negrita Centrado (APA 7 §2.3)
    add_cover_line(title, size=15, bold=True, space_before=18, space_after=8, color=NAVY_RGB)
    add_cover_line(subtitle, size=12, bold=False, italic=True, space_after=24, color=DARK_RGB)

    # Autores (Grupo 01) con códigos institucionales
    add_cover_line("Equipo de Ingeniería de Software — Grupo 01:", size=11.5, bold=True, space_before=8, space_after=4, color=NAVY_RGB)
    authors = [
        "Lady Luz Loayza Rodríguez (U22221489) — Scrum Master / DevSecOps Lead",
        "Víctor Leandro Cárdenas Fernández (U19217414) — Product Owner / DBA",
        "Harley Anthony Roman Delgado (U21313032) — Frontend Lead / UI-UX Designer",
        "Jim Alessandro Dávila Morales (U18206081) — QA Lead / Backend Developer",
        "Daniel Enrique Rojas Sánchez (U21214627) — Business Analyst / Cloud Architect",
    ]
    for auth in authors:
        add_cover_line(auth, size=11, bold=False, space_after=2, color=BLACK_RGB)

    # Datos de Asignatura, Docente y Empresa
    add_cover_line("Asignatura: Curso Integrador II: Software (100000S12F) — Sección 35374", size=11.5, bold=True, space_before=18, space_after=2)
    add_cover_line("Docente Asesor: Ing. Enrique Lee Huamani Uriarte", size=11.5, bold=True, space_after=4)
    add_cover_line("Empresa Patrocinadora: LeoFit Confecciones y Diseños Deportivos S.A.C. (RUC: 20608912345)", size=11, bold=False, space_after=14)

    # Bloque verificable de enlaces y credenciales para el docente
    add_cover_line("Enlaces Cloud Activos y Credenciales de Auditoría:", size=10.5, bold=True, space_before=6, space_after=2, color=NAVY_RGB)
    add_cover_line("Repositorio GitHub: https://github.com/Leofit-Solutions-Grupo01/leofit-pedidos-sistema", size=10, space_after=1, color=DARK_RGB)
    add_cover_line("Frontend PWA: https://leofit-solutions-grupo01.github.io/leofit-pedidos-sistema/", size=10, space_after=1, color=DARK_RGB)
    add_cover_line("Backend API & Swagger: https://leofit-backend-api.onrender.com/api/docs", size=10, space_after=1, color=DARK_RGB)
    add_cover_line("Credenciales: admin@leofit.pe (Admin123!)  |  operador@leofit.pe (Operador123!)", size=10, bold=True, space_after=18, color=DARK_RGB)

    add_cover_line("Lima, Perú", size=12, bold=False, space_before=10, space_after=2)
    add_cover_line("Noviembre de 2026", size=12, bold=False, space_after=0)

    # Salto de página al final de la Portada APA 7
    p_brk = p_anchor.insert_paragraph_before("")
    p_brk.paragraph_format.first_line_indent = Inches(0)
    p_brk.paragraph_format.space_before = Pt(0)
    p_brk.paragraph_format.space_after = Pt(0)
    p_brk.add_run().add_break(WD_BREAK.PAGE)


def polish_apa7_paragraphs_and_captions(doc, has_custom_cover=True):
    """
    Recorre los párrafos del documento aplicando:
    - Jerarquía de Títulos APA 7 (Niveles 1 a 5).
    - Separación y formato APA 7 de etiquetas de Tabla ('Tabla X' en negrita + salto + 'Título' en cursiva).
    - Separación y formato APA 7 de etiquetas de Figura ('Figura X' en negrita + salto + 'Título' en cursiva) y 'Nota.' al pie.
    - Sangría de primera línea de 1.27 cm (0.5 in) en párrafos de texto continuo.
    - Sangría francesa (Hanging Indent de 1.27 cm / 0.5 in) en todas las Referencias Bibliográficas.
    """
    in_references_section = False
    in_cover_area = True

    for idx, p in enumerate(doc.paragraphs):
        txt = p.text.strip()
        style_name = p.style.name if p.style else "Normal"

        # Detectar fin de la portada (cuando aparece el primer salto de página o primer Heading)
        if in_cover_area:
            if any(k in txt.lower() for k in ("ficha de control", "control de versiones", "resumen ejecutivo", "tabla de contenido", "índice")):
                in_cover_area = False
            elif style_name.startswith("Heading"):
                in_cover_area = False
            else:
                continue

        if not txt and len(p._p.xpath('.//w:drawing')) == 0:
            continue

        # Detectar entrada y salida de la sección de Referencias Bibliográficas
        if style_name.startswith("Heading") or style_name in ("Title", "Subtitle"):
            low_txt = txt.lower()
            if "referencias" in low_txt or "bibliografía" in low_txt:
                in_references_section = True
            elif in_references_section and any(k in low_txt for k in ("anexo", "apéndice", "glosario", "lista de")):
                in_references_section = False

        # 1. Imágenes / Figuras insertadas: Centrar sin sangría
        if len(p._p.xpath('.//w:drawing')) > 0:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(6)
            continue

        # 2. Títulos APA 7 (Heading 1 a Heading 5)
        if style_name.startswith("Heading 1"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, BODY_FONT, 14, bold=True, italic=False, color_rgb=NAVY_RGB)
            continue

        elif style_name.startswith("Heading 2"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, BODY_FONT, 13, bold=True, italic=False, color_rgb=NAVY_RGB)
            continue

        elif style_name.startswith("Heading 3"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, BODY_FONT, 12, bold=True, italic=True, color_rgb=NAVY_RGB)
            continue

        elif style_name.startswith("Heading 4"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, BODY_FONT, 12, bold=True, italic=False, color_rgb=NAVY_RGB)
            continue

        elif style_name.startswith("Heading 5"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Inches(0.5)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.keep_with_next = True
            for r in p.runs:
                set_run_font(r, BODY_FONT, 12, bold=True, italic=True, color_rgb=NAVY_RGB)
            continue

        # 3. Etiquetas de Tabla o Figura APA 7 (ej. "Tabla 5.1. Resultados..." o "Figura 5.2. Curva...")
        m_cap = re.match(r"^(Tabla|Figura)\s+([A-Za-z0-9\.\-]+)\.?\s+(.+)$", txt)
        if m_cap and len(txt) < 220:
            kind, num, title_part = m_cap.group(1), m_cap.group(2).rstrip("."), m_cap.group(3).strip()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(14)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.25
            p.paragraph_format.keep_with_next = True
            p.text = ""
            r_label = p.add_run(f"{kind} {num}\n")
            set_run_font(r_label, BODY_FONT, 11, bold=True, italic=False, color_rgb=NAVY_RGB)
            r_title = p.add_run(title_part)
            set_run_font(r_title, BODY_FONT, 11, bold=False, italic=True, color_rgb=DARK_RGB)
            continue

        # 4. Notas de Tabla o Figura APA 7 ("Nota." o "Lectura e Interpretación...")
        if txt.startswith("Nota.") or txt.startswith("Lectura e Interpretación") or txt.startswith("Trazabilidad"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.left_indent = Inches(0)
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.line_spacing = 1.2
            if not txt.startswith("Nota."):
                # Prefijar con "Nota. " según APA 7
                clean_body = txt
                p.text = ""
                r_n = p.add_run("Nota. ")
                set_run_font(r_n, BODY_FONT, 10, bold=False, italic=True, color_rgb=DARK_RGB)
                r_b = p.add_run(clean_body)
                set_run_font(r_b, BODY_FONT, 10, bold=False, italic=False, color_rgb=DARK_RGB)
            else:
                rest = txt[5:].strip()
                p.text = ""
                r_n = p.add_run("Nota. ")
                set_run_font(r_n, BODY_FONT, 10, bold=False, italic=True, color_rgb=DARK_RGB)
                r_b = p.add_run(rest)
                set_run_font(r_b, BODY_FONT, 10, bold=False, italic=False, color_rgb=DARK_RGB)
            continue

        # 5. Referencias Bibliográficas APA 7: Sangría Francesa (Hanging Indent de 1.27 cm / 0.5 in)
        if in_references_section:
            # Limpiar numeración residual si existiera ("1. Autor..." -> "Autor...")
            cleaned_ref = re.sub(r"^\d+[\.\)]\s+", "", txt)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.first_line_indent = Inches(-0.5)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.line_spacing = 1.5
            if "*" in cleaned_ref:
                p.text = ""
                parts = re.split(r"(\*[^\*]+\*)", cleaned_ref)
                for part in parts:
                    if not part:
                        continue
                    if part.startswith("*") and part.endswith("*") and len(part) > 2:
                        r = p.add_run(part[1:-1])
                        set_run_font(r, BODY_FONT, 11.5, bold=False, italic=True, color_rgb=BLACK_RGB)
                    else:
                        r = p.add_run(part)
                        set_run_font(r, BODY_FONT, 11.5, bold=False, italic=False, color_rgb=BLACK_RGB)
            else:
                if cleaned_ref != txt:
                    p.text = cleaned_ref
                for r in p.runs:
                    set_run_font(r, BODY_FONT, 11.5, bold=r.font.bold, italic=r.font.italic, color_rgb=BLACK_RGB)
            continue

        # 6. Bloques de Código Fuente (Source Code / Verbatim)
        if "Code" in style_name or "Verbatim" in style_name or any(r.font.name in ("Consolas", "Courier New") for r in p.runs if r.text.strip()):
            if len(p.runs) == 1 and p.runs[0].font.name in ("Consolas", "Courier New"):
                p.paragraph_format.first_line_indent = Inches(0)
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.1
                for r in p.runs:
                    set_run_font(r, CODE_FONT, 9.5, bold=r.font.bold, italic=r.font.italic, color_rgb=DARK_RGB)
                continue

        # 7. Listas con viñetas o numeradas y bloques de cita
        if "List" in style_name or "Compact" in style_name or txt.startswith(("•", "-", "1.", "2.", "3.", "4.", "5.")):
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.35
            if re.search(r"\*[^\*]+\*", txt):
                p.text = ""
                for part in re.split(r"(\*[^\*]+\*)", txt):
                    if not part:
                        continue
                    is_it = part.startswith("*") and part.endswith("*") and len(part) > 2
                    r = p.add_run(part[1:-1] if is_it else part)
                    set_run_font(r, BODY_FONT, 12, bold=False, italic=is_it, color_rgb=BLACK_RGB)
            else:
                for r in p.runs:
                    is_c = r.font.name in ("Consolas", "Courier New")
                    set_run_font(r, CODE_FONT if is_c else BODY_FONT, 10 if is_c else 12, bold=r.font.bold, italic=r.font.italic, color_rgb=BLACK_RGB)
            continue

        if style_name in ("Quote", "Block Text"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Inches(0.5)
            p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(8)
            p.paragraph_format.line_spacing = 1.35
            for r in p.runs:
                is_c = r.font.name in ("Consolas", "Courier New")
                set_run_font(r, CODE_FONT if is_c else BODY_FONT, 10 if is_c else 11.5, bold=r.font.bold, italic=r.font.italic, color_rgb=DARK_RGB)
            continue

        # 8. Párrafos de cuerpo estándar APA 7: Sangría de primera línea de 1.27 cm (0.5 in)
        if not style_name.startswith("TOC"):
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            # Aplicar sangría de primera línea de 1.27 cm a párrafos narrativos (> 45 caracteres)
            if len(txt) > 45 and not txt.startswith(("X =", "Donde:", "Fórmula", "Fuente:")):
                p.paragraph_format.first_line_indent = Inches(0.5)
            else:
                p.paragraph_format.first_line_indent = Inches(0)
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.5
            if re.search(r"\*[^\*]+\*", txt):
                p.text = ""
                for part in re.split(r"(\*[^\*]+\*)", txt):
                    if not part:
                        continue
                    is_it = part.startswith("*") and part.endswith("*") and len(part) > 2
                    r = p.add_run(part[1:-1] if is_it else part)
                    set_run_font(r, BODY_FONT, 12, bold=False, italic=is_it, color_rgb=BLACK_RGB)
            else:
                for r in p.runs:
                    is_c = r.font.name in ("Consolas", "Courier New")
                    set_run_font(r, CODE_FONT if is_c else BODY_FONT, 10 if is_c else 12, bold=r.font.bold, italic=r.font.italic, color_rgb=BLACK_RGB)


def format_docx_apa7(
    docx_path,
    running_head="EVALUACIÓN DE CALIDAD ISO/IEC 25010 — LEOFIT SOLUTIONS",
    rebuild_cover=False,
    title="",
    subtitle="",
    doc_code="INF-UTP"
):
    """Función principal para aplicar formato APA 7ma Edición a un archivo .docx existente."""
    doc = docx.Document(docx_path)
    apply_apa7_margins_and_styles(doc)
    if rebuild_cover and title:
        build_formal_apa7_cover(doc, title=title, subtitle=subtitle, doc_code=doc_code)
    setup_apa7_running_head(doc, running_head_text=running_head)
    polish_apa7_paragraphs_and_captions(doc, has_custom_cover=True)
    format_all_tables_apa7(doc)
    doc.save(docx_path)
    return len(doc.paragraphs), len(doc.tables)


if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DOCS_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")

    # 1. Formatear 02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx bajo APA 7ma Edición completa
    p_s14 = os.path.join(DOCS_DIR, "02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx")
    if os.path.exists(p_s14):
        np, nt = format_docx_apa7(
            p_s14,
            running_head="CONTINUACIÓN SEMANAS 14 Y 15: CALIDAD ISO/IEC 25010 — LEOFIT",
            rebuild_cover=True,
            title="INFORME ACUMULATIVO DEL PROYECTO INTEGRADOR: CONTINUACIÓN SEMANAS 14 Y 15",
            subtitle="Evaluación Cuantitativa de Rendimiento, Flexibilidad y Mantenibilidad bajo ISO/IEC 25010:2023 para el Sistema Multicanal LeoFit",
            doc_code="INF-S14-S15"
        )
        print(f"[APA 7 OK] 02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx ({np} párrafos, {nt} tablas)")

    # 2. Formatear 01_INFORME_FINAL_LEOFIT.docx bajo APA 7ma Edición (sin reconstruir su portada de libro, aplicando tablas APA 7, sangría francesa en referencias y estilos)
    p_fin = os.path.join(DOCS_DIR, "01_INFORME_FINAL_LEOFIT.docx")
    if os.path.exists(p_fin):
        np, nt = format_docx_apa7(
            p_fin,
            running_head="INFORME TÉCNICO FINAL DE INGENIERÍA DE SOFTWARE — LEOFIT",
            rebuild_cover=False
        )
        print(f"[APA 7 OK] 01_INFORME_FINAL_LEOFIT.docx ({np} párrafos, {nt} tablas)")

    # 3. Formatear 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx bajo APA 7ma Edición
    p_hoja = os.path.join(DOCS_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx")
    if os.path.exists(p_hoja):
        np, nt = format_docx_apa7(
            p_hoja,
            running_head="HOJA OFICIAL DE ENTREGA Y CREDENCIALES — LEOFIT GRUPO 01",
            rebuild_cover=False
        )
        print(f"[APA 7 OK] 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx ({np} párrafos, {nt} tablas)")
