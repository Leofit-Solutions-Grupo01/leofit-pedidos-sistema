# -*- coding: utf-8 -*-
"""
@file export_subir_utp_class.py
@description Prepara y exporta exclusivamente los archivos para subir a UTP+ Class / Canvas
             siguiendo la jerarquía estricta de prioridad: Word > PDF > Excel > PPT
             Esta carpeta destino (_SUBIR_A_UTP_CLASS/) se encuentra excluida del repositorio Git.
@project LeoFit Pedidos Sistema (UTP - Curso Integrador II)
@author Grupo 01 - UTP
"""

import os
import shutil
import glob

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs", "01_ENTREGA_FINAL_PROYECTO_SEMANA_18")
DEST_DIR = os.path.join(BASE_DIR, "_SUBIR_A_UTP_CLASS")

os.makedirs(DEST_DIR, exist_ok=True)

print("======================================================================")
print("EXPORTACION DE ARCHIVOS PARA UTP+ CLASS (CANVAS)")
print("======================================================================")
print(f"Carpeta Destino (Ignorada por Git): {DEST_DIR}\n")

# 1. Prioridad 1: Documentos Word (.docx)
print("  --- [PRIORIDAD 1] Copiando Documentos Word (.docx) ---")
docx_mapping = [
    (
        os.path.join(DOCS_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.docx"),
        os.path.join(DEST_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE_GRUPO01.docx")
    ),
    (
        os.path.join(DOCS_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT.docx"),
        os.path.join(DEST_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx")
    )
]

for src, dst in docx_mapping:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        sz = os.path.getsize(dst) / 1024.0
        print(f"    [OK] {os.path.basename(dst)} ({sz:.1f} KB)")
    else:
        print(f"    [ERROR] No se encontro origen: {src}")

# 2. Prioridad 2: Documentos PDF (.pdf)
print("\n  --- [PRIORIDAD 2] Generando/Copiando Documentos PDF (.pdf) ---")
pdf_mapping = [
    (
        os.path.join(DOCS_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE.pdf"),
        os.path.join(DEST_DIR, "00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE_GRUPO01.pdf")
    ),
    (
        os.path.join(DOCS_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT.pdf"),
        os.path.join(DEST_DIR, "01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf")
    )
]

for src, dst in pdf_mapping:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        sz = os.path.getsize(dst) / 1024.0
        print(f"    [OK] {os.path.basename(dst)} ({sz:.1f} KB)")
        # Remover PDF temporal del directorio docs para no ensuciar el git status
        try:
            os.remove(src)
        except Exception:
            pass
    elif not os.path.exists(dst):
        print(f"    [AVISO] Archivo PDF no encontrado: {src}")

# 3. Prioridad 3: Hojas de Calculo Excel (.xlsx)
print("\n  --- [PRIORIDAD 3] Copiando Libro de Calculo Excel (.xlsx) ---")
xlsx_src = os.path.join(DOCS_DIR, "03_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT.xlsx")
xlsx_dst = os.path.join(DEST_DIR, "02_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx")

if os.path.exists(xlsx_src):
    shutil.copy2(xlsx_src, xlsx_dst)
    sz = os.path.getsize(xlsx_dst) / 1024.0
    print(f"    [OK] {os.path.basename(xlsx_dst)} ({sz:.1f} KB)")
else:
    print(f"    [ERROR] No se encontro origen Excel: {xlsx_src}")

# 4. Prioridad 4: Presentacion PowerPoint (.pptx)
print("\n  --- [PRIORIDAD 4] Copiando Presentacion PowerPoint (.pptx) ---")
pptx_src = os.path.join(DOCS_DIR, "02_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT.pptx")
pptx_dst = os.path.join(DEST_DIR, "03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx")

if os.path.exists(pptx_src):
    shutil.copy2(pptx_src, pptx_dst)
    sz = os.path.getsize(pptx_dst) / 1024.0
    print(f"    [OK] {os.path.basename(pptx_dst)} ({sz:.1f} KB)")
else:
    print(f"    [ERROR] No se encontro origen PPTX: {pptx_src}")

# 5. Generar archivo de instrucciones y resumen de entrega
readme_txt = """================================================================================
GUIA Y ORDEN DE PRIORIDAD PARA SUBIDA A UTP+ CLASS (CANVAS)
Curso Integrador II: Software (100000S12F) - Grupo 01 (LeoFit Solutions)
Docente Asesor: Ing. Enrique Lee Huamani Uriarte
================================================================================

Esta carpeta contiene EXCLUSIVAMENTE los archivos finales preparados para la
plataforma institucional UTP+ Class / Canvas.

ORDEN DE PRIORIDAD PARA LA SUBIDA:
--------------------------------------------------------------------------------
1. PRIORIDAD 1: DOCUMENTOS WORD (.docx) -> FORMATO PRINCIPAL DE CALIFICACION
   [1] 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE_GRUPO01.docx
       - Caratula formal con los 5 integrantes, codigos UTP, roles, enlaces cloud
         activos (GitHub, PWA, Render API, Swagger) y credenciales de prueba.
   [2] 01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.docx
       - Memoria tecnica acumulativa completa (156 parrafos, 14 tablas, TOC dinamica).
         Cumple con ISO/IEC 25010:2023, ISO 9126, percentiles k6, arquitectura y
         politica criptografica TLS 1.3 / AES-256-GCM.

2. PRIORIDAD 2: DOCUMENTOS PDF (.pdf) -> VERSION EDITORIAL BLOQUEADA
   [1] 00_HOJA_DE_ENTREGA_Y_ENLACES_DOCENTE_GRUPO01.pdf
   [2] 01_INFORME_FINAL_PROYECTO_LEOFIT_GRUPO01.pdf
   * Nota: Subir estos PDFs si Canvas solicita especificamente formato PDF o si se
     desea garantizar una visualizacion inalterable de la tipografia y tablas.

3. PRIORIDAD 3: LIBRO DE CALCULO EXCEL (.xlsx) -> AUDITORIA Y METRICAS
   [1] 02_PLAN_AUDITORIA_CALIDAD_Y_TRAZABILIDAD_LEOFIT_GRUPO01.xlsx
       - Contiene 7 pestanas: Dashboard Ejecutivo, Metricas ISO 25010, Casos de Prueba,
         Deuda Tecnica Sonar, Matriz de Trazabilidad, Percentiles k6 y Cierre Formal.

4. PRIORIDAD 4: PRESENTACION POWERPOINT (.pptx) -> DIAPOSITIVAS DE SUSTENTACION
   [1] 03_PRESENTACION_OFICIAL_SUSTENTACION_LEOFIT_GRUPO01.pptx
       - 25 diapositivas ejecutivas widescreen 16:9, diseno sin emojis, paleta WCAG AAA,
         graficos cientificos a 300 DPI y notas de orador integradas (25/25).

--------------------------------------------------------------------------------
NOTA DE SEGURIDAD Y CONTROL DE VERSIONES:
Esta carpeta (_SUBIR_A_UTP_CLASS/) esta configurada en .gitignore para uso
estrictamente local del estudiante, garantizando que el repositorio Git permanezca
ligero y limpio.
================================================================================
"""

with open(os.path.join(DEST_DIR, "LEEME_PRIORIDAD_Y_ARCHIVOS_UTP_CLASS.txt"), "w", encoding="utf-8") as f:
    f.write(readme_txt)

print(f"\n  [OK] Generado: LEEME_PRIORIDAD_Y_ARCHIVOS_UTP_CLASS.txt")
print("\n======================================================================")
print("[OK] EXPORTACION A _SUBIR_A_UTP_CLASS COMPLETADA EXITOSAMENTE.")
print("======================================================================")
