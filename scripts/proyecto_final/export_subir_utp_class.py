# -*- coding: utf-8 -*-
"""
@file export_subir_utp_class.py
@description Exporta los entregables oficiales para UTP+ Class / Canvas segun la prioridad docente:
             1. Word (.docx)       -> 01_INFORME_FINAL_LEOFIT_GRUPO01.docx (Informe General Consolidado)
             2. Word (.docx)       -> 02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.docx (Informe Semanas 14-15)
             3. PDF (.pdf)         -> 01_INFORME_FINAL_LEOFIT_GRUPO01.pdf / 02_...pdf
             4. Excel (.xlsx)      -> 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
             5. PowerPoint (.pptx) -> 04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")
DEST_DIR = os.path.join(BASE_DIR, "_SUBIR_A_UTP_CLASS")

# Limpiar carpeta destino
if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR)
os.makedirs(DEST_DIR, exist_ok=True)

print("======================================================================")
print("EXPORTACION OFICIAL PARA UTP+ CLASS / CANVAS")
print("======================================================================")
print(f"Carpeta Destino (Ignorada en Git): {DEST_DIR}\n")

# 1. ARCHIVO 1: INFORME GENERAL FINAL (.docx) - PRIORIDAD 1
src_word1 = os.path.join(DOCS_DIR, "01_INFORME_FINAL_LEOFIT.docx")
dst_word1 = os.path.join(DEST_DIR, "01_INFORME_FINAL_LEOFIT_GRUPO01.docx")
if os.path.exists(src_word1):
    shutil.copy2(src_word1, dst_word1)
    sz = os.path.getsize(dst_word1) / 1024.0
    print(f"[1/5] [WORD GENERAL OK]      {os.path.basename(dst_word1)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro Word 1 en: {src_word1}")

# 2. ARCHIVO 2: INFORME DE CONTINUACION S14-S15 (.docx) - REEMPLAZO DEL REPORTE ANTERIOR
src_word2 = os.path.join(DOCS_DIR, "02_INFORME_CONTINUACION_S14_S15_LEOFIT.docx")
dst_word2 = os.path.join(DEST_DIR, "02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.docx")
if os.path.exists(src_word2):
    shutil.copy2(src_word2, dst_word2)
    sz = os.path.getsize(dst_word2) / 1024.0
    print(f"[2/5] [WORD CONTINUACION OK] {os.path.basename(dst_word2)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro Word 2 en: {src_word2}")

# 3. CONVERSION / EXPORTACION A PDF
dst_pdf1 = os.path.join(DEST_DIR, "01_INFORME_FINAL_LEOFIT_GRUPO01.pdf")
dst_pdf2 = os.path.join(DEST_DIR, "02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.pdf")
try:
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    word_app = win32com.client.DispatchEx("Word.Application")
    word_app.Visible = False

    # Convertir Word 1
    if os.path.exists(dst_word1):
        doc1 = word_app.Documents.Open(os.path.abspath(dst_word1))
        doc1.SaveAs(os.path.abspath(dst_pdf1), FileFormat=17)
        doc1.Close(False)
        sz = os.path.getsize(dst_pdf1) / 1024.0
        print(f"[PDF OK]  {os.path.basename(dst_pdf1)} ({sz:.1f} KB)")

    # Convertir Word 2
    if os.path.exists(dst_word2):
        doc2 = word_app.Documents.Open(os.path.abspath(dst_word2))
        doc2.SaveAs(os.path.abspath(dst_pdf2), FileFormat=17)
        doc2.Close(False)
        sz = os.path.getsize(dst_pdf2) / 1024.0
        print(f"[PDF OK]  {os.path.basename(dst_pdf2)} ({sz:.1f} KB)")

    word_app.Quit()
except Exception as e:
    print(f"[AVISO] Word COM no disponible para conversion directa PDF: {e}")

# 4. ARCHIVO 3: LIBRO DE AUDITORIA Y TRAZABILIDAD (.xlsx) - PRIORIDAD 3
src_xlsx = os.path.join(DOCS_DIR, "04_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx")
if not os.path.exists(src_xlsx):
    src_xlsx = os.path.join(DOCS_DIR, "03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx")
dst_xlsx = os.path.join(DEST_DIR, "03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx")
if os.path.exists(src_xlsx):
    shutil.copy2(src_xlsx, dst_xlsx)
    sz = os.path.getsize(dst_xlsx) / 1024.0
    print(f"[3/5] [EXCEL OK]             {os.path.basename(dst_xlsx)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro Excel en: {src_xlsx}")

# 5. ARCHIVO 4: PRESENTACION EJECUTIVA (.pptx) - PRIORIDAD 4
src_pptx = os.path.join(DOCS_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")
if not os.path.exists(src_pptx):
    src_pptx = os.path.join(DOCS_DIR, "02_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")
dst_pptx = os.path.join(DEST_DIR, "04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx")
if os.path.exists(src_pptx):
    shutil.copy2(src_pptx, dst_pptx)
    sz = os.path.getsize(dst_pptx) / 1024.0
    print(f"[4/5] [PPTX OK]              {os.path.basename(dst_pptx)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro PPTX en: {src_pptx}")

# 6. ARCHIVO DE TEXTO EXPLICATIVO
txt_path = os.path.join(DEST_DIR, "00_LEEME_PRIORIDAD_DE_SUBIDA_UTP_CLASS.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("""================================================================================
GUIA DE SUBIDA A UTP+ CLASS (CANVAS) - PROYECTO FINAL (SEMANA 18)
Curso Integrador II: Software (100000S12F) - Seccion 35374
Docente Evaluador: Ing. Enrique Lee Huamani Uriarte
Equipo de Ingenieria: Grupo 01 - LeoFit Solutions
================================================================================

Esta carpeta contiene los entregables oficiales actualizados segun las instrucciones del docente:

--------------------------------------------------------------------------------
CATALOGO DE ENTREGABLES DISPONIBLES:
--------------------------------------------------------------------------------
1. INFORME GENERAL FINAL (.docx / .pdf):
   -> 01_INFORME_FINAL_LEOFIT_GRUPO01.docx
   -> 01_INFORME_FINAL_LEOFIT_GRUPO01.pdf
   * Es el informe completo del proyecto (Memoria tecnica de 19 capitulos).
   * Incluye la evaluacion de calidad ISO 25010 de las semanas 10 y 11 que antes
     se entregaba por separado.

2. INFORME DE CONTINUACION SEMANAS 14 Y 15 (.docx / .pdf):
   -> 02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.docx
   -> 02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.pdf
   * Reemplaza al informe antiguo de semanas 10-11 segun la nueva plantilla del docente
     (Plantilla_Informe_Continuacion_S14_S15_UTP).
   * Contiene la evaluacion de Rendimiento (p95, k6), Flexibilidad (Adaptabilidad y
     Escalabilidad) y Mantenibilidad (Modularidad, Reusabilidad, Modificabilidad, Testabilidad).

3. LIBRO DE AUDITORIA Y TRAZABILIDAD (.xlsx):
   -> 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
   * Matriz integral en Excel con 7 pestanas de trazabilidad y auditoria.

4. PRESENTACION OFICIAL DE SUSTENTACION (.pptx):
   -> 04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx
   * Presentacion ejecutiva de sustentacion con 25 diapositivas y notas de orador completas.

--------------------------------------------------------------------------------
GUIA RAPIDA DE SUBIDA SEGUN LO QUE PERMITA CANVAS:
--------------------------------------------------------------------------------
- Caso A (Si solo te permite subir Word y Excel):
  Sube:
  1. 01_INFORME_FINAL_LEOFIT_GRUPO01.docx
  2. 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx

- Caso B (Si el docente habilito dos casillas de Word):
  Sube:
  1. 01_INFORME_FINAL_LEOFIT_GRUPO01.docx (Informe General)
  2. 02_INFORME_CONTINUACION_S14_S15_LEOFIT_GRUPO01.docx (Informe S14-S15)
  3. 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx (Excel)

- Caso C (Si permite adjuntar todos los formatos):
  Prioridad oficial: Word > PDF > Excel > PPTX.
--------------------------------------------------------------------------------
""")

print("\n======================================================================")
print("INVENTARIO FINAL EN _SUBIR_A_UTP_CLASS/:")
for f in sorted(os.listdir(DEST_DIR)):
    fp = os.path.join(DEST_DIR, f)
    sz = os.path.getsize(fp) / 1024.0
    print(f"  * {f} ({sz:.1f} KB)")
print("======================================================================")
