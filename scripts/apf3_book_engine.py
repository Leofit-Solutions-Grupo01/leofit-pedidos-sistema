"""
Motor de maquetación del Informe Final APF3 (formato libro).

Genera un DOCX con estilos de título reales (Heading 1/2/3) para que Word construya
automáticamente el índice general, el índice de figuras y el índice de tablas;
portada, secciones con numeración romana/arabiga, encabezados con STYLEREF y pie de página.
"""
import os
import re
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

NAVY = RGBColor(0x0F, 0x2A, 0x43)
TEAL = RGBColor(0x0E, 0x74, 0x90)
INK = RGBColor(0x1E, 0x29, 0x3B)
GREY = RGBColor(0x64, 0x74, 0x8B)

BODY_FONT = "Cambria"
HEAD_FONT = "Calibri"
CODE_FONT = "Consolas"


def _rfonts(style_or_run_element, name):
    rpr = style_or_run_element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.append(rf)
    for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rf.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rf.get(qn(a)) is not None:
            del rf.attrib[qn(a)]


def shade(cell_or_par_pr, hex_fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    cell_or_par_pr.append(shd)


def cell_bg(cell, hex_fill):
    shade(cell._tc.get_or_add_tcPr(), hex_fill)


def cell_margins(table, top=50, bottom=50, left=90, right=90):
    tblPr = table._tbl.tblPr
    m = OxmlElement("w:tblCellMar")
    for k, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        e = OxmlElement(f"w:{k}")
        e.set(qn("w:w"), str(v))
        e.set(qn("w:type"), "dxa")
        m.append(e)
    tblPr.append(m)


def table_borders(table, color="B6C4D1", sz=4):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for k in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{k}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), str(sz))
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), color)
        b.append(e)
    tblPr.append(b)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:tblHeader")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def no_split(row):
    trPr = row._tr.get_or_add_trPr()
    e = OxmlElement("w:cantSplit")
    e.set(qn("w:val"), "true")
    trPr.append(e)


def add_field(paragraph, instr, placeholder="", bold=None, size=None, color=None):
    """Campo complejo (begin / instr / separate / resultado / end)."""
    def mk(kind):
        r = paragraph.add_run()
        fc = OxmlElement("w:fldChar")
        fc.set(qn("w:fldCharType"), kind)
        r._r.append(fc)
        return r
    mk("begin")
    r = paragraph.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = f" {instr} "
    r._r.append(it)
    mk("separate")
    res = paragraph.add_run(placeholder)
    for run in (res,):
        if bold is not None:
            run.bold = bold
        if size:
            run.font.size = Pt(size)
        if color:
            run.font.color.rgb = color
    mk("end")
    return res


def para_border(paragraph, side="bottom", color="0E7490", sz=8, space=4):
    pPr = paragraph._p.get_or_add_pPr()
    pb = pPr.find(qn("w:pBdr"))
    if pb is None:
        pb = OxmlElement("w:pBdr")
        pPr.append(pb)
    e = OxmlElement(f"w:{side}")
    e.set(qn("w:val"), "single")
    e.set(qn("w:sz"), str(sz))
    e.set(qn("w:space"), str(space))
    e.set(qn("w:color"), color)
    pb.append(e)


class Book:
    def __init__(self, root):
        self.root = root
        self.doc = Document()
        self.fig_n = 0
        self.tab_n = 0
        self.chap_n = 0
        self.sec_n = 0
        self._setup_page()
        self._setup_styles()

    # ------------------------------------------------------------------ setup
    def _setup_page(self):
        s = self.doc.sections[0]
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.5)
        s.top_margin, s.bottom_margin = Cm(2.4), Cm(2.3)
        s.header_distance = Cm(1.1)
        s.footer_distance = Cm(1.0)

    def _setup_styles(self):
        st = self.doc.styles
        n = st["Normal"]
        n.font.name = BODY_FONT
        n.font.size = Pt(11)
        n.font.color.rgb = INK
        _rfonts(n.element, BODY_FONT)
        n.paragraph_format.space_after = Pt(7)
        n.paragraph_format.line_spacing = 1.25
        cfg = {
            "Heading 1": (24, NAVY, 0, 18),
            "Heading 2": (19, NAVY, 0, 14),
            "Heading 3": (14, TEAL, 16, 6),
            "Heading 4": (11.5, NAVY, 10, 4),
        }
        for name, (sz, col, before, after) in cfg.items():
            h = st[name]
            h.font.name = HEAD_FONT
            h.font.size = Pt(sz)
            h.font.bold = True
            h.font.italic = False
            h.font.color.rgb = col
            _rfonts(h.element, HEAD_FONT)
            h.paragraph_format.space_before = Pt(before)
            h.paragraph_format.space_after = Pt(after)
            h.paragraph_format.keep_with_next = True
            h.paragraph_format.line_spacing = 1.1
        cap = st["Caption"]
        cap.font.name = HEAD_FONT
        cap.font.size = Pt(9.5)
        cap.font.bold = False
        cap.font.italic = False
        cap.font.color.rgb = GREY
        _rfonts(cap.element, HEAD_FONT)
        cap.paragraph_format.space_after = Pt(10)
        for name in ("List Bullet", "List Number"):
            s_ = st[name]
            s_.font.name = BODY_FONT
            s_.font.size = Pt(11)
            _rfonts(s_.element, BODY_FONT)
            s_.paragraph_format.space_after = Pt(3)
            s_.paragraph_format.line_spacing = 1.2
        for name in ("TOC 1", "TOC 2", "TOC 3", "Table of Figures"):
            try:
                t = st[name]
            except KeyError:
                from docx.enum.style import WD_STYLE_TYPE
                t = st.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
                t.base_style = st["Normal"]
            t.font.name = HEAD_FONT
            _rfonts(t.element, HEAD_FONT)
            t.paragraph_format.space_after = Pt(3)
            t.paragraph_format.line_spacing = 1.1
        st["TOC 1"].font.bold = True
        st["TOC 1"].font.size = Pt(11.5)
        st["TOC 1"].font.color.rgb = NAVY
        st["TOC 1"].paragraph_format.space_before = Pt(10)
        st["TOC 2"].font.size = Pt(10.5)
        st["TOC 2"].paragraph_format.left_indent = Cm(0.5)
        st["TOC 3"].font.size = Pt(9.5)
        st["TOC 3"].paragraph_format.left_indent = Cm(1.2)
        st["Table of Figures"].font.size = Pt(10)

    # ------------------------------------------------------------------ texto
    def _inline(self, p, text, size=None, color=None, bold_all=False):
        parts = re.split(r"(\*\*.+?\*\*|`.+?`|_\_.+?_\_)", text)
        for part in parts:
            if not part:
                continue
            if part.startswith("**") and part.endswith("**"):
                r = p.add_run(part[2:-2])
                r.bold = True
            elif part.startswith("`") and part.endswith("`"):
                r = p.add_run(part[1:-1])
                r.font.name = CODE_FONT
                _rfonts(r._r, CODE_FONT)
                r.font.size = Pt((size or 11) - 1.5)
                r.font.color.rgb = RGBColor(0x0B, 0x5C, 0x73)
                continue
            else:
                r = p.add_run(part)
                if bold_all:
                    r.bold = True
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = color
        return p

    def p(self, text, align="justify", size=None, italic=False, after=None, indent=None):
        par = self.doc.add_paragraph()
        self._inline(par, text, size=size)
        par.alignment = {"justify": WD_ALIGN_PARAGRAPH.JUSTIFY, "left": WD_ALIGN_PARAGRAPH.LEFT,
                         "center": WD_ALIGN_PARAGRAPH.CENTER}[align]
        if italic:
            for r in par.runs:
                r.italic = True
        if after is not None:
            par.paragraph_format.space_after = Pt(after)
        if indent:
            par.paragraph_format.left_indent = Cm(indent)
        return par

    def bullets(self, items):
        for it in items:
            par = self.doc.add_paragraph(style="List Bullet")
            self._inline(par, it)
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
        self.doc.paragraphs[-1].paragraph_format.space_after = Pt(8)

    def numbered(self, items):
        for i, it in enumerate(items, 1):
            par = self.doc.add_paragraph()
            par.paragraph_format.left_indent = Cm(0.9)
            par.paragraph_format.first_line_indent = Cm(-0.6)
            par.paragraph_format.space_after = Pt(3)
            r = par.add_run(f"{i}.  ")
            r.bold = True
            r.font.color.rgb = TEAL
            self._inline(par, it)
        self.doc.paragraphs[-1].paragraph_format.space_after = Pt(8)

    # ------------------------------------------------------------------ títulos
    def part(self, title, intro=None):
        h = self.doc.add_heading(title, level=1)
        h.paragraph_format.page_break_before = True
        h.paragraph_format.space_before = Pt(120)
        para_border(h, "bottom", "06B6D4", 18, 8)
        if intro:
            par = self.p(intro, italic=True)
            par.paragraph_format.space_before = Pt(14)
        return h

    def front(self, title, page_break=True):
        h = self.doc.add_heading(title, level=1)
        h.paragraph_format.page_break_before = page_break
        h.paragraph_format.space_before = Pt(0)
        para_border(h, "bottom", "06B6D4", 12, 6)
        return h

    def chapter(self, title):
        self.chap_n += 1
        self.sec_n = 0
        h = self.doc.add_heading(f"{self.chap_n}. {title}", level=2)
        h.paragraph_format.page_break_before = True
        h.paragraph_format.space_before = Pt(0)
        para_border(h, "bottom", "0E7490", 8, 6)
        return h

    def annex(self, letter, title):
        h = self.doc.add_heading(f"Anexo {letter}. {title}", level=2)
        h.paragraph_format.page_break_before = True
        h.paragraph_format.space_before = Pt(0)
        para_border(h, "bottom", "0E7490", 8, 6)
        self.sec_n = 0
        self.annex_letter = letter
        return h

    def sec(self, title, annex=False):
        self.sec_n += 1
        label = f"{getattr(self, 'annex_letter', '')}.{self.sec_n}" if annex else f"{self.chap_n}.{self.sec_n}"
        return self.doc.add_heading(f"{label}  {title}", level=3)

    def sub(self, title):
        return self.doc.add_heading(title, level=4)

    # ------------------------------------------------------------------ captions
    def _caption(self, label, n, text, before=False):
        cp = self.doc.add_paragraph(style="Caption")
        r = cp.add_run(f"{label} ")
        r.bold = True
        r.font.color.rgb = NAVY
        res = add_field(cp, f"SEQ {label} \\* ARABIC", str(n), bold=True, color=NAVY)
        r2 = cp.add_run(f". {text}")
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if before:
            cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            cp.paragraph_format.keep_with_next = True
            cp.paragraph_format.space_before = Pt(8)
            cp.paragraph_format.space_after = Pt(4)
        return cp

    # ------------------------------------------------------------------ figuras
    def fig(self, rel_path, caption, width_cm=15.0):
        path = rel_path if os.path.isabs(rel_path) else os.path.join(self.root, rel_path)
        if not os.path.exists(path):
            raise FileNotFoundError(path)
        self.fig_n += 1
        par = self.doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.paragraph_format.keep_with_next = True
        par.paragraph_format.space_before = Pt(6)
        par.paragraph_format.space_after = Pt(3)
        par.add_run().add_picture(path, width=Cm(width_cm))
        self._caption("Figura", self.fig_n, caption)

    # ------------------------------------------------------------------ tablas
    def table(self, headers, rows, caption, widths=None, size=8.5, align=None):
        self.tab_n += 1
        self._caption("Tabla", self.tab_n, caption, before=True)
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        table_borders(t)
        cell_margins(t)
        total = 16.0
        if widths is None:
            widths = [total / len(headers)] * len(headers)
        else:
            k = total / sum(widths)
            widths = [w * k for w in widths]
        for i, h in enumerate(headers):
            c = t.rows[0].cells[i]
            c.width = Cm(widths[i])
            cell_bg(c, "0F2A43")
            c.paragraphs[0].paragraph_format.space_after = Pt(0)
            r = c.paragraphs[0].add_run(h)
            r.bold = True
            r.font.size = Pt(size)
            r.font.name = HEAD_FONT
            r.font.color.rgb = RGBColor(255, 255, 255)
        repeat_header(t.rows[0])
        for ri, row in enumerate(rows):
            cells = t.add_row().cells
            no_split(t.rows[-1])
            for i, val in enumerate(row):
                c = cells[i]
                c.width = Cm(widths[i])
                if ri % 2 == 1:
                    cell_bg(c, "EEF5F8")
                par = c.paragraphs[0]
                par.paragraph_format.space_after = Pt(0)
                par.paragraph_format.line_spacing = 1.1
                if align and align[i] == "c":
                    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
                self._inline(par, str(val), size=size)
                for r in par.runs:
                    if r.font.name != CODE_FONT:
                        r.font.name = HEAD_FONT
                        _rfonts(r._r, HEAD_FONT)
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)
        return t

    # ------------------------------------------------------------------ código
    def code(self, text, caption=None, size=7.5):
        if caption:
            self.tab_n += 1
            self._caption("Tabla", self.tab_n, caption, before=True)
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        table_borders(t, "CBD5E1", 4)
        cell_margins(t, 80, 80, 140, 140)
        c = t.rows[0].cells[0]
        c.width = Cm(16)
        cell_bg(c, "F1F5F9")
        lines = text.strip("\n").split("\n")
        for i, ln in enumerate(lines):
            par = c.paragraphs[0] if i == 0 else c.add_paragraph()
            par.paragraph_format.space_after = Pt(0)
            par.paragraph_format.line_spacing = 1.0
            r = par.add_run(ln if ln else " ")
            r.font.name = CODE_FONT
            _rfonts(r._r, CODE_FONT)
            r.font.size = Pt(size)
            r.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)

    def note(self, title, text, kind="info"):
        fills = {"info": ("E6F6FA", "06B6D4"), "warn": ("FEF3C7", "F59E0B"), "ok": ("DCFCE7", "16A34A")}
        fill, edge = fills[kind]
        t = self.doc.add_table(rows=1, cols=1)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell_margins(t, 90, 90, 160, 160)
        tblPr = t._tbl.tblPr
        b = OxmlElement("w:tblBorders")
        e = OxmlElement("w:left")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "30")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), edge)
        b.append(e)
        tblPr.append(b)
        c = t.rows[0].cells[0]
        c.width = Cm(16)
        cell_bg(c, fill)
        par = c.paragraphs[0]
        par.paragraph_format.space_after = Pt(3)
        r = par.add_run(title)
        r.bold = True
        r.font.name = HEAD_FONT
        r.font.size = Pt(10)
        r.font.color.rgb = NAVY
        p2 = c.add_paragraph()
        p2.paragraph_format.space_after = Pt(0)
        p2.paragraph_format.line_spacing = 1.15
        self._inline(p2, text, size=10)
        sp = self.doc.add_paragraph()
        sp.paragraph_format.space_after = Pt(6)

    def page_break(self):
        self.doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    # ------------------------------------------------------------------ índices
    def toc_block(self, title, instr, placeholder, page_break=True):
        h = self.doc.add_paragraph()
        h.paragraph_format.page_break_before = page_break
        r = h.add_run(title)
        r.bold = True
        r.font.size = Pt(24)
        r.font.name = HEAD_FONT
        r.font.color.rgb = NAVY
        para_border(h, "bottom", "06B6D4", 12, 6)
        h.paragraph_format.space_after = Pt(14)
        par = self.doc.add_paragraph()
        add_field(par, instr, placeholder)

    # ------------------------------------------------------------------ secciones / pie
    def _pgnum(self, section, fmt, start=None):
        sp = section._sectPr
        pg = sp.find(qn("w:pgNumType"))
        if pg is None:
            pg = OxmlElement("w:pgNumType")
            sp.append(pg)
        pg.set(qn("w:fmt"), fmt)
        if start is not None:
            pg.set(qn("w:start"), str(start))

    def _header_footer(self, section, running_head=True, header_text="LeoFit · Informe Final APF3"):
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False
        hp = section.header.paragraphs[0]
        for r in list(hp.runs):
            r._r.getparent().remove(r._r)
        if running_head:
            r = hp.add_run(header_text + "\t")
            r.font.size = Pt(8.5)
            r.font.name = HEAD_FONT
            r.font.color.rgb = GREY
            add_field(hp, 'STYLEREF "Heading 2"', "", size=8.5, color=GREY)
            para_border(hp, "bottom", "B6C4D1", 4, 4)
            hp.paragraph_format.tab_stops.add_tab_stop(Cm(16), alignment=2)
        fp = section.footer.paragraphs[0]
        for r in list(fp.runs):
            r._r.getparent().remove(r._r)
        if running_head:
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_field(fp, "PAGE", "1", size=9.5, color=NAVY)
            fp.runs[-1].bold = True

    def new_section(self, kind="front"):
        """kind: front (romano) | body (arábigo, reinicia en 1)."""
        sec = self.doc.add_section(WD_SECTION.NEW_PAGE)
        if kind == "front":
            self._pgnum(sec, "lowerRoman", 1)
        else:
            self._pgnum(sec, "decimal", 1)
        self._header_footer(sec, running_head=(kind == "body"))
        if kind == "front":
            sec.header.is_linked_to_previous = False
            self._header_footer(sec, running_head=False)
            # pie con número romano
            fp = sec.footer.paragraphs[0]
            fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_field(fp, "PAGE", "i", size=9.5, color=NAVY)
        return sec

    def finish_cover_section(self):
        s0 = self.doc.sections[0]
        self._header_footer(s0, running_head=False)

    def save(self, path):
        self.doc.save(path)
