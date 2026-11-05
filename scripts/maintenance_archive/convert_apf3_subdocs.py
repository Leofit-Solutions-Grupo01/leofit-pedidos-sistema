import os
import win32com.client

word = win32com.client.Dispatch("Word.Application")

files_to_convert = [
    'docs/APF3_GRUPO_01/02_funcionalidad/CP-F_casos_funcionales.docx',
    'docs/APF3_GRUPO_01/03_compatibilidad/CP-I_interoperabilidad.docx',
    'docs/APF3_GRUPO_01/04_interaccion/PROTOCOLO_UX.docx'
]

for doc_path in files_to_convert:
    abs_doc = os.path.abspath(doc_path)
    abs_pdf = abs_doc.replace('.docx', '.pdf')
    if os.path.exists(abs_doc):
        print(f"Converting {abs_doc} to PDF...")
        doc = word.Documents.Open(abs_doc)
        doc.SaveAs(abs_pdf, 17) # 17 = wdFormatPDF
        doc.Close()
        print(f"Created: {abs_pdf}")

word.Quit()
print("All conversions completed.")

