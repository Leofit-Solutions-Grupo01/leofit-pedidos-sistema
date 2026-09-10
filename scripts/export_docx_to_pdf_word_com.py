# -*- coding: utf-8 -*-
"""
Exportador oficial de DOCX a PDF mediante Microsoft Word COM.
Garantiza fidelidad visual, maquetacion editorial, paginacion y renderizado de tablas.
"""

import os
import glob
import pythoncom
import win32com.client

def export_all_docx_to_pdf():
    print("=== INICIANDO EXPORTACIÓN FORMAL DE DOCX A PDF (WORD COM) ===")
    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    
    docx_files = sorted(glob.glob("docs/*.docx"))
    
    for docx_file in docx_files:
        pdf_file = docx_file.replace(".docx", ".pdf")
        abs_docx = os.path.abspath(docx_file)
        abs_pdf = os.path.abspath(pdf_file)
        
        print(f"Exportando a PDF: {docx_file} -> {pdf_file}...")
        try:
            wb = word.Documents.Open(abs_docx)
            wb.SaveAs(abs_pdf, FileFormat=17) # 17 = wdFormatPDF
            wb.Close()
            file_size_kb = os.path.getsize(pdf_file) / 1024
            print(f"[PDF OK] Generado exitosamente: {pdf_file} ({file_size_kb:.1f} KB)")
        except Exception as e:
            print(f"[ERROR] Error al exportar {docx_file}: {e}")
            
    word.Quit()
    print("=== EXPORTACIÓN A PDF COMPLETADA EXITOSAMENTE ===")

if __name__ == '__main__':
    export_all_docx_to_pdf()
