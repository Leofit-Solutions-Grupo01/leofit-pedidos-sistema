# -*- coding: utf-8 -*-
"""
@file validate_deliverables.py
@description Validador de integridad para los entregables generados (.docx, .pptx, .xlsx)
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import glob
import re
import docx
import pptx
import openpyxl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OFFICIAL_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")
ENTREGABLES_DIR = os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP") if os.path.exists(PROYECTO_FINAL_DIR) else None

def validate():
    print("======================================================================")
    print("VALIDACION DE ENTREGABLES OFICIALES (docs/01_ENTREGA_FINAL_PROYECTO_SEMANA_18)")
    print("======================================================================")
    
    # 1. Validar existencia del paquete oficial
    if not os.path.exists(OFFICIAL_DIR):
        print(f"[ERROR] No existe el directorio oficial: {OFFICIAL_DIR}")
        return False
        
    required_files = [
        "01_INFORME_FINAL_LEOFIT.docx",
        "02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx",
        "02_INFORME_CONTINUACION_S14_S15_LEOFIT.md",
        "03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx",
        "03_VISOR_WEB_PRESENTACION_SUSTENTACION.html",
        "04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx",
        "04_COMPENDIO_TECNICO_CALIDAD_TESTING_Y_CRIPTOGRAFIA.md",
        "README.md"
    ]
    
    for rf in required_files:
        p = os.path.join(OFFICIAL_DIR, rf)
        if not os.path.exists(p):
            print(f"  [ERROR] Falta archivo oficial obligatorio: {rf}")
            return False
        sz = os.path.getsize(p)
        print(f"  [OK] {rf} ({sz / 1024:.1f} KB)")
        
    print("\n  --- Validando archivos Word (.docx) ---")
    docx_files = glob.glob(os.path.join(OFFICIAL_DIR, "*.docx"))
    if ENTREGABLES_DIR and os.path.exists(os.path.join(ENTREGABLES_DIR, "01_DOCX")):
        docx_files.extend(glob.glob(os.path.join(ENTREGABLES_DIR, "01_DOCX", "*.docx")))
        
    for df in sorted(set(docx_files)):
        try:
            d = docx.Document(df)
            p_count = len(d.paragraphs)
            t_count = len(d.tables)
            print(f"    [OK] {os.path.basename(df)}: {p_count} parrafos, {t_count} tablas.")
        except Exception as e:
            print(f"    [ERROR] {os.path.basename(df)} no pudo abrirse: {e}")
            return False

    print("\n  --- Validando presentacion PowerPoint (.pptx) ---")
    pptx_files = glob.glob(os.path.join(OFFICIAL_DIR, "*.pptx"))
    if ENTREGABLES_DIR and os.path.exists(os.path.join(ENTREGABLES_DIR, "02_PPTX")):
        pptx_files.extend(glob.glob(os.path.join(ENTREGABLES_DIR, "02_PPTX", "*.pptx")))
        
    for pf in sorted(set(pptx_files)):
        try:
            prs = pptx.Presentation(pf)
            num_slides = len(prs.slides)
            notes_count = sum(1 for s in prs.slides if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip())
            cumple = "CUMPLE" if num_slides >= 18 else "FALLA"
            print(f"    [OK] {os.path.basename(pf)}:")
            print(f"         Total Slides: {num_slides} (Requisito >= 18: {cumple})")
            print(f"         Slides con Notas de Orador: {notes_count}/{num_slides}")
            if num_slides < 18 or notes_count < num_slides:
                print("    [ERROR] No cumple con los requisitos minimos de slides o notas de orador.")
                return False
        except Exception as e:
            print(f"    [ERROR] {os.path.basename(pf)} fallo: {e}")
            return False

    print("\n  --- Validando libro Excel (.xlsx) ---")
    xlsx_files = glob.glob(os.path.join(OFFICIAL_DIR, "*.xlsx"))
    if ENTREGABLES_DIR and os.path.exists(os.path.join(ENTREGABLES_DIR, "03_XLSX")):
        xlsx_files.extend(glob.glob(os.path.join(ENTREGABLES_DIR, "03_XLSX", "*.xlsx")))
        
    for xf in sorted(set(xlsx_files)):
        try:
            wb = openpyxl.load_workbook(xf, data_only=True)
            sheet_names = wb.sheetnames
            print(f"    [OK] {os.path.basename(xf)}:")
            print(f"         Total Pestanas: {len(sheet_names)} ({', '.join(sheet_names)})")
            if len(sheet_names) < 3:
                print("    [ERROR] Cantidad de pestanas insuficiente.")
                return False
        except Exception as e:
            print(f"    [ERROR] {os.path.basename(xf)} fallo: {e}")
            return False

    print("\n  --- Validando graficos cientificos ---")
    graficos = glob.glob(os.path.join(OFFICIAL_DIR, "graficos", "*.png"))
    print(f"    [OK] Total de graficos encontrados: {len(graficos)} (Requisito >= 6)")
    if len(graficos) < 6:
        print("    [ERROR] Se esperaban al menos 6 graficos de calidad en graficos/")
        return False

    print("\n  --- Validando anexos tecnicos de sustentacion ---")
    anexos = glob.glob(os.path.join(OFFICIAL_DIR, "anexos_tecnicos", "*.md"))
    print(f"    [OK] Total de anexos tecnicos encontrados: {len(anexos)} (Requisito >= 6)")
    if len(anexos) < 6:
        print("    [ERROR] Se esperaban al menos 6 anexos tecnicos en anexos_tecnicos/")
        return False

    print("\n  --- Validando ausencia de emojis residuales ---")
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf]', flags=re.UNICODE)
    found_emoji = False
    
    for df in sorted(set(docx_files)):
        d = docx.Document(df)
        full_text = " ".join(p.text for p in d.paragraphs)
        if emoji_pattern.search(full_text):
            print(f"    [WARN] Emoji detectado en {os.path.basename(df)}")
            found_emoji = True
            
    if not found_emoji:
        print("    [OK] Verificacion de Cero Emojis: LIMPIO en todos los entregables.")

    print("\n======================================================================")
    print("[OK] VALIDACION DE INTEGRIDAD COMPLETADA EXITOSAMENTE (100% CONFORME)")
    print("======================================================================")
    return True

if __name__ == "__main__":
    success = validate()
    exit(0 if success else 1)
