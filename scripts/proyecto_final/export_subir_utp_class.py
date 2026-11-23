# -*- coding: utf-8 -*-
"""
@file export_subir_utp_class.py
@description Exporta exclusivamente 1 archivo de cada tipo a _SUBIR_A_UTP_CLASS/ (sin duplicados):
             1. Word (.docx)       -> 01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx
             2. PDF (.pdf)         -> 02_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf
             3. Excel (.xlsx)      -> 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
             4. PowerPoint (.pptx) -> 04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import shutil

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")
DEST_DIR = os.path.join(BASE_DIR, "_SUBIR_A_UTP_CLASS")

# Limpiar carpeta destino para garantizar que no existan archivos residuales ni duplicados
if os.path.exists(DEST_DIR):
    shutil.rmtree(DEST_DIR)
os.makedirs(DEST_DIR, exist_ok=True)

print("======================================================================")
print("EXPORTACION EXCLUSIVA PARA UTP+ CLASS (1 ARCHIVO POR TIPO)")
print("======================================================================")
print(f"Carpeta Destino (Ignorada en Git): {DEST_DIR}\n")

# 1. ARCHIVO 1: WORD (.docx) - PRIORIDAD 1
src_word = os.path.join(DOCS_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT.docx")
dst_word = os.path.join(DEST_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx")
if os.path.exists(src_word):
    shutil.copy2(src_word, dst_word)
    sz = os.path.getsize(dst_word) / 1024.0
    print(f"[1/4] [WORD OK]  {os.path.basename(dst_word)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro Word en: {src_word}")

# 2. ARCHIVO 2: PDF (.pdf) - PRIORIDAD 2 (Generado fielmente con Word COM)
dst_pdf = os.path.join(DEST_DIR, "02_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf")
try:
    import pythoncom
    import win32com.client
    pythoncom.CoInitialize()
    word_app = win32com.client.DispatchEx("Word.Application")
    word_app.Visible = False
    doc = word_app.Documents.Open(os.path.abspath(dst_word))
    try:
        doc.Fields.Update()
        for toc in doc.TablesOfContents:
            toc.Update()
    except Exception:
        pass
    doc.SaveAs(os.path.abspath(dst_pdf), FileFormat=17) # 17 = wdFormatPDF
    doc.Close(False)
    word_app.Quit()
    sz = os.path.getsize(dst_pdf) / 1024.0
    print(f"[2/4] [PDF OK]   {os.path.basename(dst_pdf)} ({sz:.1f} KB)")
except Exception as e:
    # Si falla Word COM por entorno restringido, copiar de la caché si existe
    cached_pdf = os.path.join(DOCS_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT.pdf")
    if os.path.exists(cached_pdf):
        shutil.copy2(cached_pdf, dst_pdf)
        sz = os.path.getsize(dst_pdf) / 1024.0
        print(f"[2/4] [PDF OK (Caché)] {os.path.basename(dst_pdf)} ({sz:.1f} KB)")
    else:
        print(f"[AVISO] Word COM no disponible: {e}")

# 3. ARCHIVO 3: EXCEL (.xlsx) - PRIORIDAD 3
src_xlsx = os.path.join(DOCS_DIR, "03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx")
dst_xlsx = os.path.join(DEST_DIR, "03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx")
if os.path.exists(src_xlsx):
    shutil.copy2(src_xlsx, dst_xlsx)
    sz = os.path.getsize(dst_xlsx) / 1024.0
    print(f"[3/4] [EXCEL OK] {os.path.basename(dst_xlsx)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro Excel en: {src_xlsx}")

# 4. ARCHIVO 4: POWERPOINT (.pptx) - PRIORIDAD 4
src_pptx = os.path.join(DOCS_DIR, "02_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")
dst_pptx = os.path.join(DEST_DIR, "04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx")
if os.path.exists(src_pptx):
    shutil.copy2(src_pptx, dst_pptx)
    sz = os.path.getsize(dst_pptx) / 1024.0
    print(f"[4/4] [PPTX OK]  {os.path.basename(dst_pptx)} ({sz:.1f} KB)")
else:
    print(f"[ERROR] No se encontro PPTX en: {src_pptx}")

# 5. ARCHIVO DE TEXTO EXPLICATIVO (1 por tipo: .txt)
txt_path = os.path.join(DEST_DIR, "00_LEEME_PRIORIDAD_DE_SUBIDA_UTP_CLASS.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write("""================================================================================
GUIA DE SUBIDA A UTP+ CLASS (CANVAS) - PROYECTO FINAL (SEMANA 18)
Curso Integrador II: Software (100000S12F) - Seccion 35374
Docente Evaluador: Ing. Enrique Lee Huamani Uriarte
Equipo de Ingenieria: Grupo 01 - LeoFit Solutions
================================================================================

Esta carpeta contiene exactamente 1 archivo por cada formato (sin duplicados):

--------------------------------------------------------------------------------
ORDEN DE PRIORIDAD PARA SUBIR A UTP+ CLASS:
--------------------------------------------------------------------------------
1. WORD (.docx)       -> 01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx
   * Documento principal editable con portada oficial, codigos de alumnos,
     credenciales de acceso, URLs y el reporte tecnico acumulativo completo.

2. PDF (.pdf)         -> 02_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf
   * Version formal no editable para lectura rapida del docente.

3. EXCEL (.xlsx)      -> 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
   * Matriz integral con 7 pestanas: Dashboard, Trazabilidad, Auditoria ISO 25010,
     Resultados de Testing, Criptografia, Inventario de Entregables y Equipo.

4. POWERPOINT (.pptx) -> 04_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx
   * Presentacion ejecutiva de 20 diapositivas tecnicas con notas de orador completas.

--------------------------------------------------------------------------------
SI CANVAS / UTP+ CLASS SOLO TE PERMITE SUBIR WORD Y EXCEL:
Sube unicamente:
  - 01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx
  - 03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
--------------------------------------------------------------------------------
""")

# Limpiar cualquier PDF temporal suelto en docs
for stray in [
    os.path.join(DOCS_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf"),
    os.path.join(DOCS_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT.pdf")
]:
    if os.path.exists(stray):
        try:
            os.remove(stray)
        except Exception:
            pass

print("\n======================================================================")
print("INVENTARIO FINAL EN _SUBIR_A_UTP_CLASS/ (EXACTAMENTE 4 ARCHIVOS, 1 POR TIPO):")
for f in sorted(os.listdir(DEST_DIR)):
    fp = os.path.join(DEST_DIR, f)
    sz = os.path.getsize(fp) / 1024.0
    print(f"  * {f} ({sz:.1f} KB)")
print("======================================================================")
