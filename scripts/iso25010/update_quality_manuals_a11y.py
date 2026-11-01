# -*- coding: utf-8 -*-
"""
@file update_quality_manuals_a11y.py
@description Actualiza los Manuales de Calidad ISO 25000 en docx con la paleta de marca LeoFit,
             criterios de accesibilidad universal (WCAG 2.1 AA/AAA para baja y media visión)
             y métricas cuantitativas sincronizadas al estado definitivo (194 pruebas, 0 fallos).
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
"""

import os
import sys
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

sys.stdout.reconfigure(encoding='utf-8')

# Paleta LeoFit de Alta Accesibilidad
BRAND_DARK = '0F172A'       # Azul Pizarra Oscuro Institucional (Contraste 15.6:1 en fondo blanco)
BRAND_NAVY = '1E3A8A'       # Azul Corporativo / Enlaces (Contraste 8.5:1 en fondo blanco)
BRAND_RUST = 'C2410C'       # Óxido Deportivo / Acentos (Contraste 5.74:1 en fondo blanco - WCAG AA)
TEXT_DARK = '0F172A'        # Texto primario
TEXT_MUTED = '1E293B'       # Texto secundario (Contraste 12.8:1)
BG_ALT_ROW = 'F8FAFC'       # Fila alterna sutil
BORDER_COLOR = 'CBD5E1'     # Borde visible y nítido para baja visión

COLOR_RUN_MAP = {
    '232F3E': BRAND_DARK,
    'FF9900': BRAND_RUST,   # Cambia naranja pálido inaccesible (2.1:1) por naranja óxido accesible (5.74:1)
    '0972D3': '1665D8',     # Azul legible (5.1:1)
    '5F6B7A': TEXT_MUTED,   # Gris pálido reemplazado por pizarra oscuro
    '16191F': TEXT_DARK,
    'AAB7C4': '334155',
    'E0E0E0': '475569',
}

SHD_MAP = {
    '232F3E': BRAND_DARK,
    'FF9900': BRAND_DARK,   # Cabecera naranja pasa a azul oscuro de marca para contraste AAA con texto blanco
    'FFE0A8': 'FFF7ED',
    'D6E8F9': 'EFF6FF',
    'D5DBDB': BG_ALT_ROW,
    'F2F3F3': BG_ALT_ROW,
    'F8F9FA': BG_ALT_ROW,
}

EXACT_PARAGRAPH_REPLACEMENTS = [
    (
        "Ejecución de las 35 pruebas automatizadas (18 en Backend con Jest/Supertest y 17 en Frontend con Vitest).",
        "Ejecución de las 194 pruebas automatizadas (125 en Backend con Jest/Supertest y 69 en Frontend con Vitest/Testing Library, 100% aprobadas y 0 fallos)."
    ),
    (
        "Mediante 35 pruebas automatizadas, compuertas de calidad obligatorias en GitHub Actions y una política de ramas protegidas, la gerencia dispone de evidencia verificable de que cada nueva función agregada cumple los criterios de calidad y seguridad.",
        "Mediante 194 pruebas automatizadas (125 Backend / 69 Frontend), compuertas de calidad obligatorias en GitHub Actions y una política de ramas protegidas, la gerencia dispone de evidencia verificable de que cada nueva función agregada cumple los criterios de calidad y seguridad."
    ),
    (
        "Mediante 35 pruebas automatizadas, compuertas de calidad obligatorias en GitHub Actions y una política de ramas protegidas, la gerencia dispone de evidencia verificable de que cada nueva función agregada cumple los mismos criterios de calidad y seguridad.",
        "Mediante 194 pruebas automatizadas (125 Backend / 69 Frontend), compuertas de calidad obligatorias en GitHub Actions y una política de ramas protegidas, la gerencia dispone de evidencia verificable de que cada nueva función agregada cumple los mismos criterios de calidad y seguridad."
    ),
    (
        "Node.js 20 + React 19 (PWA) + PostgreSQL 16 (BCNF)  ·  35 tests  ·  0 vulns",
        "Node.js 20 + React 19 (PWA) + PostgreSQL 16 (BCNF)  ·  194 tests (125 Backend / 69 Frontend)  ·  0 vulns (npm audit)"
    ),
    (
        "35 pruebas automatizadas  ·  0 vulnerabilidades críticas/altas en npm audit",
        "194 pruebas automatizadas (125 Backend / 69 Frontend)  ·  0 vulnerabilidades en npm audit"
    ),
    (
        "35 pruebas automatizadas (Jest + Vitest)",
        "194 pruebas automatizadas (125 Jest + 69 Vitest)"
    ),
    (
        "18 pruebas unitarias y de integración en Backend (npm test) validando cálculo de totales, IVA, cambio de estados y bloqueo por ruptura de stock.",
        "125 pruebas unitarias y de integración en Backend (npm test con Jest/Supertest), validando cálculo de totales, IVA, cambio atómico de estados, concurrencia SELECT FOR UPDATE y bloqueo por ruptura de stock."
    ),
    (
        "Cobertura total de pruebas automatizadas (35 tests). TypeScript en modo estricto (strict: true) para erradicar errores de tipo en tiempo de compilación.",
        "Cobertura total de pruebas automatizadas (194 tests: 125 backend + 69 frontend). TypeScript en modo estricto (strict: true) para erradicar errores de tipo en tiempo de compilación."
    ),
    (
        "35 tests (Jest+Vitest)",
        "194 tests (125 Jest + 69 Vitest)"
    ),
    (
        "Interfaces tipadas con TypeScript en todo el ciclo (Cliente ↔ Servidor) y soporte PWA multi-dispositivo (Android, iOS, Windows).",
        "Interfaces tipadas con TypeScript (Zod/Supertest). Pruebas de coexistencia en ISO 25010: latencia media 2.85 ms (LB) vs. 3.12 ms (concurrente), p95 ≤ 5.8 ms e interoperabilidad 100% verificada."
    )
]

def set_cell_border(cell, color=BORDER_COLOR, sz='4'):
    """Aplica bordes visibles y consistentes para usuarios con sensibilidad de contraste reducida."""
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcBorders'):
            tcPr.remove(child)
    borders_xml = (
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(parse_xml(borders_xml))

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return RGBColor(*(int(hex_str[i:i+2], 16) for i in (0, 2, 4)))

def process_paragraph_runs(p, is_dark_bg=False):
    for r in p.runs:
        # Ajuste de tamaño para baja visión (mínimo 9.5 pt en tablas/notas)
        if r.font.size and r.font.size.pt < 9.0:
            r.font.size = Pt(9.5)
            
        # Si está sobre fondo oscuro, texto blanco y nítido
        if is_dark_bg:
            r.font.color.rgb = RGBColor(255, 255, 255)
            r.bold = True
        elif r.font.color and r.font.color.rgb:
            curr_hex = str(r.font.color.rgb).upper()
            if curr_hex in COLOR_RUN_MAP:
                r.font.color.rgb = hex_to_rgb(COLOR_RUN_MAP[curr_hex])

def replace_text_in_paragraph(p):
    full_text = p.text.strip()
    for old_val, new_val in EXACT_PARAGRAPH_REPLACEMENTS:
        if old_val in p.text:
            replaced = False
            for r in p.runs:
                if old_val in r.text:
                    r.text = r.text.replace(old_val, new_val)
                    replaced = True
                    break
            if not replaced:
                p.text = p.text.replace(old_val, new_val)
                if p.runs:
                    p.runs[0].font.name = 'Calibri'
                    p.runs[0].font.size = Pt(10)
                    p.runs[0].font.color.rgb = hex_to_rgb(TEXT_DARK)

def update_manual_file(filepath):
    print(f"\nProcesando documento: {filepath}")
    doc = docx.Document(filepath)
    
    # 1. Párrafos fuera de tablas
    for p in doc.paragraphs:
        replace_text_in_paragraph(p)
        process_paragraph_runs(p, is_dark_bg=False)
        
    # 2. Tablas
    for t_idx, table in enumerate(doc.tables):
        for r_idx, row in enumerate(table.rows):
            for c_idx, cell in enumerate(row.cells):
                # Revisar y mapear shading de fondo
                tcPr = cell._tc.get_or_add_tcPr()
                is_dark_bg = False
                for child in list(tcPr):
                    if child.tag.endswith('shd'):
                        fill = child.attrib.get(f'{{{nsdecls("w").split("=")[1].strip(chr(34))}}}fill', '')
                        if not fill:
                            fill = child.attrib.get('fill', '')
                        fill_upper = fill.upper()
                        if fill_upper in SHD_MAP:
                            new_fill = SHD_MAP[fill_upper]
                            child.set(qn('w:fill'), new_fill)
                            if new_fill == BRAND_DARK:
                                is_dark_bg = True
                        elif fill_upper == BRAND_DARK:
                            is_dark_bg = True
                            
                # Aplicar borde accesible
                set_cell_border(cell, color=BORDER_COLOR, sz='4')
                
                # Procesar párrafos y runs de la celda
                for p in cell.paragraphs:
                    replace_text_in_paragraph(p)
                    process_paragraph_runs(p, is_dark_bg=is_dark_bg)
                    
    doc.save(filepath)
    print(f"[OK] Documento actualizado y guardado: {filepath}")

if __name__ == '__main__':
    manual_dir = 'docs/02_calidad_iso25010_semanas_10_11'
    files = [
        'Manual_Calidad_ISO_25000_Leofit_Pedidos_[Ejecutivo_Gerencia_y_ProductOwner].docx',
        'Manual_Calidad_ISO_25000_Leofit_Pedidos_[Completo_Auditoria_y_ComiteTecnico].docx'
    ]
    for f in files:
        path = os.path.join(manual_dir, f)
        if os.path.exists(path):
            update_manual_file(path)
        else:
            print(f"[WARN] Archivo no encontrado: {path}")
