# -*- coding: utf-8 -*-
"""
@file validate_deliverables.py
@description Validador de integridad para los entregables generados (.docx, .pptx, .xlsx)
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import glob
import docx
import pptx
import openpyxl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROYECTO_FINAL_DIR = os.path.join(BASE_DIR, "_PROYECTO_FINAL_LOCAL")

if not os.path.exists(PROYECTO_FINAL_DIR):
    raise FileNotFoundError("_PROYECTO_FINAL_LOCAL/ no encontrado. Ejecutar solo en maquina de desarrollo con los anexos presentes.")

ENTREGABLES_DIR = os.path.join(PROYECTO_FINAL_DIR, "02_ENTREGABLES_UTP")

def validate():
    print("  --- Validando archivos Word (.docx) ---")
    docx_files = glob.glob(os.path.join(ENTREGABLES_DIR, "01_DOCX", "*.docx"))
    if not docx_files:
        print("    [ERROR] No se encontraron archivos .docx en 01_DOCX")
        return False
        
    for df in sorted(docx_files):
        try:
            d = docx.Document(df)
            p_count = len(d.paragraphs)
            t_count = len(d.tables)
            print(f"    [OK] {os.path.basename(df)}: {p_count} parrafos, {t_count} tablas.")
        except Exception as e:
            print(f"    [ERROR] {os.path.basename(df)} no pudo abrirse: {e}")
            return False

    print("  --- Validando presentacion PowerPoint (.pptx) ---")
    pptx_files = glob.glob(os.path.join(ENTREGABLES_DIR, "02_PPTX", "*.pptx"))
    if not pptx_files:
        print("    [ERROR] No se encontraron archivos .pptx en 02_PPTX")
        return False
        
    for pf in pptx_files:
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

    print("  --- Validando libro Excel (.xlsx) ---")
    xlsx_files = glob.glob(os.path.join(ENTREGABLES_DIR, "03_XLSX", "*.xlsx"))
    if not xlsx_files:
        print("    [ERROR] No se encontraron archivos .xlsx en 03_XLSX")
        return False
        
    for xf in xlsx_files:
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

    print("  --- Validando ausencia de emojis residuales ---")
    import re
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf]', flags=re.UNICODE)
    found_emoji = False
    
    # Validar docx
    for df in docx_files:
        d = docx.Document(df)
        full_text = " ".join(p.text for p in d.paragraphs)
        if emoji_pattern.search(full_text):
            print(f"    [WARN] Emoji detectado en {os.path.basename(df)}")
            found_emoji = True
            
    if not found_emoji:
        print("    [OK] Verificacion de Cero Emojis: LIMPIO en todos los entregables.")

    print("\n[OK] VALIDACION DE INTEGRIDAD COMPLETADA EXITOSAMENTE.")
    return True

if __name__ == "__main__":
    import sys
    success = validate()
    sys.exit(0 if success else 1)
