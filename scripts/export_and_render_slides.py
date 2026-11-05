import os
import win32com.client

pptx_abs = os.path.abspath('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pptx')
pdf_abs = os.path.abspath('docs/00_ENTREGA_OFICIAL_DOCENTE_CANVAS_APF3/GRUP01-Curso_Integrador_II_Software.pdf')

powerpoint = win32com.client.Dispatch("PowerPoint.Application")
pres = powerpoint.Presentations.Open(pptx_abs, WithWindow=False)

print(f"Exporting PDF to {pdf_abs}...")
pres.SaveAs(pdf_abs, 32) # 32 = ppSaveAsPDF
print("PDF Exported successfully.")

for s_num in [4, 21, 23, 24, 27, 30]:
    out_png = os.path.abspath(f'scripts/slide{s_num}_render.png')
    print(f"Exporting Slide {s_num} to PNG...")
    pres.Slides.Item(s_num).Export(out_png, "PNG", 1920, 1080)

pres.Close()
powerpoint.Quit()
print("All exports completed successfully.")
