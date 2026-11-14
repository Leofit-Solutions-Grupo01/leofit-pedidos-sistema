# -*- coding: utf-8 -*-
"""
Generador de Documento Word y PDF: Métricas de Funcionalidad y Métricas de Pruebas
Curso: Calidad de Software (UTP - Sesión 28)
Estudiante: Lady Luz Loayza Rodríguez (U22221489)
Proyecto: Sistema Web de Gestión de Pedidos y Facturación Electrónica - LeoFit
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:left w:val="none"/>'
                        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:right w:val="none"/>'
                        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
                        f'<w:insideV w:val="none"/>'
                        f'</w:tblBorders>')
    tblPr.append(borders)

def build_document():
    doc = docx.Document()
    
    # Configuración de márgenes: 0.65 in para optimizar el espacio exacto de 2 páginas
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)
        
        # Encabezado
        header = section.header
        p_hdr = header.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r_hdr = p_hdr.add_run("UNIVERSIDAD TECNOLÓGICA DEL PERÚ | CALIDAD DE SOFTWARE - SESIÓN 28")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8)
        r_hdr.font.color.rgb = RGBColor(120, 120, 120)

    # Colores institucionales
    COLOR_PRIMARY = RGBColor(183, 28, 28)    # Rojo / Guinda UTP (#B71C1C)
    COLOR_NAVY = RGBColor(26, 54, 93)        # Azul Marino Técnico (#1A365D)
    COLOR_DARK = RGBColor(33, 37, 41)        # Texto principal (#212529)
    COLOR_MUTED = RGBColor(108, 117, 125)    # Gris secundario

    # ==========================================
    # PÁGINA 1: ENCABEZADO + INTRO + 4 MÉTRICAS DE FUNCIONALIDAD
    # ==========================================

    # 1. TABLA ENCABEZADO FORMAL
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = header_table.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Borde izquierdo rojo UTP grueso
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
                        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="B71C1C"/>'
                        f'<w:top w:val="none"/>'
                        f'<w:bottom w:val="none"/>'
                        f'<w:right w:val="none"/>'
                        f'</w:tcBorders>')
    tcPr.append(borders)

    p0 = cell.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.line_spacing = 1.05
    r_sub = p0.add_run("UNIVERSIDAD TECNOLÓGICA DEL PERÚ (UTP) — FACULTAD DE INGENIERÍA\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = COLOR_NAVY
    
    r_tit = p0.add_run("TALLER: 4 MÉTRICAS DE FUNCIONALIDAD Y 4 MÉTRICAS DE PRUEBAS DE SOFTWARE\n")
    r_tit.font.name = "Calibri"
    r_tit.font.size = Pt(12)
    r_tit.font.bold = True
    r_tit.font.color.rgb = COLOR_PRIMARY

    p1 = cell.add_paragraph()
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.05
    
    r_meta = p1.add_run(
        "• Asignatura: Calidad de Software (Unidad 05: Técnicas de Prueba de Errores - Sesión 28)\n"
        "• Proyecto: Sistema Web de Gestión de Pedidos y Facturación Electrónica (LeoFit)\n"
        "• Alumna: Loayza Rodríguez, Lady Luz   |   Código UTP: U22221489"
    )
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = COLOR_DARK

    # Introducción Contextual
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(5)
    p_intro.paragraph_format.space_after = Pt(4)
    p_intro.paragraph_format.line_spacing = 1.05
    r_in_b = p_intro.add_run("Marco de Referencia y Proyecto: ")
    r_in_b.font.name = "Calibri"
    r_in_b.font.size = Pt(9)
    r_in_b.font.bold = True
    r_in_b.font.color.rgb = COLOR_NAVY
    r_in_t = p_intro.add_run(
        "Siguiendo el temario de la Sesión 28 (estándar IEEE 830, pesos de realización, interacción de usuario e ISO/IEC 25010), "
        "se definen 4 métricas de funcionalidad y 4 métricas de prueba cuantificadas en el sistema de producción LeoFit "
        "(React 19, TypeScript/Node.js Express, PostgreSQL 16 ACID, Facturación SUNAT y Pasarela Culqi)."
    )
    r_in_t.font.name = "Calibri"
    r_in_t.font.size = Pt(9)
    r_in_t.font.color.rgb = COLOR_DARK

    # Título Sección 1
    p_s1 = doc.add_paragraph()
    p_s1.paragraph_format.space_before = Pt(4)
    p_s1.paragraph_format.space_after = Pt(3)
    r_s1 = p_s1.add_run("I. CUATRO (4) MÉTRICAS DE FUNCIONALIDAD DEL SOFTWARE (SESIÓN 28)")
    r_s1.font.name = "Calibri"
    r_s1.font.size = Pt(10.5)
    r_s1.font.bold = True
    r_s1.font.color.rgb = COLOR_PRIMARY

    # Tabla para Métricas de Funcionalidad
    t_func = doc.add_table(rows=5, cols=4)
    t_func.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_func, color="CCCCCC", sz="4")

    col_widths = [Inches(1.85), Inches(2.25), Inches(1.3), Inches(1.7)]
    
    headers_f = [
        "Métrica y Objetivo",
        "Fórmula de Cálculo y Parámetros",
        "Criterio / Umbral",
        "Resultado Real (LeoFit)"
    ]

    for j, h in enumerate(headers_f):
        c = t_func.cell(0, j)
        c.width = col_widths[j]
        set_cell_background(c, "1A365D") # Navy
        set_cell_margins(c, top=70, bottom=70, left=90, right=90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_func = [
        (
            "MF-01: Métrica de Éxito de Funcionalidades (MEF)\n"
            "Objetivo: Evaluar el grado de completitud de los módulos según los pesos formales de la Sesión 28 (Slide 20).",
            "MEF = [ Σ (Peso_i × Func_i) / Total_Func ] × 100%\n\n"
            "• Peso 0: Funcionalidad no realizada\n"
            "• Peso 0.5: Funcionalidad a medio realizar\n"
            "• Peso 1.0: Funcionalidad realizada y operativa",
            "Óptimo: ≥ 95%\n"
            "Aceptable: ≥ 85%\n"
            "Crítico: < 75%",
            "100.0% de Éxito\n"
            "(14 de 14 funcionalidades completas con peso 1.0: Auth, RBAC, Catálogo, Pedidos, ACID, Boletas, Pagos Culqi, Reportes)."
        ),
        (
            "MF-02: Índice de Funcionalidad Estructural vs Servidor (IFS)\n"
            "Objetivo: Medir la proporción de lógica funcional operativa frente a capas estructurales de interfaz (Slide 19).",
            "IFS = [ N_func / (N_func + N_estruc) ] × 100%\n\n"
            "• N_func: Controladores, servicios y repositorios backend (TS/Node)\n"
            "• N_estruc: Vistas, HTML y layouts UI",
            "Balanceado:\n60% a 75%\n(Refleja robustez de backend)",
            "70.0% de Lógica\n"
            "(42 archivos funcionales de servidor vs 18 archivos estructurales UI. Alta densidad de reglas de negocio)."
        ),
        (
            "MF-03: Latencia Operativa de Acceso Rápido (LOAR)\n"
            "Objetivo: Verificar cumplimiento de tiempos de respuesta de interacción (Lafuente, 2000 adaptado a SLAs de API).",
            "LOAR_p95 = Tiempo de respuesta percentil 95 en ejecución de transacciones de negocio.\n"
            "Medido con carga concurrente de 50 VUs.",
            "Visual: ≤ 1.5 s\n"
            "API Crítica: ≤ 500 ms\n"
            "Límite Humano: < 5.0 s",
            "p95 = 215 ms (Óptimo)\n"
            "• Carga catálogo: 180 ms\n"
            "• Checkout pedido: 215 ms\n"
            "• Webhook Culqi: 145 ms\n"
            "(100% transacciones < 1 s)."
        ),
        (
            "MF-04: Grado de Validación de Requisitos IEEE 830 (GVR)\n"
            "Objetivo: Determinar si las especificaciones de requerimientos funcionales son no ambiguas, trazables y verificadas.",
            "GVR = [ RF_validados / RF_especificados ] × 100%\n\n"
            "• RF_validados: Requerimientos con casos de prueba funcionales aprobados\n"
            "• RF_especificados: 14 RF formales",
            "Requerido: 100%\n(Cero omisiones de alcance)",
            "100.0% de Validación\n"
            "(14/14 RFs cubiertos con casos de prueba funcionales CP-F01 al CP-F14 en matriz de trazabilidad)."
        )
    ]

    for i, row in enumerate(data_func):
        bg = "FFFFFF" if i % 2 == 0 else "F8F9FA"
        for j, text in enumerate(row):
            c = t_func.cell(i + 1, j)
            c.width = col_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=55, bottom=55, left=85, right=85)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else (WD_ALIGN_PARAGRAPH.CENTER if j == 2 else WD_ALIGN_PARAGRAPH.LEFT)
            
            lines = text.split("\n")
            for idx, line in enumerate(lines):
                if idx > 0:
                    p = c.add_paragraph()
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.05
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else (WD_ALIGN_PARAGRAPH.CENTER if j == 2 else WD_ALIGN_PARAGRAPH.LEFT)
                
                r = p.add_run(line)
                r.font.name = "Calibri"
                r.font.size = Pt(8)
                if idx == 0 and ("MF-" in line or "100" in line or "p95" in line or "70" in line):
                    r.font.bold = True
                    r.font.color.rgb = COLOR_NAVY if "MF-" in line else COLOR_PRIMARY
                else:
                    r.font.color.rgb = COLOR_DARK

    # ==========================================
    # SALTO DE PÁGINA EXACTO -> PÁGINA 2
    # ==========================================
    doc.add_page_break()

    # ==========================================
    # PÁGINA 2: 4 MÉTRICAS DE PRUEBAS + SÍNTESIS + FIRMA
    # ==========================================

    p_s2 = doc.add_paragraph()
    p_s2.paragraph_format.space_before = Pt(0)
    p_s2.paragraph_format.space_after = Pt(3)
    r_s2 = p_s2.add_run("II. CUATRO (4) MÉTRICAS PARA PRUEBAS DE SOFTWARE (SESIÓN 28 - SLIDE 22)")
    r_s2.font.name = "Calibri"
    r_s2.font.size = Pt(10.5)
    r_s2.font.bold = True
    r_s2.font.color.rgb = COLOR_PRIMARY

    # Tabla para Métricas de Pruebas
    t_test = doc.add_table(rows=5, cols=4)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_test, color="CCCCCC", sz="4")

    for j, h in enumerate(headers_f):
        c = t_test.cell(0, j)
        c.width = col_widths[j]
        set_cell_background(c, "1A365D") # Navy
        set_cell_margins(c, top=70, bottom=70, left=90, right=90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_test = [
        (
            "MP-01: Exhaustividad de las Pruebas (EP)\n"
            "Objetivo: Evaluar la completitud de la suite de verificación automatizada ejecutada respecto a lo planificado (Slide 22).",
            "EP = [ CP_ejecutados / CP_planificados ] × 100%\n\n"
            "• CP_ejecutados: Casos de prueba automatizados ejecutados en Jest\n"
            "• CP_planificados: 122 casos del Plan QA",
            "Meta: ≥ 98%\nMínimo: ≥ 90%",
            "99.18% de Exhaustividad\n"
            "(121 pruebas ejecutadas y aprobadas en CI/CD; 1 prueba de integración aislada para entorno live)."
        ),
        (
            "MP-02: Densidad de Defectos por KLOC (DD)\n"
            "Objetivo: Cuantificar la tasa de fallos por cada mil líneas de código fuente, midiendo la calidad intrínseca del software.",
            "DD = Total_Defectos_Detectados / (Líneas_Código / 1000)\n\n"
            "• Defectos detectados en etapa de pruebas: 4\n"
            "• KLOC del sistema (TypeScript backend/frontend): 8.5 KLOC",
            "Excelente: < 1.0 def/KLOC\n"
            "Bueno: 1.0 - 3.0\n"
            "Deficiente: > 5.0",
            "0.47 defectos / KLOC\n"
            "(Nivel de madurez de clase industrial. Todos los 4 hallazgos fueron corregidos antes de cierre)."
        ),
        (
            "MP-03: Control de Pruebas Unitarias (CPU)\n"
            "Objetivo: Medir la efectividad y estabilidad de las pruebas unitarias y de integración de componentes aislados (Slide 22).",
            "CPU = [ Pruebas_Aprobadas (Pass) / Total_Pruebas_Ejecutadas ] × 100%\n\n"
            "• Valida: JWT fail-fast, HMAC webhook, RBAC roles, bloqueo pesimista ACID y stock.",
            "Obligatorio: 100%\n(Cero tolerancia a pruebas fallidas)",
            "100.0% Pass Rate\n"
            "(121/121 pruebas ejecutadas pasaron exitosamente en 8.57 segundos en consola de Jest)."
        ),
        (
            "MP-04: Índice de Madurez del Software (SMI)\n"
            "Objetivo: Medir la estabilidad y convergencia del código ante modificaciones y refactorizaciones (Software Maturity Index).",
            "SMI = [ M_T - (F_a + F_c + F_d) ] / M_T\n\n"
            "• M_T: Módulos/funciones actuales (45)\n"
            "• F_a: Añadidos (3), F_c: Modificados (2)\n"
            "• F_d: Eliminados (0)",
            "Estable: SMI ≥ 0.85\n"
            "En evolución: 0.60 - 0.84\n"
            "Inestable: < 0.60",
            "SMI = 0.889 (88.9%)\n"
            "(Alta madurez. Indica que el software se encuentra estabilizado y listo para fase de producción)."
        )
    ]

    for i, row in enumerate(data_test):
        bg = "FFFFFF" if i % 2 == 0 else "F8F9FA"
        for j, text in enumerate(row):
            c = t_test.cell(i + 1, j)
            c.width = col_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=55, bottom=55, left=85, right=85)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else (WD_ALIGN_PARAGRAPH.CENTER if j == 2 else WD_ALIGN_PARAGRAPH.LEFT)
            
            lines = text.split("\n")
            for idx, line in enumerate(lines):
                if idx > 0:
                    p = c.add_paragraph()
                    p.paragraph_format.space_before = Pt(1)
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.line_spacing = 1.05
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT if j < 2 else (WD_ALIGN_PARAGRAPH.CENTER if j == 2 else WD_ALIGN_PARAGRAPH.LEFT)
                
                r = p.add_run(line)
                r.font.name = "Calibri"
                r.font.size = Pt(8)
                if idx == 0 and ("MP-" in line or "100" in line or "99" in line or "0.47" in line or "SMI" in line):
                    r.font.bold = True
                    r.font.color.rgb = COLOR_NAVY if "MP-" in line else COLOR_PRIMARY
                else:
                    r.font.color.rgb = COLOR_DARK

    # 3. SÍNTESIS Y DICTAMEN DE CALIDAD
    p_s3 = doc.add_paragraph()
    p_s3.paragraph_format.space_before = Pt(6)
    p_s3.paragraph_format.space_after = Pt(2)
    r_s3 = p_s3.add_run("III. CUADRO RESUMEN Y DICTAMEN DE CALIDAD DEL SISTEMA LEOFIT")
    r_s3.font.name = "Calibri"
    r_s3.font.size = Pt(10)
    r_s3.font.bold = True
    r_s3.font.color.rgb = COLOR_PRIMARY

    # Tabla resumen compacta
    t_sum = doc.add_table(rows=3, cols=5)
    t_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sum, color="CCCCCC", sz="4")

    sum_widths = [Inches(1.2), Inches(1.5), Inches(1.5), Inches(1.4), Inches(1.4)]
    
    headers_s = ["Dimensión", "Métrica Principal", "Valor Obtenido", "Umbral Exigido", "Estado / Dictamen"]
    for j, h in enumerate(headers_s):
        c = t_sum.cell(0, j)
        c.width = sum_widths[j]
        set_cell_background(c, "2B6CB0") # Azul acero
        set_cell_margins(c, top=50, bottom=50, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_sum = [
        ("Funcionalidad", "Éxito Funcional (MEF)\nLatencia p95 (LOAR)", "100.0% completitud\n215 ms latencia API", "≥ 95% éxito\n< 500 ms latencia", "CONFORME (Excelente)"),
        ("Pruebas / QA", "Control Unitario (CPU)\nDensidad Defectos (DD)", "100.0% Pass (121/121)\n0.47 def / KLOC", "100% aprobadas\n< 1.0 def / KLOC", "CONFORME (Excelente)")
    ]

    for i, row in enumerate(data_sum):
        for j, text in enumerate(row):
            c = t_sum.cell(i + 1, j)
            c.width = sum_widths[j]
            set_cell_background(c, "FFFFFF" if i == 0 else "F8F9FA")
            set_cell_margins(c, top=45, bottom=45, left=70, right=70)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [0, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if j == 4:
                r.font.bold = True
                r.font.color.rgb = RGBColor(40, 167, 69) # Verde éxito
            elif j == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
            else:
                r.font.color.rgb = COLOR_DARK

    # Pie de firma breve
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(5)
    p_sign.paragraph_format.space_after = Pt(0)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run("Elaborado por: Loayza Rodríguez, Lady Luz   |   Código UTP: U22221489")
    r_sign.font.name = "Calibri"
    r_sign.font.size = Pt(8.5)
    r_sign.font.italic = True
    r_sign.font.color.rgb = COLOR_MUTED

    # Guardar documento
    out_dir = "docs/02_CALIDAD_Y_AUDITORIA/METRICAS_SESION_28_UTP"
    os.makedirs(out_dir, exist_ok=True)
    docx_path = os.path.join(out_dir, "METRICAS_FUNCIONALIDAD_Y_PRUEBAS_LOAYZA_U22221489.docx")
    doc.save(docx_path)
    print(f"Documento Word generado exitosamente en: {docx_path}")
    return docx_path

if __name__ == "__main__":
    build_document()
